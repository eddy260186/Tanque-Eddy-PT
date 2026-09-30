"""Contract tests without Supabase credentials, IA calls or WhatsApp sends."""
import importlib.util
from pathlib import Path
import sys
from types import ModuleType, SimpleNamespace
import unittest
from unittest.mock import patch

from backend.services.nutrition_service import ErrorPlanNutricional, nutrientes_opcion_texto

ROOT=Path(__file__).resolve().parents[1]


def load_file(name,path):
    spec=importlib.util.spec_from_file_location(name,ROOT/path)
    module=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class FakeDB:
    def __init__(self, existing=False, restrictions='', fail=False):
        self.existing=existing
        self.restrictions=restrictions
        self.fail=fail
        self.inserts=[]
    def table(self,name):
        db=self
        class Query:
            def __init__(self): self.action='select'; self.payload=None
            def select(self,*a,**kw): return self
            def eq(self,*a,**kw): return self
            def limit(self,*a,**kw): return self
            def update(self,payload): self.action='update'; return self
            def insert(self,payload): self.action='insert';self.payload=payload;return self
            def execute(self):
                if self.action=='insert':
                    if db.fail and name=='comidas_programadas': raise RuntimeError('DB unavailable')
                    db.inserts.append((name,self.payload));return SimpleNamespace(data=self.payload)
                if name=='perfiles_atletas':return SimpleNamespace(data=[{'restricciones_alimentarias':db.restrictions}])
                if name=='comidas_programadas' and db.existing:return SimpleNamespace(data=[{'id':'manual-plan'}])
                return SimpleNamespace(data=[])
        return Query()


class IntegrationTests(unittest.TestCase):
    def setUp(self):
        self.db=FakeDB()
        fake=ModuleType('database.conexion');fake.supabase=self.db
        self.db_patch=patch.dict(sys.modules,{'database.conexion':fake})
        self.db_patch.start()
        self.onboarding=load_file('nutrition_onboarding_test','backend/services/onboarding_service.py')

    def tearDown(self):self.db_patch.stop()

    def create(self,**kwargs):
        args=dict(alumno_id='student',p_g_total=180,c_g_total=200,g_g_total=60,
                  num_comidas=5,dieta_tipo='Clásica',pais='Argentina',cal_objetivo=2060,
                  hora_despertar='09:00',num_opciones=5)
        args.update(kwargs)
        return self.onboarding.generar_comidas_iniciales(**args)

    def test_saved_values_come_from_ingredients_not_equal_calorie_split(self):
        self.assertEqual(self.create(),5)
        rows=next(payload for name,payload in self.db.inserts if name=='comidas_programadas')
        self.assertEqual(rows[0]['hora'],'10:00')
        self.assertEqual(rows[1]['hora'],'12:30')
        for row in rows:
            summary=nutrientes_opcion_texto(row['detalle'])
            for key in ['kcal','proteina_g','carbos_g','grasa_g']:
                self.assertEqual(row[key],round(summary[key]))
            self.assertEqual(len(row['opciones']),5)
        self.assertTrue(any(nutrientes_opcion_texto(option)['kcal']!=412 for row in rows for option in row['opciones']))
        self.assertTrue(any(name=='listas_compras' for name,_ in self.db.inserts))

    def test_profile_restrictions_apply_when_caller_does_not_pass_them(self):
        self.db.restrictions='sin lactosa'
        self.create()
        rows=next(payload for name,payload in self.db.inserts if name=='comidas_programadas')
        for row in rows:
            for option in row['opciones']:
                self.assertNotIn('Yogur',option)
                self.assertNotIn('cottage',option)

    def test_existing_manual_plan_is_preserved(self):
        self.db.existing=True
        self.assertEqual(self.create(),0)
        self.assertEqual(self.db.inserts,[])

    def test_invalid_plan_and_db_failure_are_not_reported_as_success(self):
        with self.assertRaises(ErrorPlanNutricional):self.create(c_g_total=-40)
        self.assertEqual(self.db.inserts,[])
        self.db.fail=True
        with self.assertRaises(RuntimeError):self.create()
        self.assertEqual(self.db.inserts,[])

    def test_whatsapp_uses_selected_option_values_and_legacy_fallback(self):
        agent=load_file('nutrition_agent_test','automation/agente_diario.py')
        option='100g Ejemplo | Infusion: Agua | Aprox: 400.2 kcal; P: 30.1g; C: 40.2g; G: 10.3g'
        row={'opciones':[option],'kcal':999,'proteina_g':99}
        with patch.object(agent,'obtener_comida',return_value=row),patch.object(agent,'obtener_resumen_calorico',return_value=(0,'')):
            message=agent.componer_mensaje_comida('student','desayuno')
        self.assertIn('~400.2 kcal',message)
        self.assertNotIn('999',message)
        row={'detalle':'100g Pollo + 200g Arroz','kcal':450}
        with patch.object(agent,'obtener_comida',return_value=row),patch.object(agent,'obtener_resumen_calorico',return_value=(0,'')):
            self.assertIn('~450 kcal',agent.componer_mensaje_comida('student','almuerzo'))

    def test_both_pdf_engines_do_not_turn_macros_into_shopping_items(self):
        captured=[]
        class HTML:
            def __init__(self,string,**kw):captured.append(string)
            def write_pdf(self,target=None,**kw):
                if target is not None:target.write(b'pdf-stub')
                return b'pdf-stub'
        fake=ModuleType('weasyprint');fake.HTML=HTML
        menus={'DESAYUNO':['Opcion 1: 10.5g Aceite + 100g Pan | Infusion: Mate | Aprox: 450.1 kcal; P: 20.0g; C: 40.0g; G: 15.0g', 'Opcion 2: 20.5g Aceite + 200g Pan | Infusion: Agua']}
        with patch.dict(sys.modules,{'weasyprint':fake}):
            for name in ['pdf_generator.py','pdf_generator_elite.py']:
                pdf=load_file('test_'+name[:-3],'utils/'+name)
                pdf.build_pdf_ultra_elite({'m':menus,'nombre':'Eddy'})
        self.assertEqual(len(captured),2)
        for html in captured:
            self.assertIn('Aceite (465 Gramos)',html)
            self.assertIn('Pan (4.5 KG)',html)
            self.assertIn('Opcion 2: 20.5g Aceite',html)
            self.assertNotIn('Aprox: 450.1 kcal; P: (',html)


if __name__=='__main__':unittest.main()
