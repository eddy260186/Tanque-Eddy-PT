import os
import streamlit as st
from datetime import datetime, date
from database.conexion import supabase

# 🔥 IMPORTAMOS EL CASO DE USO DE NUESTRA NUEVA CAPA DE APLICACIÓN
from application.actualizar_plan import ejecutar_actualizacion_plan
from frontend.paneles.gestion_agente import tab_rutina_semanal, tab_plan_comidas, tab_actividad_alumno

def _calcular_edad(fecha_nac):
    if not fecha_nac:
        return "N/A"
    try:
        if isinstance(fecha_nac, str):
            fecha_nac = datetime.strptime(fecha_nac[:10], "%Y-%m-%d").date()
        hoy = date.today()
        return hoy.year - fecha_nac.year - ((hoy.month, hoy.day) < (fecha_nac.month, fecha_nac.day))
    except Exception:
        return "N/A"

def _inyectar_estilos_premium():
    st.markdown("""
    <style>
    /* CONTEXTO DE TABLERO DE ALTA GAMA */
    .coach-hero {
        background: linear-gradient(135deg, #111111 0%, #1a1a1a 100%);
        border: 1px solid rgba(212, 175, 55, 0.3);
        border-radius: 12px;
        padding: 24px;
        margin-bottom: 25px;
        box-shadow: 0 8px 32px rgba(0,0,0,0.4);
        display: flex;
        align-items: center;
        gap: 20px;
    }
    .coach-avatar {
        width: 75px;
        height: 75px;
        border-radius: 50%;
        border: 2px solid #d4af37;
        background-color: #222;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 28px;
        box-shadow: 0 0 15px rgba(212,175,55,0.4);
    }
    .coach-welcome-text h1 {
        color: #ffffff;
        font-size: 1.8rem;
        font-weight: 800;
        margin: 0;
        padding: 0;
        letter-spacing: 0.5px;
    }
    .coach-welcome-text p {
        color: #d4af37;
        font-size: 1rem;
        margin: 4px 0 0 0;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    /* TARJETAS MÉTRICAS ELITE */
    .metric-card-elite {
        background: #161616;
        border-left: 4px solid #d4af37;
        border-top: 1px solid #262626;
        border-right: 1px solid #262626;
        border-bottom: 1px solid #262626;
        border-radius: 6px;
        padding: 16px;
        text-align: left;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    .metric-card-title {
        color: #888888;
        font-size: 0.85rem;
        text-transform: uppercase;
        font-weight: 700;
        letter-spacing: 0.5px;
        margin-bottom: 6px;
    }
    .metric-card-value {
        color: #ffffff;
        font-size: 1.6rem;
        font-weight: 800;
        font-family: 'monospace', sans-serif;
    }
    
    /* CONTENEDOR DE FICHA EVOLUTIVA */
    .ficha-container {
        background: #121212;
        border: 1px solid #222222;
        border-radius: 10px;
        padding: 20px;
        margin-top: 15px;
    }
    
    .seccion-titulo-vip {
        color: #f4d47c;
        font-size: 1.2rem;
        font-weight: 700;
        border-bottom: 1px solid rgba(244,212,124,0.2);
        padding-bottom: 6px;
        margin-bottom: 15px;
    }
    
    /* AJUSTES PARA COMPONENTES DE STREAMLIT */
    div[data-testid="stExpander"] {
        border: 1px solid #222 !important;
        background-color: #151515 !important;
        border-radius: 8px !important;
    }
    </style>
    """, unsafe_allow_html=True)


