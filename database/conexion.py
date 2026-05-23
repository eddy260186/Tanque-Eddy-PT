import streamlit as st
from supabase import create_client, Client

# Inicializamos la conexión una sola vez y la guardamos en caché
@st.cache_resource
def iniciar_conexion() -> Client:
    try:
        url = st.secrets["SUPABASE_URL"]
        key = st.secrets["SUPABASE_KEY"]
        return create_client(url, key)
    except Exception as e:
        st.error(f"❌ Error crítico al conectar con la base de datos: {e}")
        st.stop()

# Exportamos la variable maestra para usarla en el resto del proyecto
supabase = iniciar_conexion()