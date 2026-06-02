# database/repositories.py

from database.conexion import supabase
from utils.logger import obtener_logger

logger = obtener_logger("Repositories")


class AtletaRepository:
    """
    Clase exclusiva para manejar las consultas de atletas.
    Será el núcleo central de IA + WhatsApp + Automatizaciones.
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
        Actualiza TODA la información viva del atleta.
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
            # UPDATE CENTRAL
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

            return len(response.data) > 0

        except Exception as e:

            logger.error(
                f"❌ Error DB actualizando atleta {alumno_id}: {e}"
            )

            return False