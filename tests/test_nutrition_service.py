import math
import unittest

from data.alimentos_nutricionales import ALIMENTOS_NUTRICIONALES as FOODS
from backend.services.nutrition_service import (
    ErrorPlanNutricional, generar_menu_nutricional, formatear_opcion,
    validar_macros, calcular_macros_objetivo, filtros_alimentarios,
    compras_desde_menus_texto, nutrientes_opcion_texto, validar_objetivo_energia,
)
from backend.services.plan_service import generar_menu_dinamico


class NutritionTests(unittest.TestCase):
    def generate(self, diet='Clásica / Equilibrada', restrictions='', meals=5, options=5):
        return generar_menu_nutricional(180, 200, 60, meals, options, diet, 'Argentina', restrictions)

    def test_actual_nutrients_after_rounding_and_every_meal_count(self):
        for meals in range(1, 7):
            menus, _ = self.generate(meals=meals)
            self.assertEqual(len(menus), meals)
            for options in menus.values():
                for option in options:
                    sums = [0, 0, 0, 0]
                    for item in option['ingredientes']:
                        self.assertGreater(item['gramos'], 0)
                        food = FOODS[item['id']]
                        for j, key in enumerate(['proteina_100g', 'carbos_100g', 'grasa_100g', 'kcal_100g']):
                            sums[j] += item['gramos'] * food[key] / 100
                    for j, key in enumerate(['proteina_g', 'carbos_g', 'grasa_g', 'kcal']):
                        self.assertAlmostEqual(option[key], sums[j], delta=0.051)
                    for actual, target in zip(sums, [180/meals, 200/meals, 60/meals]):
                        self.assertAlmostEqual(actual, target, delta=max(0.1, target*0.01))

    def test_dietary_exclusions_for_every_option(self):
        for diet, forbidden in [
            ('Vegana', {'carne', 'pescado', 'huevo', 'lacteos'}),
            ('Vegetariana', {'carne', 'pescado'}),
            ('Pescetariana', {'carne'}), ('Libre de Gluten', {'gluten'}),
            ('Sin Lactosa', {'lacteos'}), ('Paleolítica', {'cereal', 'legumbre', 'lacteos'}),
        ]:
            with self.subTest(diet=diet):
                menus, _ = self.generate(diet=diet, options=10)
                for options in menus.values():
                    for option in options:
                        for item in option['ingredientes']:
                            self.assertFalse(forbidden.intersection(FOODS[item['id']]['etiquetas']))

    def test_combined_allergies_accent_and_diet(self):
        menus, _ = self.generate('Vegetariana', 'sin gluten, alergia al maní; sin lactosa y frutos secos', options=1)
        for options in menus.values():
            for item in options[0]['ingredientes']:
                self.assertFalse({'gluten','mani','lacteos','frutos_secos','carne','pescado'}.intersection(FOODS[item['id']]['etiquetas']))

        _, banned = filtros_alimentarios('Vegetariana', 'sin gluten, alergia al huevo; sin lactosa y alergia a la soja')
        self.assertTrue({'gluten','huevo','lacteos','soja','carne','pescado'}.issubset(banned))

    def test_unknown_restrictions_and_diets_require_review(self):
        for diet, restrictions in [('Vegana', 'alergia a la mostaza'), ('dieta inventada', ''), ('FODMAP',''), ('DASH','')]:
            with self.assertRaises(ErrorPlanNutricional):
                self.generate(diet, restrictions)
        with self.assertRaises(ErrorPlanNutricional):
            filtros_alimentarios('Clásica', 'no soy alérgico a la soja')

    def test_negative_nonfinite_and_zero_macros(self):
        for macros in [(-1,200,60),(180,-40,60),(180,200,-1),(math.nan,200,60),(math.inf,200,60),(0,0,0),(True,200,60)]:
            with self.subTest(macros=macros), self.assertRaises(ErrorPlanNutricional):
                validar_macros(*macros)

    def test_invalid_energy_budget_is_rejected(self):
        for kcal in [0,-100,math.nan,math.inf,500]:
            with self.subTest(kcal=kcal), self.assertRaises(ErrorPlanNutricional):
                calcular_macros_objetivo(100,kcal,'Clásica')
        self.assertAlmostEqual(calcular_macros_objetivo(100,2400,'Hiperproteica')[0],220)
        with self.assertRaises(ErrorPlanNutricional):
            validar_objetivo_energia(1000,180,200,60)
        validar_objetivo_energia(2060,180,200,60)

    def test_invalid_meal_option_bounds(self):
        for meals, options in [(0,5),(7,5),(5,0),(5,11),(5,1.5),(True,5)]:
            with self.assertRaises(ErrorPlanNutricional):
                self.generate(meals=meals,options=options)

    def test_keto_counts_all_ingredient_carbohydrates(self):
        menus, _ = generar_menu_nutricional(180,30,100,5,5,'Keto','Argentina')
        for options in menus.values():
            for op in options:
                self.assertAlmostEqual(op['carbos_g'],6,delta=0.1)
                self.assertNotIn('Libre',formatear_opcion(op))

    def test_infeasible_restrictions_never_fall_back_to_forbidden_food(self):
        with self.assertRaises(ErrorPlanNutricional):
            self.generate('Vegana', 'sin gluten, soja, legumbres', options=1)

    def test_legacy_adapter_and_shopping_projection_use_all_options(self):
        text, shopping = generar_menu_dinamico(180,200,60,5,10,'Clásica','Argentina')
        self.assertEqual(shopping,compras_desde_menus_texto(text))
        for options in text.values():
            self.assertEqual(len(options),10)
            self.assertTrue(options[0].startswith('Opcion 1: '))
            self.assertIsNotNone(nutrientes_opcion_texto(options[0]))
        self.assertFalse(any('kcal' in name or 'Infusion' in name for name in shopping))

    def test_decimal_weights_and_legacy_menus_in_pdf_projection(self):
        menus={'DESAYUNO':['Opcion 1: 10.5g Aceite + 100g Pan | Infusion: Mate | Aprox: 450.1 kcal; P: 20.0g; C: 40.0g; G: 15.0g',
                            'Opcion 2: 20.5g Aceite + 200g Pan | Infusion: Té']}
        self.assertEqual(compras_desde_menus_texto(menus),{'Aceite':465.0,'Pan':4500.0})
        self.assertIsNone(nutrientes_opcion_texto('100g Pollo + 200g Arroz'))

    def test_options_are_unique_and_catalogue_has_provenance(self):
        menus,_=self.generate(options=10)
        for options in menus.values():
            self.assertEqual(len({formatear_opcion(op) for op in options}),10)
        for code, food in FOODS.items():
            self.assertEqual(len(code),5)
            self.assertTrue(food['estado'])
            self.assertTrue(food['descripcion_usda'])
        self.assertEqual(FOODS['05064']['kcal_100g'],165)
        self.assertEqual(FOODS['01256']['proteina_100g'],10.19)


if __name__ == '__main__':
    unittest.main()
