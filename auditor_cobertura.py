"""
AUDITOR DE COBERTURA DE LA BASE DE DATOS PROPIA

Revisa cuáles combinaciones de:
- tipo de entrenamiento × nivel  (rutinas)
- tipo de dieta                  (menús)

tienen contenido real en data/ejercicios.py y
data/alimentos.py, y cuáles están vacías.

Ejecutar desde la raiz del proyecto:
    python auditor_cobertura.py
"""

from backend.services.plan_service import (
    generar_rutina_entrenamiento,
    generar_menu_dinamico
)

TIPOS_ENTRENO = [
    "Fuerza / Hipertrofia (Gimnasio)",
    "CrossFit / Funcional",
    "Powerlifting / Levantamiento Olímpico",
    "Calistenia / Street Workout",
    "Resistencia (Running, Ciclismo, Natación)",
    "Deportes de Equipo (Fútbol, Básquet, Rugby)",
    "Artes Marciales / Deportes de Contacto",
    "Deportes de Raqueta (Tenis, Pádel)",
    "Pilates / Yoga / Movilidad",
    "Danza / Baile Deportivo",
    "Gimnasia Artística / Rítmica",
    "Rehabilitación / Fisioterapia Activa",
    "Ninguno (Sedentario)"
]

NIVELES = ["Principiante", "Intermedio", "Avanzado"]

DIETAS = [
    "Clásica / Equilibrada",
    "Hiperproteica (Fitness)",
    "Cetogénica (Keto)",
    "Low Carb",
    "Vegana (100% Vegetal)",
    "Vegetariana",
    "Pescetariana",
    "Paleolítica",
    "Mediterránea",
    "DASH",
    "FODMAP",
    "Libre de Gluten",
    "Sin Lactosa",
    "Flexitariana"
]


def auditar_rutinas():

    print("=" * 60)
    print("🏋️ COBERTURA DE RUTINAS (entrenamiento × nivel)")
    print("=" * 60)

    completas = 0
    vacias = []

    for tipo in TIPOS_ENTRENO:

        for nivel in NIVELES:

            rutina = generar_rutina_entrenamiento(
                tipo, nivel, 3
            )

            tiene_contenido = (
                rutina
                and "Aviso" not in rutina
                and "Descanso Activo" not in rutina
            )

            if tiene_contenido:

                dias = len(rutina)

                ejercicios = sum(
                    len(v) for v in rutina.values()
                )

                print(
                    f"✅ {tipo} | {nivel}: "
                    f"{dias} días, {ejercicios} ejercicios"
                )

                completas += 1

            else:

                print(f"❌ {tipo} | {nivel}: VACÍA")

                vacias.append(f"{tipo} | {nivel}")

    total = len(TIPOS_ENTRENO) * len(NIVELES)

    print("-" * 60)
    print(
        f"RESULTADO: {completas}/{total} "
        f"combinaciones con rutina."
    )

    if vacias:

        print("\nFALTAN CARGAR EN data/ejercicios.py:")

        for v in vacias:
            print(f"  • {v}")

    return vacias


def auditar_dietas():

    print()
    print("=" * 60)
    print("🍽️ COBERTURA DE DIETAS")
    print("=" * 60)

    problemas = []

    for dieta in DIETAS:

        try:

            menus, lista = generar_menu_dinamico(
                135.0, 180.0, 60.0,   # macros de prueba
                4, 3,                  # 4 comidas, 3 opciones
                dieta,
                "Argentina"
            )

            comidas_ok = len(menus or {})

            opciones_total = sum(
                len(v) for v in (menus or {}).values()
            )

            items_compra = len(lista or {})

            if comidas_ok and opciones_total:

                print(
                    f"✅ {dieta}: {comidas_ok} comidas, "
                    f"{opciones_total} opciones, "
                    f"{items_compra} items de compra"
                )

            else:

                print(f"❌ {dieta}: SIN CONTENIDO")

                problemas.append(dieta)

        except Exception as e:

            print(f"💥 {dieta}: ERROR → {e}")

            problemas.append(dieta)

    print("-" * 60)

    if problemas:

        print("\nDIETAS CON PROBLEMAS:")

        for p in problemas:
            print(f"  • {p}")

    else:

        print("Todas las dietas generan contenido. 💪")

    return problemas


if __name__ == "__main__":

    vacias = auditar_rutinas()
    problemas = auditar_dietas()

    print()
    print("=" * 60)

    if not vacias and not problemas:

        print(
            "🏆 COBERTURA COMPLETA: cualquier combinación "
            "que elija un alumno tiene plan."
        )

    else:

        print(
            f"⚠️ Quedan {len(vacias)} rutinas y "
            f"{len(problemas)} dietas por completar.\n"
            "Los alumnos que elijan esas combinaciones "
            "no recibirán plan inicial automático\n"
            "(el sistema no rompe, pero queda vacío "
            "hasta que el entrenador cargue manual)."
        )