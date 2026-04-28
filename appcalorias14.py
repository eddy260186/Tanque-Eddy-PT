import subprocess
import sys
import os
from datetime import datetime

# Intentar instalar reportlab automáticamente
try:
    import reportlab
    print("✅ reportlab ya está instalado")
except ImportError:
    print("⚠️ reportlab no está instalado. Intentando instalar automáticamente...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "reportlab"])
        print("✅ reportlab instalado correctamente")
        import reportlab
    except:
        print("⚠️ No se pudo instalar reportlab. Se generará un archivo de texto en su lugar.")
        reportlab = None

def generar_pdf(resultados, nombre_archivo="plan_nutricional.pdf"):
    """Genera un PDF con todos los resultados si reportlab está disponible"""
    if reportlab is None:
        print("❌ reportlab no disponible. Use generar_archivo_txt() en su lugar.")
        return False
    
    try:
        from reportlab.lib.pagesizes import letter
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.units import inch
        from reportlab.lib import colors
        
        # Crear documento PDF
        doc = SimpleDocTemplate(nombre_archivo, pagesize=letter)
        styles = getSampleStyleSheet()
        
        # Personalizar estilos
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=18,
            spaceAfter=30,
            alignment=1  # Centrado
        )
        
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=14,
            spaceAfter=12,
            textColor=colors.darkblue
        )
        
        # Contenido del documento
        story = []
        
        # Título
        story.append(Paragraph("PLAN NUTRICIONAL PERSONALIZADO", title_style))
        story.append(Spacer(1, 20))
        
        # Información básica
        story.append(Paragraph("INFORMACIÓN BÁSICA", heading_style))
        info_data = [
            ['Género', resultados.get('genero', '')],
            ['Edad', f"{resultados.get('edad', '')} años"],
            ['Peso actual', f"{resultados.get('peso_actual', '')} kg"],
            ['Altura', f"{resultados.get('altura', '')} cm"],
            ['País', resultados.get('pais', '')],
            ['IMC', f"{resultados.get('imc_redondeado', '')} - {resultados.get('clasificacion_imc', '')}"]
        ]
        
        info_table = Table(info_data, colWidths=[2*inch, 3*inch])
        info_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        story.append(info_table)
        story.append(Spacer(1, 20))
        
        # Objetivo
        story.append(Paragraph("OBJETIVO", heading_style))
        objetivo_text = f"Tu objetivo es {resultados.get('objetivo_texto', '')}"
        if resultados.get('peso_objetivo') != resultados.get('peso_actual'):
            objetivo_text += f" de {resultados.get('peso_actual')} kg a {resultados.get('peso_objetivo')} kg"
        
        tiempo_text = f"En {resultados.get('tiempo_total')} {resultados.get('unidad_tiempo')}"
        if resultados.get('semanas_estimadas'):
            tiempo_text += f" ({resultados.get('semanas_estimadas'):.1f} semanas)"
        
        story.append(Paragraph(objetivo_text, styles['Normal']))
        story.append(Paragraph(tiempo_text, styles['Normal']))
        story.append(Spacer(1, 20))
        
        # Calorías
        story.append(Paragraph("NECESIDADES CALÓRICAS", heading_style))
        calorias_data = [
            ['Metabolismo basal', f"{resultados.get('mb', '')} kcal/día"],
            ['Calorías de mantenimiento', f"{resultados.get('mantenimiento', '')} kcal/día"],
            ['Recomendación diaria', f"{resultados.get('calorias_diarias', '')} kcal/día"]
        ]
        
        if resultados.get('cambio_calorias'):
            calorias_data.append(['Ajuste diario', f"{resultados.get('cambio_calorias', '')} kcal"])
        
        calorias_table = Table(calorias_data, colWidths=[2.5*inch, 2*inch])
        calorias_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        story.append(calorias_table)
        story.append(Spacer(1, 20))
        
        # Macronutrientes
        story.append(Paragraph("MACRONUTRIENTES", heading_style))
        macro_data = [
            ['Nutriente', 'Gramos', 'Kcal', 'Porcentaje'],
            ['Proteínas', f"{resultados.get('proteinas_g', '')}", 
             f"{round(resultados.get('proteinas_g', 0) * 4)}", 
             f"{round(resultados.get('proteinas_g', 0) * 4 / resultados.get('calorias_diarias', 1) * 100)}%"],
            ['Carbohidratos', f"{resultados.get('carbohidratos_g', '')}", 
             f"{round(resultados.get('carbohidratos_g', 0) * 4)}", 
             f"{round(resultados.get('carbohidratos_g', 0) * 4 / resultados.get('calorias_diarias', 1) * 100)}%"],
            ['Grasas', f"{resultados.get('grasas_g', '')}", 
             f"{round(resultados.get('grasas_g', 0) * 9)}", 
             f"{round(resultados.get('grasas_g', 0) * 9 / resultados.get('calorias_diarias', 1) * 100)}%"]
        ]
        
        macro_table = Table(macro_data, colWidths=[1.5*inch, 1*inch, 1*inch, 1*inch])
        macro_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        story.append(macro_table)
        story.append(Spacer(1, 20))
        
        # Plan de alimentación seleccionado
        if 'variante_seleccionada' in resultados:
            story.append(Paragraph("PLAN DE ALIMENTACIÓN SELECCIONADO", heading_style))
            variante = resultados['variante_seleccionada']
            
            story.append(Paragraph(f"Tipo: {variante['nombre']}", styles['Normal']))
            story.append(Paragraph(f"Descripción: {variante['descripcion']}", styles['Normal']))
            story.append(Spacer(1, 10))
            
            comidas_data = [
                ['Comida', 'Descripción'],
                ['Desayuno', variante['desayuno']],
                ['Almuerzo', variante['almuerzo']],
                ['Snack', variante['snack']],
                ['Cena', variante['cena']],
                ['Hidratación', variante['hidratacion']]
            ]
            
            comidas_table = Table(comidas_data, colWidths=[1.5*inch, 4*inch])
            comidas_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            story.append(comidas_table)
            story.append(Spacer(1, 20))
        
        # Rutina de entrenamiento
        if 'rutina' in resultados:
            story.append(Paragraph("RUTINA DE ENTRENAMIENTO", heading_style))
            rutina_text = resultados['rutina'].replace('\n', '<br/>')
            story.append(Paragraph(rutina_text, styles['Normal']))
            story.append(Spacer(1, 20))
        
        # Consejos
        story.append(Paragraph("CONSEJOS IMPORTANTES", heading_style))
        consejos_data = [
            ['Consejo', 'Descripción'],
            ['Frecuencia de ejercicio', '3-5 días por semana'],
            ['Duración de sesiones', '45-60 minutos'],
            ['Hidratación', '2-3 litros de agua al día'],
            ['Sueño', '7-9 horas por noche'],
            ['Seguimiento', 'Mide tu peso semanalmente']
        ]
        
        consejos_table = Table(consejos_data, colWidths=[2*inch, 3*inch])
        consejos_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        story.append(consejos_table)
        story.append(Spacer(1, 20))
        
        # Pie de página
        fecha_actual = datetime.now().strftime("%d/%m/%Y")
        story.append(Paragraph(f"Generado el {fecha_actual}", styles['Normal']))
        story.append(Spacer(1, 20))
        
        # Generar PDF
        doc.build(story)
        print(f"✅ PDF generado exitosamente: {nombre_archivo}")
        return True
        
    except Exception as e:
        print(f"❌ Error al generar PDF: {e}")
        return False

