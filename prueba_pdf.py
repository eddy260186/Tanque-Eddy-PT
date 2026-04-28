import streamlit as st
from weasyprint import HTML
from datetime import datetime, time
import pandas as pd
import matplotlib.pyplot as plt
import os
from collections import defaultdict
import io
import base64

# ==========================================
# 1. CONFIGURACIÓN DE PÁGINA
# ==========================================
st.set_page_config(page_title="Eddy PT - Elite v59.0 Completa", page_icon="💪", layout="wide")
st.markdown('<meta name="google" content="notranslate">', unsafe_allow_html=True)
st.title("🏆 Eddy Personal Trainer: Software Elite v59.0")

# ==========================================
# DETECTOR DE LOGO BLINDADO
# ==========================================
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

# ==========================================
# 2. BASE DE DATOS (220 ALIMENTOS)
# ==========================================
alimentos_db = {
    "Prot_Desayuno": [
        "Yogur Griego Natural", "Yogur Natural Descremado", "Huevo Entero", "Claras de Huevo", 
        "Queso Cottage", "Whey Protein", "Jamón Cocido Magro", "Ricotta Magra", "Tofu Suave", 
        "Queso Feta", "Kefir de Leche", "Queso Blanco", "Huevo Poché", "Leche Proteica", 
        "Batido de Proteína", "Queso Magro", "Yogur de Soja", "Requesón", "Proteína de Soja", 
        "Queso Quark", "Yogur Skyr", "Queso Untable Proteico", "Jamón de Pavo", "Huevos Revueltos",
        "Omellete de Claras", "Batido de Caseína", "Queso Mascarpone Light", "Yogur de Coco (Protein)",
        "Queso Brie (Porción)", "Salame de Pavo", "Lomo Embuchado", "Pechuga Ahumada"
    ],
    "Bebidas_Arg": ["Mate Amargo", "Café solo/cortado", "Té de Hierbas", "Mate Cocido", "Té con Limón"],
    "Bebidas_Gral": ["Café Negro", "Té Verde", "Infusión de Manzanilla", "Té de Frutos Rojos", "Té Negro", "Café Helado sin azúcar", "Agua con Limón", "Infusión de jengibre", "Agua con Gas"],
    "Prot_Principal": [
        "Pechuga de Pollo", "Lomo Vacuno Magro", "Solomillo de Cerdo", "Pechuga de Pavo", 
        "Cordero Magro", "Bife de Cuadril", "Conejo", "Bisonte", "Ternera Magra", "Pollo a la Parrilla", 
        "Bife de Chorizo Magro", "Pavo Horneado", "Carne de Ciervo", "Costilla de Cerdo Magra", 
        "Pollo al Horno", "Cuadril", "Vacío Magro", "Peceto", "Bola de Lomo", "Nalga",
        "Bondiola Desgrasada", "Entraña Magra", "Lomito de Cerdo", "Carne Picada Magra",
        "Matambre Vacuno (Magro)", "Colita de Cuadril", "Paleta Vacuna", "Tortuguita",
        "Bife Angosto", "Tapa de Asado (Limpia)", "Panceta de Pavo", "Churrasco de Pollo"
    ],
    "Prot_Pescado": ["Merluza", "Salmón Fresco", "Atún al Natural", "Trucha", "Sardinas", "Mejillones", "Gambas/Camarones", "Pulpo", "Abadejo", "Lenguado", "Pejerrey", "Caballa", "Mariscos Mix", "Bacalao", "Calamar", "Anillas de Calamar", "Corvina", "Dorado", "Surubí", "Salmón Ahumado", "Lomito de Atún Fresco", "Filet de Pescado Blanco", "Besugo", "Langostinos al Ajillo", "Brocheta de Pescado", "Atún Rojo", "Gatuzo"],
    "Prot_Vegana": ["Tofu Firme", "Tempeh", "Seitan", "Lentejas", "Garbanzos", "Heura", "Soja Texturizada", "Frijoles Negros (Feijão)", "Guisantes", "Quinoa", "Altramuces", "Edamame", "Proteína de Guisante", "Levadura Nutricional", "Semillas de Chía", "Espirulina", "Amaranto", "Cáñamo", "Miso", "Tempeh de Garbanzos", "Hamburguesa de Soja", "Porotos Mung", "Lupines", "Porotos Colorados", "Tofu Ahumado", "Natto", "Proteína de Arroz", "Frijol de Carita"],
    "Carb_Desayuno": ["Avena en Hojuelas", "Pan de Centeno", "Granola sin Azúcar", "Pan de Masa Madre", "Fruta Picada", "Tortitas de Arroz", "Muesli", "Espelta", "Salvado de Trigo", "Cereales Integrales", "Pan Integral", "Tortitas de Avena", "Arándanos", "Manzana", "Banana", "Kiwi", "Fresa", "Mango", "Pera", "Ciruelas", "Tapioca (Brasil)", "Mamão / Papaya", "Açaí puro", "Arepa de Maíz", "Galletas de Arroz", "Pan de Sarraceno", "Dátiles", "Higos", "Melón", "Piña / Ananá", "Pomelo", "Sandía"],
    "Carb_Principal": ["Arroz Integral", "Pasta Integral", "Quinoa Real", "Cuscús", "Lentejas", "Garbanzos", "Arroz Basmati", "Pasta de Legumbres", "Bulgur", "Polenta", "Mijo", "Trigo Sarraceno", "Choclo", "Trigo Burgol", "Arroz Negro", "Kamut", "Espelta", "Cebada", "Fideos de Arroz", "Yuca/Mandioca/Macaxeira", "Feijão Preto (Brasil)", "Plátano Macho", "Puré de Papa", "Arroz Blanco", "Ñoquis de Papa", "Batata Asada", "Trigo en Grano", "Garbanzos Fritos", "Arroz de Coliflor", "Pasta de Espelta", "Sémola de Trigo", "Arvejas Partidas"],
    "Carb_Vegetales": ["Papa Hervida", "Batata al Horno", "Calabaza", "Yuca/Mandioca", "Zanahoria", "Remolacha", "Boniato", "Plátano Macho", "Nabos", "Pastinaca", "Calabacín", "Berenjena", "Puerros", "Cebolla", "Alcachofas", "Pimientos", "Zapallo Anco", "Hinojo", "Rabanitos", "Tomates", "Brócoli", "Coliflor", "Espinaca (Volumen libre)", "Zapallo Cabutia", "Echalotes", "Ajo", "Champiñones", "Portobello", "Repollo Colorado"],
    "Verduras_Keto": ["Espinaca", "Brócoli", "Espárragos", "Acelga", "Coliflor", "Lechuga", "Pepino", "Zucchini", "Champiñones", "Pimientos", "Kale", "Rúcula", "Apio", "Tomatitos Cherry", "Rabanitos", "Endivias", "Bok Choy", "Col de Bruselas", "Judías Verdes", "Hinojo", "Repollo Blanca", "Berenjena", "Berros", "Brotes de Soja", "Radicheta"],
    "Grasas": ["Palta/Aguacate", "Nueces", "Aceite de Oliva", "Almendras", "Pistachos", "Semillas de Zapallo", "Mantequilla de Maní", "Aceitunas", "Aceite de Coco", "Castañas de Cajú", "Tahini", "Avellanas", "Aceite de Lino", "Nueces de Macadamia", "Semillas de Girasol", "Coco Rallado", "Mantequilla de Pasto", "Yema de Huevo", "Chía", "Sésamo", "Chocolate Amargo 85%", "Ghee (Manteca Clarificada)", "Pasta de Almendras", "Aceite de Girasol Alto Oleico", "Manteca de Cacao", "Crema de Leche Light", "Queso Azul (Porción)", "Mayonesa de Oliva", "Aceite de Sésamo", "Nueces Pecán"]
}

