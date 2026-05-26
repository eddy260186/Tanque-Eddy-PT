import streamlit as st
from datetime import datetime, date
from database.conexion import supabase
from styles import aplicar_diseno_elite
from frontend.auth import renderizar_login

# === IMPORTACIONES DE SEGURIDAD Y EVENTOS ===
from core.session_manager import iniciar_sesion, obtener_rol_actual
from core.constants import Roles
from events.event_handler import registrar_todos_los_eventos

# === CONFIGURACIÓN GLOBAL (DEBE IR ANTES QUE CUALQUIER COSA DE INTERFAZ) ===
st.set_page_config(page_title="Eddy PT Elite", layout="wide", initial_sidebar_state="expanded")

# Enchufamos el cerebro de eventos silenciosos
registrar_todos_los_eventos()

# ==========================================
# 1. CARGA INICIAL Y ESTILOS VIP
# ==========================================
aplicar_diseno_elite()
st.markdown('<meta name="google" content="notranslate">', unsafe_allow_html=True)

def _normalizar_fecha_nacimiento(fecha_str):
    """Convierte fechas de Supabase a date sin romper si vienen vacias o con hora."""
    if not fecha_str:
        return date(1990, 1, 1)

    try:
        return datetime.fromisoformat(str(fecha_str).replace("Z", "+00:00")).date()
    except ValueError:
        try:
            return datetime.strptime(str(fecha_str)[:10], "%Y-%m-%d").date()
        except ValueError:
            return date(1990, 1, 1)

def ejecutar_sistema_saas():
    # 2. EL PORTERO: Interfaz modular de login
    if not renderizar_login():
        st.stop()

    # 3. CAPTURA Y EXTRACCION DE SESION CONTROLADA
    email_usuario = st.session_state.get("usuario_actual", "")
    email_limpio = email_usuario.lower().strip() if email_usuario else ""

    if not email_limpio:
        st.error("Error de sincronizacion de sesion. Reintenta el ingreso.")
        return

    # ==========================================
    # ENRUTADOR DINAMICO INTELIGENTE
    # ==========================================
    try:
        res_perfil = supabase.table("perfiles_atletas").select("*").eq("email", email_limpio).execute()
    except Exception as e:
        st.error(f"No se pudo cargar tu perfil desde la base de datos: {e}")
        return

    perfil_id = None
    perfiles = res_perfil.data or []

    if perfiles:
        perfil_db = perfiles[0]
        perfil_id = perfil_db.get("id")
        nombre_default = perfil_db.get("nombre_completo") or email_limpio.split("@")[0].capitalize()
        pais_default = perfil_db.get("pais") or "Argentina"
        genero_db = (perfil_db.get("genero") or "m").strip().lower()
        genero_idx = 0 if genero_db == "m" else 1
        fecha_nac_atleta = _normalizar_fecha_nacimiento(perfil_db.get("fecha_nacimiento"))
    else:
        nombre_default = email_limpio.split("@")[0].capitalize()
        pais_default = "Argentina"
        genero_idx = 0
        fecha_nac_atleta = date(1990, 1, 1)

    # 4. VERIFICAMOS ROL Y BLINDAMOS LA SESIÓN
    rol_asignado = Roles.ALUMNO

    if perfil_id:
        try:
            res_staff = supabase.table("roles_staff").select("rol").eq("perfil_id", perfil_id).execute()
            roles_staff = res_staff.data or []
            
            if roles_staff:
                rol_db = (roles_staff[0].get("rol") or "").lower()
                
                if rol_db == "admin":
                    rol_asignado = Roles.ADMIN
                elif rol_db in ["entrenador", "nutricionista"]:
                    rol_asignado = Roles.TRAINER
                    
        except Exception as e:
            st.error(f"No se pudo verificar el rol del usuario: {e}")
            return

    # Iniciar sesión segura
    iniciar_sesion(usuario_id=perfil_id, rol=rol_asignado, nombre=nombre_default)
    rol_seguro = obtener_rol_actual()

    # 5. ENRUTAMIENTO PROTEGIDO
    if rol_seguro == Roles.ADMIN:
        from frontend.paneles.admin import panel_admin
        panel_admin()
        st.stop()
        
    elif rol_seguro == Roles.TRAINER:
        from frontend.paneles.entrenador import panel_entrenador
        panel_entrenador(perfil_id)
        st.stop()
        
    else:
        from frontend.paneles.alumno import app_alumno_original
        app_alumno_original(perfil_id, nombre_default, pais_default, genero_idx, fecha_nac_atleta)

if __name__ == "__main__":
    ejecutar_sistema_saas()