def generar_archivo_txt(resultados, nombre_archivo="plan_nutricional.txt"):
    """Genera un archivo de texto con toda la información si reportlab no está disponible"""
    
    with open(nombre_archivo, 'w', encoding='utf-8') as f:
        f.write("=" * 80 + "\n")
        f.write("PLAN NUTRICIONAL PERSONALIZADO\n")
        f.write("=" * 80 + "\n\n")
        
        # Información básica
        f.write("INFORMACIÓN BÁSICA\n")
        f.write("-" * 40 + "\n")
        f.write(f"Género: {resultados.get('genero', '')}\n")
        f.write(f"Edad: {resultados.get('edad', '')} años\n")
        f.write(f"Peso actual: {resultados.get('peso_actual', '')} kg\n")
        f.write(f"Altura: {resultados.get('altura', '')} cm\n")
        f.write(f"País: {resultados.get('pais', '')}\n")
        f.write(f"IMC: {resultados.get('imc_redondeado', '')} - {resultados.get('clasificacion_imc', '')}\n\n")
        
        # Objetivo
        f.write("OBJETIVO\n")
        f.write("-" * 40 + "\n")
        objetivo_text = f"Tu objetivo es {resultados.get('objetivo_texto', '')}"
        if resultados.get('peso_objetivo') != resultados.get('peso_actual'):
            objetivo_text += f" de {resultados.get('peso_actual')} kg a {resultados.get('peso_objetivo')} kg"
        
        tiempo_text = f"En {resultados.get('tiempo_total')} {resultados.get('unidad_tiempo')}"
        if resultados.get('semanas_estimadas'):
            tiempo_text += f" ({resultados.get('semanas_estimadas'):.1f} semanas)"
        
        f.write(f"{objetivo_text}\n")
        f.write(f"{tiempo_text}\n\n")
        
        # Calorías
        f.write("NECESIDADES CALÓRICAS\n")
        f.write("-" * 40 + "\n")
        f.write(f"Metabolismo basal: {resultados.get('mb', '')} kcal/día\n")
        f.write(f"Calorías de mantenimiento: {resultados.get('mantenimiento', '')} kcal/día\n")
        f.write(f"Recomendación diaria: {resultados.get('calorias_diarias', '')} kcal/día\n")
        
        if resultados.get('cambio_calorias'):
            f.write(f"Ajuste diario: {resultados.get('cambio_calorias', '')} kcal\n")
        f.write("\n")
        
        # Macronutrientes
        f.write("MACRONUTRIENTES\n")
        f.write("-" * 40 + "\n")
        f.write(f"{'Nutriente':<15} {'Gramos':<10} {'Kcal':<10} {'Porcentaje':<12}\n")
        f.write("-" * 47 + "\n")
        f.write(f"{'Proteínas':<15} {resultados.get('proteinas_g', ''):<10} {round(resultados.get('proteinas_g', 0) * 4):<10} {round(resultados.get('proteinas_g', 0) * 4 / resultados.get('calorias_diarias', 1) * 100):<12}%\n")
        f.write(f"{'Carbohidratos':<15} {resultados.get('carbohidratos_g', ''):<10} {round(resultados.get('carbohidratos_g', 0) * 4):<10} {round(resultados.get('carbohidratos_g', 0) * 4 / resultados.get('calorias_diarias', 1) * 100):<12}%\n")
        f.write(f"{'Grasas':<15} {resultados.get('grasas_g', ''):<10} {round(resultados.get('grasas_g', 0) * 9):<10} {round(resultados.get('grasas_g', 0) * 9 / resultados.get('calorias_diarias', 1) * 100):<12}%\n\n")
        
        # Plan de alimentación seleccionado
        if 'variante_seleccionada' in resultados:
            variante = resultados['variante_seleccionada']
            f.write("PLAN DE ALIMENTACIÓN SELECCIONADO\n")
            f.write("-" * 40 + "\n")
            f.write(f"Tipo: {variante['nombre']}\n")
            f.write(f"Descripción: {variante['descripcion']}\n")
            f.write(f"Características: {variante['caracteristicas']}\n\n")
            
            f.write("DETALLE DE COMIDAS\n")
            f.write("-" * 40 + "\n")
            f.write(f"Desayuno: {variante['desayuno']}\n")
            f.write(f"Almuerzo: {variante['almuerzo']}\n")
            f.write(f"Snack: {variante['snack']}\n")
            f.write(f"Cena: {variante['cena']}\n")
            f.write(f"Hidratación: {variante['hidratacion']}\n\n")
        
        # Rutina de entrenamiento
        if 'rutina' in resultados:
            f.write("RUTINA DE ENTRENAMIENTO\n")
            f.write("-" * 40 + "\n")
            f.write(resultados['rutina'])
            f.write("\n\n")
        
        # Consejos
        f.write("CONSEJOS IMPORTANTES\n")
        f.write("-" * 40 + "\n")
        f.write("• Frecuencia de ejercicio: 3-5 días por semana\n")
        f.write("• Duración de sesiones: 45-60 minutos\n")
        f.write("• Hidratación: 2-3 litros de agua al día\n")
        f.write("• Sueño: 7-9 horas por noche\n")
        f.write("• Seguimiento: Mide tu peso semanalmente\n\n")
        
        # Pie de página
        fecha_actual = datetime.now().strftime("%d/%m/%Y")
        f.write(f"Generado el {fecha_actual}\n")
    
    print(f"✅ Archivo de texto generado exitosamente: {nombre_archivo}")
    return True

