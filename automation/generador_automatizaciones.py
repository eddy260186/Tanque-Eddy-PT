from datetime import datetime, timedelta

from database.conexion import supabase
from utils.logger import obtener_logger

logger = obtener_logger("GeneradorAutomatizaciones")


def generar_automatizaciones_alumno(alumno_id: str):

    """
    Genera el DIA COMPLETO del agente autonomo:

    - resumen_diario     (al despertar: rutina + macros)
    - comida x N         (cada comida programada en su hora)
    - agua               (2h antes de entrenar)
    - entrenamiento      (avisa 1h antes + rutina completa)
    - post_entreno       (1.5h despues: pregunta como fue)
    - checkin_nocturno   (22:00: cumpliste 1/2/3)
    """

    try:

        # =====================================================
        # OBTENER PERFIL DEL ATLETA
        # =====================================================

        response = (
            supabase
            .table("perfiles_atletas")
            .select("*")
            .eq("id", alumno_id)
            .execute()
        )

        if not response.data:

            logger.warning(
                f"⚠️ No existe atleta: {alumno_id}"
            )

            return

        atleta = response.data[0]

        # =====================================================
        # DATOS PRINCIPALES
        # =====================================================

        hora_entreno = str(
            atleta.get("hora_entreno")
            or "18:00"
        )[:5]

        hora_despertar = str(
            atleta.get("hora_despertar")
            or "06:30"
        )[:5]

        hora_dormir = str(
            atleta.get("hora_dormir")
            or "23:00"
        )[:5]

        agua = float(
            atleta.get("agua_actual")
            or 3.0
        )

        # =====================================================
        # LIMPIAR AUTOMATIZACIONES ANTERIORES
        # =====================================================

        supabase.table(
            "automatizaciones"
        ).delete().eq(
            "alumno_id",
            alumno_id
        ).execute()

        # =====================================================
        # CALCULAR HORARIOS RELATIVOS AL ENTRENO
        # =====================================================

        hora_dt = datetime.strptime(
            hora_entreno,
            "%H:%M"
        )

        pre_entreno = (
            hora_dt - timedelta(hours=1)
        ).strftime("%H:%M")

        post_entreno = (
            hora_dt + timedelta(minutes=90)
        ).strftime("%H:%M")

        # Suplementos: pre 40min antes, post al terminar (+5min)
        suple_pre = (
            hora_dt - timedelta(minutes=40)
        ).strftime("%H:%M")

        suple_post = (
            hora_dt + timedelta(minutes=5)
        ).strftime("%H:%M")

        # Suplemento de la mañana: 15 min despues de despertar
        suple_manana = (
            datetime.strptime(hora_despertar, "%H:%M")
            + timedelta(minutes=15)
        ).strftime("%H:%M")

        # Suplemento de la noche: 30 min antes de dormir
        suple_noche = (
            datetime.strptime(hora_dormir, "%H:%M")
            - timedelta(minutes=30)
        ).strftime("%H:%M")

        # =====================================================
        # AUTOMATIZACIONES BASE
        # =====================================================

        automatizaciones = [

            {
                "alumno_id": alumno_id,
                "tipo_alerta": "resumen_diario",
                "hora_programada": hora_despertar,
                "mensaje_plantilla": "Resumen del día"
            },

            {
                "alumno_id": alumno_id,
                "tipo_alerta": "pre_entrenamiento",
                "hora_programada": pre_entreno,
                "mensaje_plantilla": "Aviso 60 min antes"
            },

            {
                "alumno_id": alumno_id,
                "tipo_alerta": "entrenamiento",
                "hora_programada": hora_entreno,
                "mensaje_plantilla": "Rutina del día"
            },

            {
                "alumno_id": alumno_id,
                "tipo_alerta": "post_entreno",
                "hora_programada": post_entreno,
                "mensaje_plantilla": "Feedback post entreno"
            },

            {
                "alumno_id": alumno_id,
                "tipo_alerta": "checkin_nocturno",
                "hora_programada": "22:00",
                "mensaje_plantilla": "Cierre del día"
            },

            {
                "alumno_id": alumno_id,
                "tipo_alerta": "suple_manana",
                "hora_programada": suple_manana,
                "mensaje_plantilla": "Suplementos mañana"
            },

            {
                "alumno_id": alumno_id,
                "tipo_alerta": "suple_pre_entreno",
                "hora_programada": suple_pre,
                "mensaje_plantilla": "Suplementos pre-entreno"
            },

            {
                "alumno_id": alumno_id,
                "tipo_alerta": "suple_post_entreno",
                "hora_programada": suple_post,
                "mensaje_plantilla": "Suplementos post-entreno"
            },

            {
                "alumno_id": alumno_id,
                "tipo_alerta": "suple_noche",
                "hora_programada": suple_noche,
                "mensaje_plantilla": "Suplementos noche"
            }
        ]

        # =====================================================
        # AGUA PERIODICA (desde despertar+1h hasta dormir-1h)
        # Cambiar INTERVALO_AGUA_HORAS para mas/menos frecuencia
        # =====================================================

        INTERVALO_AGUA_HORAS = 2

        try:

            inicio_agua = datetime.strptime(
                hora_despertar, "%H:%M"
            ) + timedelta(hours=1)

            fin_agua = datetime.strptime(
                hora_dormir, "%H:%M"
            ) - timedelta(hours=1)

            # Cuantas tomas entran en el dia
            total_tomas = 0
            cursor = inicio_agua

            while cursor <= fin_agua and total_tomas < 12:
                total_tomas += 1
                cursor += timedelta(
                    hours=INTERVALO_AGUA_HORAS
                )

            litros_por_toma = (
                round(agua / total_tomas, 2)
                if total_tomas else agua
            )

            cursor = inicio_agua
            numero_toma = 1

            while (
                cursor <= fin_agua
                and numero_toma <= total_tomas
            ):

                automatizaciones.append({
                    "alumno_id": alumno_id,
                    "tipo_alerta": "agua",
                    "hora_programada": cursor.strftime("%H:%M"),
                    "mensaje_plantilla": (
                        f"Toma {numero_toma} de {total_tomas} "
                        f"· ~{litros_por_toma}L "
                        f"· Meta diaria: {agua}L"
                    )
                })

                cursor += timedelta(
                    hours=INTERVALO_AGUA_HORAS
                )

                numero_toma += 1

        except Exception as e:

            logger.warning(
                f"⚠️ No pude programar agua periodica: {str(e)}"
            )

        # =====================================================
        # COMIDAS PROGRAMADAS DEL ALUMNO
        # (una automatizacion por cada comida cargada)
        # =====================================================

        try:

            comidas = (
                supabase
                .table("comidas_programadas")
                .select("tipo_comida, hora")
                .eq("alumno_id", alumno_id)
                .eq("activa", True)
                .execute()
            )

            tipos_agregados = set()

            for comida in (comidas.data or []):

                tipo_comida = comida.get(
                    "tipo_comida"
                )

                hora_comida = str(
                    comida.get("hora") or ""
                )[:5]

                if (
                    not tipo_comida
                    or not hora_comida
                    or tipo_comida in tipos_agregados
                ):
                    continue

                tipos_agregados.add(tipo_comida)

                automatizaciones.append({
                    "alumno_id": alumno_id,
                    "tipo_alerta": "comida",
                    "hora_programada": hora_comida,
                    "mensaje_plantilla": tipo_comida
                })

        except Exception as e:

            logger.warning(
                f"⚠️ Sin comidas programadas: {str(e)}"
            )

        # =====================================================
        # INSERTAR EN BASE DE DATOS
        # =====================================================

        supabase.table(
            "automatizaciones"
        ).insert(
            automatizaciones
        ).execute()

        logger.info(
            f"✅ Día completo generado para atleta "
            f"{alumno_id}: {len(automatizaciones)} eventos"
        )

    except Exception as e:

        logger.error(
            f"❌ Error generando automatizaciones: {str(e)}"
        )