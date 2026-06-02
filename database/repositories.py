
from database.conexion import supabase
from utils.logger import obtener_logger
from automation.generador_automatizaciones import generar_automatizaciones_alumno

logger = obtener_logger("Repositories")


class AtletaRepository:
    """
    Clase exclusiva para manejar consultas y actualizaciones
    del perfil central del atleta.
    """

    @staticmethod
    def actualizar_plan_y_metas(
        alumno_id: str,
        rutina: str,
        dieta: str,
        peso_obj: float,
        plazo: int,
        peso_actual: float = None,
        grasa_actual: float = None,
        calorias_actuales: int = None,
        agua_actual: float = None,
        objetivo_actual: str = None,
        nivel_experiencia: str = None,
        tipo_entrenamiento: str = None,
        dias_entreno: int = None,
        hora_entreno: str = None
    ) -> bool:

        """
        Actualiza toda la información viva del atleta
        y genera automatizaciones inteligentes.
        """

        try:

            datos_actualizacion = {
                "rutina_activa": rutina,
                "dieta_activa": dieta,
                "peso_objetivo": peso_obj,
                "plazo_meses": plazo
            }

            # =====================================================
            # DATOS OPCIONALES
            # =====================================================

            if peso_actual is not None:
                datos_actualizacion["peso_actual"] = peso_actual

            if grasa_actual is not None:
                datos_actualizacion["grasa_actual"] = grasa_actual

            if calorias_actuales is not None:
                datos_actualizacion["calorias_actuales"] = calorias_actuales

            if agua_actual is not None:
                datos_actualizacion["agua_actual"] = agua_actual

            if objetivo_actual is not None:
                datos_actualizacion["objetivo_actual"] = objetivo_actual

            if nivel_experiencia is not None:
                datos_actualizacion["nivel_experiencia"] = nivel_experiencia

            if tipo_entrenamiento is not None:
                datos_actualizacion["tipo_entrenamiento"] = tipo_entrenamiento

            if dias_entreno is not None:
                datos_actualizacion["dias_entreno"] = dias_entreno

            if hora_entreno is not None:
                datos_actualizacion["hora_entreno"] = hora_entreno

            # =====================================================
            # ACTUALIZAR PERFIL CENTRAL
            # =====================================================

            response = (
                supabase
                .table("perfiles_atletas")
                .update(datos_actualizacion)
                .eq("id", alumno_id)
                .execute()
            )

            logger.info(
                f"✅ Perfil atleta actualizado correctamente: {alumno_id}"
            )

            # =====================================================
            # GENERAR AUTOMATIZACIONES AUTOMÁTICAS
            # =====================================================

            generar_automatizaciones_alumno(
                alumno_id
            )

            return len(response.data) > 0

        except Exception as e:

            logger.error(
                f"❌ Error DB actualizando atleta {alumno_id}: {e}"
            )

            return False