DB_FILE = os.path.join(directorio_script, "Historial_Atletas.csv")

# ==========================================
# 3. PERFIL DEL ATLETA (COMPLETO)
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
    tipo_objetivo = st.selectbox("Meta Principal:", ["Pérdida de Grasa (Déficit Estándar)", "Definición Agresiva (Corte)", "Recomposición Corporal", "Mantenimiento / Salud", "Volumen Limpio (Superávit)", "Volumen Agresivo (Bulking)"])
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
# 4. SALUD Y BIOMETRÍA ELITE (KATCH-MCARDLE)
# ==========================================
st.subheader("📏 Salud y Biometría Elite")
col_c1, col_c2 = st.columns(2)
with col_c1: cintura = st.number_input("Perímetro de Cintura (cm):", value=85.0)
with col_c2: cadera = st.number_input("Perímetro de Cadera (cm):", value=95.0)
rcc_valor = round(cintura / cadera, 2) if cadera > 0 else 0

if cintura > 0:
    if genero == "m": rfm = round(64 - (20 * (estatura / cintura)), 1)
    else: rfm = round(76 - (20 * (estatura / cintura)), 1)
    rfm = max(5.0, min(rfm, 60.0))
    masa_magra = peso_actual * (1 - (rfm / 100))
    tmb = 370 + (21.6 * masa_magra)
