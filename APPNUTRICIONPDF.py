import streamlit as st
from fpdf import FPDF
from datetime import datetime, time
import pandas as pd
import matplotlib.pyplot as plt
import os
from collections import defaultdict

# ==========================================
# 1. CONFIGURACIÓN DE PÁGINA Y CRM
# ==========================================
st.set_page_config(
    page_title="Eddy PT - Diseño Premium v56", 
    page_icon="💪", 
    layout="wide"
)
st.markdown('<meta name="google" content="notranslate">', unsafe_allow_html=True)
st.title("💪 Eddy Personal Trainer: Software Elite v56.0 (Expandido)")

DB_FILE = "Historial_Atletas.csv"

# ==========================================
# 2. BASE DE DATOS MAESTRA (220 ALIMENTOS)
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
    "Bebidas_Arg": [
        "Mate Amargo", "Café solo/cortado", "Té de Hierbas", "Mate Cocido", "Té con Limón"
    ],
    "Bebidas_Gral": [
        "Café Negro", "Té Verde", "Infusión de Manzanilla", "Té de Frutos Rojos", "Té Negro",
        "Café Helado sin azúcar", "Agua con Limón", "Infusión de jengibre", "Agua con Gas"
    ],
    "Prot_Principal": [
        "Pechuga de Pollo", "Lomo Vacuno Magro", "Solomillo de Cerdo", "Pechuga de Pavo", 
        "Cordero Magro", "Bife de Cuadril", "Conejo", "Bisonte", "Ternera Magra", "Pollo a la Parrilla", 
        "Bife de Chorizo Magro", "Pavo Horneado", "Carne de Ciervo", "Costilla de Cerdo Magra", 
        "Pollo al Horno", "Cuadril", "Vacío Magro", "Peceto", "Bola de Lomo", "Nalga",
        "Bondiola Desgrasada", "Entraña Magra", "Lomito de Cerdo", "Carne Picada Magra",
        "Matambre Vacuno (Magro)", "Colita de Cuadril", "Paleta Vacuna", "Tortuguita",
        "Bife Angosto", "Tapa de Asado (Limpia)", "Panceta de Pavo", "Churrasco de Pollo"
    ],
    "Prot_Pescado": [
        "Merluza", "Salmón Fresco", "Atún al Natural", "Trucha", "Sardinas", "Mejillones", 
        "Gambas/Camarones", "Pulpo", "Abadejo", "Lenguado", "Pejerrey", "Caballa", 
        "Mariscos Mix", "Bacalao", "Calamar", "Anillas de Calamar", "Corvina", "Dorado", 
        "Surubí", "Salmón Ahumado", "Lomito de Atún Fresco", "Filet de Pescado Blanco",
        "Besugo", "Langostinos al Ajillo", "Brocheta de Pescado", "Atún Rojo", "Gatuzo"
    ],
    "Prot_Vegana": [
        "Tofu Firme", "Tempeh", "Seitan", "Lentejas", "Garbanzos", "Heura", "Soja Texturizada", 
        "Frijoles Negros (Feijão)", "Guisantes", "Quinoa", "Altramuces", "Edamame", 
        "Proteína de Guisante", "Levadura Nutricional", "Semillas de Chía", "Espirulina", 
        "Amaranto", "Cáñamo", "Miso", "Tempeh de Garbanzos", "Hamburguesa de Soja", "Porotos Mung",
        "Lupines", "Porotos Colorados", "Tofu Ahumado", "Natto", "Proteína de Arroz", "Frijol de Carita"
    ],
    "Carb_Desayuno": [
        "Avena en Hojuelas", "Pan de Centeno", "Granola sin Azúcar", "Pan de Masa Madre", 
        "Fruta Picada", "Tortitas de Arroz", "Muesli", "Espelta", "Salvado de Trigo", 
        "Cereales Integrales", "Pan Integral", "Tortitas de Avena", "Arándanos", "Manzana", 
        "Banana", "Kiwi", "Fresa", "Mango", "Pera", "Ciruelas",
        "Tapioca (Brasil)", "Mamão / Papaya", "Açaí puro", "Arepa de Maíz", "Galletas de Arroz",
        "Pan de Sarraceno", "Dátiles", "Higos", "Melón", "Piña / Ananá", "Pomelo", "Sandía"
    ],
    "Carb_Principal": [
        "Arroz Integral", "Pasta Integral", "Quinoa Real", "Cuscús", "Lentejas", "Garbanzos", 
        "Arroz Basmati", "Pasta de Legumbres", "Bulgur", "Polenta", "Mijo", "Trigo Sarraceno", 
        "Choclo", "Trigo Burgol", "Arroz Negro", "Kamut", "Espelta", "Cebada", "Fideos de Arroz", 
        "Yuca/Mandioca/Macaxeira", "Feijão Preto (Brasil)", "Plátano Macho", "Puré de Papa", "Arroz Blanco",
        "Ñoquis de Papa", "Batata Asada", "Trigo en Grano", "Garbanzos Fritos", "Arroz de Coliflor",
        "Pasta de Espelta", "Sémola de Trigo", "Arvejas Partidas"
    ],
    "Carb_Vegetales": [
        "Papa Hervida", "Batata al Horno", "Calabaza", "Yuca/Mandioca", "Zanahoria", 
        "Remolacha", "Boniato", "Plátano Macho", "Nabos", "Pastinaca", "Calabacín", 
        "Berenjena", "Puerros", "Cebolla", "Alcachofas", "Pimientos", "Zapallo Anco", 
        "Hinojo", "Rabanitos", "Tomates", "Brócoli", "Coliflor", "Espinaca (Volumen libre)",
        "Zapallo Cabutia", "Echalotes", "Ajo", "Champiñones", "Portobello", "Repollo Colorado"
    ],
    "Verduras_Keto": [
        "Espinaca", "Brócoli", "Espárragos", "Acelga", "Coliflor", "Lechuga", "Pepino", 
        "Zucchini", "Champiñones", "Pimientos", "Kale", "Rúcula", "Apio", "Tomatitos Cherry", 
        "Rabanitos", "Endivias", "Bok Choy", "Col de Bruselas", "Judías Verdes", "Hinojo", 
        "Repollo Blanca", "Berenjena", "Berros", "Brotes de Soja", "Radicheta"
    ],
    "Grasas": [
        "Palta/Aguacate", "Nueces", "Aceite de Oliva", "Almendras", "Pistachos", 
        "Semillas de Zapallo", "Mantequilla de Maní", "Aceitunas", "Aceite de Coco", 
        "Castañas de Cajú", "Tahini", "Avellanas", "Aceite de Lino", "Nueces de Macadamia", 
        "Semillas de Girasol", "Coco Rallado", "Mantequilla de Pasto", "Yema de Huevo", 
        "Chía", "Sésamo", "Chocolate Amargo 85%", "Ghee (Manteca Clarificada)", "Pasta de Almendras",
        "Aceite de Girasol Alto Oleico", "Manteca de Cacao", "Crema de Leche Light",
        "Queso Azul (Porción)", "Mayonesa de Oliva", "Aceite de Sésamo", "Nueces Pecán"
    ]
}