def generar_variantes_alimentacion(objetivo, peso_actual, calorias_diarias):
    """Genera 5 variantes de plan de alimentacion para el objetivo"""
    
    variantes = []
    
    if objetivo == '2':  # Perder peso
        variantes = [
            {
                "nombre": "KETOGENICA",
                "descripcion": "Alta en grasas, baja en carbohidratos. Ideal para quemar grasa rapida.",
                "desayuno": "3 huevos revueltos con aguacate y tocino",
                "almuerzo": "150g salmon al horno + ensalada verde con aceite de oliva",
                "snack": "1 puñado de almendras + 1/2 aguacate",
                "cena": "120g pollo asado + brócoli al vapor",
                "hidratacion": "2-3 litros de agua + te verde",
                "caracteristicas": "Menos de 50g carbohidratos/dia, 70% grasas, 20% proteinas"
            },
            {
                "nombre": "PALEO",
                "descripcion": "Alimentos naturales, sin procesados. Enfocado en proteinas magras.",
                "desayuno": "Smoothie con espinacas, proteina, frutos rojos y nueces",
                "almuerzo": "180g bistec + batata asada + ensalada mixta",
                "snack": "1 manzana con mantequilla de almendra",
                "cena": "150g pescado a la plancha + calabacín salteado",
                "hidratacion": "2.5 litros de agua + infusiones",
                "caracteristicas": "Sin granos, lacteos ni azucares, alto en fibra"
            },
            {
                "nombre": "MEDITERRANEA",
                "descripcion": "Rica en grasas saludables, frutas y vegetales. Equilibrada y sostenible.",
                "desayuno": "Yogur griego con frutos rojos y semillas de chia",
                "almuerzo": "120g atun en ensalada con aceite de oliva y aceitunas",
                "snack": "1 puñado de nueces + 1 pera",
                "cena": "150g merluza a la plancha + espárragos trigueros",
                "hidratacion": "2 litros de agua + vino tinto moderado",
                "caracteristicas": "Alto en omega-3, antioxidantes y fibra"
            },
            {
                "nombre": "VEGETARIANA",
                "descripcion": "Basada en plantas, rica en fibra. Ideal para salud digestiva.",
                "desayuno": "Tofu scramble con champiñones y espinacas",
                "almuerzo": "Lentejas estofadas con verduras + quinoa",
                "snack": "1 yogur de soja + 1 plátano",
                "cena": "Hamburguesa de lentejas con ensalada",
                "hidratacion": "2.5 litros de agua + jugos vegetales",
                "caracteristicas": "Alta en proteina vegetal, hierro y fibra"
            },
            {
                "nombre": "INTERMITENTE",
                "descripcion": "Ciclos de ayuno y alimentacion. Controla apetito y mejora metabolismo.",
                "desayuno": "(Solo si no ayunas) Cafe con leche y 1 huevo",
                "almuerzo": "200g pollo + 1 taza arroz integral + verduras",
                "snack": "1 manzana + 10 almendras",
                "cena": "150g salmon + ensalada grande",
                "hidratacion": "3 litros de agua + te",
                "caracteristicas": "16/8 ayuno, calorias concentradas en 8 horas"
            }
        ]
    elif objetivo == '3':  # Ganar musculo
        variantes = [
            {
                "nombre": "HIPERCALORICA",
                "descripcion": "Alto superavit calorico. Para ganancia rapida de masa muscular.",
                "desayuno": "5 claras + 2 yemas + 1 plátano + 1 taza avena + proteina",
                "almuerzo": "250g carne magra + 1.5 taza arroz + 1 taza verduras",
                "snack": "Batido con 2 scoops proteina + 1 cda. mantequilla de maní + plátano",
                "cena": "200g pescado + 1 batata + 1 taza verduras",
                "hidratacion": "4 litros de agua + bebida isotonica",
                "caracteristicas": "500+ kcal superavit, 2.5g proteina/kg"
            },
            {
                "nombre": "CLEAN BULK",
                "descripcion": "Ganancia limpia. Enfocado en alimentos integrales.",
                "desayuno": "Huevos revueltos + aguacate + pan integral + fruta",
                "almuerzo": "200g pollo + 1 taza quinoa + 2 taza verduras",
                "snack": "Yogur griego + frutos rojos + nueces",
                "cena": "180g salmon + batata + brócoli",
                "hidratacion": "3.5 litros de agua + jugo de naranja",
                "caracteristicas": "300 kcal superavit, 2.2g proteina/kg"
            },
            {
                "nombre": "VEGANA",
                "descripcion": "100% vegetal. Con suplementacion estrategica.",
                "desayuno": "Smoothie con proteina de guisante, avena, frutos rojos, semillas",
                "almuerzo": "Tofu con tempeh + arroz integral + verduras mixtas",
                "snack": "Barra de proteina vegana + 1 manzana",
                "cena": "Hamburguesa de lentejas + quinua + ensalada",
                "hidratacion": "3 litros de agua + bebida de soja",
                "caracteristicas": "Requiere B12 y creatina, alto en fibra"
            },
            {
                "nombre": "CARBO-LOADING",
                "descripcion": "Enfoque en carbohidratos para entrenamientos intensos.",
                "desayuno": "Avena con plátano, miel y proteina",
                "almuerzo": "200g pollo + 2 taza pasta integral + verduras",
                "snack": "Batido de carbohidratos + proteina",
                "cena": "150g salmon + 1 batata + 1 taza verduras",
                "hidratacion": "4 litros de agua + bebida isotonica",
                "caracteristicas": "5g carbohidratos/kg, ideal para entrenamientos largos"
            },
            {
                "nombre": "PRE-POST ENTRENAMIENTO",
                "descripcion": "Nutricion peri-entrenamiento optimizada.",
                "desayuno": "2 horas antes: avena con proteina",
                "pre_entreno": "30min antes: plátano + 1 cda. miel",
                "post_entreno": "1h despues: batido proteina + carbohidratos",
                "cena": "200g carne magra + 1 taza arroz + verduras",
                "hidratacion": "3.5 litros de agua",
                "caracteristicas": "Nutrientes en momentos clave para recuperacion"
            }
        ]
    else:  # Mantener peso
        variantes = [
            {
                "nombre": "BALANCEADA",
                "descripcion": "Clasica y equilibrada. Facil de mantener a largo plazo.",
                "desayuno": "1 huevo + 1 rebanada pan integral + fruta",
                "almuerzo": "120g proteina + 1 taza carbohidratos + 1 taza verduras",
                "snack": "1 yogur griego + 1 manzana",
                "cena": "100g pescado + ensalada grande",
                "hidratacion": "2 litros de agua",
                "caracteristicas": "40% carbo, 30% proteina, 30% grasa"
            },
            {
                "nombre": "MINDFUL EATING",
                "descripcion": "Consciente y emocional. Control porciones y sabores.",
                "desayuno": "Tazon de avena con frutas y nueces",
                "almuerzo": "Ensalada de quinoa con verduras y proteina magra",
                "snack": "1 puñado de almendras + 1 pera",
                "cena": "Salmon al horno con verduras",
                "hidratacion": "2 litros de agua + te",
                "caracteristicas": "Comer despacio, 80% saciedad, variedad de colores"
            },
            {
                "nombre": "FLEXITARIANA",
                "descripcion": "Mayormente vegetal, con proteina ocasional.",
                "desayuno": "Tofu scramble con verduras",
                "almuerzo": "Lentejas con arroz integral y verduras",
                "snack": "1 yogur de soja + frutos rojos",
                "cena": "150g pollo + ensalada grande",
                "hidratacion": "2.5 litros de agua",
                "caracteristicas": "80% vegetal, 20% proteina animal"
            },
            {
                "nombre": "LOW CARB",
                "descripcion": "Moderada en carbohidratos, enfocada en proteinas.",
                "desayuno": "Huevos revueltos con espinacas y queso",
                "almuerzo": "150g carne magra + ensalada mixta",
                "snack": "1 puñado de nueces + 1 aguacate",
                "cena": "Pescado a la plancha + verduras asadas",
                "hidratacion": "2.5 litros de agua",
                "caracteristicas": "100g carbohidratos/dia, alto en fibra"
            },
            {
                "nombre": "MEDITERRANEA MODERNA",
                "descripcion": "Version moderna de la dieta mediterranea.",
                "desayuno": "Yogur griego con granola y frutos rojos",
                "almuerzo": "Ensalada de atun con aceitunas y verduras",
                "snack": "1 manzana + 1 cda. de almendras",
                "cena": "Merluza al vapor con verduras",
                "hidratacion": "2 litros de agua + vino tinto ocasional",
                "caracteristicas": "Alto en omega-3, antioxidantes y fibra"
            }
        ]
    
    return variantes

