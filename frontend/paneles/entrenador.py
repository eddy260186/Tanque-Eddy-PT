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

def panel_entrenador(entrenador_uuid):
    """
    Suite Elite para Entrenadores.
    Muestra la nomina de atletas asignados a este entrenador_uuid y despliega 
    toda su informacion biometrica, de actividad, horarios y seguimiento.
    """
    # =========================================================================
    # BARRA LATERAL VIP: CONTROL DE SESIÓN
    # =========================================================================
    with st.sidebar:
        st.markdown("### 📋 Panel del Profesional")
        st.success("Sesión Activa: Entrenador / Staff")
        st.write("---")
        if st.button("🚪 Cerrar Sesión", type="primary", use_container_width=True):
            supabase.auth.sign_out()
            st.session_state.clear()
            st.rerun()

    # =========================================================================
    # CUERPO PRINCIPAL: EXTRACCIÓN DE ALUMNOS VINCULADOS
    # =========================================================================
    st.markdown("## ⚡ Sistema Clínico de Entrenamiento y Seguimiento")
    st.caption("Visualización de fichas técnicas, evolución biométrica y gestión adaptativa de atletas asignados.")
    st.write("---")

    try:
        # Traemos solo los alumnos cuyo entrenador_id coincida con el UUID del entrenador logueado
        atletas_resp = supabase.table("perfiles_atletas").select("*").eq("entrenador_id", entrenador_uuid).execute()
        lista_alumnos = atletas_resp.data if atletas_resp.data else []
    except Exception as e:
        st.error(f"Error al conectar con la base de datos de atletas: {e}")
        lista_alumnos = []

    # =========================================================================
    # CONTROL DE FLUJO SI NO HAY ALUMNOS ASIGNADOS
    # =========================================================================
    if not lista_alumnos:
        st.info("👋 ¡Bienvenido a la Suite Elite! Actualmente no tenés alumnos asignados por la administración.")
        st.markdown(
            """
            <div style='background-color: #1e1e1e; padding: 20px; border-radius: 8px; border: 1px solid #333;'>
                <p style='color: #f4d47c; font-weight: bold; margin-bottom: 5px;'>¿Qué sigue?</p>
                <p style='color: #b7bdca; margin: 0;'>Póngase en contacto con el Administrador General para que vincule alumnos a su perfil desde la <b>Matriz de Asignación</b>.</p>
            </div>
            """, 
            unsafe_allow_html=True
        )
        st.stop()

    # =========================================================================
    # PANEL ACTIVO: SELECTOR DE ATLETA TRABAJADO
    # =========================================================================
    dict_alumnos = {
        f"👤 {a.get('nombre_completo', 'Sin Nombre')} [{a.get('email')}]": a 
        for a in lista_alumnos
    }
    
    col_sel, _ = st.columns([2, 2])
    with col_sel:
        atleta_seleccionado = st.selectbox(
            "Seleccioná el alumno para auditar su ficha completa:", 
            options=list(dict_alumnos.keys())
        )
    
    st.write("---")
    
    # Extraemos el registro limpio de la base de datos del alumno elegido
    alumno = dict_alumnos[atleta_seleccionado]
    
    # Pre-calculos de datos protegidos contra valores nulos
    edad = _calcular_edad(alumno.get("fecha_nacimiento"))
    genero_raw = str(alumno.get("genero", "m")).strip().lower()
    genero = "Masculino" if genero_raw == "m" else "Femenino"
    
    # =========================================================================
    # PESTAÑAS DETALLADAS DE INFORMACIÓN DE 360 GRADOS
    # =========================================================================
    tab_ficha, tab_biometria, tab_rutina_dieta, tab_progreso = st.tabs([
        "📄 Ficha Técnica y Horarios", 
        "📏 Medidas y Biometría", 
        "🍏 Prescripción Actual",
        "📈 Historial de Seguimiento"
    ])

    # -------------------------------------------------------------------------
    # TAB 1: FICHA TÉCNICA Y HORARIOS
    # -------------------------------------------------------------------------
    with tab_ficha:
        st.markdown("#### Datos de Identificación y Disponibilidad")
        
        c1, c2, c3, c4 = st.columns(4)
        with c1: st.metric(label="Edad", value=f"{edad} años")
        with c2: st.metric(label="Género", value=genero)
        with c3: st.metric(label="País de Residencia", value=alumno.get("pais", "Argentina"))
        with c4: st.metric(label="Teléfono / WhatsApp", value=alumno.get("telefono", "No registrado"))
        
        st.write("---")
        st.markdown("#### ⏰ Horarios y Estilo de Vida")
        
        # El uso de .get(campo, "No definido") evita errores si la columna está vacía
        col_h1, col_h2 = st.columns(2)
        with col_h1:
            st.text_input("Horarios disponibles para entrenar:", value=alumno.get("horario_entrenamiento", "No definido"), disabled=True)
            st.text_input("Ocupación / Trabajo:", value=alumno.get("ocupacion", "No definido"), disabled=True)
        with col_h2:
            st.text_input("Nivel de Actividad Física diario:", value=alumno.get("actividad_fisica", "No definido"), disabled=True)
            st.text_input("Objetivo Principal declarado:", value=alumno.get("objetivo", "Hipertrofia / Descenso de grasa"), disabled=True)

    # -------------------------------------------------------------------------
    # TAB 2: MEDIDAS Y BIOMETRÍA
    # -------------------------------------------------------------------------
    with tab_biometria:
        st.markdown("#### Último Registro Antropométrico Detectado")
        
        # Variables de control extraídas directamente de la fila del alumno
        peso_actual = alumno.get("peso", 0.0)
        altura_actual = alumno.get("altura", 0.0)
        
        col_b1, col_b2, col_b3 = st.columns(3)
        with col_b1: st.metric(label="Peso Actual", value=f"{peso_actual} kg" if peso_actual else "S/D")
        with col_b2: st.metric(label="Estatura", value=f"{altura_actual} m" if altura_actual else "S/D")
        with col_b3: 
            if peso_actual and altura_actual:
                imc = round(peso_actual / (altura_actual ** 2), 1)
                st.metric(label="Índice de Masa Corporal (IMC)", value=f"{imc}")
            else:
                st.metric(label="Índice de Masa Corporal (IMC)", value="S/D")

        st.write("---")
        st.markdown("#### Perímetros Corporales (Cm)")
        
        col_m1, col_m2, col_m3, col_m4 = st.columns(4)
        with col_m1:
            st.text_input("Cuello:", value=f"{alumno.get('medida_cuello', 'S/D')} cm", disabled=True)
            st.text_input("Pecho:", value=f"{alumno.get('medida_pecho', 'S/D')} cm", disabled=True)
        with col_m2:
            st.text_input("Brazo Izquierdo:", value=f"{alumno.get('medida_brazo_izq', 'S/D')} cm", disabled=True)
            st.text_input("Brazo Derecho:", value=f"{alumno.get('medida_brazo_der', 'S/D')} cm", disabled=True)
        with col_m3:
            st.text_input("Cintura / Abdomen:", value=f"{alumno.get('medida_cintura', 'S/D')} cm", disabled=True)
            st.text_input("Cadera:", value=f"{alumno.get('medida_cadera', 'S/D')} cm", disabled=True)
        with col_m4:
            st.text_input("Muslo Izquierdo:", value=f"{alumno.get('medida_muslo_izq', 'S/D')} cm", disabled=True)
            st.text_input("Muslo Derecho:", value=f"{alumno.get('medida_muslo_der', 'S/D')} cm", disabled=True)

    # -------------------------------------------------------------------------
    # TAB 3: PRESCRIPCIÓN ACTUAL (DIETA Y RUTINA ACTIVA)
    # -------------------------------------------------------------------------
    with tab_rutina_dieta:
        st.markdown("#### Programación Asignada al Alumno")
        st.caption("Acá podés auditar qué plan tiene cargado el sistema actualmente para este usuario.")
        
        col_p1, col_p2 = st.columns(2)
        with col_p1:
            st.markdown("##### 🏋️ Esquema de Entrenamiento")
            st.text_area(
                label="Rutina Vigente:",
                value=alumno.get("rutina_activa", "No hay ninguna rutina asignada actualmente a este atleta."),
                height=200,
                key="view_rutina"
            )
        with col_p2:
            st.markdown("##### 🍏 Planificación Nutricional")
            st.text_area(
                label="Macronutrientes y Menú:",
                value=alumno.get("dieta_activa", "No hay ninguna planificación nutricional asignada actualmente."),
                height=200,
                key="view_dieta"
            )

    # -------------------------------------------------------------------------
    # TAB 4: HISTORIAL DE SEGUIMIENTO (PREPARADO PARA LOGS DE SUPABASE)
    # -------------------------------------------------------------------------
    with tab_progreso:
        st.markdown("#### Línea de Tiempo de Evolución")
        st.caption("Historial de auditorías métricas guardadas cronológicamente.")
        
        # Consultamos si existen registros históricos para este alumno en una tabla relacional
        try:
            historial_resp = supabase.table("evaluaciones_biometricas").select("*").eq("perfil_id", alumno["id"]).order("fecha_evaluacion", ascending=False).execute()
            logs_evolucion = historial_resp.data if historial_resp.data else []
        except Exception:
            logs_evolucion = []

        if not logs_evolucion:
            st.info("El alumno todavía no cuenta con un historial de chequeos biométricos guardados en la base de datos.")
            
            # Simulador visual estático para diseño Pixel Perfect mientras el alumno no cargue datos
            st.markdown("##### *Vista de ejemplo de gráfico evolutivo estructural:*")
            datos_simulados = {"Peso Corporal (Kg)": [peso_actual, peso_actual], "Semanas": ["Semana 1", "Semana 2"]}
            st.line_chart(data=[peso_actual if peso_actual else 80.0, peso_actual if peso_actual else 79.5])
        else:
            tabla_historial = []
            for log in logs_evolucion:
                tabla_historial.append({
                    "Fecha de Control": log.get("fecha_evaluacion"),
                    "Peso Registrado (Kg)": log.get("peso"),
                    "% Grasa Estimado": log.get("porcentaje_grasa", "S/D"),
                    "Comentarios del Coach": log.get("observaciones", "Sin observaciones")
                })
            st.dataframe(tabla_historial, use_container_width=True)