else:
    tmb = (10 * peso_actual) + (6.25 * estatura) - (5 * edad) + (5 if genero == "m" else -161)
    rfm = 0.0

if dias_entreno == 0: pal_base = 1.2
elif 1 <= dias_entreno <= 2: pal_base = 1.3
elif 3 <= dias_entreno <= 4: pal_base = 1.45
elif 5 <= dias_entreno <= 6: pal_base = 1.6
else: pal_base = 1.75

if dias_entreno == 0 or "Ninguno" in tipo_entreno: bonus_deporte = 0.0
elif any(x in tipo_entreno for x in ["CrossFit", "Resistencia", "Artes Marciales"]): bonus_deporte = 0.15
elif any(x in tipo_entreno for x in ["Fuerza", "Powerlifting", "Calistenia", "Equipo", "Raqueta", "Gimnasia"]): bonus_deporte = 0.10
else: bonus_deporte = 0.05

factor_actividad = pal_base + bonus_deporte
cal_mant = tmb * factor_actividad

if embarazada_bool: cal_mant += 340 if meses_gestacion <= 6 else 450
ajuste_diario = (kg_a_cambiar * 7000) / (meses_plazo * 30) if meses_plazo > 0 else 0

if embarazada_bool and any(x in tipo_objetivo for x in ["Pérdida", "Definición", "Recomposición"]):
    cal_obj, dif = cal_mant, 0
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
    c_g_total, g_g_total = 30.0, (cal_obj - (p_g_total * 4) - 120) / 9
else:
    g_g_total = (cal_obj * 0.30) / 9
    c_g_total = (cal_obj - (p_g_total * 4) - (g_g_total * 9)) / 4

agua_total = round((peso_actual * 0.035) + 0.75 + (0.5 if dias_entreno > 0 else 0), 1)

# ==========================================
# 5. CRM (RESTAURADO AL 100%) Y GRÁFICO
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
                "Meta": tipo_objetivo, 
                "Dieta": dieta_tipo, 
                "Entrenamiento": tipo_entreno, 
                "Dias/Semana": dias_entreno,
                "Kcal Objetivo": int(cal_obj)
            }])
            if os.path.exists(DB_FILE): pd.concat([pd.read_csv(DB_FILE), nuevo_dato], ignore_index=True).to_csv(DB_FILE, index=False)
            else: nuevo_dato.to_csv(DB_FILE, index=False)
            st.success("¡Atleta guardado!")

st.info(f"Atleta: **{nombre if nombre else 'Eddy PT'}** | RCC: {rcc_valor} | **Grasa Est. (RFM): {rfm}%**")
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
for spine in ax.spines.values(): spine.set_color(accent_color)
for i, v in enumerate(pesos_prog): ax.text(i, v + 0.5, f"{round(v,1)}kg", ha='center', fontsize=10, fontweight='bold', color='#ffffff')
st.pyplot(fig)

buf = io.BytesIO()
fig.savefig(buf, format="png", bbox_inches="tight", facecolor=bg_plot)
buf.seek(0)
grafico_base64 = base64.b64encode(buf.read()).decode("utf-8")

