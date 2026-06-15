"""
SCRIPT DE UNA SOLA VEZ — RELLENAR MACROS POR COMIDA

Para alumnos que ya tenían comidas guardadas ANTES de la
mejora de macros. Recalcula proteína/carbos/grasa de cada
comida y las actualiza, sin tocar el resto del plan.

Ejecutar desde la raíz:
    python actualizar_macros_comidas.py
"""

from dotenv import load_dotenv
load_dotenv()

from database.conexion import supabase


def main():

    atletas = (
        supabase.table("perfiles_atletas")
        .select("*")
        .execute()
    ).data or []

    print(f"Encontrados {len(atletas)} alumnos.\n")

    for atleta in atletas:

        alumno_id = atleta["id"]
        nombre = atleta.get("nombre_completo", "?")

        # Traer sus comidas
        comidas = (
            supabase.table("comidas_programadas")
            .select("id, kcal, proteina_g")
            .eq("alumno_id", alumno_id)
            .eq("activa", True)
            .execute()
        ).data or []

        if not comidas:
            continue

        # Si ya tienen macros, saltar
        if comidas[0].get("proteina_g"):
            print(f"♻️  {nombre}: ya tenía macros.")
            continue

        num_comidas = len(comidas)

        # Calcular macros totales del perfil
        peso = float(atleta.get("peso_actual") or 75)
        calorias = int(atleta.get("calorias_actuales") or 2000)

        prote_total = round(peso * 2.0)
        grasa_total = round(peso * 0.9)
        carbos_total = round(max(
            (calorias - prote_total * 4 - grasa_total * 9) / 4,
            50
        ))

        # Por comida
        p = int(prote_total / max(1, num_comidas))
        car = int(carbos_total / max(1, num_comidas))
        g = int(grasa_total / max(1, num_comidas))

        # Actualizar cada comida
        for comida in comidas:
            supabase.table("comidas_programadas").update({
                "proteina_g": p,
                "carbos_g": car,
                "grasa_g": g
            }).eq("id", comida["id"]).execute()

        print(
            f"✅ {nombre}: {num_comidas} comidas actualizadas "
            f"(P:{p}g C:{car}g G:{g}g por comida)."
        )

    print("\nListo. 🏆")


if __name__ == "__main__":
    main()