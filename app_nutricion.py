import streamlit as st
from datetime import datetime, date
from database.conexion import supabase
from styles import aplicar_diseno_elite
from frontend.auth import renderizar_login

# ==========================================
# 1. CARGA INICIAL Y ESTILOS VIP
# ==========================================
aplicar_diseno_elite()
st.markdown('<meta name="google" content="notranslate">', unsafe_allow_html=True)


def ejecutar_sistema_saas():
    # 2. EL PORTERO: Interfaz modular de login
    if not renderizar_login():
        st.stop()

    # 3. CAPTURA Y EXTRACCIÓN DE SESIÓN CONTROLADA
    email_usuario = st.session_state.get("usuario_actual", "")
    email_limpio = email_usuario.lower().strip() if email_usuario else ""

    if not email_limpio:
        st.error("🚨 Error de sincronización de sesión. Reintentá el ingreso.")
        return

    # ==========================================
    # 🛡️ ENRUTADOR DINÁMICO INTELIGENTE
    # Lee el rol real de la base de datos sin forzar correos a mano
    # ==========================================
    res_perfil = supabase.table("perfiles_atletas").select("*").eq("email", email_limpio).execute()

    perfil_id = None 
    if len(res_perfil.data) > 0:
        perfil_db = res_perfil.data[0]
        perfil_id = perfil_db.get("id")
        nombre_default = perfil_db.get("nombre_completo", "")
        pais_default = perfil_db.get("pais", "Argentina")
        genero_db = perfil_db.get("genero")
        genero_idx = 0 if (genero_db and genero_db.strip() == "m") else 1
        fecha_str = perfil_db.get("fecha_nacimiento")
        fecha_nac_atleta = datetime.strptime(fecha_str, "%Y-%m-%d").date() if fecha_str else date(1990, 1, 1)
    else:
        nombre_default = email_limpio.split("@")[0].capitalize()
        pais_default = "Argentina"
        genero_idx = 0
        fecha_nac_atleta = date(1990, 1, 1)

    # 4. VERIFICAMOS SI EL USUARIO TIENE UN ROL DE STAFF (ADMIN / ENTRENADOR / NUTRI)
    if perfil_id:
        res_staff = supabase.table("roles_staff").select("rol").eq("perfil_id", perfil_id).execute()
        
        if len(res_staff.data) > 0:
            rol_actual = res_staff.data[0].get("rol", "").lower()
            st.session_state["rol"] = rol_actual
            
            if rol_actual == "admin":
                from frontend.paneles.admin import panel_admin
                panel_admin()
                st.stop()
            elif rol_actual == "entrenador":
                from frontend.paneles.entrenador import panel_entrenador
                # ¡Le pasamos el UUID real para que pueda ver los alumnos que le asignaste!
                panel_entrenador(perfil_id)
                st.stop()
            elif rol_actual == "nutricionista":
                from frontend.paneles.entrenador import panel_entrenador
                panel_entrenador(perfil_id) 
                st.stop()

    # 5. RUTA POR DEFECTO: Panel modular del alumno si no es Staff
    from frontend.paneles.alumno import app_alumno_original
    app_alumno_original(perfil_id, nombre_default, pais_default, genero_idx, fecha_nac_atleta)


if __name__ == "__main__":
    ejecutar_sistema_saas()