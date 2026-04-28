import streamlit as st
from fpdf import FPDF

# Configuración de la página
st.set_page_config(page_title="Eddy PT - Metas Inteligentes", page_icon="📈")

st.title("💪 Eddy Personal Trainer: Plan de Metas")
st.write("Configura tus objetivos temporales para un seguimiento preciso.")

# 1. ENTRADA DE DATOS BIOMÉTRICOS
col1, col2 = st.columns(2)

with col1:
    nombre = st.text_input("Nombre Completo:")
    edad = st.number_input("Edad:", min_value=10, max_value=100, value=30)
    genero = st.selectbox("Género:", ["Masculino", "Femenino"])
    estatura = st.number_input("Estatura (cm):", min_value=100, max_value=250, value=170)

with col2:
    peso_actual = st.number_input("Peso actual (kg):", min_value=30.0, max_value=250.0, value=75.0)
    pais = st.text_input("País donde reside:")
    tipo_objetivo = st.radio("Meta principal:", ["Bajar de peso", "Subir masa muscular", "Mantenimiento"])

# 2. NUEVA SECCIÓN: OBJETIVOS TEMPORALES
st.subheader("🗓️ Cronograma de Meta")
col3, col4 = st.columns(2)

with col3:
    kg_a_cambiar = st.number_input("¿Cuántos kg totales quieres modificar?", min_value=0.5, max_value=50.0, value=5.0)
with col4:
    meses_plazo = st.number_input("¿En cuántos meses lo quieres lograr?", min_value=1, max_value=24, value=3)

# Cálculos de progreso
kg_por_mes = kg_a_cambiar / meses_plazo
kg_por_semana = kg_por_mes / 4

# 3. ACTIVIDAD Y CALORÍAS
st.divider()
entrenamientos_semana = st.slider("Días de entrenamiento por semana:", 0, 7, 3)

# Lógica Harris-Benedict
if genero == "Masculino":
    tmb = (10 * peso_actual) + (6.25 * estatura) - (5 * edad) + 5
else:
    tmb = (10 * peso_actual) + (6.25 * estatura) - (5 * edad) - 161

factores = {0: 1.2, 1: 1.375, 2: 1.375, 3: 1.55, 4: 1.55, 5: 1.55, 6: 1.725, 7: 1.9}
mantenimiento = tmb * factores[entrenamientos_semana]

# Ajuste calórico según la agresividad de la meta (basado en kg/semana)
# 7000 kcal aprox = 1kg de grasa. 
ajuste_diario = (kg_por_semana * 7000) / 7

if tipo_objetivo == "Bajar de peso":
    calorias_finales = mantenimiento - ajuste_diario
    peso_objetivo_final = peso_actual - kg_a_cambiar
elif tipo_objetivo == "Subir masa muscular":
    calorias_finales = mantenimiento + (ajuste_diario * 0.5) # El superávit suele ser más moderado
    peso_objetivo_final = peso_actual + kg_a_cambiar
else:
    calorias_finales = mantenimiento
    peso_objetivo_final = peso_actual

# 4. FUNCIÓN PARA EL PDF MEJORADO
def generar_pdf_metas(d):
    pdf = FPDF()
    pdf.add_page()
    
    # Encabezado
    pdf.set_font("helvetica", "B", 20)
    pdf.set_text_color(46, 125, 50)
    pdf.cell(0, 15, "EDDY PERSONAL TRAINER", align="C", new_x="LMARGIN", new_y="NEXT")
    
    # Perfil
    pdf.set_fill_color(240, 240, 240)
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("helvetica", "B", 12)
    pdf.cell(0, 10, f" PLAN DE TRANSFORMACIÓN: {d['nombre'].upper()}", fill=True, new_x="LMARGIN", new_y="NEXT")
    
    pdf.set_font("helvetica", "", 11)
    pdf.cell(0, 8, f"Peso Inicial: {d['p_actual']} kg | Estatura: {d['estatura']} cm", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 8, f"Meta Final: {d['p_final']:.1f} kg | Plazo: {d['meses']} meses", new_x="LMARGIN", new_y="NEXT")
    
    pdf.ln(5)
    
    # Cuadro de Metas Temporales
    pdf.set_font("helvetica", "B", 12)
    pdf.set_fill_color(200, 230, 200)
    pdf.cell(0, 10, " HOJA DE RUTA (MONITORIZACIÓN)", fill=True, new_x="LMARGIN", new_y="NEXT")
    
    pdf.set_font("helvetica", "", 11)
    pdf.cell(0, 10, f"- Objetivo semanal: {d['kg_sem']:.2f} kg", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 10, f"- Objetivo mensual: {d['kg_mes']:.2f} kg", new_x="LMARGIN", new_y="NEXT")
    
    pdf.ln(5)
    
    # Energía
    pdf.set_font("helvetica", "B", 14)
    pdf.set_draw_color(46, 125, 50)
    pdf.cell(0, 15, f"CONSUMO DIARIO: {int(d['cals'])} KCAL", border=1, align="C", new_x="LMARGIN", new_y="NEXT")
    
    pdf.ln(10)
    pdf.set_font("helvetica", "I", 10)
    pdf.multi_cell(0, 7, "Recuerda: El pesaje debe hacerse en ayunas, una vez por semana, para monitorizar que estemos cumpliendo los objetivos semanales marcados arriba.")

    return bytes(pdf.output())

# 5. BOTÓN Y EJECUCIÓN
if st.button("📊 Generar Plan con Metas Temporales"):
    if nombre and meses_plazo > 0:
        datos = {
            "nombre": nombre, "p_actual": peso_actual, "estatura": estatura,
            "p_final": peso_objetivo_final, "meses": meses_plazo,
            "kg_sem": kg_por_semana, "kg_mes": kg_por_mes,
            "cals": calorias_finales
        }
        pdf_file = generar_pdf_metas(datos)
        st.download_button(
            label="💾 Descargar Mi Plan Eddy PT",
            data=pdf_file,
            file_name=f"Metas_EddyPT_{nombre}.pdf",
            mime="application/pdf"
        )
        st.success(f"¡Todo listo! Para llegar a tu meta, el enfoque debe ser {int(calorias_finales)} kcal.")
    else:
        st.error("Por favor completa los campos correctamente.")