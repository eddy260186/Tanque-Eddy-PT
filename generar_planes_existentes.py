"""
SCRIPT DE UNA SOLA VEZ — PLAN PARA ALUMNOS EXISTENTES

Los alumnos NUEVOS reciben su plan automaticamente al
registrarse (onboarding en alumno.py). Este script hace
lo mismo para los alumnos que YA EXISTIAN antes:

Por cada alumno con telefono que NO tenga rutina/comidas:
1. Genera su rutina semanal desde data/ejercicios.py
2. Genera su dieta con horarios desde data/alimentos.py
3. Genera su lista de compras mensual
4. Regenera su agenda de WhatsApp (agua periodica,
   comidas, entreno, checkin)

Ejecutar desde la raiz del proyecto:
    python generar_planes_existentes.py
"""

from dotenv import load_dotenv
load_dotenv()

from database.conexion import supabase
from backend.services.onboarding_service import generar_plan_inicial_completo
from automation.generador_automatizaciones import generar_automatizaciones_alumno
from backend.services.suplementos_ia import asignar_suplementacion_automatica


def main():

    res = (
        supabase
        .table("perfiles_atletas")
        .select("*")
        .execute()
    )

    atletas = res.data or []

    print(f"Encontrados {len(atletas)} alumnos.\n")

    for atleta in atletas:

        nombre = atleta.get("nombre_completo", "?")
        alumno_id = atleta["id"]

        if not atleta.get("telefono"):

            print(f"⏭️  {nombre}: sin teléfono, salteado.")

            continue

        # --- Datos del perfil (con defaults razonables) ---

        peso = float(atleta.get("peso_actual") or 75)

        calorias = int(
            atleta.get("calorias_actuales") or 2000
        )

        # Macros: del perfil si existen, sino calculados
        # con formula estandar (P 2g/kg, G 0.9g/kg, resto C)
        proteina_g = round(peso * 2.0)
        grasa_g = round(peso * 0.9)

        carbos_g = round(max(
            (calorias - proteina_g * 4 - grasa_g * 9) / 4,
            50
        ))

        dieta = (
            atleta.get("dieta_activa")
            or "Clásica / Equilibrada"
        )

        tipo_entreno = (
            atleta.get("tipo_entrenamiento")
            or "Fuerza / Hipertrofia (Gimnasio)"
        )

        nivel = (
            atleta.get("nivel_experiencia")
            or "Principiante"
        )

        dias = int(atleta.get("dias_entreno") or 3)

        pais = atleta.get("pais") or "Argentina"

        hora_despertar = str(
            atleta.get("hora_despertar") or "06:30"
        )[:5]

        # --- Generar plan (solo si no tiene nada) ---

        dias_creados, comidas_creadas = (
            generar_plan_inicial_completo(
                alumno_id=alumno_id,
                tipo_entreno=tipo_entreno,
                nivel_experiencia=nivel,
                dias_entreno=dias,
                p_g_total=proteina_g,
                c_g_total=carbos_g,
                g_g_total=grasa_g,
                num_comidas=4,
                dieta_tipo=dieta,
                pais=pais,
                cal_objetivo=calorias,
                hora_despertar=hora_despertar,
                num_opciones=3
            )
        )

        # --- Suplementación automática (por detrás) ---

        estado_sup, _ = asignar_suplementacion_automatica(
            alumno_id, solo_si_vacio=True
        )

        # --- Regenerar agenda con todo incluido ---

        generar_automatizaciones_alumno(alumno_id)

        suple_txt = {
            "asignado": "💊 suplementos asignados",
            "revision_manual": "⚠️ suplementación MANUAL (caso médico)",
            "ya_tenia": "💊 ya tenía suplementos",
            "error": "💊 sin suplementos"
        }.get(estado_sup, "")

        if dias_creados or comidas_creadas:

            print(
                f"✅ {nombre}: {dias_creados} días de rutina, "
                f"{comidas_creadas} comidas, {suple_txt}, "
                f"agenda regenerada."
            )

        else:

            print(
                f"♻️  {nombre}: ya tenía plan, {suple_txt}, "
                f"agenda regenerada."
            )

    print("\nListo. 🏆")


if __name__ == "__main__":
    main()