# ==========================================
# 3. ENTRADA DE DATOS
# ==========================================
with st.sidebar:
    st.header("👤 Perfil del Atleta")
    nombre = st.text_input("Nombre Completo:")
    pais = st.text_input("País de Residencia:", value="Argentina")
    edad = st.number_input("Edad:", min_value=10, value=30)
    
    genero_seleccion = st.selectbox("Género:", ["m ", "f "]) 
    genero = genero_seleccion.strip() 
    
    st.divider()
    
    embarazada_bool = False
    if genero == "f":
        embarazada_bool = st.checkbox("¿Está embarazada?")
        
    meses_gestacion = st.slider("Meses de gestación:", min_value=1, max_value=9, value=3, disabled=not embarazada_bool)
    
    st.divider()
    hora_entreno = st.time_input("¿A qué hora entrena?", time(18, 0))
    estatura = st.number_input("Estatura (cm):", min_value=100, value=170)
    peso_actual = st.number_input("Peso actual (kg):", min_value=30.0, value=75.0)
    
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

mapa_nombres = {
    1: ["Comida Única"], 
    2: ["Almuerzo", "Cena"], 
    3: ["Desayuno", "Almuerzo", "Cena"],
    4: ["Desayuno", "Almuerzo", "Merienda", "Cena"], 
    5: ["Desayuno", "Media Mañana", "Almuerzo", "Merienda", "Cena"],
    6: ["Desayuno", "Media Mañana", "Almuerzo", "Merienda", "Pre-Cena", "Cena"]
}
nombres_actuales = mapa_nombres[num_comidas]

