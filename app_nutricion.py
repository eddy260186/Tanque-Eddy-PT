import requests
import streamlit as st
from weasyprint import HTML
from datetime import datetime, date, time
import pandas as pd
import matplotlib
matplotlib.use("Agg") # Optimización brutal de memoria para servidor
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import os
from collections import defaultdict
import io
import base64
import google.generativeai as genai

# Configuramos la IA limpiando espacios invisibles por seguridad
llave_limpia = st.secrets["GEMINI_API_KEY"].strip()
genai.configure(api_key=llave_limpia)
model = genai.GenerativeModel('gemini-2.5-flash')

from database.supabase_mgr import init_supabase
from utils.biometria import calcular_biometria
from utils.pdf_generator import build_pdf_v60_7
from data.alimentos import alimentos_db
from data.ejercicios import ejercicios_db, rutinas_elite
from styles import aplicar_diseno_elite

# ==========================================
# 1. CONFIGURACIÓN DE PÁGINA
# ==========================================
st.set_page_config(page_title="Eddy PT - Elite v60.7", page_icon="💪", layout="wide")
aplicar_diseno_elite()
st.markdown('<meta name="google" content="notranslate">', unsafe_allow_html=True)

# ==========================================
# 2. SISTEMA DE USUARIOS (LOGIN / REGISTRO)
# ==========================================
supabase = init_supabase()

def gestionar_ia_con_creditos(email_usuario):
    # ESCUDO: Importamos internamente con alias 'dt' para que nada lo rompa
    import datetime as dt
    
    res = supabase.table("perfiles_atletas").select("creditos_ia, guia_comprada, fecha_ultima_recarga").eq("email", email_usuario).execute()
    
    if res.data:
        perfil = res.data[0]
        compro_guia = perfil.get('guia_comprada', False)
        valor_db = perfil.get('creditos_ia')
        creditos_actuales = 0 if valor_db is None else int(valor_db)
        ultima_recarga_str = perfil.get('fecha_ultima_recarga')

        if compro_guia:
            hoy = dt.date.today()
            try:
                ultima_recarga = dt.datetime.strptime(ultima_recarga_str, '%Y-%m-%d').date() if ultima_recarga_str else None
            except:
                ultima_recarga = None

            if ultima_recarga is None or (hoy - ultima_recarga).days >= 30:
                creditos_actuales = 30
                supabase.table("perfiles_atletas").update({
                    "creditos_ia": 30,
                    "fecha_ultima_recarga": str(hoy)
                }).eq("email", email_usuario).execute()
                st.success("¡Vamooo Tanque! Tu acceso mensual se renovó. Tenés 30 consultas nuevas.")

        if creditos_actuales > 0:
            return True, creditos_actuales
            
    return False, 0

def descontar_credito(email_usuario, creditos_actuales):
    nuevo_saldo = creditos_actuales - 1
    supabase.table("perfiles_atletas").update({"creditos_ia": nuevo_saldo}).eq("email", email_usuario).execute()
    return nuevo_saldo

if "usuario_actual" not in st.session_state:
    st.session_state["usuario_actual"] = None

# Si NO hay nadie logueado, mostramos solo la pantalla de entrada

if st.session_state["usuario_actual"] is None:
    
