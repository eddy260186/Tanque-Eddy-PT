import os
import streamlit as st
from datetime import datetime, date
from database.conexion import supabase

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
    """
    _inyectar_estilos_premium()

    # =========================================================================
    # BARRA LATERAL CORPORATIVA
    # =========================================================================
    with st.sidebar:
        st.markdown("<div style='text-align: center; padding: 10px 0;'>", unsafe_allow_html=True)
        st.markdown("<h2 style='color: #d4af37; font-weight: 900; margin: 0;'>EDDY PT</h2>", unsafe_allow_html=True)
        st.markdown("<p style='color: #666; font-size: 0.8rem; margin: 0;'>SaaS Elite v2.1</p>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        st.write("---")
        st.info("Consola de Monitoreo Antropométrico y Prescripción Directa.")
        st.write("---")
        if st.button("🚪 Cerrar Sesión Activa", type="primary", use_container_width=True):
            supabase.auth.sign_out()
            st.session_state.clear()
            st.rerun()

    # =========================================================================
    # EXTRACCIÓN DE DATOS DE CABECERA (NOMBRE REAL DEL ENTRENADOR)
    # =========================================================================
    nombre_entrenador = "Profesional Staff"
    try:
        perfil_coach = supabase.table("perfiles_atletas").select("nombre_completo").eq("id", entrenador_uuid).execute()
        if perfil_coach.data:
            nombre_entrenador = perfil_coach.data[0].get("nombre_completo", "Profesional Staff")
    except Exception:
        pass

    # cabecera de la app
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
    # EXTRACCIÓN DE LOS ATLETAS ASIGNADOS
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

    # =========================================================================
    # BUSCADOR INTERACTIVO Y DASHBOARD DE MANDO
    # =========================================================================
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
            help="Escriba o seleccione el nombre del cliente para abrir su expediente clínico."
        )
    
    alumno = dict_alumnos[atleta_seleccionado]
    
    # Variables biométricas seguras
    edad = _calcular_edad(alumno.get("fecha_nacimiento"))
    genero = "Masculino" if str(alumno.get("genero", "m")).strip().lower() == "m" else "Femenino"
    peso_actual = alumno.get("peso", 0.0)
    altura_actual = alumno.get("altura", 0.0)
    
    # Recuperación interactiva de metas y plazos (evitando caídas si no existen las columnas)
    peso_objetivo = alumno.get("peso_objetivo", 0.0) if alumno.get("peso_objetivo") else (peso_actual - 5.0 if peso_actual else 70.0)
    plazo_meses = alumno.get("plazo_meses", 4) if alumno.get("plazo_meses") else 3

    with col_stats:
        # Fila de métricas interactivas diseñadas con HTML puro para romper la monotonía estética
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
    tab_diagnostico, tab_antropometria, tab_prescripcion, tab_seguimiento = st.tabs([
        "🔍 Diagnóstico Funcional", 
        "📏 Anatomía y Medidas", 
        "📝 Modificar Planificación (Rutina/Dieta)", 
        "📈 Gráfica de Progreso Real"
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

    # TAB 3: ACCIONES DE PRESCRIPCIÓN DIRECTA (INTERACTIVO)
    with tab_prescripcion:
        st.markdown("<div class='ficha-container'>", unsafe_allow_html=True)
        st.markdown("<div class='seccion-titulo-vip'>⚙️ Modificación de Rutinas y Planificación Calórica</div>", unsafe_allow_html=True)
        st.caption("Los cambios guardados impactarán instantáneamente en la interfaz web de la aplicación del alumno.")
        
        with st.form("form_actualizar_plan"):
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
            
            if btn_guardar_plan:
                try:
                    # Actualizamos de forma masiva y limpia todas las columnas funcionales
                    supabase.table("perfiles_atletas").update({
                        "rutina_activa": nueva_rutina,
                        "dieta_activa": nueva_dieta,
                        "peso_objetivo": nuevo_peso_obj,
                        "plazo_meses": nuevo_plazo_meses
                    }).eq("id", alumno["id"]).execute()
                    
                    st.success(f"🔥 Sincronización Exitosa: El plan de {alumno.get('nombre_completo')} fue actualizado en la nube.")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error al escribir en Supabase: {e}")
        st.markdown("</div>", unsafe_allow_html=True)

    # TAB 4: SEGUIMIENTO GRÁFICO REAL
    with tab_seguimiento:
        st.markdown("<div class='ficha-container'>", unsafe_allow_html=True)
        st.markdown("<div class='seccion-titulo-vip'>📈 Curva Evolutiva de Composición Corporal</div>", unsafe_allow_html=True)
        
        try:
            historial_resp = supabase.table("evaluaciones_biometricas").select("*").eq("perfil_id", alumno["id"]).order("fecha_evaluacion", ascending=True).execute()
            logs_evolucion = historial_resp.data if historial_resp.data else []
        except Exception:
            logs_evolucion = []

        if not logs_evolucion:
            st.info("💡 Historial inicial activo. Mostrando proyección de control en base al peso actual y la meta configurada.")
            
            # Gráfica interactiva de alta fidelidad para el control visual del progreso
            p_inicial = peso_actual if peso_actual else 85.0
            curva_proyeccion = [p_inicial, p_inicial - ((p_inicial - peso_objetivo) * 0.3), p_inicial - ((p_inicial - peso_objetivo) * 0.6), peso_objetivo]
            
            st.line_chart(data=curva_proyeccion, use_container_width=True)
            st.caption("Eje X: Línea temporal del proceso // Eje Y: Peso registrado en Kg.")
        else:
            pesos_historicos = [log.get("peso") for log in logs_evolucion if log.get("peso")]
            fechas_historicas = [log.get("fecha_evaluacion") for log in logs_evolucion if log.get("fecha_evaluacion")]
            
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