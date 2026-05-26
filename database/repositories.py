# database/repositories.py
from database.conexion import supabase
from utils.logger import obtener_logger

logger = obtener_logger("Repositories")

class AtletaRepository:
    """Clase exclusiva para manejar las consultas de los atletas a la base de datos."""
    
    @staticmethod
    def actualizar_plan_y_metas(alumno_id: str, rutina: str, dieta: str, peso_obj: float, plazo: int) -> bool:
        """Guarda la nueva rutina y dieta del alumno en Supabase."""
        try:
            response = supabase.table("perfiles_atletas").update({
                "rutina_activa": rutina,
                "dieta_activa": dieta,
                "peso_objetivo": peso_obj,
                "plazo_meses": plazo
            }).eq("id", alumno_id).execute()
            
            # Devuelve True si se actualizó correctamente
            return len(response.data) > 0
        except Exception as e:
            logger.error(f"Error DB actualizando plan de {alumno_id}: {e}")
            return False