def generar_rutina(actividad, nivel, objetivo, pais):
    """Genera una rutina de entrenamiento personalizada"""
    
    # Diccionario de rutinas por actividad
    rutinas = {
        "1": {  # Gimnasio/Entrenamiento de fuerza
            "1": """RUTINA DE GIMNASIO PARA PRINCIPIANTES
Lunes: Pierna y gluteos
- Sentadillas con peso corporal: 3x12
- Peso muerto rumano: 3x10
- Extensiones de cuadriceps: 3x15
- Curl femoral: 3x15

Miércoles: Tren superior
- Press de banca: 3x10
- Press militar: 3x10
- Remo con mancuerna: 3x12
- Curl de biceps: 3x15

Viernes: Core y cardio
- Plancha: 3x30 segundos
- Crunch abdominal: 3x20
- Caminadora: 20 minutos

Duracion: 45-60 minutos por sesion
Frecuencia: 3 dias/semana""",
            
            "2": """RUTINA DE GIMNASIO INTERMEDIA
Lunes: Pierna y gluteos
- Sentadillas con barra: 4x8-10
- Peso muerto rumano: 4x8-10
- Prensa de piernas: 3x12
- Curl femoral: 3x12

Miércoles: Tren superior
- Press de banca con barra: 4x8-10
- Press inclinado: 3x10
- Remo con barra: 4x8-10
- Fondos en paralelas: 3x10

Viernes: Full body + cardio
- Press militar: 3x10
- Remo con mancuerna: 3x12
- Curl de biceps: 3x12
- Extensiones de triceps: 3x12
- Eliptica: 25 minutos

Duracion: 60-75 minutos por sesion
Frecuencia: 3-4 dias/semana""",
            
            "3": """RUTINA DE GIMNASIO AVANZADA
Lunes: Pierna y gluteos
- Sentadillas con barra: 5x5
- Peso muerto: 5x5
- Prensa de piernas: 4x10
- Curl femoral: 4x12
- Gluteos: 4x15

Miércoles: Tren superior
- Press de banca: 5x5
- Press inclinado: 4x8
- Remo con barra: 5x5
- Fondos en paralelas: 4x10
- Curl martillo: 4x12

Viernes: Full body + HIIT
- Press militar: 4x8
- Remo con mancuerna: 4x10
- Curl de biceps: 4x10
- Extensiones de triceps: 4x10
- Burpees: 3x15
- Sprints: 8x30 segundos

Duracion: 75-90 minutos por sesion
Frecuencia: 4-5 dias/semana""",
            
            "4": """RUTINA DE GIMNASIO PROFESIONAL
Lunes: Hipertrofia pierna
- Sentadillas: 6x6
- Peso muerto rumano: 6x6
- Prensa de piernas: 5x8
- Curl femoral: 5x10
- Gluteos: 5x15
- Pantorrillas: 5x15

Miércoles: Hipertrofia torso
- Press de banca: 6x6
- Press inclinado: 5x8
- Remo con barra: 6x6
- Fondos en paralelas: 5x10
- Curl de biceps: 5x10
- Extensiones de triceps: 5x10

Viernes: Fuerza y explosividad
- Sentadillas con salto: 5x5
- Peso muerto explosivo: 5x5
- Press militar: 5x5
- Remo explosivo: 5x5
- Sprint: 10x40m
- Saltos: 5x10

Sábado: recuperacion activa
- Yoga: 45 minutos
- Natacion: 30 minutos
- Estiramientos: 20 minutos

Duracion: 90-120 minutos por sesion
Frecuencia: 5-6 dias/semana"""
        },
        
        "2": {  # Cardio
            "1": """RUTINA CARDIO PARA PRINCIPIANTES
Lunes: Caminata
- Caminata moderada: 30 minutos
- Inclinacion: 3-5%
- Ritmo: 5.5 km/h

Miércoles: Bicicleta
- Bicicleta estatica: 25 minutos
- Resistencia moderada
- Ritmo: 15-20 km/h

Viernes: Eliptica
- Eliptica: 20 minutos
- Resistencia moderada
- Ritmo: 6-8 METS

Sábado: Caminata ligera
- Caminata en parque: 45 minutos
- Ritmo: 5.0 km/h

Duracion: 20-30 minutos por sesion
Frecuencia: 3-4 dias/semana""",
            
            "2": """RUTINA CARDIO INTERMEDIA
Lunes: Correr
- Calentamiento: 5 minutos caminata
- Carrera continua: 20 minutos
- Ritmo: 9-10 km/h
- Enfriamiento: 5 minutos caminata

Miércoles: HIIT
- Calentamiento: 5 minutos
- HIIT: 20 minutos (30s sprint/90s caminata)
- Enfriamiento: 5 minutos

Viernes: Bicicleta
- Calentamiento: 5 minutos
- Intervalos: 30 min (2 min fuerte/2 suave)
- Resistencia: 70-80%
- Enfriamiento: 5 minutos

Sábado: Eliptica
- Eliptica: 30 minutos
- Resistencia variable
- Ritmo: 8-10 METS

Duracion: 30-45 minutos por sesion
Frecuencia: 4-5 dias/semana""",
            
            "3": """RUTINA CARDIO AVANZADA
Lunes: Correr larga distancia
- Calentamiento: 10 minutos
- Carrera continua: 45 minutos
- Ritmo: 11-12 km/h
- Enfriamiento: 10 minutos

Miércoles: HIIT avanzado
- Calentamiento: 10 minutos
- HIIT: 30 minutos (20s sprint/40s caminata)
- Enfriamiento: 10 minutos

Viernes: Bicicleta de montaña
- Calentamiento: 10 minutos
- Subidas: 30 minutos
- Resistencia alta
- Enfriamiento: 10 minutos

Sábado: Cross training
- Natacion: 30 minutos
- Remo: 20 minutos
- Escaleras: 10 minutos

Domingo: Descanso activo
- Yoga: 30 minutos
- Estiramientos: 15 minutos

Duracion: 45-60 minutos por sesion
Frecuencia: 5-6 dias/semana""",
            
            "4": """RUTINA CARDIO PROFESIONAL
Lunes: Carrera de velocidad
- Calentamiento: 15 minutos
- Intervalos: 8x400m (1:30 descanso)
- Ritmo: 15-16 km/h
- Enfriamiento: 10 minutos

Miércoles: HIIT extremo
- Calentamiento: 10 minutos
- HIIT: 40 minutos (15s maximo/45s descanso)
- Ejercicios: burpees, saltos, sprints
- Enfriamiento: 10 minutos

Viernes: Bicicleta de competicion
- Calentamiento: 15 minutos
- Simulacro: 60 minutos
- Resistencia: 85-90%
- Enfriamiento: 10 minutos

Sábado: Triatlon parcial
- Natacion: 1000m
- Ciclismo: 30 km
- Carrera: 5 km

Domingo: Descanso activo
- Masaje: 30 minutos
- Flotacion: 20 minutos

Duracion: 60-90 minutos por sesion
Frecuencia: 6-7 dias/semana"""
        },
        
        "3": {  # Deportes
            "1": """RUTINA DE DEPORTES PARA PRINCIPIANTES
Lunes: Futbol basico
- Calentamiento: 10 minutos (carrera suave, estiramientos)
- Control del balon: 15 minutos
- Pases basicos: 15 minutos
- Tiro a puerta: 10 minutos
- Partido 5v5: 20 minutos
- Enfriamiento: 10 minutos

Miércoles: Tenis basico
- Calentamiento: 10 minutos
- Golpeo de derecha: 15 minutos
- Golpeo de izquierda: 15 minutos
- Servicio: 10 minutos
- Partido ligero: 20 minutos
- Enfriamiento: 10 minutos

Viernes: Baloncesto basico
- Calentamiento: 10 minutos
- Dribbling: 15 minutos
- Tiro en movimiento: 15 minutos
- Pases: 10 minutos
- Partido 3v3: 20 minutos
- Enfriamiento: 10 minutos

Duracion: 75-90 minutos por sesion
Frecuencia: 3 dias/semana""",
            
            "2": """RUTINA DE DEPORTES INTERMEDIA
Lunes: Futbol tactico
- Calentamiento: 15 minutos
- Tactica posicional: 20 minutos
- Ataque-defensa: 20 minutos
- Partido 7v7: 30 minutos
- Enfriamiento: 10 minutos

Miércoles: Tenis competitivo
- Calentamiento: 15 minutos
- Golpeo potente: 20 minutos
- Servicio con efecto: 15 minutos
- Partido: 30 minutos
- Enfriamiento: 10 minutos

Viernes: Baloncesto avanzado
- Calentamiento: 15 minutos
- Conduccion con dribble: 20 minutos
- Tiro con presion: 15 minutos
- Partido 5v5: 30 minutos
- Enfriamiento: 10 minutos

Sábado: Deporte mixto
- Voleibol: 45 minutos
- Badminton: 45 minutos

Duracion: 90-120 minutos por sesion
Frecuencia: 4 dias/semana""",
            
            "3": """RUTINA DE DEPORTES AVANZADA
Lunes: Futbol profesional
- Calentamiento: 20 minutos
- Ejercicios tecnicos: 30 minutos
- Tactica ofensiva: 25 minutos
- Tactica defensiva: 25 minutos
- Partido 11v11: 60 minutos
- Enfriamiento: 15 minutos

Miércoles: Tenis de competicion
- Calentamiento: 20 minutos
- Golpeo agresivo: 30 minutos
- Servicio y saque: 20 minutos
- Partido: 60 minutos
- Enfriamiento: 15 minutos

Viernes: Baloncesto de alto nivel
- Calentamiento: 20 minutos
- Entrenamiento de habilidades: 30 minutos
- Sistema ofensivo: 25 minutos
- Partido 5v5: 60 minutos
- Enfriamiento: 15 minutos

Sábado: Preparacion fisica
- Fuerza explosiva: 30 minutos
- Agilidad: 30 minutos
- Resistencia: 30 minutos

Domingo: Descanso activo
- Estiramientos: 30 minutos
- Masaje: 30 minutos

Duracion: 120-150 minutos por sesion
Frecuencia: 5-6 dias/semana""",
            
            "4": """RUTINA DE DEPORTES PROFESIONAL
Lunes: Entrenamiento especifico
- Calentamiento: 30 minutos
- Ejercicios tecnicos especializados: 45 minutos
- Tactica avanzada: 45 minutos
- Partido simulacro: 90 minutos
- Enfriamiento: 20 minutos

Martes: Preparacion fisica
- Fuerza maxima: 60 minutos
- Potencia: 45 minutos
- Resistencia: 45 minutos

Miércoles: Competicion
- Partido oficial: 90 minutos
- Analisis: 30 minutos
- Recuperacion: 30 minutos

Jueves: Regeneracion
- Masaje: 45 minutos
- Flotacion: 30 minutos
- Estiramientos: 30 minutos

Viernes: Entrenamiento tactico
- Calentamiento: 30 minutos
- Tactica ofensiva: 45 minutos
- Tactica defensiva: 45 minutos
- Partido: 60 minutos

Sábado: Preparacion mental
- Visualizacion: 30 minutos
- Estrategia: 45 minutos
- Ejercicios psicologicos: 30 minutos

Domingo: Descanso completo
- Nada programado

Duracion: 180+ minutos por sesion
Frecuencia: 6-7 dias/semana"""
        }
    }
    
    # Obtener la rutina segun la actividad preferida y nivel de experiencia
    rutina_seleccionada = rutinas.get(actividad, {}).get(nivel, "Rutina no disponible para tu seleccion")
    
    return rutina_seleccionada

