# ai/providers/gemini_provider.py
import streamlit as st
import google.generativeai as genai
from utils.logger import obtener_logger

logger = obtener_logger("GeminiProvider")

def inicializar_gemini():
    """Configura la conexión con la API de Google Gemini usando los secretos."""
    try:
        api_key = st.secrets.get("GEMINI_API_KEY", "")
        if not api_key:
            logger.error("No se encontró GEMINI_API_KEY en los secretos.")
            return False
        
        genai.configure(api_key=api_key)
        return True
    except Exception as e:
        logger.error(f"Error inicializando Gemini: {e}")
        return False

def generar_texto(prompt: str, modelo: str = "gemini-1.5-flash", temperatura: float = 0.7) -> str:
    """Envía un prompt a Gemini y devuelve el texto limpio."""
    if not inicializar_gemini():
        return "Error: Inteligencia Artificial desconectada."
        
    try:
        model = genai.GenerativeModel(modelo)
        # Configuramos la creatividad (temperatura)
        generation_config = genai.types.GenerationConfig(temperature=temperatura)
        
        response = model.generate_content(prompt, generation_config=generation_config)
        return response.text.strip()
    except Exception as e:
        logger.error(f"Error generando texto con IA: {e}")
        return f"Error procesando la solicitud con IA."