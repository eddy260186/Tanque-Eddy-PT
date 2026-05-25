import streamlit as st
import os
from datetime import date
from database.conexion import supabase
from utils.biometria import calcular_biometria
from backend.services.whatsapp_service import enviar_mensaje_texto_whatsapp

def panel_entrenador(staff_id):
    # ==========================================
    # 1. BARRA LATERAL (SIDEBAR) Y CERRAR SESIÓN
    # ==========================================
    with st.sidebar:
        st.header("🏢 Branding")
        dir_raiz = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        foto_side = None
        for n in ["logo.png", "logo(1).png", "logo.png.png"]:
            ruta_s = os.path.join(dir_raiz, n)
            if os.path.exists(ruta_s):
                foto_side = ruta_s
                break
        if foto_side:
            try:
                st.image(str(foto_side), use_container_width=True)
            except:
                pass
        
        st.divider()
        st.markdown(
            f"""
            <div style="background-color: #151a26; border: 1px solid #d4af37; padding: 15px; border-radius: 10px; margin-bottom: 20px; text-align: center;">
                <span style="color: #d4af37; font-weight: bold; font-size: 16px;">🛡️ Modo Entrenador</span><br>
                <span style="color: #ffffff; font-size: 13px;">Panel de Gestión Elite</span>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        # 🚪 BOTÓN DE SALIDA (Ubicado abajo a la izquierda en la app)
        if st.button("🚪 CERRAR SESIÓN", use_container_width=True, type="primary"):
            supabase.auth.sign_out()
            st.session_state["usuario_actual"] = None
            if "rol" in st.session_state:
                del st.session_state["rol"]
            st.rerun()

    # ==========================================
    # 2. PANEL PRINCIPAL
    # ==========================================
    st.markdown("## 📋 Panel de Control - Entrenador Elite")
    st.write("---")

    try:
        res_alumnos = supabase.table("perfiles_atletas").select("id").eq("entrenador_id", staff_id).execute()
        total_mis_alumnos = len(res_alumnos.data)
    except:
        total_mis_alumnos = 0

    col1, col2, col3 = st.columns(3)
    col1.metric("👥 Mis Alumnos Activos", total_mis_alumnos)
    col2.metric("💧 Adherencia Promedio", "89%")
    col3.metric("🤖 Consultas IA Disponibles", "Ilimitadas")
    
    st.write("---")

    tab_lista, tab_alta = st.tabs(["👥 Mi Cartera de Clientes", "➕ Dar de Alta / Actualizar Alumno"])

    # ---------------------------------------------------------
    # TAB 1: LISTA DE ALUMNOS (AHORA CON BUSCADOR Y EDICIÓN RÁPIDA)
    # ---------------------------------------------------------
    with tab_lista:
        st.markdown("### 👥 Tus Alumnos Asignados")
        
        try:
            # Traemos a todos los alumnos ordenados alfabéticamente
            res_alumnos_lista = supabase.table("perfiles_atletas").select("*").eq("entrenador_id", staff_id).order("nombre_completo").execute()
            alumnos_totales = res_alumnos_lista.data
            
            if not alumnos_totales:
                st.info("Aún no tienes alumnos asignados o registrados.")
            else:
                # 🔍 EL NUEVO BUSCADOR INTELIGENTE
                busqueda = st.text_input("🔍 Buscar atleta por nombre o correo electrónico...", placeholder="Escribe para buscar...").lower()
                
                # Filtramos la lista en tiempo real
                alumnos = [a for a in alumnos_totales if busqueda in str(a.get('nombre_completo', '')).lower() or busqueda in str(a.get('email', '')).lower()]
                
                if not alumnos:
                    st.warning("No se encontraron alumnos que coincidan con tu búsqueda.")

                for alu in alumnos:
                    nombre_alu = alu.get('nombre_completo', 'Sin Nombre')
                    email_alu = alu.get('email', '')
                    tel_alu = alu.get('telefono')
                    tel_mostrar = tel_alu if tel_alu else "Sin teléfono cargado"

                    with st.container():
                        c1, c2, c3 = st.columns([3, 3, 2])
                        with c1:
                            st.markdown(f"**{nombre_alu}**")
                            st.caption(f"✉️ {email_alu}")
                        with c2:
                            st.markdown(f"📱 `{tel_mostrar}`")
                        with c3:
                            # ✏️ EDICIÓN AL VUELO DE WHATSAPP
                            with st.expander("✏️ Editar WhatsApp"):
                                nuevo_tel = st.text_input("Número (Ej: +54911...)", value=tel_alu if tel_alu else "", key=f"edit_tel_{alu['id']}")
                                if st.button("💾 Guardar Número", key=f"btn_tel_{alu['id']}", use_container_width=True):
                                    try:
                                        supabase.table("perfiles_atletas").update({"telefono": nuevo_tel.strip()}).eq("id", alu['id']).execute()
                                        st.success("¡Actualizado!")
                                        st.rerun()
                                    except Exception as e:
                                        st.error("Error al actualizar.")
                                        
                        with st.expander(f"👁️ VER FICHA TÉCNICA DE {nombre_alu.upper()}"):
                            res_bio = supabase.table("evaluaciones_biometricas").select("*").eq("perfil_id", alu['id']).order("fecha_registro", desc=True).limit(1).execute()
                            
                            if res_bio.data:
                                bio = res_bio.data[0]
                                st.markdown(f"🗓️ **Último Control:** {bio.get('fecha_registro', 'Sin fecha')}")
                                
                                col_f1, col_f2, col_f3, col_f4 = st.columns(4)
                                col_f1.metric("Peso", f"{bio.get('peso', 0)} kg")
                                col_f2.metric("Estatura", f"{bio.get('estatura', 0)} cm")
                                col_f3.metric("Grasa (RFM)", f"{round(float(bio.get('rfm', 0)), 1)} %")
                                col_f4.metric("Cintura", f"{bio.get('cintura', 0)} cm")
                                
                                st.markdown(f"🎯 **Meta Actual:** `{bio.get('meta', 'No definida')}`")
                            else:
                                st.warning("⚠️ Todavía no se registraron controles biométricos completos para este atleta.")
                                
                    st.markdown("<hr style='margin:0.2em 0px; border-color: #333;' />", unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Error al renderizar cartera: {e}")

    # ---------------------------------------------------------
    # TAB 2: FORMULARIO DE ALTA / EDICIÓN BLINDADO
    # ---------------------------------------------------------
    with tab_alta:
        st.markdown("### 🚀 Registrar Atleta y Disparar Rutina")
        st.info("Si el alumno ya existe, el sistema actualizará sus datos e incorporará la nueva medición en su historial.")
        
        with st.form("form_alta_alumno"):
            col_a, col_b = st.columns(2)
            
            with col_a:
                nombre_alum = st.text_input("Nombre Completo:")
                email_alum = st.text_input("Correo Electrónico (Clave de unicidad):")
                tel_alum = st.text_input("📱 WhatsApp del Alumno (Ej: +5491123456789):")
                genero_alum = st.selectbox("Género:", ["Masculino", "Femenino"])
            
            with col_b:
                peso_alum = st.number_input("Peso Inicial (kg):", min_value=30.0, value=75.0)
                estatura_alum = st.number_input("Estatura (cm):", min_value=100, value=170)
                cintura_alum = st.number_input("Cintura (cm):", value=85.0)
                meta_alum = st.selectbox("Meta Principal:", ["Pérdida de Grasa", "Recomposición", "Volumen"])

            if st.form_submit_button("💾 Guardar y Disparar IA por WhatsApp"):
                if nombre_alum and email_alum and tel_alum:
                    try:
                        gen_val = "m" if genero_alum == "Masculino" else "f"
                        email_limpio = email_alum.lower().strip()
                        
                        perfil_data = {
                            "email": email_limpio,
                            "nombre_completo": nombre_alum,
                            "genero": gen_val,
                            "telefono": tel_alum.strip(),
                            "entrenador_id": staff_id
                        }
                        res_perfil = supabase.table("perfiles_atletas").upsert(perfil_data, on_conflict="email").execute()
                        p_id = res_perfil.data[0]["id"]

                        rfm_calc, masa_magra, tmb = calcular_biometria(gen_val, estatura_alum, cintura_alum, peso_alum)

                        bio_data = {
                            "perfil_id": p_id,
                            "peso": float(peso_alum),
                            "estatura": float(estatura_alum),
                            "cintura": float(cintura_alum),
                            "rfm": float(rfm_calc),
                            "meta": meta_alum,
                            "fecha_registro": str(date.today())
                        }
                        
                        supabase.table("evaluaciones_biometricas").insert(bio_data).execute()

                        mensaje_bienvenida = (
                            f"Hola {nombre_alum}. Ya quedaste registrado en el seguimiento de Eddy Personal Trainer. "
                            f"Tu objetivo actual es: {meta_alum}. Responde por este WhatsApp cuando tengas dudas de tu plan."
                        )
                        whatsapp_ok = enviar_mensaje_texto_whatsapp(
                            alumno_id=p_id,
                            entrenador_id=staff_id,
                            telefono=tel_alum,
                            mensaje=mensaje_bienvenida,
                        )

                        if whatsapp_ok:
                            st.success(f"✅ Datos guardados y WhatsApp de bienvenida enviado a {nombre_alum}.")
                        else:
                            st.warning("Datos guardados, pero WhatsApp no se envio. Revisa WHATSAPP_TOKEN y WHATSAPP_PHONE_NUMBER_ID.")
                    except Exception as e:
                        st.error(f"❌ Error de persistencia: {str(e)}")
                else:
                    st.warning("⚠️ El Nombre, Email y WhatsApp son obligatorios.")