# ==========================================
# 4. MOTOR MATEMÁTICO EXPANDIDO
# ==========================================
st.subheader("📏 Salud y Mediciones")
col_c1, col_c2 = st.columns(2)

with col_c1: 
    cintura = st.number_input("Perímetro de Cintura (cm):", value=85.0)

with col_c2: 
    cadera = st.number_input("Perímetro de Cadera (cm):", value=95.0)

if cadera > 0:
    rcc_valor = round(cintura / cadera, 2)
else:
    rcc_valor = 0

if genero == "m": 
    tmb = (10 * peso_actual) + (6.25 * estatura) - (5 * edad) + 5
else: 
    tmb = (10 * peso_actual) + (6.25 * estatura) - (5 * edad) - 161

cal_mant = tmb * 1.5

if embarazada_bool == True:
    if meses_gestacion <= 6:
        cal_mant = cal_mant + 340
    else:
        cal_mant = cal_mant + 450

if meses_plazo > 0:
    ajuste_diario = (kg_a_cambiar * 7000) / (meses_plazo * 30)
else:
    ajuste_diario = 0

if embarazada_bool == True and any(x in tipo_objetivo for x in ["Pérdida", "Definición", "Recomposición"]):
    cal_obj = cal_mant
    dif = 0
else:
    if "Pérdida" in tipo_objetivo: 
        dif = -ajuste_diario
    elif "Definición" in tipo_objetivo: 
        dif = -(ajuste_diario * 1.3)
    elif "Recomposición" in tipo_objetivo: 
        if cal_mant > 1500:
            dif = -300
        else:
            dif = -150
    elif "Volumen Limpio" in tipo_objetivo: 
        dif = ajuste_diario
    elif "Volumen Agresivo" in tipo_objetivo: 
        dif = ajuste_diario * 1.5
    else: 
        dif = 0
        
    cal_obj = cal_mant + dif

if "Hiper" in dieta_tipo:
    p_g_total = peso_actual * 2.2
else:
    p_g_total = peso_actual * 1.8

if "Keto" in dieta_tipo:
    c_g_total = 30.0
    g_g_total = (cal_obj - (p_g_total * 4) - (120)) / 9
else:
    g_g_total = (cal_obj * 0.30) / 9
    c_g_total = (cal_obj - (p_g_total * 4) - (g_g_total * 9)) / 4

agua_total = round((peso_actual * 0.035) + 0.75, 1)

if 11 <= hora_entreno.hour <= 14:
    choque_almuerzo = True
else:
    choque_almuerzo = False

if 19 <= hora_entreno.hour <= 22:
    choque_cena = True
else:
    choque_cena = False

if choque_almuerzo == True or choque_cena == True:
    choque_comida_principal = True
else:
    choque_comida_principal = False

# ==========================================
# 5. LÓGICA DE GUARDADO (CRM EXCEL)
# ==========================================
with st.sidebar:
    st.divider()
    if st.button("💾 Guardar Atleta (CRM)"):
        if nombre:
            nuevo_dato = pd.DataFrame([{
                "Fecha": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "Nombre": nombre,
                "Pais": pais,
                "Peso Actual (kg)": peso_actual,
                "Meta": tipo_objetivo,
                "Dieta": dieta_tipo,
                "Kcal Objetivo": int(cal_obj)
            }])
            
            if os.path.exists(DB_FILE):
                df_existente = pd.read_csv(DB_FILE)
                df_final = pd.concat([df_existente, nuevo_dato], ignore_index=True)
                df_final.to_csv(DB_FILE, index=False)
            else:
                nuevo_dato.to_csv(DB_FILE, index=False)
                
            st.success("¡Atleta guardado!")
        else: 
            st.error("Ingresá un nombre.")

