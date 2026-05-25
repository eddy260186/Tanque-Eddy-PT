import os
import streamlit as st

class Settings:
    # Supabase Config (Intenta leer de st.secrets para producción o de variables de entorno)
    SUPABASE_URL = st.secrets.get("SUPABASE_URL") or os.getenv("SUPABASE_URL", "https://tu-url.supabase.co")
    SUPABASE_KEY = st.secrets.get("SUPABASE_KEY") or os.getenv("SUPABASE_KEY", "tu-anon-key")
    
    # AI Config
    GEMINI_API_KEY = st.secrets.get("GEMINI_API_KEY") or os.getenv("GEMINI_API_KEY", "")
    
    # WhatsApp Config (Meta Cloud API / Proveedor Externo)
    WHATSAPP_TOKEN = st.secrets.get("WHATSAPP_TOKEN") or os.getenv("WHATSAPP_TOKEN", "")
    WHATSAPP_PHONE_NUMBER_ID = st.secrets.get("WHATSAPP_PHONE_NUMBER_ID") or os.getenv("WHATSAPP_PHONE_NUMBER_ID", "")

settings = Settings()