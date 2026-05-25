import streamlit as st

def ejecutar_enrutamiento(rol_actual, perfil_id, nombre_default, pais_default, genero_idx, fecha_nac_atleta):
    """
    Router Central: Única y exclusivamente redirige a las vistas.
    Cero lógica de negocio, cero consultas SQL, cero IA.
    """
    if rol_actual == "admin":
        from frontend.paneles.admin import panel_admin
        panel_admin()
        st.stop()
        
    elif rol_actual == "entrenador" or rol_actual == "nutricionista":
        from frontend.paneles.entrenador import panel_entrenador
        panel_entrenador(perfil_id)
        st.stop()
        
    elif rol_actual == "alumno":
        from frontend.paneles.alumno import app_alumno_original
        app_alumno_original(perfil_id, nombre_default, pais_default, genero_idx, fecha_nac_atleta)
        st.stop()
        
    else:
        st.error("🚨 Acceso denegado: Rol no reconocido.")
        st.stop()