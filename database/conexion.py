from supabase import create_client, Client
from config.settings import settings
from utils.logger import obtener_logger

logger = obtener_logger("DatabaseConnection")

def inicializar_supabase() -> Client:
    try:
        if not settings.SUPABASE_URL or not settings.SUPABASE_KEY:
            raise ValueError("Faltan las credenciales de Supabase en la configuración.")
        
        client = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)
        logger.info("⚡ Conexión exitosa con Supabase establecida.")
        return client
    except Exception as e:
        logger.error(f"❌ Error al conectar con Supabase: {str(e)}")
        raise e

# Instancia única reutilizable en todo el proyecto
supabase = inicializar_supabase()