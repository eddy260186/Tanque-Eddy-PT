import os


def _leer_secreto(nombre: str, default: str = "") -> str:
    valor_entorno = os.getenv(nombre)
    if valor_entorno:
        return valor_entorno

    try:
        import streamlit as st
        return st.secrets.get(nombre, default)
    except Exception:
        return default


class Settings:
    # Supabase Config
    SUPABASE_URL = _leer_secreto("SUPABASE_URL", "https://tu-url.supabase.co")
    SUPABASE_KEY = _leer_secreto("SUPABASE_KEY", "tu-anon-key")

    # AI Config
    GEMINI_API_KEY = _leer_secreto("GEMINI_API_KEY", "")

    # WhatsApp / Meta Cloud API
    WHATSAPP_TOKEN = _leer_secreto("WHATSAPP_TOKEN", "")
    WHATSAPP_PHONE_NUMBER_ID = _leer_secreto("WHATSAPP_PHONE_NUMBER_ID", "")
    WHATSAPP_VERIFY_TOKEN = _leer_secreto("WHATSAPP_VERIFY_TOKEN", "mi_token_secreto_eddy_pt_2026")

    # Mercado Pago
    MERCADO_PAGO_TOKEN = _leer_secreto("MERCADO_PAGO_TOKEN", "")


settings = Settings()
