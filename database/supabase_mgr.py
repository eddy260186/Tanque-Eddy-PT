import streamlit as st
from supabase import create_client, Client

@st.cache_resource
def init_supabase():
    """
    Establece la conexión con Supabase usando las credenciales 
    almacenadas en los Secrets de Streamlit.
    """
    try:
        url = st.secrets["SUPABASE_URL"]
        key = st.secrets["SUPABASE_KEY"]
        return create_client(url, key)
    except Exception as e:
        # Si no hay credenciales, devuelve None para trabajar en modo local
        return None