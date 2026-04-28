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

def crear_rutina_combinada(rutinas_combinadas, objetivo_opcion):
    """Crea una rutina combinada que integra todas las actividades seleccionadas"""
    
    # Determinar dias disponibles
    dias_disponibles = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']
    
    # Asignar dias a actividades
    asignacion_dias = {}
    dias_restantes = dias_disponibles.copy()
    
    for rutina in rutinas_combinadas:
        actividad = rutina['actividad']
        dias_preferidos = rutina['dias']
        
        # Encontrar dias disponibles preferidos
        dias_asignados = []
        for dia in dias_preferidos:
            if dia in dias_restantes:
                dias_asignados.append(dia)
                dias_restantes.remove(dia)
        
        # Si no hay dias preferidos disponibles, asignar aleatorios
        if not dias_asignados and dias_restantes:
            dias_asignados = [dias_restantes.pop(0)]
        
        if dias_asignados:
            asignacion_dias[actividad] = dias_asignados
    
    # Crear rutina combinada
    rutina_texto = "RUTINA COMBINADA INTEGRADA\n"
    rutina_texto += "="*40 + "\n\n"
    
    # Asignar dias a actividades
    dias_asignados = {}
    for actividad, dias in asignacion_dias.items():
        for dia in dias:
            if dia not in dias_asignados:
                dias_asignados[dia] = []
            dias_asignados[dia].append(actividad)
    
    # Generar rutina por dia
    for dia in dias_disponibles:
        if dia in dias_asignados:
            actividades_dia = dias_asignados[dia]
            rutina_texto += f"{dia}:\n"
            
            # Si hay varias actividades, dividir el tiempo
            if len(actividades_dia) > 1:
                tiempo_por_actividad = 45 // len(actividades_dia)  # Dividir 45 minutos
                rutina_texto += f"   - {actividades_dia[0]}: {tiempo_por_actividad} minutos\n"
                
                # Obtener rutina específica y recortar
                for act in actividades_dia[1:]:
                    rutina_completa = ""
                    for rutina in rutinas_combinadas:
                        if rutina['actividad'] == act:
                            rutina_completa = rutina['rutina']
                            break
                    
                    if rutina_completa:
                        # Extraer solo las primeras lineas (ajustar tiempo)
                        lineas = rutina_completa.split('\n')
                        rutina_texto += f"   - {act}: {tiempo_por_actividad} minutos (rutina simplificada)\n"
            else:
                rutina_texto += f"   - {actividades_dia[0]}: 45 minutos\n"
            
            rutina_texto += "\n"
        else:
            rutina_texto += f"{dia}: Descanso o actividad suave (30 min)\n\n"
    
    # Consejos adicionales para rutina combinada
    rutina_texto += "CONSEJOS PARA RUTINA COMBINADA:\n"
    rutina_texto += "• Alterna entre diferentes tipos de ejercicio para evitar el estancamiento\n"
    rutina_texto += "• Escucha a tu cuerpo y ajusta la intensidad según el dia\n"
    rutina_texto += "• Prioriza la calidad sobre la cantidad en cada actividad\n"
    rutina_texto += "• Considera dias de descanso activo (caminatas suaves, yoga)\n"
    
    return rutina_texto

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
        
        # Título con nombre completo
        story.append(Paragraph(f"PLAN NUTRICIONAL PERSONALIZADO\nPara: {resultados['nombre_completo']}", title_style))
        story.append(Spacer(1, 20))
        
        # Información básica
        story.append(Paragraph("INFORMACIÓN BÁSICA", heading_style))
        info_data = [
            ['Nombre', resultados['nombre_completo']],
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
        
        # Rutina combinada
        story.append(Paragraph("RUTINA COMBINADA", heading_style))
        rutina_combinada = resultados.get('rutina_combinada', '')
        rutina_text = rutina_combinada.replace('\n', '<br/>')
        story.append(Paragraph(rutina_text, styles['Normal']))
        story.append(Spacer(1, 20))
        
        # Rutinas individuales
        story.append(Paragraph("RUTINAS INDIVIDUALES", heading_style))
        rutinas_individuales = resultados.get('rutinas_individuales', {})
        nombres_actividades = {
            '1': 'Gimnasio/Fuerza',
            '2': 'Cardio',
            '3': 'Deportes',
            '4': 'Yoga/Pilates',
            '5': 'Baile/Danza',
            '6': 'Natación',
            '7': 'Entrenamiento en casa',
            '8': 'Combinado'
        }
        
        for act, rutina in rutinas_individuales.items():
            if act in nombres_actividades:
                story.append(Paragraph(f"{nombres_actividades[act]}", styles['Heading3']))
                rutina_text = rutina.replace('\n', '<br/>')
                story.append(Paragraph(rutina_text, styles['Normal']))
                story.append(Spacer(1, 10))
        
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
        f.write(f"PLAN NUTRICIONAL PERSONALIZADO\n")
        f.write(f"Para: {resultados['nombre_completo']}\n")
        f.write("=" * 80 + "\n\n")
        
        # Información básica
        f.write("INFORMACIÓN BÁSICA\n")
        f.write("-" * 40 + "\n")
        f.write(f"Nombre: {resultados['nombre_completo']}\n")
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
        
        # Rutina combinada
        f.write("RUTINA COMBINADA\n")
        f.write("-" * 40 + "\n")
        f.write(resultados.get('rutina_combinada', ''))
        f.write("\n\n")
        
        # Rutinas individuales
        f.write("RUTINAS INDIVIDUALES\n")
        f.write("-" * 40 + "\n")
        rutinas_individuales = resultados.get('rutinas_individuales', {})
        nombres_actividades = {
            '1': 'Gimnasio/Fuerza',
            '2': 'Cardio',
            '3': 'Deportes',
            '4': 'Yoga/Pilates',
            '5': 'Baile/Danza',
            '6': 'Natación',
            '7': 'Entrenamiento en casa',
            '8': 'Combinado'
        }
        
        for act, rutina in rutinas_individuales.items():
            if act in nombres_actividades:
                f.write(f"\n{nombres_actividades[act]}:\n")
                f.write(rutina)
                f.write("\n")
        
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

def calcular_calorias():
    print("=== Calculadora de Calorias Personalizada ===\n")
    
    # Recopilar datos básicos incluyendo nombre y apellido
    nombre = input("Nombre: ").strip()
    apellido = input("Apellido: ").strip()
    nombre_completo = f"{nombre} {apellido}"
    
    while not nombre or not apellido:
        print("El nombre y apellido no pueden estar vacíos")
        nombre = input("Nombre: ").strip()
        apellido = input("Apellido: ").strip()
        nombre_completo = f"{nombre} {apellido}"
    
    # Limpiar el nombre completo para usarlo en el nombre de archivo
    nombre_limpio = ''.join(c if c.isalnum() or c == ' ' else '_' for c in nombre_completo)
    nombre_limpio = nombre_limpio.replace(' ', '_')
    # Eliminar múltiples guiones bajos consecutivos
    while '__' in nombre_limpio:
        nombre_limpio = nombre_limpio.replace('__', '_')
    nombre_limpio = nombre_limpio.strip('_')
    nombre_archivo_base = f"plan_nutricional_{nombre_limpio}"
    
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
    
    # Preguntar preferencias de actividades (permite múltiples)
    print("\nQue actividades te gustaria realizar? (puedes seleccionar varias)")
    print("1. Gimnasio/Entrenamiento de fuerza")
    print("2. Cardio (caminar, correr, bicicleta)")
    print("3. Deportes (futbol, tenis, baloncesto)")
    print("4. Yoga/Pilates")
    print("5. Baile/Danza")
    print("6. Natacion")
    print("7. Entrenamiento en casa (sin equipo)")
    print("8. Combinacion de varias actividades")
    
    print("\nEjemplo de seleccion: 1,3,5 (separa con comas)")
    actividades_seleccionadas = input("Selecciona tus actividades (ej: 1,2,3): ")
    
    # Procesar las actividades seleccionadas
    actividades_lista = []
    if actividades_seleccionadas:
        try:
            nums = [int(x.strip()) for x in actividades_seleccionadas.split(',')]
            validas = [str(x) for x in nums if 1 <= x <= 8]
            if validas:
                actividades_lista = validas
            else:
                print("⚠️ No seleccionaste actividades válidas. Usaremos la opción 1 por defecto")
                actividades_lista = ['1']
        except:
            print("⚠️ Formato inválido. Usaremos la opción 1 por defecto")
            actividades_lista = ['1']
    else:
        actividades_lista = ['1']
    
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
        objetivo_texto = "Mantener peso actual"
    elif objetivo_opcion == '2':
        peso_objetivo = float(input("Cuantos kg quieres bajar? "))
        objetivo_texto = f"Bajar de {peso_actual} kg a {peso_objetivo} kg"
        
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
        objetivo_texto = f"Subir de {peso_actual} kg a {peso_objetivo} kg"
        
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
    
    # Generar rutinas de entrenamiento para cada actividad seleccionada
    rutinas_individuales = {}
    rutinas_combinadas = []
    
    print("\nGenerando rutinas de entrenamiento...")
    
    # Generar rutina para cada actividad seleccionada
    for act in actividades_lista:
        rutina_individual = generar_rutina(act, nivel_experiencia, objetivo_opcion, pais)
        rutinas_individuales[act] = rutina_individual
        
        # Extraer dias de la semana de la rutina para combinación
        dias_rutina = []
        for linea in rutina_individual.split('\n'):
            if any(dia in linea for dia in ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']):
                dias_rutina.append(linea.split(':')[0])
        
        rutinas_combinadas.append({
            'actividad': act,
            'dias': dias_rutina,
            'rutina': rutina_individual
        })
    
    # Crear rutina combinada
    rutina_combinada = crear_rutina_combinada(rutinas_combinadas, objetivo_opcion)
    
    # Recopilar todos los resultados para el PDF
    resultados_pdf = {
        'nombre_completo': nombre_completo,
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
        'proteinas_g': None,  # Se calculará después
        'carbohidratos_g': None,
        'grasas_g': None,
        'rutinas_individuales': rutinas_individuales,
        'rutina_combinada': rutina_combinada,
        'actividades_seleccionadas': actividades_lista,
        'nivel_experiencia': nivel_experiencia
    }
    
    # Calcular macronutrientes
    if objetivo_opcion == '2':  # Perder peso
        proteinas_g = round(peso_actual * 2.2)  # 2.2g/kg para preservar musculo
        carbohidratos_g = round((calorias_diarias - (proteinas_g * 4) - (calorias_diarias * 0.25)) / 4)
        grasas_g = round(calorias_diarias * 0.25 / 9)
    elif objetivo_opcion == '3':  # Ganar musculo
        proteinas_g = round(peso_actual * 2.0)  # 2.0g/kg para ganancia muscular
        carbohidratos_g = round((calorias_diarias - (proteinas_g * 4) - (calorias_diarias * 0.25)) / 4)
        grasas_g = round(calorias_diarias * 0.25 / 9)
    else:  # Mantener
        proteinas_g = round(peso_actual * 1.6)
        carbohidratos_g = round((calorias_diarias - (proteinas_g * 4) - (calorias_diarias * 0.25)) / 4)
        grasas_g = round(calorias_diarias * 0.25 / 9)
    
    resultados_pdf['proteinas_g'] = proteinas_g
    resultados_pdf['carbohidratos_g'] = carbohidratos_g
    resultados_pdf['grasas_g'] = grasas_g
    
    # Mostrar resultados detallados
    print("\n" + "="*60)
    print("RESULTADOS PERSONALIZADOS DETALLADOS")
    print("="*60)
    
    print(f"\n{color_imc} Estado actual: IMC {imc_redondeado} - {clasificacion_imc}")
    print(f"Metabolismo basal: {round(mb)} calorias/dia")
    print(f"Calorias de mantenimiento: {mantenimiento} calorias/dia")
    
    if objetivo_opcion == '1':
        print(f"\nOBJETIVO: MANTENER {peso_actual} KG")
        print(f"Recomendacion diaria: {calorias_diarias} calorias")
        print(f"Plan: Mantener este consumo indefinidamente")
    elif objetivo_opcion == '2':
        print(f"\nOBJETIVO: BAJAR DE {peso_actual} KG A {peso_objetivo} KG")
        print(f"Duracion: {tiempo_total} {unidad_tiempo} ({semanas_estimadas:.1f} semanas)")
        print(f"Deficit calorico diario: {abs(cambio_calorias)} calorias")
        print(f"Recomendacion diaria: {calorias_diarias} calorias")
        print(f"Total calorias a reducir: {round((peso_actual - peso_objetivo) * 7700)} kcal")
    else:
        print(f"\nOBJETIVO: SUBIR DE {peso_actual} KG A {peso_objetivo} KG")
        print(f"Duracion: {tiempo_total} {unidad_tiempo} ({semanas_estimadas:.1f} semanas)")
        print(f"Superavit calorico diario: {cambio_calorias} calorias")
        print(f"Recomendacion diaria: {calorias_diarias} calorias")
        print(f"Total calorias a aumentar: {round((peso_objetivo - peso_actual) * 7700)} kcal")
    
    # Desglose nutricional completo
    print("\nDESGLOSE NUTRICIONAL COMPLETO:")
    
    print("\nMACRONUTRIENTES:")
    print(f"Proteinas: {proteinas_g}g ({round(proteinas_g * 4)} kcal) - {round(proteinas_g * 4 / calorias_diarias * 100)}%")
    print(f"Carbohidratos: {carbohidratos_g}g ({round(carbohidratos_g * 4)} kcal) - {round(carbohidratos_g * 4 / calorias_diarias * 100)}%")
    print(f"Grasas: {grasas_g}g ({round(grasas_g * 9)} kcal) - {round(grasas_g * 9 / calorias_diarias * 100)}%")
    
    # Mostrar rutinas de entrenamiento
    print("\n" + "="*60)
    print("RUTINAS DE ENTRENAMIENTO")
    print("="*60)
    
    # Mostrar rutina combinada primero
    print("\n🔄 RUTINA COMBINADA (todas las actividades integradas):")
    print(rutina_combinada)
    
    # Mostrar rutinas individuales
    print("\n" + "="*60)
    print("RUTINAS INDIVIDUALES POR ACTIVIDAD")
    print("="*60)
    
    nombres_actividades = {
        '1': 'Gimnasio/Fuerza',
        '2': 'Cardio',
        '3': 'Deportes',
        '4': 'Yoga/Pilates',
        '5': 'Baile/Danza',
        '6': 'Natacion',
        '7': 'Entrenamiento en casa',
        '8': 'Combinado'
    }
    
    for act in actividades_lista:
        if act in rutinas_individuales:
            print(f"\n🏋️‍♂️ {nombres_actividades.get(act, act)}:")
            print(rutinas_individuales[act])
    
    # Consejos específicos por objetivo
    print("\nCONSEJOS ESPECIFICOS:")
    if objetivo_opcion == '1':  # Mantener
        print("Para mantener peso:")
        print("   - Mide tu peso 1-2 veces por semana")
        print("   - Ajusta calorias segun cambios en la actividad")
        print("   - Manten una rutina de ejercicio regular")
        print("   - Prioriza alimentos integrales y procesados minimos")
    elif objetivo_opcion == '2':  # Perder peso
        print("Para perder peso de forma saludable:")
        print("   - Combina cardio (3-4 dias/semana) con fuerza (2-3 dias/semana)")
        print("   - Prioriza proteinas en cada comida para saciedad")
        print("   - Controla porciones usando platos mas pequenos")
        print("   - Limita azucares añadidos y bebidas azucaradas")
        print("   - Duerme 7-9 horas por noche para regular hormonas")
        
        if imc_redondeado >= 30:
            print("\nADVERTENCIA: Tu IMC indica obesidad.")
            print("   - Consulta a un profesional antes de iniciar cualquier dieta intensiva")
            print("   - Considera un deficit inicial mas moderado (300-500 kcal)")
    else:  # Ganar musculo
        print("Para ganar musculo de forma efectiva:")
        print("   - Entrena con pesas 3-4 dias/semana con progresion de cargas")
        print("   - Consume proteina dentro de 1 hora post-entrenamiento")
        print("   - Asegura descanso muscular entre grupos musculares")
        print("   - Prioriza carbohidratos antes y despues del entrenamiento")
        print("   - Duerme 7-9 horas para la recuperacion muscular")
        
        if imc_redondeado < 18.5:
            print("\nADVERTENCIA: Tu IMC indica bajo peso.")
            print("   - Consulta a un nutricionista para un plan personalizado")
            print("   - Considera un superavit inicial mas moderado (300-500 kcal)")
    
    # Informacion por pais
    print(f"\nRECOMENDACIONES PARA {pais}:")
    print(f"Alimentos locales recomendados: {pais_info['alimentos']}")
    print(f"Actividades populares: {pais_info['actividad']}")
    print(f"Actividades locales sugeridas: {', '.join(pais_info['locales'][:3])}")
    print(f"Aspecto cultural: {pais_info['cultura']}")
    
    # Timeline de hitos
    print("\nTIMELINE DE HITOS:")
    if objetivo_opcion == '2':  # Perder peso
        print("Semana 1-2: Adaptacion al nuevo regimen (perdida de agua)")
        print("Semana 3-4: Primeras perdidas de grasa (0.5-1 kg)")
        print("Semana 5-8: Progreso constante (1-2 kg totales)")
        print("Semana 9-12: Ajuste si necesario (meta final)")
    elif objetivo_opcion == '3':  # Ganar musculo
        print("Semana 1-2: Adaptacion al nuevo regimen")
        print("Semana 3-4: Primeros signos de ganancia muscular")
        print("Semana 5-8: Ganancia notable de fuerza (1-2 kg totales)")
        print("Semana 9-12: Consolidacion de ganancias (meta final)")
    else:  # Mantener
        print("Cada semana: Monitoreo de peso y composicion corporal")
        print("Cada mes: Ajuste segun progreso y actividad")
    
    print("\nIMPORTANTE:")
    print("• Estos valores son estimaciones individuales")
    print("• Para un plan personalizado, consulta a un nutricionista o medico")
    print("• La perdida o ganancia de peso saludable es de 0.5-1 kg por semana")
    print("• Escucha a tu cuerpo y ajusta segun como te sientas")
    print("• La consistencia es mas importante que la perfeccion")
    print("• Las rutinas combinadas te permiten disfrutar de diferentes actividades")
    
    # Preguntar si generar documento
    print("\n" + "="*60)
    print("¿Deseas generar tu plan nutricional en un archivo?")
    print("1. Generar PDF (formato profesional, requiere reportlab)")
    print("2. Generar archivo de texto (formato simple)")
    print("3. No generar archivo")
    
    opcion = input("Selecciona una opción (1-3): ")
    
    if opcion == '1':
        nombre_archivo = f"{nombre_archivo_base}.pdf"
        if not generar_pdf(resultados_pdf, nombre_archivo):
            print("⚠️ No se pudo generar PDF. Se generará un archivo de texto en su lugar.")
            generar_archivo_txt(resultados_pdf, nombre_archivo_base + ".txt")
    elif opcion == '2':
        nombre_archivo = f"{nombre_archivo_base}.txt"
        generar_archivo_txt(resultados_pdf, nombre_archivo)
    else:
        print("No se generó archivo. ¡Gracias por usar la calculadora!")

if __name__ == "__main__":
    calcular_calorias()