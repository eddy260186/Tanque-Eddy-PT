from datetime import datetime, timedelta
from database.conexion import supabase
from utils.logger import obtener_logger

logger = obtener_logger("GeneradorAutomatizaciones")


def generar_automatizaciones_alumno(alumno_id: str):

    """
    Genera automáticamente:
    - agua
    - comidas
    - entrenamiento
    - suplementos
    - checkins
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

        hora_entreno = atleta.get(
            "hora_entreno",
            "08:00"
        )

        agua = float(
            atleta.get(
                "agua_actual",
                3.0
            )
        )

        rutina = atleta.get(
            "rutina_activa",
            "Rutina del día"
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
        # CALCULAR HORARIOS
        # =====================================================

        hora_dt = datetime.strptime(
            hora_entreno,
            "%H:%M"
        )

        desayuno = (
            hora_dt - timedelta(hours=1)
        ).strftime("%H:%M")

        agua_1 = (
            hora_dt - timedelta(hours=2)
        ).strftime("%H:%M")

        post_entreno = (
            hora_dt + timedelta(hours=1)
        ).strftime("%H:%M")

        almuerzo = (
            hora_dt + timedelta(hours=5)
        ).strftime("%H:%M")

        check_noche = "22:00"

        # =====================================================
        # AUTOMATIZACIONES
        # =====================================================

        automatizaciones = [

            {
                "alumno_id": alumno_id,
                "tipo_alerta": "agua",
                "hora_programada": agua_1,
                "mensaje_plantilla": f"Meta diaria: {agua}L"
            },

            {
                "alumno_id": alumno_id,
                "tipo_alerta": "comida",
                "hora_programada": desayuno,
                "mensaje_plantilla": "Desayuno pre-entreno"
            },

            {
                "alumno_id": alumno_id,
                "tipo_alerta": "entrenamiento",
                "hora_programada": hora_entreno,
                "mensaje_plantilla": rutina
            },

            {
                "alumno_id": alumno_id,
                "tipo_alerta": "suplementos",
                "hora_programada": post_entreno,
                "mensaje_plantilla": "Creatina + proteína"
            },

            {
                "alumno_id": alumno_id,
                "tipo_alerta": "comida",
                "hora_programada": almuerzo,
                "mensaje_plantilla": "Almuerzo principal"
            },

            {
                "alumno_id": alumno_id,
                "tipo_alerta": "pesaje",
                "hora_programada": check_noche,
                "mensaje_plantilla": "Registrar progreso diario"
            }
        ]

        # =====================================================
        # INSERTAR EN BASE DE DATOS
        # =====================================================

        supabase.table(
            "automatizaciones"
        ).insert(
            automatizaciones
        ).execute()

        logger.info(
            f"✅ Automatizaciones creadas para atleta {alumno_id}"
        )

    except Exception as e:

        logger.error(
            f"❌ Error generando automatizaciones: {str(e)}"
        )