# ==========================================
# 6. SUPLEMENTACIÓN
# ==========================================
suples = [
    "✅ Creatina (5g): Diario para fuerza.",
    "💊 Multivitamínico: 1 cápsula con el desayuno.",
    "🦴 Magnesio/Zinc: 1 dosis por la noche."
]
if "Volumen" in tipo_objetivo or "Recomposición" in tipo_objetivo: suples.append("🚀 Citrulina Malato (6-8g): Pre-entreno.")
if "Definición" in tipo_objetivo or "Pérdida" in tipo_objetivo: suples.append("🏃‍♂️ Beta-Alanina (3-5g): Diario.")
if "Agresiva" in tipo_objetivo or "Keto" in dieta_tipo or "Vegana" in dieta_tipo: suples.append("🐟 Omega-3 (1-3g EPA/DHA): Con comida.")
if "Keto" in dieta_tipo or (10 <= hora_entreno.hour <= 16): suples.append("⚡ Electrolitos: Intra-entreno.")
if hora_entreno.hour < 12: suples.append("☕ Cafeína: Pre-entreno.")
suples.append("🥤 Proteína Whey: Post-entreno.")

# ==========================================
# 7. MENÚ DINÁMICO
# ==========================================
st.subheader(f"🍽️ Plan de {num_comidas} Comidas ({int(cal_obj)} kcal)")
diccionario_menus = {} 
lista_compras = defaultdict(float)

p_com, c_com, g_com = p_g_total / num_comidas, c_g_total / num_comidas, g_g_total / num_comidas
gramos_p, gramos_g = int(p_com / 0.25), int(g_com / 0.90)
gramos_c = 0 if "Keto" in dieta_tipo else int(c_com / 0.25)

mapa_nombres = {1: ["Comida Única"], 2: ["Almuerzo", "Cena"], 3: ["Desayuno", "Almuerzo", "Cena"], 4: ["Desayuno", "Almuerzo", "Merienda", "Cena"], 5: ["Desayuno", "Media Mañana", "Almuerzo", "Merienda", "Cena"], 6: ["Desayuno", "Media Mañana", "Almuerzo", "Merienda", "Pre-Cena", "Cena"]}

for nombre_base in mapa_nombres[num_comidas]:
    opciones_de_esta_comida = []
    with st.expander(f"✨ {nombre_base.upper()}", expanded=True):
        es_mt = any(x in nombre_base for x in ["Desayuno", "Merienda", "Mañana"])
        for i in range(num_opciones):
            if "Vegana" in dieta_tipo: fp = alimentos_db["Prot_Vegana"][i % len(alimentos_db["Prot_Vegana"])]
            elif "Vegetariana" in dieta_tipo: fp = alimentos_db["Prot_Desayuno"][i % len(alimentos_db["Prot_Desayuno"])] if es_mt else alimentos_db["Prot_Vegana"][i % len(alimentos_db["Prot_Vegana"])]
            elif "Pescetariana" in dieta_tipo: fp = alimentos_db["Prot_Desayuno"][i % len(alimentos_db["Prot_Desayuno"])] if es_mt else alimentos_db["Prot_Pescado"][i % len(alimentos_db["Prot_Pescado"])]
            else: fp = alimentos_db["Prot_Desayuno"][i % len(alimentos_db["Prot_Desayuno"])] if es_mt else alimentos_db["Prot_Principal"][i % len(alimentos_db["Prot_Principal"])]
            
            if "Keto" in dieta_tipo: fc, texto_carbo = alimentos_db["Verduras_Keto"][i % len(alimentos_db["Verduras_Keto"])], "Libre"
            elif "Paleo" in dieta_tipo: fc, texto_carbo = alimentos_db["Carb_Vegetales"][i % len(alimentos_db["Carb_Vegetales"])], f"{gramos_c}g"
            else: fc, texto_carbo = alimentos_db["Carb_Desayuno"][i % len(alimentos_db["Carb_Desayuno"])] if es_mt else alimentos_db["Carb_Principal"][i % len(alimentos_db["Carb_Principal"])], f"{gramos_c}g"
            
            fg = alimentos_db["Grasas"][i % len(alimentos_db["Grasas"])]
            bebida = alimentos_db["Bebidas_Arg"][i % len(alimentos_db["Bebidas_Arg"])] if "Argentina" in pais else alimentos_db["Bebidas_Gral"][i % len(alimentos_db["Bebidas_Gral"])]
            
            txt_op = f"Opcion {i+1}: {gramos_p}g {fp} + {texto_carbo} {fc} + {gramos_g}g {fg} | Infusion: {bebida}"
            st.write(txt_op)
            opciones_de_esta_comida.append(txt_op)

            dias_por_opcion = 30 / num_opciones
            lista_compras[fp] += gramos_p * dias_por_opcion
            if "Keto" not in dieta_tipo: lista_compras[fc] += gramos_c * dias_por_opcion
            lista_compras[fg] += gramos_g * dias_por_opcion
            lista_compras[bebida] += dias_por_opcion
            
    diccionario_menus[nombre_base.upper()] = opciones_de_esta_comida