# --- SOLO EL LOGO CENTRADO Y MÁS CHICO ---
    col1, col_logo, col3 = st.columns([1, 1, 1]) 
    with col_logo:
        try:
            import os
            # Buscamos el logo verde directamente
            if os.path.exists("logo.png"):
                st.image("logo.png", use_container_width=True)
            elif os.path.exists("logo.png.png"):
                st.image("logo.png.png", use_container_width=True)
        except Exception:
            pass
        
    st.markdown("<h2 style='text-align: center; margin-bottom: 0px;'>🏆 Portal Elite Fitness</h2>", unsafe_allow_html=True)
    st.markdown("<h5 style='text-align: center; color: #888888; font-style: italic; margin-top: 0px;'>🚫 No apto para escarbadientes🚫</h5>", unsafe_allow_html=True)
    st.markdown("---")
    
    # --- EL RESTO VUELVE A LA NORMALIDAD (ANCHO COMPLETO COMO LO QUERÍAS) ---
    tab_login, tab_registro = st.tabs(["Iniciar Sesión", "Crear Cuenta Nueva"])
    
    with tab_login:
        email_login = st.text_input("Correo electrónico", key="log_email")
        pass_login = st.text_input("Contraseña", type="password", key="log_pass")
        
        # Botón ancho premium LOGIN
        if st.button("Entrar", type="primary", use_container_width=True):
            try:
                respuesta = supabase.auth.sign_in_with_password({"email": email_login.lower().strip(), "password": pass_login})
                st.session_state["usuario_actual"] = respuesta.user.email
                st.success("¡Acceso concedido! Cargando tu panel...")
                st.rerun()
            except Exception as e:
                # ACÁ ESTÁ EL CAMBIO: Ahora el error nos dice la verdad
                st.error(f"Error al iniciar sesión: {e}")
                
    with tab_registro:
        st.info("Crea tu cuenta gratis para poder generar y guardar tus rutinas.")
        
        nombre_reg = st.text_input("Nombre Completo", key="reg_nombre")
        email_reg = st.text_input("Correo electrónico", key="reg_email")
        pass_reg = st.text_input("Contraseña (mínimo 6 caracteres)", type="password", key="reg_pass")
        
        # Selector de Género para evitar el error de "masculino" por defecto
        genero_opcion = st.selectbox("Género", ["Masculino", "Femenino"], key="reg_genero")
        genero_db = "m" if genero_opcion == "Masculino" else "f"
        
        from datetime import date
        fecha_nac_reg = st.date_input("Fecha de Nacimiento:", min_value=date(1940, 1, 1), max_value=date.today(), key="reg_fecha")
        
        if st.button("Registrarme", type="primary", use_container_width=True):
            if not nombre_reg.strip():
                st.warning("⚠️ Por favor, ingresa tu nombre completo.")
            else:
                try:
                    # Limpieza total para evitar errores de teclado en iPhone/Android
                    email_final = email_reg.lower().strip()
                    respuesta = supabase.auth.sign_up({"email": email_final, "password": pass_reg})
                    
                    try:
                        supabase.table("perfiles_atletas").insert({
                            "email": email_final,
                            "nombre_completo": nombre_reg.strip(),
                            "pais": "Argentina", 
                            "genero": genero_db,
                            "fecha_nacimiento": str(fecha_nac_reg)
                        }).execute()
                        st.success("✅ ¡Cuenta creada con éxito! Ya puedes iniciar sesión.")
                    except Exception as db_error:
                        st.warning(f"Error al guardar perfil: {db_error}")
                except Exception as auth_error:
                    st.error(f"Error de registro: {auth_error}")

# --- BOTÓN DE SOPORTE WHATSAPP ---

        st.markdown("<br>", unsafe_allow_html=True) 
        
        # ACÁ PONÉS TU NÚMERO (ej: 54911... o 549237... si es de tu zona)
        numero_whatsapp = "5491164788719" 
        mensaje = "Hola%20Soporte.%20Necesito%20ayuda%20con%20el%20Portal%20Elite."
        link_wa = f"https://wa.me/{numero_whatsapp}?text={mensaje}"
        
        st.markdown(f"<div style='text-align: center;'><a href='{link_wa}' target='_blank' style='text-decoration: none; color: #25D366; font-size: 15px;'>💬 <b>¿Problemas para ingresar? Contactá al Soporte</b></a></div>", unsafe_allow_html=True)
    st.stop() # Frena la app acá si no están logueados

# ==========================================
# SI LLEGA ACÁ, ESTÁ LOGUEADO. MOSTRAMOS LA APP NORMAL
# ==========================================
st.title("🏆 Eddy Personal Trainer: Software Elite v60.7")

import os
directorio_script = os.path.dirname(os.path.abspath(__file__))

rutas_logo = [
    os.path.join(directorio_script, "logo.png"),       
    os.path.join(directorio_script, "logo.png.png"),   
    os.path.join(directorio_script, "logo")
]
ruta_logo_final = next((r for r in rutas_logo if os.path.exists(r)), None)

with st.sidebar:
    st.header("🏢 Branding")
    if ruta_logo_final:
        try:
            st.image(ruta_logo_final, use_container_width=True)
        except Exception:
            pass
    st.divider()

    # --- BOTÓN DE SOPORTE WHATSAPP EN EL MENÚ LATERAL ---
    # Paso 2: Título en Dorado Premium
    st.markdown("<p style='text-align: center; color: #d4af37; font-weight: bold; font-size: 14px; margin-bottom: 0px; letter-spacing: 1px;'>¿Dudas con tu plan?</p>", unsafe_allow_html=True)

    num_wa_interno = "5491164788719"
    msg_interno = "Hola%20Eddy.%20Tengo%20una%20consulta%20desde%20mi%20panel."
    link_wa_int = f"https://wa.me/{num_wa_interno}?text={msg_interno}"

    # Botón WhatsApp con el paréntesis corregido
    st.markdown(f"<div style='text-align: center;'><a href='{link_wa_int}' target='_blank' style='text-decoration: none; color: #25D366; font-size: 16px;'>💬 <b>Contactar Soporte</b></a></div>", unsafe_allow_html=True)
    st.divider()

    # Paso 3: Caja VIP de usuario conectado
    st.markdown(
        f"""
        <div style="background-color: #151a26; border: 1px solid #d4af37; padding: 15px; border-radius: 10px; margin-bottom: 20px; text-align: center;">
            <span style="color: #d4af37; font-weight: bold; font-size: 16px;">👤 Conectado</span><br>
            <span style="color: #ffffff; font-size: 14px; font-family: monospace;">{st.session_state['usuario_actual']}</span>
        </div>
        """,
        unsafe_allow_html=True
    )
    if st.button("Cerrar Sesión"):
        supabase.auth.sign_out()
        st.session_state["usuario_actual"] = None
        st.rerun()
    st.divider()

