
import os

from supabase import create_client, Client
from utils.logger import obtener_logger

logger = obtener_logger("DatabaseConnection")


def inicializar_supabase() -> Client:

    try:

        # =====================================================
        # VARIABLES DE ENTORNO RAILWAY
        # =====================================================

        url = os.getenv("SUPABASE_URL")
        key = os.getenv("SUPABASE_KEY")

        # =====================================================
        # VALIDACION
        # =====================================================

        if not url or not key:

            raise Exception(
                "No se encontraron credenciales SUPABASE_URL o SUPABASE_KEY."
            )

        logger.info(
            "✅ Conectando a Supabase correctamente..."
        )

        # =====================================================
        # CONEXION
        # =====================================================

        cliente = create_client(
            url,
            key
        )

        logger.info(
            "✅ Supabase conectado exitosamente."
        )

        return cliente

    except Exception as e:

        logger.error(
            f"❌ Error al conectar Supabase: {str(e)}"
        )

        raise e


# =========================================================
# CLIENTE GLOBAL
# =========================================================

supabase = inicializar_supabase()
