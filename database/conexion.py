import os
import streamlit as st
from supabase import create_client, Client
from utils.logger import obtener_logger

logger = obtener_logger("DatabaseConnection")

def inicializar_supabase() -> Client:
    try:
        # Prioridad 1: Leer de las variables de entorno de Railway
        url = os.getenv("SUPABASE_URL")
        key = os.getenv("SUPABASE_KEY")
        
        # Prioridad 2: Leer de los secretos de Streamlit (por si acaso)
        if not url:
            url = st.secrets.get("SUPABASE_URL")
        if not key:
            key = st.secrets.get("SUPABASE_KEY")
            
        if not url or not key:
            raise Exception("No se encontraron credenciales de Supabase en el entorno.")
            
        logger.info("Conectando a Supabase con credenciales de entorno...")
        return create_client(url, key)
    except Exception as e:
        logger.error(f"❌ Error al conectar con Supabase: {e}")
        raise e

supabase = inicializar_supabase()