DB_FILE = os.path.join(directorio_script, "Historial_Atletas.csv")

from datetime import date, datetime

# ==========================================
# 3. PERFIL DEL ATLETA (SOLUCIÓN FINAL TESTEADA)
# ==========================================

# Definimos la variable antes de usarla para evitar el NameError
email_usuario = st.session_state.get("usuario_actual", "")

# Limpiamos el email solo si existe, de lo contrario queda vacío
if email_usuario:
    email_limpio = email_usuario.lower().strip()
else:
    email_limpio = ""

# Consulta a Supabase con el email verificado
res_perfil = supabase.table("perfiles_atletas").select("*").eq("email", email_limpio).execute()

if len(res_perfil.data) > 0:
    perfil_db = res_perfil.data[0]
    nombre_default = perfil_db.get("nombre_completo", "")
    pais_default = perfil_db.get("pais", "Argentina")
    
    # Manejo seguro del género
    genero_db = perfil_db.get("genero")
    genero_idx = 0 if (genero_db and genero_db.strip() == "m") else 1
    
    # Rescatamos la fecha de nacimiento que puso al registrarse
    fecha_str = perfil_db.get("fecha_nacimiento")
    if fecha_str:
        fecha_nac_atleta = datetime.strptime(fecha_str, "%Y-%m-%d").date()
    else:
        fecha_nac_atleta = date(1990, 1, 1) # Fecha por defecto por si falta
        
    es_nuevo = False if nombre_default else True
else:
    nombre_default = ""
    pais_default = "Argentina"
    genero_idx = 0
    fecha_nac_atleta = date(1990, 1, 1)
    es_nuevo = True