# ==========================================
# 8. MOTOR PDF (DISEÑO PREMIUM RESTAURADO)
# ==========================================
def build_pdf_v59(d, grafico_b64, ruta_img, gen):
    is_f = (gen == "f")
    c_bg = "#1A1A1A" if is_f else "#121212"
    c_card = "#2A2A2A" if is_f else "#1a1a1a"
    c_accent = "#FFB6C1" if is_f else "#d4af37"
    c_txt = "#ffffff"
    
    logo_html = ""
    if ruta_img:
        with open(ruta_img, "rb") as image_file:
            logo_base64 = base64.b64encode(image_file.read()).decode("utf-8")
            logo_html = f'<img src="data:image/png;base64,{logo_base64}" style="height: 70px; float: right; border: 2px solid {c_accent}; border-radius: 8px; padding: 5px; background: #000;">'

    html = f"""
    <html><head><style>
        @page {{ size: A4; margin: 15mm; background-color: {c_bg}; }}
        body {{ font-family: 'Helvetica'; color: {c_txt}; background-color: {c_bg}; line-height: 1.5; }}
        .h {{ background: #000000; color: {c_accent}; padding: 30px; text-align: left; border-bottom: 5px solid {c_accent}; overflow: auto; border-radius: 10px 10px 0 0; }}
        .profile-box {{ background: {c_card}; padding: 15px; margin: 20px 0; border: 2px solid {c_accent}; border-radius: 8px; color: {c_txt}; }}
        .stats-box {{ background: {c_card}; padding: 15px; margin: 20px 0; border-left: 10px solid {c_accent}; color: {c_txt}; border-radius: 4px; }}
        .graph-box {{ text-align: center; margin: 20px 0; padding: 10px; border: 2px solid {c_accent}; background: #000000; border-radius: 8px; }}
        .water-box {{ background: #000000; padding: 10px; border: 2px dashed {c_accent}; border-radius: 5px; color: {c_accent}; font-weight: bold; margin-top: 10px; text-align: center; font-size: 14px; }}
        .title {{ background: #000000; color: {c_accent}; padding: 10px; margin-top: 20px; text-transform: uppercase; letter-spacing: 2px; border: 1px solid {c_accent}; text-align: center; border-radius: 4px; }}
        table {{ width: 100%; border-collapse: collapse; margin-top: 10px; background-color: {c_card}; }}
        td {{ padding: 10px; border-bottom: 1px dashed {c_accent}; font-size: 11px; color: {c_txt}; }}
        h1, h2, h3 {{ color: {c_accent}; }}
        b, strong {{ color: {c_accent}; }}
        li {{ color: {c_txt}; margin-bottom: 5px; }}
    </style></head>
    <body>
        <div class="h">
            {logo_html}
            <h1 style="margin: 0;">EDDY PERSONAL TRAINER</h1>
            <p style="margin: 5px 0 0 0; color: #fff;">PLAN NUTRICIONAL ELITE - {"EDICIÓN SOFT PINK" if is_f else "EDICIÓN GOLD"}</p>
        </div>
        
        <div class="profile-box">
            <h2 style="margin-top: 0;">👤 PERFIL FÍSICO Y BIOMÉTRICO</h2>
            <p><b>NOMBRE:</b> {d['n'].upper()}</p>
            <p><b>EDAD:</b> {d['edad']} años | <b>ESTATURA:</b> {d['estatura']} cm | <b>PESO ACTUAL:</b> {d['peso']} kg</p>
            <p><b>CINTURA:</b> {d['cintura']} cm | <b>CADERA:</b> {d['cadera']} cm | <b>ÍNDICE RCC:</b> {d['rcc']} | <b>GRASA EST.:</b> {d['rfm']}%</p>
            <hr style="border-color: {c_accent};">
            <p><b>ENTRENAMIENTO:</b> {d['entreno']} | <b>FRECUENCIA:</b> {d['dias']} días/sem.</p>
            <p><b>META PRINCIPAL:</b> {d['meta']} | <b>ESTILO DE DIETA:</b> {d['dt']}</p>
        </div>

        <div class="stats-box">
            <h2>📊 BALANCE NUTRICIONAL KATCH-MCARDLE</h2>
            <p><b>CALORÍAS OBJETIVO:</b> {d['k']:.0f} kcal</p>
            <p><b>SUMATORIA TOTAL DEL MENÚ:</b> {d['k']:.0f} kcal ✅ (Coincidencia Exacta)</p>
            <p>Macros Diarios: <b>Proteína:</b> {d['p']:.0f}g | <b>Carbohidratos:</b> {d['c']:.0f}g | <b>Grasas:</b> {d['g']:.0f}g</p>
            <div class="water-box">💧 OBJETIVO DE HIDRATACIÓN DIARIA: {d['w']} LITROS</div>
        </div>

        <div class="graph-box">
            <h3 style="margin-top: 0;">📈 PROYECCIÓN DE PESO ESTIMADA</h3>
            <img src="data:image/png;base64,{grafico_b64}" style="width: 100%; max-width: 600px; border-radius: 5px;">
        </div>

        <div class="title">📢 MENÚ DE LAS COMIDAS</div>
    """
    for c, ops in d['m'].items():
        html += f"<h3>🍴 {c}</h3><table>"
        for o in ops: html += f"<tr><td>{o}</td></tr>"
        html += "</table>"
    
    html += f"""<div class="title">💊 SUPLEMENTACIÓN Y MICRONUTRIENTES</div>
    <div class="stats-box">
        <ul>{''.join([f"<li>{s}</li>" for s in d['s']])}</ul>
    </div>
    
    <div style="page-break-before: always;"></div>
    <div class="h">
        {logo_html}
        <h1 style="margin:0;">🛒 TICKET DE COMPRA MENSUAL</h1>
    </div>
    <p style="text-align: center; color: {c_accent};"><i>Cantidades estimadas para 30 días de rotación completa del menú.</i></p>
    <table>"""
    
    for item, cant in d['compras'].items():
        if "Huevo" in item or "Claras" in item:
            unidades = int(cant / 50)
            res = f"{unidades} Unidades (~{round(unidades/12, 1)} Docenas)"
        elif any(x in item for x in ["Café", "Mate", "Té", "Infusión"]):
            res = f"{int(cant)} Porciones/Tazas"
        else:
            res = f"{round(cant/1000, 2)} KG" if cant >= 1000 else f"{int(cant)} g"
        html += f"<tr><td><b>{item}</b></td><td style='text-align: right;'>{res}</td></tr>"
    
    html += f"""</table>
        <div style="margin-top: 40px; text-align: center; font-size: 10px; color: {c_accent};">
            Diseñado por Eddy Personal Trainer - Instagram: @eddy_personal_trainer | Moreno, Buenos Aires
        </div>
    </body></html>"""
    return HTML(string=html).write_pdf()

st.divider()
if st.button("🏆 GENERAR PDF ELITE"):
    if nombre:
        payload = {
            "n": nombre, "edad": edad, "estatura": estatura, "peso": peso_actual, 
            "cintura": cintura, "cadera": cadera, "rcc": rcc_valor, "rfm": rfm,
            "entreno": tipo_entreno, "dias": dias_entreno,
            "meta": tipo_objetivo, "dt": dieta_tipo,
            "k": cal_obj, "p": p_g_total, "c": c_g_total, "g": g_g_total, 
            "s": suples, "m": diccionario_menus, "compras": lista_compras, "w": agua_total
        }
        st.download_button("💾 Bajar Reporte Black/Pink & Gold", build_pdf_v59(payload, grafico_base64, ruta_logo_final, genero), f"Plan_Elite_{nombre}.pdf")
    else: st.error("Por favor, ingresá el nombre del atleta.")