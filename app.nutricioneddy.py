import requests
import streamlit as st
from weasyprint import HTML
from datetime import datetime, time
import pandas as pd
import matplotlib.pyplot as plt
import os
from collections import defaultdict
import io
import base64

from database.supabase_mgr import init_supabase
from utils.biometria import calcular_biometria
from utils.pdf_generator import build_pdf_v60_7
from data.alimentos import alimentos_db
from data.ejercicios import ejercicios_db, rutinas_elite

# ==========================================
# 1. CONFIGURACIÓN DE PÁGINA
# ==========================================
st.set_page_config(page_title="Eddy PT - Elite v60.7", page_icon="💪", layout="wide")
st.markdown('<meta name="google" content="notranslate">', unsafe_allow_html=True)

# ==========================================
# 2. SISTEMA DE USUARIOS (LOGIN / REGISTRO)
# ==========================================
supabase = init_supabase()

if "usuario_actual" not in st.session_state:
    st.session_state["usuario_actual"] = None

# Si NO hay nadie logueado, mostramos solo la pantalla de entrada
if st.session_state["usuario_actual"] is None:
    st.title("🏆 Eddy Personal Trainer: Portal Elite")
    st.subheader("🔐 Acceso Exclusivo")
    tab_login, tab_registro = st.tabs(["Iniciar Sesión", "Crear Cuenta Nueva"])
    
    with tab_login:
        email_login = st.text_input("Correo electrónico", key="log_email")
        pass_login = st.text_input("Contraseña", type="password", key="log_pass")
        if st.button("Entrar", type="primary"):
            try:
                respuesta = supabase.auth.sign_in_with_password({"email": email_login, "password": pass_login})
                st.session_state["usuario_actual"] = respuesta.user.email
                st.success("¡Acceso concedido! Cargando tu panel...")
                st.rerun()
            except Exception as e:
                st.error("Error: Correo o contraseña incorrectos.")
                
    with tab_registro:
        st.info("Crea tu cuenta gratis para poder generar y guardar tus rutinas.")
        email_reg = st.text_input("Correo electrónico", key="reg_email")
        pass_reg = st.text_input("Contraseña (mínimo 6 caracteres)", type="password", key="reg_pass")
        if st.button("Registrarme", type="primary"):
            try:
                respuesta = supabase.auth.sign_up({"email": email_reg, "password": pass_reg})
                st.success("✅ ¡Cuenta creada con éxito! Ahora puedes iniciar sesión en la pestaña de al lado.")
            except Exception as e:
                st.error("Error al crear la cuenta. Verifica que la contraseña tenga al menos 6 caracteres.")
                
    st.stop() # Frena la app acá si no están logueados

# ==========================================
# SI LLEGA ACÁ, ESTÁ LOGUEADO. MOSTRAMOS LA APP NORMAL
# ==========================================
st.title("🏆 Eddy Personal Trainer: Software Elite v60.7")

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
        st.success("✅ Logo DETECTADO")
        st.image(ruta_logo_final, width=150)
    else:
        st.error("❌ Logo NO detectado")
    st.divider()
    
    # Botón para cerrar sesión
    st.success(f"👤 Conectado:\n{st.session_state['usuario_actual']}")
    if st.button("Cerrar Sesión"):
        supabase.auth.sign_out()
        st.session_state["usuario_actual"] = None
        st.rerun()
    st.divider()

DB_FILE = os.path.join(directorio_script, "Historial_Atletas.csv")

# ==========================================
# 3. PERFIL DEL ATLETA 
# ==========================================
with st.sidebar:
    st.header("👤 Perfil del Atleta")
    nombre = st.text_input("Nombre Completo:")
    pais = st.text_input("País de Residencia:", value="Argentina")
    edad = st.number_input("Edad:", min_value=10, value=30)
    
    genero_seleccion = st.selectbox("Género:", ["m ", "f "])
    genero = genero_seleccion.strip()
    
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
    if st.button("💾 Guardar Atleta (CRM)"):
        if nombre:
            nuevo_dato = pd.DataFrame([{
                "Fecha": datetime.now().strftime("%Y-%m-%d %H:%M"), 
                "Nombre": nombre, 
                "Pais": pais, 
                "Peso Actual (kg)": peso_actual, 
                "Grasa Est. (%)": rfm, 
                "Nivel": nivel_experiencia,
                "Meta": tipo_objetivo, 
                "Dieta": dieta_tipo, 
                "Entrenamiento": tipo_entreno, 
                "Dias/Semana": dias_entreno, 
                "Kcal Objetivo": int(cal_obj)
            }])
            if os.path.exists(DB_FILE): 
                historico = pd.read_csv(DB_FILE)
                historico_actualizado = pd.concat([historico, nuevo_dato], ignore_index=True)
                historico_actualizado.to_csv(DB_FILE, index=False)
            else: 
                nuevo_dato.to_csv(DB_FILE, index=False)
            st.success("¡Atleta guardado!")