# ==========================================
# 6. RESULTADOS Y GRÁFICO
# ==========================================
st.divider()
st.info(f"Atleta: **{nombre if nombre else 'Eddy PT'}** | País: {pais} | RCC: {rcc_valor}")

col_r1, col_r2, col_r3, col_r4 = st.columns(4)

col_r1.metric("Mantenimiento", f"{int(cal_mant)} kcal")
col_r2.metric("Ajuste Diario", f"{int(dif)} kcal", delta=int(dif))
col_r3.metric("Objetivo Final", f"{int(cal_obj)} kcal")
col_r4.metric("💧 Agua Diaria", f"{agua_total} L")

kg_mes_real = (dif * 30) / 7000 

meses_lista = ["Inicio"]
for i in range(int(meses_plazo)):
    meses_lista.append(f"Mes {i+1}")

pesos_prog = []
for i in range(len(meses_lista)):
    peso_calculado = peso_actual + (kg_mes_real * i)
    pesos_prog.append(peso_calculado)

fig, ax = plt.subplots(figsize=(10, 2))
ax.bar(meses_lista, pesos_prog, color='#2E7D32')

for i, v in enumerate(pesos_prog): 
    ax.text(i, v + 1, f"{round(v,1)}kg", ha='center', fontsize=8)

st.pyplot(fig)

# ==========================================
# 7. SUPLEMENTACIÓN VISUAL EXPANDIDA
# ==========================================
suples = []
suples.append("✅ Creatina (5g): Diario para fuerza.")

if "Volumen" in tipo_objetivo or "Recomposición" in tipo_objetivo: 
    suples.append("🚀 Citrulina Malato (6-8g): Pre-entreno.")

if "Definición" in tipo_objetivo or "Pérdida" in tipo_objetivo: 
    suples.append("🏃‍♂️ Beta-Alanina (3-5g): Diario.")

if "Agresiva" in tipo_objetivo or "Keto" in dieta_tipo or "Vegana" in dieta_tipo: 
    suples.append("🐟 Omega-3 (1-3g EPA/DHA): Con comida.")

if "Keto" in dieta_tipo or (10 <= hora_entreno.hour <= 16): 
    suples.append("⚡ Electrolitos: Intra-entreno.")

if hora_entreno.hour < 12: 
    suples.append("☕ Cafeína: Pre-entreno.")
else: 
    suples.append("💤 Magnesio: Por la noche.")

if choque_comida_principal == False: 
    suples.append("🥤 Proteína Whey: Post-entreno.")

st.divider()
col_s1, col_s2 = st.columns(2)

with col_s1:
    st.subheader("💧 Plan de Hidratación")
    st.success(f"**Objetivo Diario:** {agua_total} Litros.")

with col_s2:
    st.subheader("💊 Suplementación Clínica")
    for r in suples: 
        st.write(r)

st.divider()

# ==========================================
# 8. MENÚ DINÁMICO Y TICKET MENSUAL
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

