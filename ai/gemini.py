import streamlit as st
import google.generativeai as genai

# Configuramos la API Key una sola vez
def configurar_gemini():
    try:
        api_key = st.secrets["GEMINI_API_KEY"]
        genai.configure(api_key=api_key)
    except Exception as e:
        st.error(f"❌ Error al configurar la API de Gemini: {e}")
        st.stop()

# Función maestra para generar la dieta con caché (Ahorra plata y RAM)
@st.cache_data(ttl=3600, show_spinner=False)
def generar_menu_ia(prompt: str) -> str:
    configurar_gemini()
    try:
        # Usamos el modelo más rápido y estable
        model = genai.GenerativeModel('gemini-2.5-flash')
        respuesta = model.generate_content(prompt)
        return respuesta.text
    except Exception as e:
        # Blindaje contra caídas de servidor de Google
        return f"⚠️ Error temporal del servidor de IA. Por favor, reintenta en unos segundos. Detalle: {e}"