import os
import streamlit as st
from database.conexion import supabase


def _renderizar_estilos_login():
    st.markdown("""
    <style>
    .login-shell {
        height: 0;
        margin: 0;
        padding: 0;
    }

    div[data-testid="stHorizontalBlock"]:has(.login-image-wrap) {
        width: min(100%, 1060px);
        margin: clamp(1.5rem, 10vh, 5rem) auto 0;
        align-items: center;
    }

    .login-panel-title {
        color: #f4d47c;
        font-size: 1.05rem;
        font-weight: 750;
        margin: 0 0 0.35rem 0;
    }

    .login-helper {
        color: #b7bdca;
        font-size: 0.95rem;
        line-height: 1.45;
        margin-bottom: 1.25rem;
    }

    .login-field-label {
        color: #f4d47c;
        font-weight: 700;
        margin: 0.9rem 0 0.35rem 0;
    }

    .login-quote {
        color: #9ca3b5;
        font-style: italic;
        line-height: 1.45;
        text-align: center;
        margin-top: 1.25rem;
    }

    .login-image-wrap img {
        width: 100%;
        max-width: 560px;
        border-radius: 8px;
        border: 1px solid rgba(212, 175, 55, 0.26);
        box-shadow: 0 18px 42px rgba(0, 0, 0, 0.26);
    }

    @media (max-width: 768px) {
        .login-shell {
            height: 0;
            padding: 0;
        }

        div[data-testid="stHorizontalBlock"]:has(.login-image-wrap) {
            width: 100%;
            margin-top: 0.75rem;
        }

        .login-image-wrap img {
            max-height: 360px;
            object-fit: contain;
        }

        .login-helper {
            margin-bottom: 0.75rem;
        }
    }
    </style>
    """, unsafe_allow_html=True)


def _mostrar_imagen_login():
    dir_raiz = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    archivos_tanque = [
        f for f in os.listdir(dir_raiz)
        if "tanque" in f.lower() and f.lower().endswith(".png")
    ]

    st.markdown('<div class="login-image-wrap">', unsafe_allow_html=True)
    if archivos_tanque:
        ruta_segura = os.path.join(dir_raiz, archivos_tanque[0])
        st.image(ruta_segura, use_column_width=True)
    else:
        st.warning("La imagen principal no se encontro en la carpeta del proyecto.")
    st.markdown('</div>', unsafe_allow_html=True)


def renderizar_login():
    """
    Sistema de autenticacion con Supabase Auth.
    Devuelve True si el usuario ya esta autenticado, o False si muestra la pantalla.
    """
    if "usuario_actual" not in st.session_state:
        st.session_state["usuario_actual"] = None

    if st.session_state["usuario_actual"] is not None:
        return True

    _renderizar_estilos_login()
    st.markdown('<div class="login-shell">', unsafe_allow_html=True)

    _, col_izq, col_der, _ = st.columns([0.18, 1.15, 1.0, 0.18], gap="large")

    with col_izq:
        _mostrar_imagen_login()

    with col_der:
        st.markdown('<p class="login-panel-title">Acceso a tu panel</p>', unsafe_allow_html=True)
        st.markdown(
            '<p class="login-helper">Ingresa con tu cuenta o crea un perfil nuevo para empezar a usar la plataforma.</p>',
            unsafe_allow_html=True,
        )

        tab_login, tab_registro = st.tabs(["Iniciar sesion", "Crear cuenta"])

        with tab_login:
            st.markdown('<p class="login-field-label">Correo electronico</p>', unsafe_allow_html=True)
            email_login = st.text_input(
                "Correo",
                key="log_email",
                label_visibility="collapsed",
                placeholder="tu@email.com",
            )

            st.markdown('<p class="login-field-label">Contrasena</p>', unsafe_allow_html=True)
            pass_login = st.text_input(
                "Contrasena",
                type="password",
                key="log_pass",
                label_visibility="collapsed",
                placeholder="Ingresa tu contrasena",
            )

            if st.button("Entrar", type="primary", width="stretch"):
                if not email_login or not pass_login:
                    st.warning("Completa correo y contrasena para ingresar.")
                else:
                    try:
                        respuesta = supabase.auth.sign_in_with_password({
                            "email": email_login.lower().strip(),
                            "password": pass_login,
                        })
                        st.session_state["usuario_actual"] = respuesta.user.email
                        st.success("Acceso concedido.")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error login: {e}")

            st.markdown(
                '<p class="login-quote">"La excelencia no es un acto, es un habito.<br>Tu eres tu unico limite."</p>',
                unsafe_allow_html=True,
            )

        with tab_registro:
            st.markdown('<p class="login-field-label">Nombre completo</p>', unsafe_allow_html=True)
            nombre_reg = st.text_input(
                "Nombre",
                key="reg_nombre",
                label_visibility="collapsed",
                placeholder="Nombre y apellido",
            )

            st.markdown('<p class="login-field-label">Correo electronico</p>', unsafe_allow_html=True)
            email_reg = st.text_input(
                "Correo Reg",
                key="reg_email",
                label_visibility="collapsed",
                placeholder="tu@email.com",
            )

            st.markdown('<p class="login-field-label">Contrasena</p>', unsafe_allow_html=True)
            pass_reg = st.text_input(
                "Pass Reg",
                type="password",
                key="reg_pass",
                label_visibility="collapsed",
                placeholder="Minimo 6 caracteres",
            )

            st.markdown('<p class="login-field-label">Genero</p>', unsafe_allow_html=True)
            genero = st.selectbox(
                "Genero",
                ["Masculino", "Femenino"],
                key="reg_genero",
                label_visibility="collapsed",
            )

            if st.button("Crear mi cuenta", type="primary", width="stretch"):
                if not nombre_reg or not email_reg or not pass_reg:
                    st.warning("Completa nombre, correo y contrasena para crear tu cuenta.")
                else:
                    try:
                        email_final = email_reg.lower().strip()
                        supabase.auth.sign_up({"email": email_final, "password": pass_reg})
                        supabase.table("perfiles_atletas").insert({
                            "email": email_final,
                            "nombre_completo": nombre_reg.strip(),
                            "genero": "m" if genero == "Masculino" else "f",
                        }).execute()
                        st.success("Cuenta creada correctamente. Ahora inicia sesion para entrar.")
                    except Exception as e:
                        st.error(f"Error en el registro: {e}")

    st.markdown('</div>', unsafe_allow_html=True)
    return False