def panel_entrenador(entrenador_uuid):
    """
    Suite Avanzada e Interactiva para Entrenadores con Interfaz Gráfica Premium.
    Desacoplada de la lógica de SQL para máxima velocidad (Arquitectura Limpia).
    """
    _inyectar_estilos_premium()

    # =========================================================================
    # BARRA LATERAL CORPORATIVA
    # =========================================================================
    with st.sidebar:
        st.markdown("<div style='text-align: center; padding: 10px 0;'>", unsafe_allow_html=True)
        st.markdown("<h2 style='color: #d4af37; font-weight: 900; margin: 0;'>EDDY PT</h2>", unsafe_allow_html=True)
        st.markdown("<p style='color: #666; font-size: 0.8rem; margin: 0;'>SaaS Elite v2.2</p>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        st.write("---")
        st.info("Consola de Monitoreo Antropométrico y Prescripción Directa.")
        st.write("---")
        if st.button("🚪 Cerrar Sesión Activa", type="primary", use_container_width=True):
            from core.session_manager import cerrar_sesion
            cerrar_sesion()
            st.rerun()

    # =========================================================================
    # EXTRACCIÓN DE DATOS DE CABECERA (NOMBRE REAL DEL ENTRENADOR)
    # =========================================================================
    nombre_entrenador = "Profesional Staff"
    try:
        # Nota: En futuras fases moveremos esta consulta también al repositorio
        perfil_coach = supabase.table("perfiles_atletas").select("nombre_completo").eq("id", entrenador_uuid).execute()
        if perfil_coach.data:
            nombre_entrenador = perfil_coach.data[0].get("nombre_completo", "Profesional Staff")
    except Exception:
        pass

    # Cabecera dinámica VIP
    st.markdown(f"""
    <div class="coach-hero">
        <div class="coach-avatar">👑</div>
        <div class="coach-welcome-text">
            <h1>Coach {nombre_entrenador}</h1>
            <p>Director Técnico del Ecosistema de Rendimiento</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # =========================================================================
    # EXTRACCIÓN DE LOS ATLETAS ASIGNADOS Y SELECTOR DINÁMICO (ANTI-CACHÉ)
    # =========================================================================
    try:
        atletas_resp = supabase.table("perfiles_atletas").select("*").eq("entrenador_id", entrenador_uuid).execute()
        lista_alumnos = atletas_resp.data if atletas_resp.data else []
    except Exception as e:
        st.error(f"Error crítico al conectar con la base de datos de atletas: {e}")
        return

    if not lista_alumnos:
        st.markdown("""
        <div style='background-color: #1a1a1a; padding: 25px; border-radius: 8px; border: 1px dashed #444; text-align: center;'>
            <h4 style='color: #d4af37; margin: 0 0 10px 0;'>Sin Alumnos Asignados</h4>
            <p style='color: #aaa; margin: 0;'>Su cuenta corporativa no tiene atletas vinculados por el Administrador General.</p>
        </div>
        """, unsafe_allow_html=True)
        return

    st.markdown("<h3 style='color: #ffffff; font-weight: 700; margin-bottom: 10px;'>📊 Centro de Control de Atletas</h3>", unsafe_allow_html=True)
    
    dict_alumnos = {
        f"{a.get('nombre_completo', 'Sin Nombre')} ({a.get('email', '')})": a 
        for a in lista_alumnos
    }
    
    col_busc, col_stats = st.columns([1.5, 2.5], gap="large")
    
    with col_busc:
        atleta_seleccionado = st.selectbox(
            "Buscar Atleta en su Red:", 
            options=list(dict_alumnos.keys()),
            key="selector_global_alumnos",
            help="Escriba o seleccione el nombre del cliente para abrir su expediente clínico."
        )
    
    alumno = dict_alumnos[atleta_seleccionado]
    alumno_id = str(alumno.get("id"))
    
    # Variables biométricas seguras
    edad = _calcular_edad(alumno.get("fecha_nacimiento"))
    genero = "Masculino" if str(alumno.get("genero", "m")).strip().lower() == "m" else "Femenino"
    peso_actual = alumno.get("peso", 0.0)
    
    peso_objetivo = alumno.get("peso_objetivo", 0.0) if alumno.get("peso_objetivo") else (peso_actual - 5.0 if peso_actual else 70.0)
    plazo_meses = alumno.get("plazo_meses", 4) if alumno.get("plazo_meses") else 3

    # 🛡️ Blindaje: nunca dejar que un dato fuera de rango rompa los inputs
    try:
        peso_objetivo = max(30.0, min(250.0, float(peso_objetivo)))
    except Exception:
        peso_objetivo = 70.0
    try:
        plazo_meses = max(1, min(24, int(plazo_meses)))
    except Exception:
        plazo_meses = 3

    with col_stats:
        cm1, cm2, cm3 = st.columns(3)
        with cm1:
            st.markdown(f"""
            <div class="metric-card-elite">
                <div class="metric-card-title">Peso Actual</div>
                <div class="metric-card-value" style="color: #f4d47c;">{peso_actual if peso_actual else 'S/D'} <span style='font-size:12px;'>KG</span></div>
            </div>
            """, unsafe_allow_html=True)
        with cm2:
            st.markdown(f"""
            <div class="metric-card-elite">
                <div class="metric-card-title">Meta Objetivo</div>
                <div class="metric-card-value" style="color: #00ffcc;">{peso_objetivo} <span style='font-size:12px;'>KG</span></div>
            </div>
            """, unsafe_allow_html=True)
        with cm3:
            st.markdown(f"""
            <div class="metric-card-elite">
                <div class="metric-card-title">Plazo Fijado</div>
                <div class="metric-card-value" style="color: #ff9900;">{plazo_meses} <span style='font-size:12px;'>Meses</span></div>
            </div>
            """, unsafe_allow_html=True)

    st.write("")

    # =========================================================================
    # ÁREA DE EXPEDIENTE 360 GRADOS
    # =========================================================================
    tab_diagnostico, tab_antropometria, tab_prescripcion, tab_rutina_sem, tab_comidas, tab_actividad, tab_seguimiento, tab_whatsapp_saas = st.tabs([
        "🔍 Diagnóstico Funcional", 
        "📏 Anatomía y Medidas", 
        "📝 Modificar Planificación (Rutina/Dieta)", 
        "📅 Rutina Semanal",
        "🍽️ Plan de Comidas",
        "🏋️ Actividad WhatsApp",
        "📈 Gráfica de Progreso Real",
        "📲 Vinculación WhatsApp QR"
    ])

    # TAB 1: DIAGNÓSTICO FUNCIONAL
    with tab_diagnostico:
        st.markdown("<div class='ficha-container'>", unsafe_allow_html=True)
        st.markdown("<div class='seccion-titulo-vip'>📋 Perfil de Estilo de Vida e Historial</div>", unsafe_allow_html=True)
        
        c_f1, c_f2, c_f3 = st.columns(3)
        with c_f1:
            st.markdown(f"**Edad Clínica:** {edad} años")
            st.markdown(f"**Género:** {genero}")
        with c_f2:
            st.markdown(f"**País/Región:** {alumno.get('pais', 'Argentina')}")
            st.markdown(f"**Contacto Directo:** {alumno.get('telefono', 'Sin Teléfono')}")
        with c_f3:
            st.markdown(f"**Ocupación:** {alumno.get('ocupacion', 'No especificada')}")
            st.markdown(f"**Nivel de Actividad:** {alumno.get('actividad_fisica', 'No especificado')}")
            
        st.write("---")
        st.markdown("**Horarios de Entrenamiento Disponibles:**")
        st.info(alumno.get("horario_entrenamiento", "No configurado por el atleta."))
        st.markdown("**Objetivo Primario Auto-declarado:**")
        st.warning(alumno.get("objetivo", "Recomposición corporal avanzada."))
        st.markdown("</div>", unsafe_allow_html=True)

    # TAB 2: ANATOMÍA Y PERÍMETROS
    with tab_antropometria:
        st.markdown("<div class='ficha-container'>", unsafe_allow_html=True)
        st.markdown("<div class='seccion-titulo-vip'>📐 Ficha Métrica Perimetral (Cm)</div>", unsafe_allow_html=True)
        
        m1, m2, m3, m4 = st.columns(4)
        with m1:
            st.metric("Cuello", f"{alumno.get('medida_cuello', '—')} cm")
            st.metric("Pecho", f"{alumno.get('medida_pecho', '—')} cm")
        with m2:
            st.metric("Brazo Izq.", f"{alumno.get('medida_brazo_izq', '—')} cm")
            st.metric("Brazo Der.", f"{alumno.get('medida_brazo_der', '—')} cm")
        with m3:
            st.metric("Cintura / Abdomen", f"{alumno.get('medida_cintura', '—')} cm")
            st.metric("Cadera", f"{alumno.get('medida_cadera', '—')} cm")
        with m4:
            st.metric("Muslo Izq.", f"{alumno.get('medida_muslo_izq', '—')} cm")
            st.metric("Muslo Der.", f"{alumno.get('medida_muslo_der', '—')} cm")
        st.markdown("</div>", unsafe_allow_html=True)

    # TAB 3: ACCIONES DE PRESCRIPCIÓN DIRECTA (ARQUITECTURA LIMPIA)
    with tab_prescripcion:
        st.markdown("<div class='ficha-container'>", unsafe_allow_html=True)
        st.markdown("<div class='seccion-titulo-vip'>⚙️ Modificación de Rutinas y Planificación Calórica</div>", unsafe_allow_html=True)
        st.caption("Los cambios guardados se actualizarán en la base de datos y despacharán un aviso automático al WhatsApp del alumno.")
        
        with st.form(key=f"form_actualizar_plan_{alumno_id}"):
            col_p1, col_p2 = st.columns(2)
            with col_p1:
                st.markdown("##### 🏋️ Programación de Estímulo Muscular")
                nueva_rutina = st.text_area(
                    "Bloque de Rutina Activa:",
                    value=alumno.get("rutina_activa", "Ingresar ejercicios, series y repeticiones."),
                    height=250
                )
            with col_p2:
                st.markdown("##### 🍏 Diseño de Macronutrientes y Menú")
                nueva_dieta = st.text_area(
                    "Estructura Nutricional Vigente:",
                    value=alumno.get("dieta_activa", "Ingresar distribución calórica y comidas habituales."),
                    height=250
                )
                
            st.write("---")
            st.markdown("##### 🏁 Configuración de Metas e Indicadores de Seguimiento")
            col_fmeta1, col_fmeta2 = st.columns(2)
            with col_fmeta1:
                nuevo_peso_obj = st.number_input("Establecer Peso Objetivo (Kg):", min_value=30.0, max_value=250.0, value=float(peso_objetivo))
            with col_fmeta2:
                nuevo_plazo_meses = st.number_input("Establecer Plazo del Proceso (Meses):", min_value=1, max_value=24, value=int(plazo_meses))

            st.write("")
            btn_guardar_plan = st.form_submit_button("💾 Modificar y Sincronizar Ficha del Alumno", type="primary", use_container_width=True)
            
            # 🔥 FLUJO MAESTRO DE DATOS ORQUESTADO DESDE LA CAPA DE APLICACIÓN
            if btn_guardar_plan:
                with st.spinner("Sincronizando plan y conectando con el servidor..."):
                    
                    resultado = ejecutar_actualizacion_plan(
                        entrenador_id=entrenador_uuid,
                        alumno_id=alumno_id,
                        alumno_data=alumno,
                        nueva_rutina=nueva_rutina,
                        nueva_dieta=nueva_dieta,
                        nuevo_peso_obj=nuevo_peso_obj,
                        nuevo_plazo=nuevo_plazo_meses
                    )
                    
                    # El panel solo reacciona visualmente al resultado del orquestador
                    if resultado.get("exito"):
                        if resultado.get("ws_enviado"):
                            st.success(f"🔥 Sincronización Exitosa: {resultado.get('mensaje')}")
                        else:
                            st.warning(f"⚠️ {resultado.get('mensaje')}")
                    else:
                        st.error(f"❌ Error Crítico: {resultado.get('error', 'Falla general del sistema')}")
                        
        st.markdown("</div>", unsafe_allow_html=True)

    # TAB 4: SEGUIMIENTO GRÁFICO REAL
    with tab_seguimiento:
        st.markdown("<div class='ficha-container'>", unsafe_allow_html=True)
        st.markdown("<div class='seccion-titulo-vip'>📈 Curva Evolutiva de Composición Corporal</div>", unsafe_allow_html=True)
        
        try:
            historial_resp = supabase.table("evaluaciones_biometricas").select("*").eq("perfil_id", alumno_id).order("fecha_evaluacion", ascending=True).execute()
            logs_evolucion = historial_resp.data if historial_resp.data else []
        except Exception:
            logs_evolucion = []

        if not logs_evolucion:
            st.info("💡 Historial inicial activo. Mostrando proyección de control en base al peso actual y la meta configurada.")
            p_inicial = peso_actual if peso_actual else 85.0
            curva_proyeccion = [p_inicial, p_inicial - ((p_inicial - peso_objetivo) * 0.3), p_inicial - ((p_inicial - peso_objetivo) * 0.6), peso_objetivo]
            
            st.line_chart(data=curva_proyeccion, use_container_width=True)
            st.caption("Eje X: Línea temporal del proceso // Eje Y: Peso registrado en Kg.")
        else:
            pesos_historicos = [log.get("peso") for log in logs_evolucion if log.get("peso")]
            st.line_chart(data=pesos_historicos, use_container_width=True)
            
            tabla_historial = []
            for log in reversed(logs_evolucion):
                tabla_historial.append({
                    "Fecha de Control": log.get("fecha_evaluacion"),
                    "Peso Registrado (Kg)": log.get("peso"),
                    "% Grasa Corporal": log.get("porcentaje_grasa", "S/D"),
                    "Observaciones del Ajuste": log.get("observaciones", "Sin anotaciones")
                })
            st.dataframe(tabla_historial, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # TAB 5: VINCULACIÓN WHATSAPP SINCRO
    with tab_whatsapp_saas:
        st.markdown("<div class='ficha-container'>", unsafe_allow_html=True)
        st.markdown("<div class='seccion-titulo-vip'>📲 Consola de Activación de WhatsApp Automático</div>", unsafe_allow_html=True)
        st.caption("Escaneá el código QR para que la Inteligencia Artificial de la app pueda enviar rutinas y recordatorios automáticos firmados con tu propio número.")
        
        instancia_nombre = f"coach_{str(entrenador_uuid)[:8]}"
        
        from backend.services.whatsapp_service import EvolutionAPI
        
        col_qr_actions, col_qr_display = st.columns([1.5, 2.5])
        
        with col_qr_actions:
            st.markdown("##### ⚙️ Gestión de Conexión")
            st.write("Presioná el botón para solicitar un nuevo token y sincronizar la terminal inalámbrica.")
            btn_generar_qr = st.button("🔄 Generar Código QR de Vinculación", type="primary", use_container_width=True, key=f"btn_qr_{entrenador_uuid}")
            
        with col_qr_display:
            if btn_generar_qr:
                with st.spinner("Conectando con el motor de Railway y generando QR corporativo..."):
                    try:
                        evo = EvolutionAPI()
                        resultado = evo.crear_instancia_y_obtener_qr(instancia_nombre)
                        
                        if resultado.get("exito") and resultado.get("qr_base64"):
                            st.success("✅ ¡Código generado! Escanealo desde la app de WhatsApp de tu celular (Dispositivos vinculados).")
                            datos_qr = resultado["qr_base64"]
                            st.markdown(
                                f"""
                                <div style='text-align: center; background: white; padding: 15px; border-radius: 8px; width: fit-content; margin: 10px auto;'>
                                    <img src="{datos_qr}" style="width: 280px; height: 280px;" />
                                </div>
                                """, 
                                unsafe_allow_html=True
                            )
                        else:
                            st.error(f"No se pudo inicializar la API de WhatsApp: {resultado.get('error')}")
                            st.info("Verificá que las credenciales de EVOLUTION_API_URL y KEY en tus Secrets sean las correctas.")
                    except Exception as fatal_e:
                        st.error(f"Falla crítica de red conectando al servidor: {fatal_e}")
        st.markdown("</div>", unsafe_allow_html=True)

    # TAB 6: RUTINA SEMANAL (alimenta el agente diario)
    with tab_rutina_sem:
        st.markdown("<div class='ficha-container'>", unsafe_allow_html=True)
        tab_rutina_semanal(alumno_id)
        st.markdown("</div>", unsafe_allow_html=True)

    # TAB 7: PLAN DE COMIDAS (alimenta el agente diario)
    with tab_comidas:
        st.markdown("<div class='ficha-container'>", unsafe_allow_html=True)
        tab_plan_comidas(alumno_id)
        st.markdown("</div>", unsafe_allow_html=True)

    # TAB 8: ACTIVIDAD REPORTADA POR WHATSAPP
    with tab_actividad:
        st.markdown("<div class='ficha-container'>", unsafe_allow_html=True)
        tab_actividad_alumno(alumno_id)
        st.markdown("</div>", unsafe_allow_html=True)