for idx, nombre_base in enumerate(nombres_actuales):
    
    if choque_almuerzo == True and "Almuerzo" in nombre_base:
        etiqueta = " [ Post-Entreno ]"
    elif choque_cena == True and "Cena" in nombre_base:
        etiqueta = " [ Post-Entreno ]"
    else:
        etiqueta = ""
        
    nombre_final = f"{nombre_base.upper()}{etiqueta} - {int(cal_obj/num_comidas)} Kcal"
    
    opciones_de_esta_comida = []
    
    with st.expander(f"✨ {nombre_final}", expanded=True):
        
        if "Desayuno" in nombre_base or "Merienda" in nombre_base or "Mañana" in nombre_base:
            es_mt = True
        else:
            es_mt = False
            
        for i in range(num_opciones):
            
            # FILTROS DE PROTEÍNAS EXPANDIDOS
            if "Vegana" in dieta_tipo: 
                fp = alimentos_db["Prot_Vegana"][i % len(alimentos_db["Prot_Vegana"])]
            elif "Vegetariana" in dieta_tipo: 
                if es_mt == True:
                    fp = alimentos_db["Prot_Desayuno"][i % len(alimentos_db["Prot_Desayuno"])] 
                else:
                    fp = alimentos_db["Prot_Vegana"][i % len(alimentos_db["Prot_Vegana"])]
            elif "Pescetariana" in dieta_tipo: 
                if es_mt == True:
                    fp = alimentos_db["Prot_Desayuno"][i % len(alimentos_db["Prot_Desayuno"])] 
                else:
                    fp = alimentos_db["Prot_Pescado"][i % len(alimentos_db["Prot_Pescado"])]
            else: 
                if es_mt == True:
                    fp = alimentos_db["Prot_Desayuno"][i % len(alimentos_db["Prot_Desayuno"])] 
                else:
                    fp = alimentos_db["Prot_Principal"][i % len(alimentos_db["Prot_Principal"])]
            
            # FILTROS DE CARBOHIDRATOS EXPANDIDOS
            if "Keto" in dieta_tipo: 
                fc = alimentos_db["Verduras_Keto"][i % len(alimentos_db["Verduras_Keto"])]
            elif "Paleo" in dieta_tipo: 
                fc = alimentos_db["Carb_Vegetales"][i % len(alimentos_db["Carb_Vegetales"])]
            else: 
                if es_mt == True:
                    fc = alimentos_db["Carb_Desayuno"][i % len(alimentos_db["Carb_Desayuno"])] 
                else:
                    fc = alimentos_db["Carb_Principal"][i % len(alimentos_db["Carb_Principal"])]
            
            fg = alimentos_db["Grasas"][i % len(alimentos_db["Grasas"])]
            
            if "Argentina" in pais:
                bebida = alimentos_db["Bebidas_Arg"][i % len(alimentos_db["Bebidas_Arg"])]
            else:
                bebida = alimentos_db["Bebidas_Gral"][i % len(alimentos_db["Bebidas_Gral"])]
            
            if "Keto" in dieta_tipo:
                texto_carbo = "Libre"
            else:
                texto_carbo = f"{gramos_c}g"
                
            txt_op = f"Opcion {i+1}: {gramos_p}g {fp} + {texto_carbo} {fc} + {gramos_g}g {fg} | Infusion: {bebida}"
            
            st.write(txt_op)
            opciones_de_esta_comida.append(txt_op)

            # Suma Ticket Mensual
            dias_por_opcion = 30 / num_opciones
            lista_compras[fp] = lista_compras[fp] + (gramos_p * dias_por_opcion)
            
            if "Keto" not in dieta_tipo: 
                lista_compras[fc] = lista_compras[fc] + (gramos_c * dias_por_opcion)
                
            lista_compras[fg] = lista_compras[fg] + (gramos_g * dias_por_opcion)
            lista_compras[bebida] = lista_compras[bebida] + dias_por_opcion
            
    diccionario_menus[nombre_final] = opciones_de_esta_comida

# ==========================================
# 9. CLASE PDF PERSONALIZADA (ESTILO A - VIP)
# ==========================================
class ElitePDF(FPDF):
    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.set_text_color(120, 120, 120)
        self.cell(0, 10, 'Instagram: @EddyPersonalTrainer | Plan Nutricional Elite', 0, 0, 'C')

