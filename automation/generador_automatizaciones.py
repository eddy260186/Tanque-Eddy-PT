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

        agua_1 = (
            hora_dt - timedelta(hours=2)
        ).strftime("%H:%M")

        post_entreno = (
            hora_dt + timedelta(minutes=90)
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
                "tipo_alerta": "agua",
                "hora_programada": agua_1,
                "mensaje_plantilla": f"Meta diaria: {agua}L"
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
            }
        ]

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