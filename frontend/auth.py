import streamlit as st
import os
from database.conexion import supabase

def renderizar_login():
    """
    Pieza 1: Sistema de Autenticación VIP (Login y Registro)
    Maneja la interfaz responsiva dorada y las credenciales con Supabase Auth.
    Devuelve True si el usuario ya está autenticado, o False si se está mostrando la pantalla.
    """
    if "usuario_actual" not in st.session_state:
        st.session_state["usuario_actual"] = None

    # Si ya hay una sesión activa, devuelve True de inmediato
    if st.session_state["usuario_actual"] is not None:
        return True

    # ==========================================
    # ESTILOS CSS VIP DORADOS Y RESPONSIVOS (EDICIÓN PIXEL PERFECT)
    # ==========================================
    st.markdown("""
    <style>
    /* Estilizamos las cajas de texto con bordes dorados cuando se seleccionan */
    div[data-baseweb="input"] > div {
        background-color: #1a1a1a !important;
        border: 1px solid #333 !important;
        border-radius: 8px !important;
    }
    div[data-baseweb="input"] > div:focus-within {
        border: 1px solid #d4af37 !important;
        box-shadow: 0 0 5px rgba(212,175,55,0.5) !important;
    }
    /* Botón dorado VIP */
    .stButton>button{
        background: linear-gradient(90deg, #b8860b 0%, #ffd700 50%, #b8860b 100%);
        color: black !important;
        border: none;
        border-radius:8px;
        font-weight:800;
        height:50px;
        font-size:18px;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: scale(1.02);
        box-shadow: 0 0 15px rgba(212,175,55,0.6);
    }
    
    /* 💎 MAGIA RESPONSIVA: ELIMINACIÓN DEL CRÁTER EN CELULARES 💎 */
    .espaciador-vip {
        height: 120px; /* En PC lo empuja para abajo para centrarlo con la foto */
    }
    
    @media (max-width: 768px) {
        /* 1. Apagamos el espaciador de computadora */
        .espaciador-vip {
            height: 0px !important;
            display: none !important;
        }
        
        /* 2. FOTO DE BORDE A BORDE: Eliminamos los márgenes laterales de Streamlit */
        .block-container {
            padding-left: 0rem !important;
            padding-right: 0rem !important;
            padding-top: 1rem !important;
            max-width: 100% !important;
        }
        
        /* 3. TRACCIÓN VIP (PUNTO DULCE): Subimos -65px exactos para no amontonar */
        div[data-testid="stTabs"] {
            margin-top: -65px !important; 
            position: relative;
            z-index: 99; 
            padding-left: 1.5rem !important; /* Devolvemos un pequeño margen para que el texto no toque el borde del teléfono */
            padding-right: 1.5rem !important;
        }
    }
    </style>
    """, unsafe_allow_html=True)

    # ==========================================
    # ESTRUCTURA DE 2 COLUMNAS (MAGIA PURA)
    # ==========================================
    col_izq, col_der = st.columns([1.4, 1.0], gap="large")

    with col_izq:
        # Buscamos la súper imagen subiendo un nivel hacia la raíz del proyecto
        dir_raiz = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        archivos_tanque = [f for f in os.listdir(dir_raiz) if "tanque" in f.lower() and f.lower().endswith(".png")]
        
        if archivos_tanque:
            ruta_segura = os.path.join(dir_raiz, archivos_tanque[0])
            # CORRECCIÓN DE ARQUITECTURA: Se utiliza use_column_width=True para compatibilidad absoluta en la nube
            st.image(ruta_segura, use_column_width=True)
        else:
            st.error("❌ La súper imagen no se encontró en el servidor de GitHub.")

    with col_der:
        st.markdown("<div class='espaciador-vip'></div>", unsafe_allow_html=True) 
        tab_login, tab_registro = st.tabs(["Iniciar Sesión", "Crear Cuenta Nueva"])

        with tab_login:
            st.markdown("<p style='color:#d4af37; font-weight:bold; margin-bottom:5px;'>✉️ Correo electrónico</p>", unsafe_allow_html=True)
            email_login = st.text_input("Correo", key="log_email", label_visibility="collapsed", placeholder="Ingresa tu correo electrónico")
            
            st.markdown("<p style='color:#d4af37; font-weight:bold; margin-top:15px; margin-bottom:5px;'>🔒 Contraseña</p>", unsafe_allow_html=True)
            pass_login = st.text_input("Pass", type="password", key="log_pass", label_visibility="collapsed", placeholder="Ingresa tu contraseña")
            
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("ENTRAR ➔", type="primary", use_container_width=True):
                try:
                    respuesta = supabase.auth.sign_in_with_password({"email": email_login.lower().strip(), "password": pass_login})
                    st.session_state["usuario_actual"] = respuesta.user.email
                    st.success("¡Acceso concedido!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error login: {e}")
            
            st.markdown("<br><p style='text-align:center; color:#888; font-style:italic;'>\"La excelencia no es un acto, es un hábito.<br>Tú eres tu único límite.\"</p>", unsafe_allow_html=True)

        with tab_registro:
            st.markdown("<p style='color:#d4af37; font-weight:bold; margin-bottom:5px;'>👤 Nombre completo</p>", unsafe_allow_html=True)
            nombre_reg = st.text_input("Nombre", key="reg_nombre", label_visibility="collapsed", placeholder="Ingresa tu nombre y apellido")
            
            st.markdown("<p style='color:#d4af37; font-weight:bold; margin-top:15px; margin-bottom:5px;'>✉️ Correo electrónico</p>", unsafe_allow_html=True)
            email_reg = st.text_input("Correo Reg", key="reg_email", label_visibility="collapsed", placeholder="Ingresa tu mejor correo")
            
            st.markdown("<p style='color:#d4af37; font-weight:bold; margin-top:15px; margin-bottom:5px;'>🔒 Contraseña secreta</p>", unsafe_allow_html=True)
            pass_reg = st.text_input("Pass Reg", type="password", key="reg_pass", label_visibility="collapsed", placeholder="Crea una contraseña fuerte")
            
            st.markdown("<p style='color:#d4af37; font-weight:bold; margin-top:15px; margin-bottom:5px;'>⚧️ Género</p>", unsafe_allow_html=True)
            genero = st.selectbox("Género", ["Masculino", "Femenino"], key="reg_genero", label_visibility="collapsed")
            
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("CREAR MI CUENTA ELITE ➔", type="primary", use_container_width=True):
                try:
                    email_final = email_reg.lower().strip()
                    respuesta = supabase.auth.sign_up({"email": email_final, "password": pass_reg})
                    # Entrada simplificada m/f para tu base de datos
                    supabase.table("perfiles_atletas").insert({
                        "email": email_final, 
                        "nombre_completo": nombre_reg, 
                        "genero": "m" if genero == "Masculino" else "f"
                    }).execute()
                    st.success("✅ ¡Cuenta VIP creada correctamente! Volvé a la pestaña de Iniciar Sesión para entrar.")
                except Exception as e:
                    st.error(f"Error en el registro: {e}")

    return False