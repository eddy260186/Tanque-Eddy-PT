# core/permissions.py
import streamlit as st
from core.constants import Roles, Permisos
from core.session_manager import obtener_rol_actual

# El Mapa Maestro: ¿Qué permisos tiene cada rol?
MAPA_PERMISOS = {
    Roles.ADMIN: [
        Permisos.VER_DASHBOARD_COACH, 
        Permisos.EDITAR_RUTINAS, 
        Permisos.ENVIAR_WHATSAPP, 
        Permisos.GESTIONAR_PAGOS
    ],
    Roles.TRAINER: [
        Permisos.VER_DASHBOARD_COACH, 
        Permisos.EDITAR_RUTINAS, 
        Permisos.ENVIAR_WHATSAPP
    ],
    Roles.ALUMNO: [
        Permisos.VER_FICHA_PROPIA
    ]
}

def tiene_permiso(permiso_requerido: str) -> bool:
    """
    Pregunta suave: Retorna True o False. 
    Ideal para ocultar botones silenciosamente.
    Ej: if tiene_permiso(Permisos.EDITAR_RUTINAS): st.button("Guardar")
    """
    rol_actual = obtener_rol_actual()
    if not rol_actual:
        return False
    
    permisos_del_rol = MAPA_PERMISOS.get(rol_actual, [])
    return permiso_requerido in permisos_del_rol

def requerir_permiso(permiso_requerido: str):
    """
    Protección dura: Si no tiene permiso, detiene la app entera mostrando un error.
    Ideal para poner en la primera línea de un panel.
    """
    if not tiene_permiso(permiso_requerido):
        st.error("⛔ Acceso de Seguridad Denegado. Tu nivel de suscripción o rol no permite ver esta sección.")
        st.stop() # Esto frena a Streamlit en seco