def build_pdf_v56(d):
    pdf = ElitePDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    
    if os.path.exists("logo.png"):
        try:
            pdf.image("logo.png", 170, 8, 30) 
        except:
            pass 
            
    pdf.set_fill_color(30, 30, 30)
    pdf.rect(0, 0, 210, 40, 'F')
    pdf.set_text_color(212, 175, 55) 
    pdf.set_font("Arial", "B", 22)
    pdf.set_y(12)
    pdf.cell(0, 10, "PLAN NUTRICIONAL ELITE", ln=True, align='L')
    
    pdf.set_text_color(255, 255, 255) 
    pdf.set_font("Arial", "", 12)
    pdf.cell(0, 8, f"ATLETA: {d['n'].upper().encode('latin-1','ignore').decode('latin-1')}", ln=True, align='L')
    
    pdf.set_y(45)
    pdf.set_text_color(0, 0, 0)
    
    pdf.set_font("Arial", "B", 12)
    pdf.set_fill_color(240, 240, 240)
    pdf.cell(0, 8, " METRICAS Y REQUERIMIENTOS", ln=True, fill=True)
    
    pdf.set_font("Arial", "", 10)
    pdf.cell(0, 6, f" - Tasa Metabolica Basal (TMB): {int(d['tmb'])} kcal en reposo absoluto.", ln=True)
    pdf.cell(0, 6, f" - Calorias de Mantenimiento Activo: {int(d['mant'])} kcal.", ln=True)
    pdf.cell(0, 6, f" - Calorias Objetivo Final ({d['meta']}): {int(d['k'])} kcal.", ln=True)
    pdf.cell(0, 6, f" - Objetivo Diario de Hidratacion: {d['w']} Litros.", ln=True)
    pdf.ln(5)
    
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 8, " SUPLEMENTACION CLINICA", ln=True, fill=True)
    pdf.set_font("Arial", "", 9)
    for s in d['s']: 
        pdf.cell(0, 6, f" {s.encode('latin-1','ignore').decode('latin-1')}", ln=True)
    pdf.ln(5)
    
    pdf.set_font("Arial", "B", 14)
    pdf.set_text_color(212, 175, 55) 
    pdf.cell(0, 10, "EL MENU DIARIO", ln=True, align='C')
    pdf.set_text_color(0, 0, 0)
    
    for nombre_comida, lista_opciones in d['menus'].items():
        pdf.set_fill_color(30, 30, 30)
        pdf.set_text_color(212, 175, 55)
        pdf.set_font("Arial", "B", 10)
        pdf.cell(0, 8, f" {nombre_comida.encode('latin-1','ignore').decode('latin-1')}", ln=True, fill=True)
        
        pdf.set_text_color(0, 0, 0)
        pdf.set_font("Arial", "", 9)
        
        fill = False
        for op in lista_opciones:
            if fill == True:
                pdf.set_fill_color(245, 245, 245) 
            else:
                pdf.set_fill_color(255, 255, 255) 
            
            pdf.multi_cell(0, 7, op.encode('latin-1','ignore').decode('latin-1'), border=1, fill=True)
            if fill == True:
                fill = False
            else:
                fill = True
            
        pdf.ln(3) 
        
    pdf.add_page()
    pdf.set_fill_color(30, 30, 30)
    pdf.rect(0, 0, 210, 20, 'F')
    pdf.set_y(6)
    pdf.set_text_color(212, 175, 55)
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "TICKET DE COMPRA MENSUAL", ln=True, align='C')
    
    pdf.set_text_color(0, 0, 0)
    pdf.set_y(25)
    pdf.set_font("Arial", "I", 9)
    pdf.cell(0, 6, "Inventario estimado para 30 dias de rotacion completa del menu.", ln=True, align='C')
    pdf.ln(5)
    
    pdf.set_font("Arial", "", 10)
    for alimento, cantidad in d['compras'].items():
        if "Huevo" in alimento or "Claras" in alimento:
            unidades = int(cantidad / 50)
            txt_item = f" + {alimento.encode('latin-1','ignore').decode('latin-1')}: {unidades} Unidades (~{round(unidades/12, 1)} Docenas)"
        elif "Café" in alimento or "Té" in alimento or "Mate" in alimento or "Infusión" in alimento:
            txt_item = f" + {alimento.encode('latin-1','ignore').decode('latin-1')}: {int(cantidad)} Porciones/Tazas"
        else:
            if cantidad >= 1000:
                kilos = round(cantidad / 1000, 1)
                txt_item = f" + {alimento.encode('latin-1','ignore').decode('latin-1')}: {kilos} KG"
            else:
                txt_item = f" + {alimento.encode('latin-1','ignore').decode('latin-1')}: {int(cantidad)} gramos"
        
        pdf.cell(0, 7, txt_item, ln=True, border='B') 

    return pdf.output(dest='S').encode('latin-1')

st.divider()

if st.button("📥 Generar PDF Estilo A (Elite)"):
    if nombre:
        data_p = {
            "n": nombre, "meta": tipo_objetivo, "k": cal_obj, "s": suples, 
            "menus": diccionario_menus, "w": agua_total, "compras": lista_compras,
            "tmb": tmb, "mant": cal_mant
        }
        st.download_button("💾 Descargar Plan Elite VIP", build_pdf_v56(data_p), file_name=f"Plan_{nombre}_VIP.pdf")
    else: 
        st.error("Por favor, ingresa el nombre del atleta para generar el PDF.")