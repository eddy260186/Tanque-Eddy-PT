# core/session_manager.py
import streamlit as st

def iniciar_sesion(usuario_id: str, rol: str, nombre: str):
    """Guarda los datos del usuario de forma segura y estructurada en la sesión."""
    st.session_state["autenticado"] = True
    st.session_state["usuario_id"] = usuario_id
    st.session_state["rol"] = rol
    st.session_state["nombre"] = nombre

def cerrar_sesion():
    """Destruye por completo la sesión actual por seguridad."""
    for key in list(st.session_state.keys()):
        del st.session_state[key]

def esta_autenticado() -> bool:
    """Verifica rápidamente si hay un usuario activo."""
    return st.session_state.get("autenticado", False)

def obtener_usuario_actual() -> dict:
    """Retorna un diccionario limpio con los datos del usuario activo."""
    if esta_autenticado():
        return {
            "id": st.session_state.get("usuario_id"),
            "rol": st.session_state.get("rol"),
            "nombre": st.session_state.get("nombre")
        }
    return None

def obtener_rol_actual() -> str:
    """Atajo directo para saber el rol del usuario."""
    return st.session_state.get("rol", None)