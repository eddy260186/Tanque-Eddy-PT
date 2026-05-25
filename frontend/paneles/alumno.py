import streamlit as st
import os
import io
import base64
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from datetime import datetime, date, time
from database.conexion import supabase
from ai.gemini import generar_menu_ia
from utils.biometria import calcular_biometria

# IMPORTACIÓN DE TUS MÓDULOS DE SERVICIO ESPECIALIZADOS
from frontend.components.graficos import (
    renderizar_grafico_macros_sidebar,
    renderizar_grafico_proyeccion,
    renderizar_evolucion_historica
)
from backend.services.payment_service import validar_comprobante_pago
from backend.services.plan_service import generar_menu_dinamico, generar_rutina_entrenamiento
from backend.services.ia_service import gestionar_ia_con_creditos, descontar_credito

def app_alumno_original(perfil_id: str, nombre_default: str, pais_default: str, genero_idx: int, fecha_nac_atleta):
    """
    Pieza Central: El Panel Completo del Atleta Elite.
    Maneja la interfaz del alumno conectada a los servicios externos de forma limpia.
    """
    directorio_script = os.path.dirname(os.path.abspath(__file__))
    
    nombre = nombre_default
    pais = pais_default
    genero = "m" if genero_idx == 0 else "f"
    hoy = date.today()
    edad = hoy.year - fecha_nac_atleta.year - ((hoy.month, hoy.day) < (fecha_nac_atleta.month, fecha_nac_atleta.day))

    # 🎨 COMPILACIÓN INDESTRUCTIBLE DE VARIABLES VISUALES
    accent_color = "#FFB6C1" if genero == "f" else "#d4af37"
    bg_plot = "#1A1A1A"

    # ==========================================
    # CONSTRUCCIÓN DEL MENÚ LATERAL (SIDEBAR VIP)
    # ==========================================
    with st.sidebar:
        st.header("🏢 Branding")
        nombres_sidebar = ["logo.png", "logo(1).png", "logo.png.png"]
        foto_side = None
        
        dir_raiz = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        for n in nombres_sidebar:
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

        st.markdown("<p style='text-align: center; color: #d4af37; font-weight: bold; font-size: 14px; margin-bottom: 0px; letter-spacing: 1px;'>¿Dudas con tu plan?</p>", unsafe_allow_html=True)
        num_wa_interno = "5491164788719"
        msg_interno = "Hola%20Eddy.%20Tengo%20una%20consulta%20desde%20mi%20panel."
        link_wa_int = f"https://wa.me/{num_wa_interno}?text={msg_interno}"
        st.markdown(f"<div style='text-align: center;'><a href='{link_wa_int}' target='_blank' style='text-decoration: none; color: #25D366; font-size: 16px;'>💬 <b>Contactar Soporte</b></a></div>", unsafe_allow_html=True)
        st.divider()

        nombre_mostrar = nombre if nombre else "Atleta Elite"
        st.markdown(
            f"""
            <div style="background-color: #151a26; border: 1px solid #d4af37; padding: 15px; border-radius: 10px; margin-bottom: 20px; text-align: center;">
                <span style="color: #d4af37; font-weight: bold; font-size: 16px;">👤 Conectado</span><br>
                <span style="color: #ffffff; font-size: 15px; font-family: Arial, sans-serif; font-weight: bold; text-transform: capitalize;">{nombre_mostrar}</span>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        if st.button("Cerrar Sesión", use_container_width=True):
            supabase.auth.sign_out()
            st.session_state["usuario_actual"] = None
            st.rerun()
            
        st.divider()

        st.header("📏 Medidas Actuales")
        embarazada_bool = False
        if genero == "f": 
            embarazada_bool = st.checkbox("¿Está embarazada?")
            meses_gestacion = st.slider("Meses de gestación:", min_value=1, max_value=9, value=3, disabled=not embarazada_bool)
            st.divider()
            
        estatura = st.number_input("Estatura (cm):", min_value=100, value=170)
        peso_actual = st.number_input("Peso actual (kg):", min_value=30.0, value=75.0)

        st.header("🏋️‍♂️ Perfil Deportivo")
        nivel_experiencia = st.selectbox("Nivel de Experiencia:", ["Principiante", "Intermedio", "Avanzado"])
        tipo_entreno = st.selectbox("Tipo de Entrenamiento:", [
            "Fuerza / Hipertrofia (Gimnasio)", "CrossFit / Funcional", "Powerlifting / Levantamiento Olímpico",
            "Calistenia / Street Workout", "Resistencia (Running, Ciclismo, Natación)", "Deportes de Equipo (Fútbol, Básquet, Rugby)", 
            "Artes Marciales / Deportes de Contacto", "Deportes de Raqueta (Tenis, Pádel)", "Pilates / Yoga / Movilidad",
            "Danza / Baile Deportivo", "Gimnasia Artística / Rítmica", "Rehabilitación / Fisioterapia Activa", "Ninguno (Sedentario)"
        ])
        dias_entreno = st.slider("Días de entrenamiento por semana:", 0, 7, 3)
        hora_entreno = st.time_input("¿A qué hora entrena?", time(18, 0))
        
        st.divider()
        tipo_objetivo = st.selectbox("Meta Principal:", [
            "Pérdida de Grasa (Déficit Estándar)", "Definición Agresiva (Corte)", "Recomposición Corporal", 
            "Mantenimiento / Salud", "Volumen Limpio (Superávit)", "Volumen Agresivo (Bulking)"
        ])
        kg_a_cambiar = st.number_input("Kilos de referencia a modificar:", min_value=0.0, value=5.0)
        meses_plazo = st.number_input("Plazo en meses:", min_value=1, value=3)
        
        st.divider()
        dieta_tipo = st.selectbox("Tipo de Dieta:", [
            "Clásica / Equilibrada", "Hiperproteica (Fitness)", "Cetogénica (Keto)", "Low Carb",
            "Vegana (100% Vegetal)", "Vegetariana", "Pescetariana", "Paleolítica",
            "Mediterránea", "DASH", "FODMAP", "Libre de Gluten", "Sin Lactosa", "Flexitariana"
        ])
        num_comidas = st.selectbox("Cantidad de comidas al día:", [1, 2, 3, 4, 5, 6], index=3)
        num_opciones = st.slider("¿Cuántas opciones de menú por comida?", min_value=1, max_value=10, value=5)

    # ==========================================
    # BIOMETRÍA Y SALUD ELITE
    # ==========================================
    st.subheader("📏 Salud y Biometría Elite")
    st.markdown("<p style='color:#d4af37; font-weight:bold; font-size:16px; margin-bottom:5px;'>🔑 Base Científica (Grasa y Salud)</p>", unsafe_allow_html=True)
    col_b1, col_b2 = st.columns(2)
    with col_b1: cintura = st.number_input("Perímetro de Cinta / Cintura (cm):", value=85.0, key="medida_cintura")
    with col_b2: cadera = st.number_input("Perímetro de Cadera (cm):", value=95.0, key="medida_cadera")

    st.divider()
    st.markdown("<p style='color:#d4af37; font-weight:bold; font-size:16px; margin-bottom:5px;'>🦅 Tren Superior Premium</p>", unsafe_allow_html=True)
    col_sup1, col_sup2, col_sup3 = st.columns(3)
    with col_sup1: cuello = st.number_input("Perímetro de Cuello (cm):", value=38.0, key="medida_cuello")
    with col_sup2: torso = st.number_input("Pectoral / Torso (cm):", value=100.0, key="medida_torso")
    with col_sup3: brazos = st.number_input("Brazos (Promedio cm):", value=35.0, key="medida_brazos")

    st.divider()
    st.markdown("<p style='color:#d4af37; font-weight:bold; font-size:16px; margin-bottom:5px;'>🍑 Tren Inferior y Escultura Estética</p>", unsafe_allow_html=True)
    col_inf1, col_inf2, col_inf3 = st.columns(3)
    with col_inf1: gluteos = st.number_input("Perímetro de Glúteos (cm):", value=98.0, key="medida_gluteos")
    with col_inf2: piernas = st.number_input("Muslos / Piernas (cm):", value=55.0, key="medida_piernas")
    with col_inf3: pantorrillas = st.number_input("Pantorrillas (cm):", value=38.0, key="medida_pantorrillas")

    # Cálculos Biométricos Cruzados
    rcc_valor = round(cintura / cadera, 2) if cadera > 0 else 0
    rfm, masa_magra, tmb = calcular_biometria(genero, estatura, cintura, peso_actual)

    pal_base = 1.2 if dias_entreno == 0 else (1.3 if dias_entreno <= 2 else (1.45 if dias_entreno <= 4 else (1.6 if dias_entreno <= 6 else 1.75)))
    bonus_deporte = 0.15 if any(x in tipo_entreno for x in ["CrossFit", "Resistencia", "Artes Marciales"]) else (0.10 if any(x in tipo_entreno for x in ["Fuerza", "Powerlifting", "Calistenia", "Equipo", "Raqueta", "Gimnasia"]) else 0.05)
    if dias_entreno == 0 or "Ninguno" in tipo_entreno: bonus_deporte = 0.0

    factor_actividad = pal_base + bonus_deporte
    cal_mant = tmb * factor_actividad
    if embarazada_bool: cal_mant += 340 if meses_gestacion <= 6 else 450

    ajuste_diario = (kg_a_cambiar * 7000) / (meses_plazo * 30) if meses_plazo > 0 else 0

    if embarazada_bool and any(x in tipo_objetivo for x in ["Pérdida", "Definición", "Recomposición"]):
        cal_obj = cal_mant
        dif = 0
    else:
        if "Pérdida" in tipo_objetivo: dif = -ajuste_diario
        elif "Definición" in tipo_objetivo: dif = -(ajuste_diario * 1.3)
        elif "Recomposición" in tipo_objetivo: dif = -300 if cal_mant > 1500 else -150
        elif "Volumen Limpio" in tipo_objetivo: dif = ajuste_diario
        elif "Volumen Agresivo" in tipo_objetivo: dif = ajuste_diario * 1.5
        else: dif = 0
        cal_obj = cal_mant + dif

    p_g_total = peso_actual * (2.2 if "Hiper" in dieta_tipo else 1.8)
    if "Keto" in dieta_tipo:
        c_g_total = 30.0
        g_g_total = (cal_obj - (p_g_total * 4) - 120) / 9
    else:
        g_g_total = (cal_obj * 0.30) / 9
        c_g_total = (cal_obj - (p_g_total * 4) - (g_g_total * 9)) / 4

    agua_total = round((peso_actual * 0.035) + 0.75 + (0.5 if dias_entreno > 0 else 0), 1)

    # Llama al componente de dona de macros
    renderizar_grafico_macros_sidebar(p_g_total, c_g_total, g_g_total)

    # CRM DE GUARDADO
    with st.sidebar:
        st.divider()
        if st.button("💾 Guardar Progreso en Supabase", type="primary", use_container_width=True):
            if nombre:
                try:
                    email_usuario = st.session_state["usuario_actual"]
                    supabase.table("evaluaciones_biometricas").insert({
                        "perfil_id": perfil_id, "edad": edad, "estatura": estatura, "peso": peso_actual, "cintura": cintura, "cadera": cadera, "cuello": cuello,
                        "torso": torso, "brazos": brazos, "gluteos": gluteos, "piernas": piernas, "pantorrillas": pantorrillas, "rfm": rfm, "nivel_experiencia": nivel_experiencia, 
                        "meta": tipo_objetivo, "kcal_objetivo": int(cal_obj), "tipo_entrenamiento": tipo_entreno, "dias_entreno": dias_entreno, "fecha_registro": str(date.today())
                    }).execute()
                    
                    info_extra_json = {
                        "macros": {"proteina": round(p_g_total, 1), "carbos": round(c_g_total, 1), "grasas": round(g_g_total, 1)},
                        "biometria_extra": {"masa_magra": round(masa_magra, 1), "tmb": round(tmb, 1), "rcc": rcc_valor},
                        "metas_tiempo": {"kg_a_cambiar": kg_a_cambiar, "meses_plazo": meses_plazo},
                        "habitos": {"hora_entreno": str(hora_entreno), "comidas_dia": num_comidas, "agua_litros": agua_total},
                        "embarazo": {"es_embarazada": embarazada_bool, "meses_gestacion": meses_gestacion if embarazada_bool else 0}
                    }
                    supabase.table("historial_planes").insert({"perfil_id": perfil_id, "tipo_plan": dieta_tipo, "detalle_macros": info_extra_json, "rutina_asignada": f"Rutina de {tipo_entreno} ({dias_entreno} días)"}).execute()
                    st.success("✅ ¡Evolución y Plan guardados al 100%!")
                except Exception as e:
                    st.error(f"❌ Error al guardar: {e}")

    st.info(f"Atleta: **{nombre if nombre else 'Eddy PT'}** | RCC: {rcc_valor} | **Grasa Est. (RFM): {rfm}%** | Nivel: {nivel_experiencia}")
    col_r1, col_r2, col_r3, col_r4 = st.columns(4)
    col_r1.metric("Mantenimiento", f"{int(cal_mant)} kcal")
    col_r2.metric("Ajuste Diario", f"{int(dif)} kcal", delta=int(dif))
    col_r3.metric("Objetivo Final", f"{int(cal_obj)} kcal")
    col_r4.metric("💧 Agua (Con Entreno)", f"{agua_total} L")

    # Cálculos y renderizado de la Proyección de peso
    kg_mes_real = (dif * 30) / 7000 
    fechas_reales = [(datetime.now() + pd.DateOffset(months=i)).strftime("%d/%m/%Y") for i in range(int(meses_plazo) + 1)]
    pesos_prog = [peso_actual + (kg_mes_real * i) for i in range(len(fechas_reales))]

    # Renderiza gráfico de proyección interactivo pasando el color de acento
    renderizar_grafico_proyeccion(fechas_reales, pesos_prog, accent_color)

    # Renderiza todo el bloque histórico conectado en vivo
    renderizar_evolucion_historica(perfil_id, peso_actual, rfm, brazos, piernas, tipo_objetivo)

    # ==========================================
    # SUPLEMENTACIÓN Y MENÚ DINÁMICO VIA SERVICE
    # ==========================================
    st.subheader(f"🍽️ Plan de {num_comidas} Comidas ({int(cal_obj)} kcal)")
    
    diccionario_menus, lista_compras = generar_menu_dinamico(
        p_g_total, c_g_total, g_g_total, num_comidas, num_opciones, dieta_tipo, pais
    )

    for nombre_base, opciones in diccionario_menus.items():
        st.button(f"› ✨ {nombre_base}", use_container_width=True, disabled=True)
        for op in opciones:
            st.write(op)

    # --- CONSULTORÍA IA TEAM EDDY ---
    st.divider()
    st.subheader("🏆 Consultoría Directa con Eddy Personal Trainer")
    puedo_usar, total_creditos = gestionar_ia_con_creditos(st.session_state['usuario_actual'])

    if puedo_usar:
        st.info(f"Hola Tanque, hoy tenés **{total_creditos}** consultas disponibles con el equipo.")
        pregunta_atleta = st.text_area("¿Qué duda tenés hoy para el equipo, Tanque?", placeholder="Ej: Eddy, ¿qué puedo cenar hoy para recuperar después de hacer piernas?")

        if st.button("💬 ENVIAR CONSULTA AL TEAM EDDY", use_container_width=True):
            if pregunta_atleta:
                with st.spinner("Bancame un toque..."):
                    prompt_eddy = f"Actuá como Eddy, un Personal Trainer de Élite argentino. Tu estilo es motivador, directo y profesional, usando modismos como 'Tanque', 'Dale con todo', 'viste', 'metele mecha'. Pregunta del atleta: {pregunta_atleta} Firmá siempre al final: Team Eddy - Software Elite."
                    try:
                        respuesta_texto = generar_menu_ia(prompt_eddy)
                        st.markdown("### 📢 Respuesta de Eddy:")
                        st.write(respuesta_texto)
                        descontar_credito(st.session_state['usuario_actual'], total_creditos)
                    except Exception as e:
                        st.error(f"Se cortó la conexión, Tanque: {e}")
            else:
                st.warning("Escribime algo antes de enviar, Tanque.")
    else:
        st.error("🚫 Ya agotaste tus consultas de prueba.")

    # --- ENTRENAMIENTO VIA SERVICE ---
    st.subheader(f"🏋️‍♂️ Plan de Entrenamiento ({nivel_experiencia})")
    diccionario_rutinas = generar_rutina_entrenamiento(tipo_entreno, nivel_experiencia, dias_entreno)
    st.button("› 👁️ VER RUTINA GENERADA", use_container_width=True, disabled=True)
    for k, v in diccionario_rutinas.items():
        st.markdown(f"**{k}**")
        for ex in v: st.write(ex)

    # --- PASARELA DE MERCADO PAGO VIA SERVICE ---
    st.divider()
    st.markdown("### 🔒 Descarga Protegida")

    if "pago_validado" not in st.session_state:
        st.session_state.pago_validado = False

    if not st.session_state.pago_validado:
        st.info("Para descargar tu Plan Elite, ingresa el número de operation de tu pago.")
        col_p, col_v = st.columns(2)
        with col_p:
            st.link_button("💳 REALIZAR PAGO ($10.000)", "https://mpago.la/27TKbMf", type="primary")
        with col_v:
            nro_operacion = st.text_input("Ingresá el # de Operación:")
            if st.button("🔓 Validar y Descargar"):
                exito_pago, mensaje_pago = validar_comprobante_pago(nro_operacion, st.session_state["usuario_actual"])
                if exito_pago:
                    st.session_state.pago_validado = True
                    st.success(mensaje_pago)
                    st.rerun()
                else:
                    st.error(mensaje_pago)

    # --- ENTORNO DE CONSTRUCCIÓN DE PDF ---
    if st.session_state.pago_validado:
        st.success("✅ ¡Pago validado! Tu Plan Elite ha sido desbloqueado.")
        
        fig_matt, ax_matt = plt.subplots(figsize=(10, 3))
        fig_matt.patch.set_facecolor(bg_plot)
        ax_matt.set_facecolor(bg_plot)
        ax_matt.bar(fechas_reales, pesos_prog, color=accent_color)
        ax_matt.tick_params(colors=accent_color)
        for spine in ax_matt.spines.values(): spine.set_color(accent_color)
        for i, v in enumerate(pesos_prog): ax_matt.text(i, v + 0.5, f"{round(v,1)}kg", ha='center', fontsize=10, fontweight='bold', color='#ffffff')

        buf = io.BytesIO()
        fig_matt.savefig(buf, format="png", bbox_inches="tight", facecolor=bg_plot)
        buf.seek(0)
        grafico_base64 = base64.b64encode(buf.read()).decode("utf-8")
        plt.close(fig_matt)

        payload = {
            "n": nombre, "edad": edad, "estatura": estatura, "peso": peso_actual, "rfm": rfm, "k": cal_obj,
            "p": p_g_total, "c": c_g_total, "g": g_g_total, "meta": tipo_objetivo, "nivel": nivel_experiencia,
            "w": agua_total, "entreno": tipo_entreno, "m": diccionario_menus, "rutina": diccionario_rutinas
        }

        with st.container():
            with st.spinner("⏳ Ensamblando tu PDF Ultra Elite..."):
                try:
                    from utils.pdf_generator_elite import build_pdf_ultra_elite
                    pdf_elite = build_pdf_ultra_elite(data=payload, grafico_b64=grafico_base64, genero=genero)
                    if pdf_elite:
                        st.download_button(
                            label="🏆 DESCARGAR PLAN ULTRA ELITE", data=pdf_elite,
                            file_name=f"Plan_Elite_{nombre.replace(' ', '_')}.pdf", mime="application/pdf",
                            type="primary", key="descarga_pdf"
                        )
                except Exception as e:
                    st.error(f"❌ Error técnico al generar PDF: {e}")