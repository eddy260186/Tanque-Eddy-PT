import streamlit as st
from supabase import create_client, Client

# Cacheamos la conexión para que la app sea rapidísima
@st.cache_resource
def init_supabase() -> Client:
    # Streamlit va a buscar estas claves en su bóveda secreta
    url: str = st.secrets["SUPABASE_URL"]
    key: str = st.secrets["SUPABASE_KEY"]
    return create_client(url, key)