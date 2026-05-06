import streamlit as st

def aplicar_diseno_elite():
    st.markdown("""
    <style>
    /* FONDO GENERAL EXTRA OSCURO */
    .stApp {
        background-color: #0b0e14 !important;
        color: #ffffff;
        font-family: 'Segoe UI', sans-serif;
    }

    /* SIDEBAR OSCURO CON LINEA DORADA BRILLANTE */
    section[data-testid="stSidebar"] {
        background-color: #12161f !important;
        border-right: 2px solid #d4af37 !important;
        box-shadow: 2px 0px 15px rgba(212, 175, 55, 0.15);
    }

    /* TITULOS EN DORADO PREMIUM */
    h1, h2, h3 { 
        color: #d4af37 !important; 
        font-weight: 800 !important; 
        letter-spacing: 1px;
    }

    /* BOTONES ESTILO NEÓN DORADO */
    .stButton > button {
        background: linear-gradient(90deg, #d4af37, #fde08b) !important;
        color: #000000 !important;
        border-radius: 10px !important;
        border: none !important;
        font-weight: 800 !important;
        text-transform: uppercase;
        box-shadow: 0px 0px 15px rgba(212, 175, 55, 0.4) !important;
        transition: all 0.3s ease;
        width: 100%;
    }
    .stButton > button:hover {
        transform: scale(1.03);
        box-shadow: 0px 0px 25px rgba(212, 175, 55, 0.7) !important;
    }

    /* TARJETAS DE MÉTRICAS */
    [data-testid="stMetric"] {
        background-color: #151a26 !important;
        padding: 20px !important;
        border-radius: 12px !important;
        border: 1px solid #d4af37 !important;
        box-shadow: 0px 0px 12px rgba(212, 175, 55, 0.2) !important;
    }
    
    [data-testid="stMetricValue"] {
        color: #fde08b !important;
        font-weight: bold !important;
    }

    /* INPUTS Y CAJAS DE TEXTO */
    .stTextInput input, .stNumberInput input, .stSelectbox div[data-baseweb="select"] {
        background-color: #151a26 !important;
        border: 1px solid #d4af37 !important;
        border-radius: 8px !important;
        color: white !important;
    }
    
    .stTextInput input:focus, .stNumberInput input:focus {
        border-color: #fde08b !important;
        box-shadow: 0px 0px 10px rgba(212, 175, 55, 0.5) !important;
    }

    header[data-testid="stHeader"] {
        background: transparent !important;
    }
    </style>
    """, unsafe_allow_html=True)