def calcular_calorias():
    print("=== Calculadora de Calorias Personalizada ===\n")
    
    # Inicializar todas las variables que se usarán en el PDF
    genero = ""
    edad = 0
    peso_actual = 0.0
    altura = 0.0
    pais = ""
    imc_redondeado = 0.0
    clasificacion_imc = ""
    objetivo_texto = ""
    peso_objetivo = 0.0
    tiempo_total = 0.0
    unidad_tiempo = ""
    semanas_estimadas = 0.0
    mb = 0.0
    mantenimiento = 0.0
    calorias_diarias = 0.0
    cambio_calorias = 0.0
    proteinas_g = 0.0
    carbohidratos_g = 0.0
    grasas_g = 0.0
    variante_seleccionada = None
    rutina = ""
    
    # Recopilar datos básicos
    genero = input("Genero (H/M): ").upper()
    while genero not in ['H', 'M']:
        genero = input("Genero invalido. Usa H (hombre) o M (mujer): ").upper()
    
    try:
        edad = int(input("Edad (anos): "))
        peso_actual = float(input("Peso actual (kg): "))
        altura = float(input("Altura (cm): "))
        pais = input("Pais de residencia: ").title()
    except ValueError:
        print("Error: Debes introducir numeros validos para edad, peso y altura.")
        return
    
    # Calcular IMC
    altura_m = altura / 100
    imc = peso_actual / (altura_m ** 2)
    imc_redondeado = round(imc, 1)
    
    # Clasificacion del IMC
    if imc < 18.5:
        clasificacion_imc = "Bajo peso"
        color_imc = "Azul"
    elif 18.5 <= imc < 25:
        clasificacion_imc = "Peso normal"
        color_imc = "Verde"
    elif 25 <= imc < 30:
        clasificacion_imc = "Sobrepeso"
        color_imc = "Amarillo"
    else:
        clasificacion_imc = "Obesidad"
        color_imc = "Rojo"
    
    # Nivel de actividad fisica
    print("\nNivel de actividad fisica actual:")
    print("1. Sedentario (poco o ningun ejercicio)")
    print("2. Ligero (ejercicio ligero 1-3 dias/semana)")
    print("3. Moderado (ejercicio moderado 3-5 dias/semana)")
    print("4. Activo (ejercicio intenso 6-7 dias/semana)")
    print("5. Muy activo (trabajo fisico + ejercicio intenso)")
    
    actividad = input("Selecciona tu nivel (1-5): ")
    factores = {
        '1': 1.2,
        '2': 1.375,
        '3': 1.55,
        '4': 1.725,
        '5': 1.9
    }
    
    while actividad not in factores:
        actividad = input("Opcion invalida. Elige entre 1 y 5: ")
    
    # Preguntar preferencias de actividades
    print("\nQue tipo de actividades te gustaria realizar?")
    print("1. Gimnasio/Entrenamiento de fuerza")
    print("2. Cardio (caminar, correr, bicicleta)")
    print("3. Deportes (futbol, tenis, baloncesto)")
    print("4. Yoga/Pilates")
    print("5. Baile/Danza")
    print("6. Natacion")
    print("7. Entrenamiento en casa (sin equipo)")
    print("8. Combinacion de varias actividades")
    
    actividad_preferida = input("Selecciona tu preferencia (1-8): ")
    
    # Nivel de experiencia
    print("\nCual es tu nivel de experiencia en ejercicio?")
    print("1. Principiante (menos de 3 meses de experiencia)")
    print("2. Intermedio (3-12 meses de experiencia)")
    print("3. Avanzado (1-3 anos de experiencia)")
    print("4. Profesional (mas de 3 anos de experiencia)")
    
    nivel_experiencia = input("Selecciona tu nivel (1-4): ")
    
    # Calcular metabolismo basal (Mifflin-St Jeor)
    if genero == 'H':
        mb = (10 * peso_actual) + (6.25 * altura) - (5 * edad) + 5
    else:
        mb = (10 * peso_actual) + (6.25 * altura) - (5 * edad) - 161
    
    # Calcular calorias de mantenimiento
    mantenimiento = round(mb * factores[actividad])
    
    # Objetivo de peso personalizado
    print("\n=== OBJETIVO DE PESO ===")
    print("1. Mantener peso actual")
    print("2. Bajar de peso")
    print("3. Subir de peso (ganar musculo)")
    
    objetivo_opcion = input("Selecciona tu objetivo (1-3): ")
    
    if objetivo_opcion == '1':
        peso_objetivo = peso_actual
        calorias_diarias = mantenimiento
        semanas_estimadas = 0
        cambio_calorias = 0
        unidad_tiempo = "semanas"
        tiempo_total = 0
        objetivo_texto = "mantener el peso actual"
    elif objetivo_opcion == '2':
        peso_objetivo = float(input("Cuantos kg quieres bajar? "))
        objetivo_texto = "bajar de peso"
        
        # Unidad de tiempo
        print("\nEn que unidad de tiempo quieres lograrlo?")
        print("1. Dias")
        print("2. Semanas")
        print("3. Meses")
        print("4. Anos")
        
        unidad_opcion = input("Selecciona (1-4): ")
        unidades = {
            '1': ('dias', 1),
            '2': ('semanas', 7),
            '3': ('meses', 30),
            '4': ('anos', 365)
        }
        
        while unidad_opcion not in unidades:
            unidad_opcion = input("Opcion invalida. Elige entre 1 y 4: ")
        
        unidad_tiempo, dias_por_unidad = unidades[unidad_opcion]
        tiempo_total = float(input(f"En cuantos {unidad_tiempo} quieres lograrlo? "))
        dias_totales = tiempo_total * dias_por_unidad
        
        # Calculo de deficit calorico (1 kg = 7700 kcal)
        total_calorias_necesarias = (peso_actual - peso_objetivo) * 7700
        cambio_calorias = -total_calorias_necesarias / dias_totales
        calorias_diarias = round(mantenimiento + cambio_calorias)
        semanas_estimadas = dias_totales / 7
    elif objetivo_opcion == '3':
        peso_objetivo = float(input("Cuantos kg quieres subir? "))
        objetivo_texto = "subir de peso (ganar musculo)"
        
        # Unidad de tiempo
        print("\nEn que unidad de tiempo quieres lograrlo?")
        print("1. Dias")
        print("2. Semanas")
        print("3. Meses")
        print("4. Anos")
        
        unidad_opcion = input("Selecciona (1-4): ")
        unidades = {
            '1': ('dias', 1),
            '2': ('semanas', 7),
            '3': ('meses', 30),
            '4': ('anos', 365)
        }
        
        while unidad_opcion not in unidades:
            unidad_opcion = input("Opcion invalida. Elige entre 1 y 4: ")
        
        unidad_tiempo, dias_por_unidad = unidades[unidad_opcion]
        tiempo_total = float(input(f"En cuantos {unidad_tiempo} quieres lograrlo? "))
        dias_totales = tiempo_total * dias_por_unidad
        
        # Calculo de superavit calorico (1 kg = 7700 kcal)
        total_calorias_necesarias = (peso_objetivo - peso_actual) * 7700
        cambio_calorias = total_calorias_necesarias / dias_totales
        calorias_diarias = round(mantenimiento + cambio_calorias)
        semanas_estimadas = dias_totales / 7
    else:
        print("Opcion invalida")
        return
    
    # Informacion relevante por pais
    info_pais = {
        "España": {
            "alimentos": "Prioriza aceite de oliva, pescado, frutas y verduras de temporada",
            "actividad": "Caminar, senderismo o deportes tradicionales como la pelota",
            "cultura": "Las comidas suelen ser en familia, intenta no saltarte comidas y controla porciones",
            "locales": ["Senderismo en montañas", "Padel", "Futbol playa", "Senderismo urbano", "Ciclismo de montaña"]
        },
        "México": {
            "alimentos": "Incorpora nopal, frijoles, chayote y aguacate en tu dieta",
            "actividad": "Caminata, futbol o danzas tradicionales",
            "cultura": "Evita excesos de tortillas y salsas muy caloricas. Opta por preparaciones al vapor o a la plancha",
            "locales": ["Danza folclorica", "Futbol sala", "Basquetbol callejero", "Volleyball de playa", "Senderismo en volcanes"]
        },
        "Argentina": {
            "alimentos": "Aprovecha carne magra, legumbres y lacteos. Reduce asados frecuentes",
            "actividad": "Futbol, ciclismo o correr en parques",
            "cultura": "Las asadas son tradicionales pero caloricas. Compensa con mas vegetales",
            "locales": ["Futbol", "Polo", "Tango", "Patin", "Senderismo en sierras"]
        },
        "Colombia": {
            "alimentos": "Incluye granadilla, lulo, frijoles y pescado fresco",
            "actividad": "Ciclismo, futbol o senderismo en montañas",
            "cultura": "Las arepas y bandejas son caloricas. Opta por versiones mas ligeras",
            "locales": ["Tejo", "Ciclismo de montaña", "Futbol", "Salsa dancing", "Senderismo en jungla"]
        },
        "Perú": {
            "alimentos": "Aprovecha quinoa, camote, kiwicha y pescado como trucha",
            "actividad": "Surf, senderismo o deportes acuaticos",
            "cultura": "Evita excesos de acevichado y lomo saltado. Prefiere platos a la plancha",
            "locales": ["Surf", "Senderismo en Andes", "Futbol playa", "Volleyball", "Senderismo en Amazonia"]
        },
        "Estados Unidos": {
            "alimentos": "Prioriza proteinas magras, vegetales y granos integrales. Evita comida procesada",
            "actividad": "Caminar, levantamiento de pesas o clases de HIIT",
            "cultura": "Controla porciones en restaurantes y evita bebidas azucaradas",
            "locales": ["CrossFit", "Yoga", "Running", "Ciclismo urbano", "Senderismo nacional"]
        },
        "Japón": {
            "alimentos": "Aprovecha pescado, algas, tofu y verduras. Reduce arroz blanco",
            "actividad": "Caminar, tai chi o karate",
            "cultura": "Come despacio y hasta el 80% de saciedad. Evita fritos",
            "locales": ["Karate", "Judo", "Tai Chi", "Senderismo en templos", "Caminata urbana"]
        },
        "Brasil": {
            "alimentos": "Incorpora arroz integral, frijoles negros, frutas tropicales y pescado",
            "actividad": "Capoeira, futbol o jiu-jitsu",
            "cultura": "Evita excesos de feijoada y carnes grasas. Prioriza preparaciones a la parrilla",
            "locales": ["Capoeira", "Futbol", "Jiu-Jitsu", "Volleyball de playa", "Carnaval dancing"]
        }
    }
    
    # Obtener informacion del pais si esta disponible
    pais_info = info_pais.get(pais, {
        "alimentos": "Busca alimentos frescos y locales. Evita alimentos procesados",
        "actividad": "Realiza actividad fisica que disfrutes, al menos 30 minutos al dia",
        "cultura": "Cada cultura tiene sus habitos. Intenta adaptar tu dieta a tradiciones con porciones moderadas",
        "locales": ["Caminar", "Correr", "Ciclismo", "Senderismo local", "Deportes recreativos"]
    })
    
    # Generar rutina de entrenamiento personalizada
    rutina = generar_rutina(actividad_preferida, nivel_experiencia, objetivo_opcion, pais)
    
    # Desglose nutricional
    if objetivo_opcion == '2':  # Perder peso
        proteinas_g = round(peso_actual * 2.2)
        carbohidratos_g = round((calorias_diarias - (proteinas_g * 4) - (calorias_diarias * 0.25)) / 4)
        grasas_g = round(calorias_diarias * 0.25 / 9)
    elif objetivo_opcion == '3':  # Ganar musculo
        proteinas_g = round(peso_actual * 2.0)
        carbohidratos_g = round((calorias_diarias - (proteinas_g * 4) - (calorias_diarias * 0.25)) / 4)
        grasas_g = round(calorias_diarias * 0.25 / 9)
    else:  # Mantener
        proteinas_g = round(peso_actual * 1.6)
        carbohidratos_g = round((calorias_diarias - (proteinas_g * 4) - (calorias_diarias * 0.25)) / 4)
        grasas_g = round(calorias_diarias * 0.25 / 9)
    
    # Mostrar variantes de plan de alimentacion
    variantes = generar_variantes_alimentacion(objetivo_opcion, peso_actual, calorias_diarias)
    
    print("\nPLAN DE ALIMENTACION - 5 VARIANTES DISPONIBLES")
    print("="*60)
    
    for i, variante in enumerate(variantes, 1):
        print(f"\n{i}. {variante['nombre']}")
        print(f"   {variante['descripcion']}")
        print(f"   {variante['caracteristicas']}")
    
    print("\n" + "="*60)
    eleccion = input("Quieres ver los detalles de alguna variante? (1-5): ")
    
    if eleccion in ['1', '2', '3', '4', '5']:
        indice = int(eleccion) - 1
        variante_seleccionada = variantes[indice]
        
        print(f"\nDETALLES: {variante_seleccionada['nombre']}")
        print(f"{variante_seleccionada['descripcion']}")
        print(f"{variante_seleccionada['caracteristicas']}")
        print("\nDESAYUNO:")
        print(f"   {variante_seleccionada['desayuno']}")
        print("\nALMUERZO:")
        print(f"   {variante_seleccionada['almuerzo']}")
        print("\nSNACK:")
        print(f"   {variante_seleccionada['snack']}")
        print("\nCENA:")
        print(f"   {variante_seleccionada['cena']}")
        print("\nHIDRATACION:")
        print(f"   {variante_seleccionada['hidratacion']}")
        
        print("\nCONSEJOS ADICIONALES:")
        if objetivo_opcion == '2':
            print("• Controla porciones usando platos mas pequenos")
            print("• Bebe agua antes de cada comida")
            print("• Limita azucares añadidos")
        elif objetivo_opcion == '3':
            print("• Consume proteina dentro de 1 hora post-entrenamiento")
            print("• Aumenta carbohidratos pre-entrenamiento")
            print("• Duerme 7-9 horas para recuperacion")
        else:
            print("• Mide porciones ocasionalmente")
            print("   - Proteina: tamaño de tu palma")
            print("   - Carbohidratos: tamaño de tu puño")
            print("   - Grasas: tamaño de tu pulgar")
    else:
        print("\nCONSEJO: Prueba diferentes variantes para encontrar la que mejor se adapte a tu estilo de vida")
        print("   Puedes cambiar cada semana o combinar elementos de varias variantes")
    
    # Mostrar rutina de entrenamiento
    print("\n" + "="*60)
    print("RUTINA DE ENTRENAMIENTO PERSONALIZADA")
    print("="*60)
    print(rutina)
    
    # Recopilar todos los resultados para el PDF
    resultados_pdf = {
        'genero': genero,
        'edad': edad,
        'peso_actual': peso_actual,
        'altura': altura,
        'pais': pais,
        'imc_redondeado': imc_redondeado,
        'clasificacion_imc': clasificacion_imc,
        'objetivo_texto': objetivo_texto,
        'peso_objetivo': peso_objetivo,
        'tiempo_total': tiempo_total,
        'unidad_tiempo': unidad_tiempo,
        'semanas_estimadas': semanas_estimadas,
        'mb': mb,
        'mantenimiento': mantenimiento,
        'calorias_diarias': calorias_diarias,
        'cambio_calorias': cambio_calorias,
        'proteinas_g': proteinas_g,
        'carbohidratos_g': carbohidratos_g,
        'grasas_g': grasas_g,
        'variante_seleccionada': variante_seleccionada,
        'rutina': rutina
    }
    
    # Preguntar si generar documento
    print("\n" + "="*60)
    print("¿Deseas generar tu plan nutricional en un archivo?")
    print("1. Generar PDF (formato profesional, requiere reportlab)")
    print("2. Generar archivo de texto (formato simple)")
    print("3. No generar archivo")
    
    opcion = input("Selecciona una opción (1-3): ")
    
    if opcion == '1':
        nombre_archivo = f"plan_nutricional_{genero}_{peso_actual}kg.pdf"
        if not generar_pdf(resultados_pdf, nombre_archivo):
            print("⚠️ No se pudo generar PDF. Se generará un archivo de texto en su lugar.")
            generar_archivo_txt(resultados_pdf, nombre_archivo.replace('.pdf', '.txt'))
    elif opcion == '2':
        nombre_archivo = f"plan_nutricional_{genero}_{peso_actual}kg.txt"
        generar_archivo_txt(resultados_pdf, nombre_archivo)
    else:
        print("No se generó archivo. ¡Gracias por usar la calculadora!")

if __name__ == "__main__":
    calcular_calorias()