st.info(f"Atleta: **{nombre if nombre else 'Eddy PT'}** | RCC: {rcc_valor} | **Grasa Est. (RFM): {rfm}%** | Nivel: {nivel_experiencia}")
col_r1, col_r2, col_r3, col_r4 = st.columns(4)
col_r1.metric("Mantenimiento", f"{int(cal_mant)} kcal")
col_r2.metric("Ajuste Diario", f"{int(dif)} kcal", delta=int(dif))
col_r3.metric("Objetivo Final", f"{int(cal_obj)} kcal")
col_r4.metric("💧 Agua (Con Entreno)", f"{agua_total} L")

kg_mes_real = (dif * 30) / 7000 
fechas_reales = [(datetime.now() + pd.DateOffset(months=i)).strftime("%d/%m/%Y") for i in range(int(meses_plazo) + 1)]
pesos_prog = [peso_actual + (kg_mes_real * i) for i in range(len(fechas_reales))]

fig, ax = plt.subplots(figsize=(10, 3))
fig.patch.set_facecolor(bg_plot)
ax.set_facecolor(bg_plot)
ax.bar(fechas_reales, pesos_prog, color=accent_color)
ax.tick_params(colors=accent_color)
for spine in ax.spines.values(): 
    spine.set_color(accent_color)
for i, v in enumerate(pesos_prog): 
    ax.text(i, v + 0.5, f"{round(v,1)}kg", ha='center', fontsize=10, fontweight='bold', color='#ffffff')
st.pyplot(fig)

buf = io.BytesIO()
fig.savefig(buf, format="png", bbox_inches="tight", facecolor=bg_plot)
buf.seek(0)
grafico_base64 = base64.b64encode(buf.read()).decode("utf-8")

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
    with st.expander(f"✨ {nombre_base.upper()}", expanded=True):
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
            st.write(txt_op)
            opciones_de_esta_comida.append(txt_op)

            dias_por_opcion = 30 / num_opciones
            lista_compras[fp] += gramos_p * dias_por_opcion
            if "Keto" not in dieta_tipo: 
                lista_compras[fc] += gramos_c * dias_por_opcion
            lista_compras[fg] += gramos_g * dias_por_opcion
            lista_compras[bebida] += dias_por_opcion
            
    diccionario_menus[nombre_base.upper()] = opciones_de_esta_comida

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

with st.expander("👁️ VER RUTINA GENERADA", expanded=True):
    for dia_nombre, ejercicios in diccionario_rutinas.items():
        st.markdown(f"**{dia_nombre}**")
        for e in ejercicios:
            st.write(f"- {e}")

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

# --- PANTALLA DE DESCARGA LIBERADA ---
if st.session_state.pago_validado:
    st.balloons()
    st.success("✅ ¡Pago validado! Tu Plan Elite ha sido desbloqueado.")
    
    if nombre:
        payload = {
            "n": nombre, "edad": edad, "estatura": estatura, "peso": peso_actual, 
            "cintura": cintura, "cadera": cadera, "rcc": rcc_valor, "rfm": rfm,
            "nivel": nivel_experiencia, "entreno": tipo_entreno, "dias": dias_entreno,
            "meta": tipo_objetivo, "dt": dieta_tipo,
            "k": cal_obj, "p": p_g_total, "c": c_g_total, "g": g_g_total, 
            "s": suples, "m": diccionario_menus, "compras": lista_compras, "w": agua_total,
            "rutina": diccionario_rutinas
        }
        st.download_button(
            label="📥 DESCARGAR MI PLAN ELITE (PDF)", 
            data=build_pdf_v60_7(payload, grafico_base64, ruta_logo_final, genero), 
            file_name=f"Plan_Elite_{nombre}.pdf",
            mime="application/pdf",
            type="primary"
        )
    else:
        st.warning("⚠️ Escribe el nombre del atleta para generar el archivo.")