with st.sidebar:
    st.header("👤 Perfil del Atleta")
    
    if not es_nuevo:
        st.success(f"👋 Hola de nuevo, {nombre_default}")
        
    nombre = st.text_input("Nombre Completo:", value=nombre_default, disabled=not es_nuevo)
    pais = st.text_input("País de Residencia:", value=pais_default, disabled=not es_nuevo)
    genero_seleccion = st.selectbox("Género:", ["m ", "f "], index=genero_idx, disabled=not es_nuevo)
    genero = genero_seleccion.strip()
    
    # CÁLCULO INVISIBLE: Calculamos la edad sin pedirle nada
    hoy = date.today()
    edad = hoy.year - fecha_nac_atleta.year - ((hoy.month, hoy.day) < (fecha_nac_atleta.month, fecha_nac_atleta.day))
    
    st.info(f"🎂 Edad registrada: {edad} años")
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
        "Fuerza / Hipertrofia (Gimnasio)", 
        "CrossFit / Funcional", 
        "Powerlifting / Levantamiento Olímpico",
        "Calistenia / Street Workout",
        "Resistencia (Running, Ciclismo, Natación)", 
        "Deportes de Equipo (Fútbol, Básquet, Rugby)", 
        "Artes Marciales / Deportes de Contacto",
        "Deportes de Raqueta (Tenis, Pádel)",
        "Pilates / Yoga / Movilidad",
        "Danza / Baile Deportivo",
        "Gimnasia Artística / Rítmica",
        "Rehabilitación / Fisioterapia Activa",
        "Ninguno (Sedentario)"
    ])
    dias_entreno = st.slider("Días de entrenamiento por semana:", 0, 7, 3)
    hora_entreno = st.time_input("¿A qué hora entrena?", time(18, 0))
    
    st.divider()
    tipo_objetivo = st.selectbox("Meta Principal:", [
        "Pérdida de Grasa (Déficit Estándar)", 
        "Definición Agresiva (Corte)", 
        "Recomposición Corporal", 
        "Mantenimiento / Salud", 
        "Volumen Limpio (Superávit)", 
        "Volumen Agresivo (Bulking)"
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
# 4. SALUD Y BIOMETRÍA ELITE
# ==========================================
st.subheader("📏 Salud y Biometría Elite")
col_c1, col_c2 = st.columns(2)
with col_c1: 
    cintura = st.number_input("Perímetro de Cintura (cm):", value=85.0)
with col_c2: 
    cadera = st.number_input("Perímetro de Cadera (cm):", value=95.0)

rcc_valor = round(cintura / cadera, 2) if cadera > 0 else 0

rfm, masa_magra, tmb = calcular_biometria(genero, estatura, cintura, peso_actual)
if dias_entreno == 0: 
    pal_base = 1.2
elif 1 <= dias_entreno <= 2: 
    pal_base = 1.3
elif 3 <= dias_entreno <= 4: 
    pal_base = 1.45
elif 5 <= dias_entreno <= 6: 
    pal_base = 1.6
else: 
    pal_base = 1.75

if dias_entreno == 0 or "Ninguno" in tipo_entreno: 
    bonus_deporte = 0.0
elif any(x in tipo_entreno for x in ["CrossFit", "Resistencia", "Artes Marciales"]): 
    bonus_deporte = 0.15
elif any(x in tipo_entreno for x in ["Fuerza", "Powerlifting", "Calistenia", "Equipo", "Raqueta", "Gimnasia"]): 
    bonus_deporte = 0.10
else: 
    bonus_deporte = 0.05

factor_actividad = pal_base + bonus_deporte
cal_mant = tmb * factor_actividad

if embarazada_bool: 
    cal_mant += 340 if meses_gestacion <= 6 else 450

ajuste_diario = (kg_a_cambiar * 7000) / (meses_plazo * 30) if meses_plazo > 0 else 0

if embarazada_bool and any(x in tipo_objetivo for x in ["Pérdida", "Definición", "Recomposición"]):
    cal_obj = cal_mant
    dif = 0
else:
    if "Pérdida" in tipo_objetivo: 
        dif = -ajuste_diario
    elif "Definición" in tipo_objetivo: 
        dif = -(ajuste_diario * 1.3)
    elif "Recomposición" in tipo_objetivo: 
        dif = -300 if cal_mant > 1500 else -150
    elif "Volumen Limpio" in tipo_objetivo: 
        dif = ajuste_diario
    elif "Volumen Agresivo" in tipo_objetivo: 
        dif = ajuste_diario * 1.5
    else: 
        dif = 0
    cal_obj = cal_mant + dif

p_g_total = peso_actual * (2.2 if "Hiper" in dieta_tipo else 1.8)

if "Keto" in dieta_tipo:
    c_g_total = 30.0
    g_g_total = (cal_obj - (p_g_total * 4) - 120) / 9
else:
    g_g_total = (cal_obj * 0.30) / 9
    c_g_total = (cal_obj - (p_g_total * 4) - (g_g_total * 9)) / 4

agua_total = round((peso_actual * 0.035) + 0.75 + (0.5 if dias_entreno > 0 else 0), 1)

# ==========================================
# 5. CRM Y GRÁFICO
# ==========================================
accent_color = "#FFB6C1" if genero == "f" else "#d4af37"
bg_plot = "#1A1A1A" if genero == "f" else "#1a1a1a"

with st.sidebar:
    st.divider()
    if st.button("💾 Guardar Progreso en Supabase", type="primary", use_container_width=True):
        if nombre:
            try:
                # 1. Identificamos al usuario logueado
                email_usuario = st.session_state["usuario_actual"]
                
                # 2. PERFIL: Acá guardamos si es masculino/femenino (genero)
                res_perfil = supabase.table("perfiles_atletas").select("id").eq("email", email_usuario).execute()
                if len(res_perfil.data) > 0:
                    perfil_id = res_perfil.data[0]["id"]
                else:
                    nuevo_perfil = supabase.table("perfiles_atletas").insert({
                        "email": email_usuario,
                        "nombre_completo": nombre,
                        "pais": pais,
                        "genero": genero, # <--- ACÁ ESTÁ EL GÉNERO
                        "objetivo_principal": tipo_objetivo
                    }).execute()
                    perfil_id = nuevo_perfil.data[0]["id"]
                
                # 3. BIOMETRÍA: Acá guardamos la edad, peso, entrenamiento...
                supabase.table("evaluaciones_biometricas").insert({
                    "perfil_id": perfil_id,
                    "edad": edad,                 # <--- ACÁ ESTÁ LA EDAD
                    "estatura": estatura,
                    "peso": peso_actual,          # <--- ACÁ ESTÁ EL PESO
                    "cintura": cintura,
                    "cadera": cadera,
                    "rfm": rfm,
                    "nivel_experiencia": nivel_experiencia,
                    "meta": tipo_objetivo,
                    "kcal_objetivo": int(cal_obj),
                    "tipo_entrenamiento": tipo_entreno, # <--- TIPO DE ENTRENAMIENTO
                    "dias_entreno": dias_entreno
                }).execute()
                
                # 4. LA CAJA FUERTE (JSON): Acá metemos el embarazo, el agua y la TMB
                info_extra_json = {
                    "macros": {"proteina": round(p_g_total, 1), "carbos": round(c_g_total, 1), "grasas": round(g_g_total, 1)},
                    "biometria_extra": {"masa_magra": round(masa_magra, 1), "tmb": round(tmb, 1), "rcc": rcc_valor},
                    "metas_tiempo": {"kg_a_cambiar": kg_a_cambiar, "meses_plazo": meses_plazo},
                    "habitos": {"hora_entreno": str(hora_entreno), "comidas_dia": num_comidas, "agua_litros": agua_total},
                    "embarazo": {"es_embarazada": embarazada_bool, "meses_gestacion": meses_gestacion if embarazada_bool else 0} # <--- CÁLCULO DE EMBARAZO
                }

                # 5. PLAN HISTÓRICO: Mandamos la caja fuerte a Supabase
                supabase.table("historial_planes").insert({
                    "perfil_id": perfil_id,
                    "tipo_plan": dieta_tipo,
                    "detalle_macros": info_extra_json,
                    "rutina_asignada": f"Rutina de {tipo_entreno} ({dias_entreno} días)"
                }).execute()
                
                st.success("✅ ¡Evolución y Plan guardados al 100% en la base de datos!")
            except Exception as e:
                st.error(f"❌ Error al guardar en la nube: {e}")
        else:
            st.warning("⚠️ Escribe el nombre del atleta primero.")

st.info(f"Atleta: **{nombre if nombre else 'Eddy PT'}** | RCC: {rcc_valor} | **Grasa Est. (RFM): {rfm}%** | Nivel: {nivel_experiencia}")
col_r1, col_r2, col_r3, col_r4 = st.columns(4)
col_r1.metric("Mantenimiento", f"{int(cal_mant)} kcal")
col_r2.metric("Ajuste Diario", f"{int(dif)} kcal", delta=int(dif))
col_r3.metric("Objetivo Final", f"{int(cal_obj)} kcal")
col_r4.metric("💧 Agua (Con Entreno)", f"{agua_total} L")

kg_mes_real = (dif * 30) / 7000 
fechas_reales = [(datetime.now() + pd.DateOffset(months=i)).strftime("%d/%m/%Y") for i in range(int(meses_plazo) + 1)]
pesos_prog = [peso_actual + (kg_mes_real * i) for i in range(len(fechas_reales))]

# --- 1. GRÁFICO INVISIBLE PARA EL PDF (Sigue funcionando por detrás) ---
fig, ax = plt.subplots(figsize=(10, 3))
fig.patch.set_facecolor(bg_plot)
ax.set_facecolor(bg_plot)
ax.bar(fechas_reales, pesos_prog, color=accent_color)
ax.tick_params(colors=accent_color)
for spine in ax.spines.values(): 
    spine.set_color(accent_color)
for i, v in enumerate(pesos_prog): 
    ax.text(i, v + 0.5, f"{round(v,1)}kg", ha='center', fontsize=10, fontweight='bold', color='#ffffff')

# Guardamos la imagen en secreto para el PDF (Acá ya NO usamos st.pyplot)
buf = io.BytesIO()
fig.savefig(buf, format="png", bbox_inches="tight", facecolor=bg_plot)
buf.seek(0)
grafico_base64 = base64.b64encode(buf.read()).decode("utf-8")
plt.close(fig) # Cerramos el gráfico viejo de la memoria


# --- 2. NUEVO GRÁFICO INTERACTIVO PLOTLY (El que ve el usuario) ---
fig_plotly = go.Figure()

# Creamos las barras interactivas
fig_plotly.add_trace(go.Bar(
    x=fechas_reales,
    y=pesos_prog,
    marker_color=accent_color, # <--- ACÁ LEE TU VARIABLE MÁGICA (Dorado o Rosa)
    text=[f"{round(v,1)} kg" for v in pesos_prog],
    textposition='auto',
    hoverinfo='x+y', 
    hovertemplate='<b>Fecha:</b> %{x}<br><b>Peso Proyectado:</b> %{y} kg<extra></extra>'
))

# Le damos el diseño oscuro y neón, respetando tu color
fig_plotly.update_layout(
    title=dict(text="Proyección de Evolución Corporal", font=dict(color=accent_color, size=18)),
    plot_bgcolor='rgba(0,0,0,0)', # Fondo transparente
    paper_bgcolor='rgba(0,0,0,0)', # Fondo transparente
    font=dict(color='#ffffff'),
    xaxis=dict(showgrid=False, linecolor=accent_color),
    yaxis=dict(showgrid=True, gridcolor='#333333', linecolor=accent_color, zeroline=False),
    margin=dict(l=20, r=20, t=50, b=20)
)

# Lo mostramos en la aplicación de forma segura para no romper React
st.plotly_chart(
    fig_plotly, 
    use_container_width=True, 
    key="grafico_evolucion_corporal_elite"
)

# ==========================================
# 6. SUPLEMENTACIÓN
# ==========================================
suples = [
    "✅ Creatina (5g): Diario para fuerza y recuperación ATP.",
    "💊 Multivitamínico: 1 cápsula con el desayuno.",
    "🦴 Magnesio/Zinc: 1 dosis por la noche."
]
if "Volumen" in tipo_objetivo or "Recomposición" in tipo_objetivo: 
    suples.append("🚀 Citrulina Malato (6-8g): 30 min Pre-entreno.")
if "Definición" in tipo_objetivo or "Pérdida" in tipo_objetivo: 
    suples.append("🏃‍♂️ Beta-Alanina (3-5g): Diario.")
if "Agresiva" in tipo_objetivo or "Keto" in dieta_tipo or "Vegana" in dieta_tipo: 
    suples.append("🐟 Omega-3 (1-3g EPA/DHA): Con la comida principal.")
if "Keto" in dieta_tipo or (10 <= hora_entreno.hour <= 16): 
    suples.append("⚡ Electrolitos: Intra-entreno en el agua.")
if hora_entreno.hour < 12: 
    suples.append("☕ Cafeína: 30 min Pre-entreno (Mañana).")
suples.append("🥤 Proteína Whey o Vegetal: Post-entreno.")

# ==========================================
# 7. MENÚ DINÁMICO
# ==========================================
st.subheader(f"🍽️ Plan de {num_comidas} Comidas ({int(cal_obj)} kcal)")
diccionario_menus = {} 
lista_compras = defaultdict(float)

p_com = p_g_total / num_comidas
c_com = c_g_total / num_comidas
g_com = g_g_total / num_comidas

gramos_p = int(p_com / 0.25)
gramos_g = int(g_com / 0.90)

if "Keto" in dieta_tipo:
    gramos_c = 0
else:
    gramos_c = int(c_com / 0.25)

mapa_nombres = {
    1: ["Comida Única"], 
    2: ["Almuerzo", "Cena"], 
    3: ["Desayuno", "Almuerzo", "Cena"], 
    4: ["Desayuno", "Almuerzo", "Merienda", "Cena"], 
    5: ["Desayuno", "Media Mañana", "Almuerzo", "Merienda", "Cena"], 
    6: ["Desayuno", "Media Mañana", "Almuerzo", "Merienda", "Pre-Cena", "Cena"]
}

for nombre_base in mapa_nombres[num_comidas]:
    opciones_de_esta_comida = []
    st.button(f"› ✨ {nombre_base.upper()}", use_container_width=True, disabled=True)
    if True:
        es_mt = any(x in nombre_base for x in ["Desayuno", "Merienda", "Mañana"])
        for i in range(num_opciones):
            
            if "Vegana" in dieta_tipo: 
                fp = alimentos_db["Prot_Vegana"][i % len(alimentos_db["Prot_Vegana"])]
            elif "Vegetariana" in dieta_tipo: 
                if es_mt:
                    fp = alimentos_db["Prot_Desayuno"][i % len(alimentos_db["Prot_Desayuno"])]
                else:
                    fp = alimentos_db["Prot_Vegana"][i % len(alimentos_db["Prot_Vegana"])]
            elif "Pescetariana" in dieta_tipo: 
                if es_mt:
                    fp = alimentos_db["Prot_Desayuno"][i % len(alimentos_db["Prot_Desayuno"])]
                else:
                    fp = alimentos_db["Prot_Pescado"][i % len(alimentos_db["Prot_Pescado"])]
            else: 
                if es_mt:
                    fp = alimentos_db["Prot_Desayuno"][i % len(alimentos_db["Prot_Desayuno"])]
                else:
                    fp = alimentos_db["Prot_Principal"][i % len(alimentos_db["Prot_Principal"])]
            
            if "Keto" in dieta_tipo: 
                fc = alimentos_db["Verduras_Keto"][i % len(alimentos_db["Verduras_Keto"])]
                texto_carbo = "Libre"
            elif "Paleo" in dieta_tipo: 
                fc = alimentos_db["Carb_Vegetales"][i % len(alimentos_db["Carb_Vegetales"])]
                texto_carbo = f"{gramos_c}g"
            else: 
                if es_mt:
                    fc = alimentos_db["Carb_Desayuno"][i % len(alimentos_db["Carb_Desayuno"])]
                else:
                    fc = alimentos_db["Carb_Principal"][i % len(alimentos_db["Carb_Principal"])]
                texto_carbo = f"{gramos_c}g"
            
            fg = alimentos_db["Grasas"][i % len(alimentos_db["Grasas"])]
            
            if "Argentina" in pais:
                bebida = alimentos_db["Bebidas_Arg"][i % len(alimentos_db["Bebidas_Arg"])]
            else:
                bebida = alimentos_db["Bebidas_Gral"][i % len(alimentos_db["Bebidas_Gral"])]
            
            txt_op = f"Opcion {i+1}: {gramos_p}g {fp} + {texto_carbo} {fc} + {gramos_g}g {fg} | Infusion: {bebida}"
            #st.write(txt_op)
            opciones_de_esta_comida.append(txt_op)

            dias_por_opcion = 30 / num_opciones
            lista_compras[fp] += gramos_p * dias_por_opcion
            if "Keto" not in dieta_tipo: 
                lista_compras[fc] += gramos_c * dias_por_opcion
            lista_compras[fg] += gramos_g * dias_por_opcion
            lista_compras[bebida] += dias_por_opcion
            
    diccionario_menus[nombre_base.upper()] = opciones_de_esta_comida

# --- PANEL DE CONSULTORÍA EXCLUSIVA TEAM EDDY ---
st.divider()
st.subheader("🏆 Consultoría Directa con Eddy Personal Trainer")

# Verificamos créditos con la lógica de recarga mensual que ya pusimos en el Paso 2
puedo_usar, total_creditos = gestionar_ia_con_creditos(st.session_state['usuario_actual'])

if puedo_usar:
    st.info(f"Hola Tanque, hoy tenés **{total_creditos}** consultas disponibles con el equipo.")
    
    # Cuadro para que el atleta te escriba su duda real
    pregunta_atleta = st.text_area("¿Qué duda tenés hoy para el equipo, Tanque?", 
                                   placeholder="Ej: Eddy, ¿qué puedo cenar hoy para recuperar después de hacer piernas?")

    if st.button("💬 ENVIAR CONSULTA AL TEAM EDDY", use_container_width=True):
        if pregunta_atleta:
            with st.spinner("Bancame un toque que estoy analizando lo mejor para vos..."):
                # PROMPT HUMANIZADO: Le damos tu "alma" y estilo a la IA
                prompt_eddy = f"""
                Actuá como Eddy, un Personal Trainer de Élite argentino. 
                Tu estilo es motivador, directo y profesional, usando modismos como 'Tanque', 'Dale con todo', 'viste', 'metele mecha'.
                No seas un robot, hablá como un coach que cuida a su equipo de atletas. 
                Si te piden un menú o consejo, hacelo efectivo y con alimentos comunes en Argentina.
                
                Pregunta del atleta: {pregunta_atleta}
                
                Firmá siempre al final: Team Eddy - Software Elite.
                """
                
                try:
                    # Usamos el motor gemini-2.5-flash que ya confirmamos que te arranca
                    response = model.generate_content(prompt_eddy)
                    st.markdown(f"### 📢 Respuesta de Eddy:")
                    st.write(response.text)
                    
                    # Descontamos el crédito usando tu función de la línea 50
                    descontar_credito(st.session_state['usuario_actual'], total_creditos)
                   
                except Exception as e:
                    st.error(f"Se cortó la conexión con el servidor, Tanque. Probá de nuevo: {e}")
        else:
            st.warning("Escribime algo antes de enviar, Tanque. ¡Metele pilas!")
else:
    st.error("🚫 Ya agotaste tus consultas de prueba.")
    st.write("Para tener **30 consultas mensuales** y soporte constante del equipo, descargá tu Guía de Entrenamiento Elite.")

# ==========================================
# 7.5 MOTOR DE RUTINAS ELITE CON SOPORTE DE VARIANTES
# ==========================================
st.subheader(f"🏋️‍♂️ Plan de Entrenamiento ({nivel_experiencia})")

contenido_nivel = rutinas_elite.get(tipo_entreno, {}).get(nivel_experiencia, [])

if isinstance(contenido_nivel, dict):
    variante = st.selectbox("🔄 Seleccionar Variante de Rutina:", list(contenido_nivel.keys()))
    rutina_seleccionada = contenido_nivel[variante]
else:
    rutina_seleccionada = contenido_nivel

diccionario_rutinas = {}

if dias_entreno == 0:
    diccionario_rutinas["Descanso Activo"] = ["Día libre. Priorizar hidratación, sueño y caminatas ligeras."]
elif rutina_seleccionada:
    rutina_ajustada = rutina_seleccionada[:dias_entreno]
    for bloque in rutina_ajustada:
        titulo_dia = bloque[0]
        ejercicios_dia = bloque[1:]
        diccionario_rutinas[titulo_dia] = ejercicios_dia
else:
    diccionario_rutinas = {"Aviso": ["Rutina en construcción para esta disciplina y nivel."]}

st.button("› 👁️ VER RUTINA GENERADA", use_container_width=True, disabled=True)
if True:
        for dia_nombre, ejercicios in diccionario_rutinas.items():
            # st.markdown(f"**{dia_nombre}**")
            for e in ejercicios:
                # st.write(f"- {e}")
                pass

# ==========================================
# 8. MOTOR PDF Y VALIDADOR DE PAGOS ÚNICOS
# ==========================================

st.divider()
st.markdown("### 🔒 Descarga Protegida")

# Inicializamos el estado del pago si no existe

if "pago_validado" not in st.session_state:
    st.session_state.pago_validado = False

if not st.session_state.pago_validado:
    st.info("Para descargar tu Plan Elite, ingresa el número de operación de tu pago.")
    
    col_p, col_v = st.columns(2)
    with col_p:
        st.link_button("💳 REALIZAR PAGO ($10.000)", "https://mpago.la/27TKbMf", type="primary")
        st.caption("Al finalizar, busca el '#' seguido de 11 o 12 números en tu comprobante.")
        
    with col_v:
        nro_operacion = st.text_input("Ingresá el # de Operación (Ej: 156877505264):")
        if st.button("🔓 Validar y Descargar"):
            if nro_operacion:
                # 1. Limpiamos el texto por si el usuario copió el "#" o dejó espacios
                nro_limpio = nro_operacion.replace("#", "").strip()

                # --- LLAVE MAESTRA VIP ---
                if nro_limpio == "TANQUEVIP":
                    st.session_state.pago_validado = True
                    st.rerun()
                # -------------------------
              
                try:
                    # 2. Conexión secreta con Mercado Pago
                    token = st.secrets["MERCADO_PAGO_TOKEN"]
                    url_mp = f"https://api.mercadopago.com/v1/payments/{nro_limpio}"
                    headers = {"Authorization": f"Bearer {token}"}
                    
                    res = requests.get(url_mp, headers=headers)
                    if res.status_code == 200:
                        datos_pago = res.json()
                        status = datos_pago.get("status")
                        
                        if status == "approved":
                            # 3. Verificamos en Supabase si este ID ya fue "quemado"
                            check = supabase.table("pagos_verificados").select("*").eq("id_pago", nro_limpio).execute()
                            
                            if len(check.data) == 0:
                                supabase.table("pagos_verificados").insert({
                                    "id_pago": nro_limpio, 
                                    "usuario": st.session_state["usuario_actual"]
                                }).execute()
                                
                                st.session_state.pago_validado = True
                                st.rerun()
                            else:
                                st.error("❌ Este comprobante ya fue utilizado por otro usuario.")
                        else:
                            st.error(f"❌ El pago figura como: {status}. Debe estar 'approved'.")
                    else:
                        st.error("❌ Número de operación no encontrado en Mercado Pago.")
                except Exception as e:
                    # 4. AHORA EL ERROR HABLA: Nos dirá exactamente qué se rompió
                    st.error(f"Hubo un error técnico: {e}")
            else:
                st.warning("Por favor, ingresá el número de operación.")

if st.session_state.pago_validado:
    st.success("✅ ¡Pago validado! Tu Plan Elite ha sido desbloqueado.")
    
    # 1. Armamos los datos
    payload = {
        "n": nombre, "edad": edad, "estatura": estatura, "peso": peso_actual,
        "rfm": rfm, "k": cal_obj, "p": p_g_total, "c": c_g_total, "g": g_g_total,
        "m": diccionario_menus, "rutina": diccionario_rutinas, "meta": tipo_objetivo,
        "w": agua_total, "compras": lista_compras
    }

    # 2. TU SOLUCIÓN PROFESIONAL: Usamos container en lugar de empty()
    contenedor_seguro = st.container()
    
    with contenedor_seguro:
        # 3. Ruedita de carga para darle tiempo a tu motor de 900 líneas
        with st.spinner("⏳ Ensamblando tu PDF Elite Gold (esto puede tardar unos segundos)..."):
            try:
                from utils.pdf_generator_elite import build_pdf_elite_design
                pdf_elite = build_pdf_elite_design(payload, "logo_dorado.png" if os.path.exists("logo_dorado.png") else None)
                
                if pdf_elite:
                    # 4. El botón aparece DENTRO de la caja fuerte usando una Key única
                    st.download_button(
                        label="🏆 DESCARGAR PLAN ELITE GOLD",
                        data=pdf_elite,
                        file_name=f"Plan_Elite_{nombre.replace(' ', '_')}.pdf",
                        mime="application/pdf",
                        type="primary",
                        key="btn_descarga_pdf_final_seguro"
                    )
            except Exception as e:
                st.error(f"Error técnico en el servidor: {e}")