import streamlit as st
from database.conexion import supabase

def panel_admin():
    # =========================================================================
    # BARRA LATERAL VIP: INFO DE SESIÓN Y BOTÓN DE CIERRE
    # =========================================================================
    with st.sidebar:
        st.markdown("### 👑 Panel de Control")
        st.success("Sesión Activa: Administrador")
        st.write("---")
        if st.button("🚪 Cerrar Sesión", type="primary", use_container_width=True):
            supabase.auth.sign_out()
            st.session_state.clear()
            st.rerun()

    # =========================================================================
    # CUERPO PRINCIPAL
    # =========================================================================
    st.markdown("## 👑 Suite de Administración General")
    st.caption("Control global del ecosistema multi-inquilino, límites de consumo de IA y licenciamiento de Staff.")
    st.write("---")
    
    # =========================================================================
    # 1. CAPA DE MÉTRICAS EN TIEMPO REAL (CONEXIÓN CON SUPABASE)
    # =========================================================================
    try:
        atletas_resp = supabase.table("perfiles_atletas").select("id, nombre_completo, email").execute()
        lista_alumnos = atletas_resp.data if atletas_resp.data else []
        total_alumnos = len(lista_alumnos)
        
        staff_resp = supabase.table("roles_staff").select("id, perfil_id, rol, whatsapp, limite_alumnos, nivel_plan").execute()
        lista_staff = staff_resp.data if staff_resp.data else []
        total_entrenadores = len([x for x in lista_staff if x['rol'] == 'entrenador'])
        total_nutricionistas = len([x for x in lista_staff if x['rol'] == 'nutricionista'])
        total_admins = len([x for x in lista_staff if x['rol'] == 'admin'])
    except Exception:
        lista_alumnos, lista_staff = [], []
        total_alumnos, total_entrenadores, total_nutricionistas, total_admins = 0, 0, 0, 0

    col1, col2, col3, col4 = st.columns(4)
    with col1: 
        st.metric(label="📊 Alumnos Registrados", value=total_alumnos)
    with col2: 
        st.metric(label="📋 Entrenadores Activos", value=total_entrenadores)
    with col3: 
        st.metric(label="🍏 Nutricionistas Activos", value=total_nutricionistas)
    with col4: 
        st.metric(label="🛡️ Administradores", value=total_admins)
        
    st.write("")

    # =========================================================================
    # 2. SISTEMA DE PESTAÑAS PARA LA WEB
    # =========================================================================
    tab_clientes, tab_licencias, tab_vinculacion, tab_auditoria = st.tabs([
        "👥 Monitoreo de Clientes", 
        "➕ Otorgar Licencia / Alta Staff", 
        "🔗 Vincular Atleta ➔ Entrenador", 
        "🔒 Monitor de Auditoría"
    ])

    # =========================================================================
    # TAB 1: MONITOREO DE CLIENTES (REVISAR SI EXISTEN O SI FALTA ROL)
    # =========================================================================
    with tab_clientes:
        st.markdown("#### Clientes Registrados en la Plataforma Web")
        st.caption("Lista general de personas autenticadas. Podés verificar su ID de base de datos y su estado.")
        
        if not lista_alumnos:
            st.info("No se encontraron registros de clientes en la base de datos actualmente.")
        else:
            # Cruzar datos de perfiles con roles de staff existentes
            staff_dict = {x['perfil_id']: x['rol'] for x in lista_staff}
            
            tabla_visual = []
            for al in lista_alumnos:
                rol_asignado = staff_dict.get(al['id'], "alumno (atleta)")
                tabla_visual.append({
                    "Nombre Completo": al.get("nombre_completo", "Sin Nombre"),
                    "Email": al.get("email", "Sin Email"),
                    "UUID de Usuario": al.get("id"),
                    "Rol del Sistema": rol_asignado.upper()
                })
            
            st.dataframe(tabla_visual, use_container_width=True)

    # =========================================================================
    # TAB 2: OTORGAR LICENCIA (ALTA DE NUEVO STAFF CON DATOS COMPLETOS)
    # =========================================================================
    with tab_licencias:
        st.markdown("#### Autorizar y Configurar Nuevo Personal de Staff")
        st.caption("Si un cliente ya se registró en la web, acá lo ascendés a Entrenador, Nutricionista o Administrador.")
        
        if not lista_alumnos:
            st.warning("Debe existir almsnos un usuario en la plataforma para otorgarle una licencia de trabajo.")
        else:
            dict_usuarios_disponibles = {
                f"{u.get('nombre_completo', 'Sin Nombre')} [{u.get('email')}]": u 
                for u in lista_alumnos
            }
            
            with st.form("form_alta_licencia", clear_on_submit=False):
                usuario_seleccionado = st.selectbox(
                    "Selecciona el usuario que será parte del Staff:", 
                    options=list(dict_usuarios_disponibles.keys())
                )
                
                col_r1, col_r2 = st.columns(2)
                with col_r1:
                    rol_seleccionado = st.selectbox("Rol del Staff:", ["entrenador", "nutricionista", "admin"])
                with col_r2:
                    plan_nivel = st.selectbox("Nivel del Plan SaaS:", ["basico", "elite"])
                    
                col_r3, col_r4 = st.columns(2)
                with col_r3:
                    whatsapp_comercial = st.text_input("WhatsApp Comercial (Ej: +5491123456789):", placeholder="+549...")
                with col_r4:
                    limite_alumnos = st.number_input("Límite de Alumnos Permitidos:", min_value=1, max_value=500, value=25)
                
                st.write("")
                btn_crear_staff = st.form_submit_button("🚀 Autorizar y Crear Acceso de Staff", type="primary", use_container_width=True)
                
                if btn_crear_staff:
                    perfil = dict_usuarios_disponibles[usuario_seleccionado]
                    
                    if not whatsapp_comercial.strip():
                        st.error("❌ El campo de WhatsApp es obligatorio para la futura automatización.")
                    else:
                        # Verificar si el usuario ya tiene un rol asignado
                        ya_existe = any(x['perfil_id'] == perfil['id'] for x in lista_staff)
                        
                        data_staff = {
                            "perfil_id": perfil["id"],
                            "rol": rol_seleccionado,
                            "whatsapp": whatsapp_comercial.strip(),
                            "limite_alumnos": int(limite_alumnos),
                            "nivel_plan": plan_nivel
                        }
                        
                        try:
                            if ya_existe:
                                # Actualizar datos existentes
                                supabase.table("roles_staff").update(data_staff).eq("perfil_id", perfil["id"]).execute()
                                st.success(f"🔄 Licencia actualizada: {perfil['nombre_completo']} ahora es {rol_seleccionado.upper()} con Plan {plan_nivel.upper()}.")
                            else:
                                # Insertar nuevo rol corporativo
                                supabase.table("roles_staff").insert(data_staff).execute()
                                st.success(f"✅ Licencia otorgada con éxito: {perfil['nombre_completo']} se incorporó como {rol_seleccionado.upper()}.")
                            st.rerun()
                        except Exception as e:
                            st.error(f"Error de consistencia en base de datos: {e}")

    # =========================================================================
    # TAB 3: VINCULAR ATLETA A UN ENTRENADOR ESPECÍFICO
    # =========================================================================
    with tab_vinculacion:
        st.markdown("#### Matriz de Asignación de Alumnos")
        st.caption("Vincula de forma directa a un Atleta con su Entrenador o Nutricionista responsable.")
        
        # Filtrar solo el personal que puede tener alumnos asignados (entrenador o nutricionista)
        staff_activo = [x for x in lista_staff if x['rol'] in ['entrenador', 'nutricionista']]
        
        if not lista_alumnos or not staff_activo:
            st.info("Se requiere tener alumnos cargados y staff con rol de Entrenador/Nutricionista configurado.")
        else:
            # Crear mapas de búsqueda por ID
            perfiles_dict = {p['id']: p for p in lista_alumnos}
            
            dict_alumnos = {
                f"{al.get('nombre_completo')} [{al.get('email')}]": al['id'] 
                for al in lista_alumnos
            }
            
            dict_staff = {}
            for s in staff_activo:
                p_id = s['perfil_id']
                if p_id in perfiles_dict:
                    nombre_prof = perfiles_dict[p_id].get('nombre_completo', 'Sin Nombre')
                    email_prof = perfiles_dict[p_id].get('email', '')
                    dict_staff[f"[{s['rol'].upper()}] {nombre_prof} - {email_prof}"] = p_id
            
            # Formulario de enlace
            with st.form("form_vinculacion_directa"):
                alumno_elegido = st.selectbox("Seleccionar Alumno Atleta:", list(dict_alumnos.keys()))
                staff_elegido = st.selectbox("Asignar al Profesional Profesional:", list(dict_staff.keys()))
                
                if st.form_submit_button("Vincular Atleta ➔", type="primary", use_container_width=True):
                    id_alumno = dict_alumnos[alumno_elegido]
                    id_entrenador = dict_staff[staff_elegido]
                    
                    try:
                        supabase.table("perfiles_atletas").update({"entrenador_id": id_entrenador}).eq("id", id_alumno).execute()
                        st.success(f"✅ Operación exitosa. El alumno ha sido transferido al panel exclusivo de {staff_elegido}.")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error al intentar escribir la clave foránea del entrenador: {e}")

    # =========================================================================
    # TAB 4: MONITOR DE AUDITORÍA (ESTÁTICO PARA LOGS DE SERVIDORES DE IA)
    # =========================================================================
    with tab_auditoria:
        st.markdown("#### Monitor de Infraestructura y Costos de Operación")
        col_c1, col_c2, col_c3 = st.columns(3)
        with col_c1: 
            st.metric(label="Costos Estimados OpenAI/Gemini", value="$4.32 USD")
        with col_c2: 
            st.metric(label="PDFs Generados en Servidor", value="42 archivos")
        with col_c3: 
            st.metric(label="API Status WhatsApp Cloud", value="Connected 📡")
            
        st.write("")
        st.text_area(
            "Logs del Orquestador de Mensajería (Simulado para producción)", 
            value="[INFO] 2026-05-25 10:14:02 - Supabase Webhook detectado en tabla 'evaluaciones_biometricas'\n"
                  "[INFO] 2026-05-25 10:14:05 - Respuesta exitosa del motor de Inteligencia Artificial\n"
                  "[INFO] 2026-05-25 10:14:06 - Evolution API despachó mensaje de texto al alumno de forma correcta.",
            height=120
        )