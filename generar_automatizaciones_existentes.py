"""
SCRIPT DE UNA SOLA VEZ
Genera las automatizaciones (agua, comidas, entreno,
suplementos, pesaje) para TODOS los alumnos que ya
existen en la base de datos.

Ejecutar desde la raiz del proyecto:
    python generar_automatizaciones_existentes.py
"""
from dotenv import load_dotenv
load_dotenv()

from database.conexion import supabase
from automation.generador_automatizaciones import generar_automatizaciones_alumno


def main():

    res = (
        supabase
        .table("perfiles_atletas")
        .select("id, nombre_completo, telefono")
        .execute()
    )

    atletas = res.data or []

    print(f"Encontrados {len(atletas)} alumnos.")

    for atleta in atletas:

        if not atleta.get("telefono"):

            print(
                f"⏭️  {atleta.get('nombre_completo')} "
                f"sin teléfono, salteado."
            )

            continue

        generar_automatizaciones_alumno(
            atleta["id"]
        )

        print(
            f"✅ Automatizaciones generadas: "
            f"{atleta.get('nombre_completo')}"
        )

    print("Listo.")


if __name__ == "__main__":
    main()