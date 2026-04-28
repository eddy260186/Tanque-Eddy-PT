def calcular_calorias():
    print("=== 🎯 Calculadora de Calorías Personalizada 🎯 ===\n")
    
    # Recopilar datos básicos
    genero = input("Género (H/M): ").upper()
    while genero not in ['H', 'M']:
        genero = input("Género inválido. Usa H (hombre) o M (mujer): ").upper()
    
    try:
        edad = int(input("Edad (años): "))
        peso_actual = float(input("Peso actual (kg): "))
        altura = float(input("Altura (cm): "))
        pais = input("País de residencia: ").title()
    except ValueError:
        print("Error: Debes introducir números válidos para edad, peso y altura.")
        return
    
    # Calcular IMC
    altura_m = altura / 100
    imc = peso_actual / (altura_m ** 2)
    imc_redondeado = round(imc, 1)
    
    # Clasificación del IMC
    if imc < 18.5:
        clasificacion_imc = "Bajo peso"
        color_imc = "🔵"
    elif 18.5 <= imc < 25:
        clasificacion_imc = "Peso normal"
        color_imc = "🟢"
    elif 25 <= imc < 30:
        clasificacion_imc = "Sobrepeso"
        color_imc = "🟡"
    else:
        clasificacion_imc = "Obesidad"
        color_imc = "🔴"
    
    # Nivel de actividad física general
    print("\n📊 Nivel de actividad física actual:")
    print("1. Sedentario (poco o ningún ejercicio)")
    print("2. Ligero (ejercicio ligero 1-3 días/semana)")
    print("3. Moderado (ejercicio moderado 3-5 días/semana)")
    print("4. Activo (ejercicio intenso 6-7 días/semana)")
    print("5. Muy activo (trabajo físico + ejercicio intenso)")
    
    actividad = input("Selecciona tu nivel (1-5): ")
    factores = {
        '1': 1.2,
        '2': 1.375,
        '3': 1.55,
        '4': 1.725,
        '5': 1.9
    }
    
    while actividad not in factores:
        actividad = input("Opción inválida. Elige entre 1 y 5: ")
    
    # Preguntar preferencias de actividades
    print("\n🏃‍♂️ ¿Qué tipo de actividades te gustaría realizar?")
    print("1. Gimnasio/Entrenamiento de fuerza")
    print("2. Cardio (caminar, correr, bicicleta)")
    print("3. Deportes (fútbol, tenis, baloncesto)")
    print("4. Yoga/Pilates")
    print("5. Baile/Danza")
    print("6. Natación")
    print("7. Entrenamiento en casa (sin equipo)")
    print("8. Combinación de varias actividades")
    
    actividad_preferida = input("Selecciona tu preferencia (1-8): ")
    
    # Nivel de experiencia
    print("\n📈 ¿Cuál es tu nivel de experiencia en ejercicio?")
    print("1. Principiante (menos de 3 meses de experiencia)")
    print("2. Intermedio (3-12 meses de experiencia)")
    print("3. Avanzado (1-3 años de experiencia)")
    print("4. Profesional (más de 3 años de experiencia)")
    
    nivel_experiencia = input("Selecciona tu nivel (1-4): ")
    
    # Calcular metabolismo basal (Mifflin-St Jeor)
    if genero == 'H':
        mb = (10 * peso_actual) + (6.25 * altura) - (5 * edad) + 5
    else:
        mb = (10 * peso_actual) + (6.25 * altura) - (5 * edad) - 161
    
    # Calcular calorías de mantenimiento
    mantenimiento = round(mb * factores[actividad])
    
    # Objetivo de peso personalizado
    print("\n=== 🎯 OBJETIVO DE PESO ===")
    print("1. Mantener peso actual")
    print("2. Bajar de peso")
    print("3. Subir de peso (ganar músculo)")
    
    objetivo_opcion = input("Selecciona tu objetivo (1-3): ")
    
    if objetivo_opcion == '1':
        peso_objetivo = peso_actual
        calorias_diarias = mantenimiento
        semanas_estimadas = 0
        cambio_calorias = 0
        unidad_tiempo = "semanas"
        tiempo_total = 0
    elif objetivo_opcion == '2':
        peso_objetivo = float(input("¿Cuántos kg quieres bajar? "))
        
        # Unidad de tiempo
        print("\n⏱️ ¿En qué unidad de tiempo quieres lograrlo?")
        print("1. Días")
        print("2. Semanas")
        print("3. Meses")
        print("4. Años")
        
        unidad_opcion = input("Selecciona (1-4): ")
        unidades = {
            '1': ('días', 1),
            '2': ('semanas', 7),
            '3': ('meses', 30),
            '4': ('años', 365)
        }
        
        while unidad_opcion not in unidades:
            unidad_opcion = input("Opción inválida. Elige entre 1 y 4: ")
        
        unidad_tiempo, dias_por_unidad = unidades[unidad_opcion]
        tiempo_total = float(input(f"¿En cuántos {unidad_tiempo} quieres lograrlo? "))
        dias_totales = tiempo_total * dias_por_unidad
        
        # Cálculo de déficit calórico (1 kg = 7700 kcal)
        total_calorias_necesarias = (peso_actual - peso_objetivo) * 7700
        cambio_calorias = -total_calorias_necesarias / dias_totales
        calorias_diarias = round(mantenimiento + cambio_calorias)
        semanas_estimadas = dias_totales / 7
    elif objetivo_opcion == '3':
        peso_objetivo = float(input("¿Cuántos kg quieres subir? "))
        
        # Unidad de tiempo
        print("\n⏱️ ¿En qué unidad de tiempo quieres lograrlo?")
        print("1. Días")
        print("2. Semanas")
        print("3. Meses")
        print("4. Años")
        
        unidad_opcion = input("Selecciona (1-4): ")
        unidades = {
            '1': ('días', 1),
            '2': ('semanas', 7),
            '3': ('meses', 30),
            '4': ('años', 365)
        }
        
        while unidad_opcion not in unidades:
            unidad_opcion = input("Opción inválida. Elige entre 1 y 4: ")
        
        unidad_tiempo, dias_por_unidad = unidades[unidad_opcion]
        tiempo_total = float(input(f"¿En cuántos {unidad_tiempo} quieres lograrlo? "))
        dias_totales = tiempo_total * dias_por_unidad
        
        # Cálculo de superávit calórico (1 kg = 7700 kcal)
        total_calorias_necesarias = (peso_objetivo - peso_actual) * 7700
        cambio_calorias = total_calorias_necesarias / dias_totales
        calorias_diarias = round(mantenimiento + cambio_calorias)
        semanas_estimadas = dias_totales / 7
    else:
        print("Opción inválida")
        return
    
    # Información relevante por país
    info_pais = {
        "España": {
            "alimentos": "Prioriza aceite de oliva, pescado, frutas y verduras de temporada",
            "actividad": "Caminar, senderismo o deportes tradicionales como la pelota",
            "cultura": "Las comidas suelen ser en familia, intenta no saltarte comidas y controla porciones",
            "locales": ["Senderismo en montañas", "Padel", "Fútbol playa", "Senderismo urbano", "Ciclismo de montaña"]
        },
        "México": {
            "alimentos": "Incorpora nopal, frijoles, chayote y aguacate en tu dieta",
            "actividad": "Caminata, fútbol o danzas tradicionales",
            "cultura": "Evita excesos de tortillas y salsas muy calóricas. Opta por preparaciones al vapor o a la plancha",
            "locales": ["Danza folclórica", "Fútbol sala", "Basquetbol callejero", "Volleyball de playa", "Senderismo en volcanes"]
        },
        "Argentina": {
            "alimentos": "Aprovecha carne magra, legumbres y lácteos. Reduce asados frecuentes",
            "actividad": "Fútbol, ciclismo o correr en parques",
            "cultura": "Las asadas son tradicionales pero calóricas. Compensa con más vegetales",
            "locales": ["Fútbol", "Polo", "Tango", "Patín", "Senderismo en sierras"]
        },
        "Colombia": {
            "alimentos": "Incluye granadilla, lulo, fríjoles y pescado fresco",
            "actividad": "Ciclismo, fútbol o senderismo en montañas",
            "cultura": "Las arepas y bandejas son calóricas. Opta por versiones más ligeras",
            "locales": ["Tejo", "Ciclismo de montaña", "Fútbol", "Salsa dancing", "Senderismo en jungla"]
        },
        "Perú": {
            "alimentos": "Aprovecha quinoa, camote, kiwicha y pescado como trucha",
            "actividad": "Surf, senderismo o deportes acuáticos",
            "cultura": "Evita excesos de acevichado y lomo saltado. Prefiere platos a la plancha",
            "locales": ["Surf", "Senderismo en Andes", "Fútbol playa", "Volleyball", "Senderismo en Amazonía"]
        },
        "Estados Unidos": {
            "alimentos": "Prioriza proteínas magras, vegetales y granos integrales. Evita comida procesada",
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
            "actividad": "Capoeira, fútbol o jiu-jitsu",
            "cultura": "Evita excesos de feijoada y carnes grasas. Prioriza preparaciones a la parrilla",
            "locales": ["Capoeira", "Fútbol", "Jiu-Jitsu", "Volleyball de playa", "Carnaval dancing"]
        }
    }
    
    # Obtener información del país si está disponible
    pais_info = info_pais.get(pais, {
        "alimentos": "Busca alimentos frescos y locales. Evita alimentos procesados",
        "actividad": "Realiza actividad física que disfrutes, al menos 30 minutos al día",
        "cultura": "Cada cultura tiene sus hábitos. Intenta adaptar tu dieta a tradiciones con porciones moderadas",
        "locales": ["Caminar", "Correr", "Ciclismo", "Senderismo local", "Deportes recreativos"]
    })
    
    # Generar rutina de entrenamiento personalizada
    rutina = generar_rutina(actividad_preferida, nivel_experiencia, objetivo_opcion, pais)
    
    # Mostrar resultados detallados
    print("\n" + "="*60)
    print("📊 RESULTADOS PERSONALIZADOS DETALLADOS")
    print("="*60)
    
    print(f"\n{color_imc} Estado actual: IMC {imc_redondeado} - {clasificacion_imc}")
    print(f"🔥 Metabolismo basal: {round(mb)} calorías/día")
    print(f"⚖️ Calorías de mantenimiento: {mantenimiento} calorías/día")
    
    if objetivo_opcion == '1':
        print(f"\n🎯 TU OBJETIVO: MANTENER {peso_actual} KG")
        print(f"💡 Recomendación diaria: {calorias_diarias} calorías")
        print(f"📅 Plan: Mantener este consumo indefinidamente")
    elif objetivo_opcion == '2':
        print(f"\n🎯 TU OBJETIVO: BAJAR DE {peso_actual} KG A {peso_objetivo} KG")
        print(f"⏱️ Duración: {tiempo_total} {unidad_tiempo} ({semanas_estimadas:.1f} semanas)")
        print(f"📉 Déficit calórico diario: {abs(cambio_calorias)} calorías")
        print(f"🔥 Recomendación diaria: {calorias_diarias} calorías")
        print(f"📊 Total calorías a reducir: {round((peso_actual - peso_objetivo) * 7700)} kcal")
    else:
        print(f"\n🎯 TU OBJETIVO: SUBIR DE {peso_actual} KG A {peso_objetivo} KG")
        print(f"⏱️ Duración: {tiempo_total} {unidad_tiempo} ({semanas_estimadas:.1f} semanas)")
        print(f"📈 Superávit calórico diario: {cambio_calorias} calorías")
        print(f"🔥 Recomendación diaria: {calorias_diarias} calorías")
        print(f"📊 Total calorías a aumentar: {round((peso_objetivo - peso_actual) * 7700)} kcal")
    
    # Desglose nutricional
    print("\n🥗 DESGLOSE NUTRICIONAL RECOMENDADO:")
    if objetivo_opcion == '2':  # Perder peso
        proteinas_g = round(peso_actual * 2.2)  # 2.2g/kg para preservar músculo
        carbohidratos_g = round((calorias_diarias - (proteinas_g * 4) - (calorias_diarias * 0.25)) / 4)
        grasas_g = round(calorias_diarias * 0.25 / 9)
    elif objetivo_opcion == '3':  # Ganar músculo
        proteinas_g = round(peso_actual * 2.0)  # 2.0g/kg para ganancia muscular
        carbohidratos_g = round((calorias_diarias - (proteinas_g * 4) - (calorias_diarias * 0.25)) / 4)
        grasas_g = round(calorias_diarias * 0.25 / 9)
    else:  # Mantener
        proteinas_g = round(peso_actual * 1.6)
        carbohidratos_g = round((calorias_diarias - (proteinas_g * 4) - (calorias_diarias * 0.25)) / 4)
        grasas_g = round(calorias_diarias * 0.25 / 9)
    
    print(f"🥩 Proteínas: {proteinas_g}g ({round(proteinas_g * 4)} kcal) - {round(proteinas_g * 4 / calorias_diarias * 100)}%")
    print(f"🍞 Carbohidratos: {carbohidratos_g}g ({round(carbohidratos_g * 4)} kcal) - {round(carbohidratos_g * 4 / calorias_diarias * 100)}%")
    print(f"🥑 Grasas: {grasas_g}g ({round(grasas_g * 9)} kcal) - {round(grasas_g * 9 / calorias_diarias * 100)}%")
    
    # Plan de alimentación básico
    print("\n🍽️ PLAN DE ALIMENTACIÓN BÁSICO:")
    if objetivo_opcion == '2':  # Perder peso
        print("🥗 Desayuno: 1 huevo + 1/2 aguacate + café/té")
        print("🍎 Almuerzo: 150g proteína magra + 1 taza verduras + 1/2 taza arroz integral")
        print("🍪 Snack: 1 manzana + 10 almendras")
        print("🍲 Cena: 120g salmón + ensalada grande con aceite de oliva")
        print("💧 Hidratación: 2-3 litros de agua al día")
    elif objetivo_opcion == '3':  # Ganar músculo
        print("🥗 Desayuno: 3 claras + 1 yema + 1 plátano + avena")
        print("🍖 Almuerzo: 200g pollo/pavo + 1 taza arroz integral + 1 taza verduras")
        print("🥜 Snack: 1 batido de proteína + 1 cucharada de mantequilla de maní")
        print("🍲 Cena: 180g carne magra + batata + verduras salteadas")
        print("💧 Hidratación: 3-4 litros de agua al día")
    else:  # Mantener
        print("🥗 Desayuno: 1 huevo + 1 rebanada pan integral + fruta")
        print("🍖 Almuerzo: 120g proteína + 1 taza carbohidratos complejos + verduras")
        print("🍪 Snack: 1 yogur griego + frutas")
        print("🍲 Cena: 100g pescado + ensalada grande")
        print("💧 Hidratación: 2 litros de agua al día")
    
    # Mostrar rutina de entrenamiento
    print("\n" + "="*60)
    print("🏋️‍♂️ RUTINA DE ENTRENAMIENTO PERSONALIZADA")
    print("="*60)
    print(rutina)
    
    # Consejos específicos por objetivo
    print("\n💡 CONSEJOS ESPECÍFICOS:")
    if objetivo_opcion == '1':  # Mantener
        print("✅ Para mantener peso:")
        print("   - Mide tu peso 1-2 veces por semana")
        print("   - Ajusta calorías según cambios en la actividad")
        print("   - Mantén una rutina de ejercicio regular")
        print("   - Prioriza alimentos integrales y procesados mínimos")
    elif objetivo_opcion == '2':  # Perder peso
        print("✅ Para perder peso de forma saludable:")
        print("   - Combina cardio (3-4 días/semana) con fuerza (2-3 días/semana)")
        print("   - Prioriza proteínas en cada comida para saciedad")
        print("   - Controla porciones usando platos más pequeños")
        print("   - Limita azúcares añadidos y bebidas azucaradas")
        print("   - Duerme 7-9 horas por noche para regular hormonas")
        
        if imc_redondeado >= 30:
            print("\n⚠️ ADVERTENCIA: Tu IMC indica obesidad.")
            print("   - Consulta a un profesional antes de iniciar cualquier dieta intensiva")
            print("   - Considera un déficit inicial más moderado (300-500 kcal)")
    else:  # Ganar músculo
        print("✅ Para ganar músculo de forma efectiva:")
        print("   - Entrena con pesas 3-4 días/semana con progresión de cargas")
        print("   - Consume proteína dentro de 1 hora post-entrenamiento")
        print("   - Asegura descanso muscular entre grupos musculares")
        print("   - Prioriza carbohidratos antes y después del entrenamiento")
        print("   - Duerme 7-9 horas para la recuperación muscular")
        
        if imc_redondeado < 18.5:
            print("\n⚠️ ADVERTENCIA: Tu IMC indica bajo peso.")
            print("   - Consulta a un nutricionista para un plan personalizado")
            print("   - Considera un superávit inicial más moderado (300-500 kcal)")
    
    # Información por país
    print(f"\n🌍 RECOMENDACIONES PARA {pais}:")
    print(f"🍎 Alimentos locales recomendados: {pais_info['alimentos']}")
    print(f"🏃‍♂️ Actividades populares: {pais_info['actividad']}")
    print(f"🎪 Actividades locales sugeridas: {', '.join(pais_info['locales'][:3])}")
    print(f"🍽️ Aspecto cultural: {pais_info['cultura']}")
    
    # Timeline de hitos
    print("\n📅 TIMELINE DE HITOS:")
    if objetivo_opcion == '2':  # Perder peso
        print("🔵 Semana 1-2: Adaptación al nuevo régimen (pérdida de agua)")
        print("🟢 Semana 3-4: Primeras pérdidas de grasa (0.5-1 kg)")
        print("🟡 Semana 5-8: Progreso constante (1-2 kg totales)")
        print("🔴 Semana 9-12: Ajuste si necesario (meta final)")
    elif objetivo_opcion == '3':  # Ganar músculo
        print("🔵 Semana 1-2: Adaptación al nuevo régimen")
        print("🟢 Semana 3-4: Primeros signos de ganancia muscular")
        print("🟡 Semana 5-8: Ganancia notable de fuerza (1-2 kg totales)")
        print("🔴 Semana 9-12: Consolidación de ganancias (meta final)")
    else:  # Mantener
        print("🔵 Cada semana: Monitoreo de peso y composición corporal")
        print("🟢 Cada mes: Ajuste según progreso y actividad")
    
    print("\n🚨 IMPORTANTE:")
    print("• Estos valores son estimaciones individuales")
    print("• Para un plan personalizado, consulta a un nutricionista o médico")
    print("• La pérdida o ganancia de peso saludable es de 0.5-1 kg por semana")
    print("• Escucha a tu cuerpo y ajusta según cómo te sientas")
    print("• La consistencia es más importante que la perfección")

def generar_rutina(actividad, nivel, objetivo, pais):
    """Genera una rutina de entrenamiento personalizada"""
    
    # Diccionario de rutinas por actividad
    rutinas = {
        "1": {  # Gimnasio/Entrenamiento de fuerza
            "1": """🏋️‍♂️ RUTINA DE GIMNASIO PARA PRINCIPIANTES
Lunes: Pierna y glúteos
- Sentadillas con peso corporal: 3x12
- Peso muerto rumano: 3x10
- Extensiones de cuádriceps: 3x15
- Curl femoral: 3x15

Miércoles: Tren superior
- Press de banca: 3x10
- Press militar: 3x10
- Remo con mancuerna: 3x12
- Curl de bíceps: 3x15

Viernes: Core y cardio
- Plancha: 3x30 segundos
- Crunch abdominal: 3x20
- Caminadora: 20 minutos

Duración: 45-60 minutos por sesión
Frecuencia: 3 días/semana""",
            
            "2": """🏋️‍♂️ RUTINA DE GIMNASIO INTERMEDIA
Lunes: Pierna y glúteos
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
- Curl de bíceps: 3x12
- Extensiones de tríceps: 3x12
- Elíptica: 25 minutos

Duración: 60-75 minutos por sesión
Frecuencia: 3-4 días/semana""",
            
            "3": """🏋️‍♂️ RUTINA DE GIMNASIO AVANZADA
Lunes: Pierna y glúteos
- Sentadillas con barra: 5x5
- Peso muerto: 5x5
- Prensa de piernas: 4x10
- Curl femoral: 4x12
- Glúteos: 4x15

Miércoles: Tren superior
- Press de banca: 5x5
- Press inclinado: 4x8
- Remo con barra: 5x5
- Fondos en paralelas: 4x10
- Curl martillo: 4x12

Viernes: Full body + HIIT
- Press militar: 4x8
- Remo con mancuerna: 4x10
- Curl de bíceps: 4x10
- Extensiones de tríceps: 4x10
- Burpees: 3x15
- Sprints: 8x30 segundos

Duración: 75-90 minutos por sesión
Frecuencia: 4-5 días/semana""",
            
            "4": """🏋️‍♂️ RUTINA DE GIMNASIO PROFESIONAL
Lunes: Hipertrofia pierna
- Sentadillas: 6x6
- Peso muerto rumano: 6x6
- Prensa de piernas: 5x8
- Curl femoral: 5x10
- Glúteos: 5x12
- Pantorrillas: 5x15

Miércoles: Hipertrofia torso
- Press de banca: 6x6
- Press inclinado: 5x8
- Remo con barra: 6x6
- Fondos en paralelas: 5x10
- Curl de bíceps: 5x10
- Extensiones de tríceps: 5x10

Viernes: Fuerza y explosividad
- Sentadillas con salto: 5x5
- Peso muerto explosivo: 5x5
- Press militar: 5x5
- Remo explosivo: 5x5
- Sprint: 10x40m
- Saltos: 5x10

Sábado: recuperación activa
- Yoga: 45 minutos
- Natación: 30 minutos
- Estiramientos: 20 minutos

Duración: 90-120 minutos por sesión
Frecuencia: 5-6 días/semana"""
        },
        
        "2": {  # Cardio
            "1": """🏃‍♂️ RUTINA CARDIO PARA PRINCIPIANTES
Lunes: Caminata
- Caminata moderada: 30 minutos
- Inclinación: 3-5%
- Ritmo: 5.5 km/h

Miércoles: Bicicleta
- Bicicleta estática: 25 minutos
- Resistencia moderada
- Ritmo: 15-20 km/h

Viernes: Elíptica
- Elíptica: 20 minutos
- Resistencia moderada
- Ritmo: 6-8 METS

Sábado: Caminata ligera
- Caminata en parque: 45 minutos
- Ritmo: 5.0 km/h

Duración: 20-30 minutos por sesión
Frecuencia: 3-4 días/semana""",
            
            "2": """🏃‍♂️ RUTINA CARDIO INTERMEDIA
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

Sábado: Elíptica
- Elíptica: 30 minutos
- Resistencia variable
- Ritmo: 8-10 METS

Duración: 30-45 minutos por sesión
Frecuencia: 4-5 días/semana""",
            
            "3": """🏃‍♂️ RUTINA CARDIO AVANZADA
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
- Natación: 30 minutos
- Remo: 20 minutos
- Escaleras: 10 minutos

Domingo: Descanso activo
- Yoga: 30 minutos
- Estiramientos: 15 minutos

Duración: 45-60 minutos por sesión
Frecuencia: 5-6 días/semana""",
            
            "4": """🏃‍♂️ RUTINA CARDIO PROFESIONAL
Lunes: Carrera de velocidad
- Calentamiento: 15 minutos
- Intervalos: 8x400m (1:30 descanso)
- Ritmo: 15-16 km/h
- Enfriamiento: 10 minutos

Miércoles: HIIT extremo
- Calentamiento: 10 minutos
- HIIT: 40 minutos (15s máximo/45s descanso)
- Ejercicios: burpees, saltos, sprints
- Enfriamiento: 10 minutos

Viernes: Bicicleta de competición
- Calentamiento: 15 minutos
- Simulacro: 60 minutos
- Resistencia: 85-90%
- Enfriamiento: 10 minutos

Sábado: Triatlón parcial
- Natación: 1000m
- Ciclismo: 30 km
- Carrera: 5 km

Domingo: Descanso activo
- Masaje: 30 minutos
- Flotación: 20 minutos

Duración: 60-90 minutos por sesión
Frecuencia: 6-7 días/semana"""
        },
        
        "3": {  # Deportes
            "1": """⚽ RUTINA DE DEPORTES PARA PRINCIPIANTES
Lunes: Fútbol básico
- Calentamiento: 10 minutos (carrera suave, estiramientos)
- Control del balón: 15 minutos
- Pases básicos: 15 minutos
- Tiro a puerta: 10 minutos
- Partido 5v5: 20 minutos
- Enfriamiento: 10 minutos

Miércoles: Tenis básico
- Calentamiento: 10 minutos
- Golpeo de derecha: 15 minutos
- Golpeo de izquierda: 15 minutos
- Servicio: 10 minutos
- Partido ligero: 20 minutos
- Enfriamiento: 10 minutos

Viernes: Baloncesto básico
- Calentamiento: 10 minutos
- Dribbling: 15 minutos
- Tiro en movimiento: 15 minutos
- Pases: 10 minutos
- Partido 3v3: 20 minutos
- Enfriamiento: 10 minutos

Duración: 75-90 minutos por sesión
Frecuencia: 3 días/semana""",
            
            "2": """⚽ RUTINA DE DEPORTES INTERMEDIA
Lunes: Fútbol táctico
- Calentamiento: 15 minutos
- Táctica posicional: 20 minutos
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
- Conducción con dribble: 20 minutos
- Tiro con presión: 15 minutos
- Partido 5v5: 30 minutos
- Enfriamiento: 10 minutos

Sábado: Deporte mixto
- Voleibol: 45 minutos
- Bádminton: 45 minutos

Duración: 90-120 minutos por sesión
Frecuencia: 4 días/semana""",
            
            "3": """⚽ RUTINA DE DEPORTES AVANZADA
Lunes: Fútbol profesional
- Calentamiento: 20 minutos
- Ejercicios técnicos: 30 minutos
- Táctica ofensiva: 25 minutos
- Táctica defensiva: 25 minutos
- Partido 11v11: 60 minutos
- Enfriamiento: 15 minutos

Miércoles: Tenis de competición
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

Sábado: Preparación física
- Fuerza explosiva: 30 minutos
- Agilidad: 30 minutos
- Resistencia: 30 minutos

Domingo: Descanso activo
- Estiramientos: 30 minutos
- Masaje: 30 minutos

Duración: 120-150 minutos por sesión
Frecuencia: 5-6 días/semana""",
            
            "4": """⚽ RUTINA DE DEPORTES PROFESIONAL
Lunes: Entrenamiento específico
- Calentamiento: 30 minutos
- Ejercicios técnicos especializados: 45 minutos
- Táctica avanzada: 45 minutos
- Partido simulacro: 90 minutos
- Enfriamiento: 20 minutos

Martes: Preparación física
- Fuerza máxima: 60 minutos
- Potencia: 45 minutos
- Resistencia: 45 minutos

Miércoles: Competición
- Partido oficial: 90 minutos
- Análisis: 30 minutos
- Recuperación: 30 minutos

Jueves: Regeneración
- Masaje: 45 minutos
- Flotación: 30 minutos
- Estiramientos: 30 minutos

Viernes: Entrenamiento táctico
- Calentamiento: 30 minutos
- Táctica ofensiva: 45 minutos
- Táctica defensiva: 45 minutos
- Partido: 60 minutos

Sábado: Preparación mental
- Visualización: 30 minutos
- Estrategia: 45 minutos
- Ejercicios psicológicos: 30 minutos

Domingo: Descanso completo
- Nada programado

Duración: 180+ minutos por sesión
Frecuencia: 6-7 días/semana"""
        },
        
        "4": {  # Yoga/Pilates
            "1": """🧘‍♀️ RUTINA YOGA/PILATES PARA PRINCIPIANTES
Lunes: Yoga básico
- Saludo al sol: 10 minutos
- Posturas de pie: 20 minutos
- Posturas de equilibrio: 15 minutos
- Posturas sentadas: 15 minutos
- Relajación: 10 minutos

Miércoles: Pilates básico
- Calentamiento: 10 minutos
- Centrado: 15 minutos
- Fortalecimiento core: 20 minutos
- Estiramientos: 15 minutos
- Relajación: 5 minutos

Viernes: Yoga suave
- Respiración: 10 minutos
- Posturas suaves: 30 minutos
- Meditación: 10 minutos
- Relajación: 10 minutos

Sábado: Movimiento libre
- Caminata consciente: 45 minutos
- Estiramientos suaves: 15 minutos

Duración: 60-75 minutos por sesión
Frecuencia: 3-4 días/semana""",
            
            "2": """🧘‍♀️ RUTINA YOGA/PILATES INTERMEDIA
Lunes: Vinyasa Yoga
- Saludo al sol: 15 minutos
- Secuencias dinámicas: 30 minutos
- Posturas de equilibrio avanzadas: 20 minutos
- Inversiones suaves: 10 minutos
- Meditación: 10 minutos

Miércoles: Pilates intermedio
- Calentamiento: 15 minutos
- Fortalecimiento core avanzado: 25 minutos
- Movilidad articular: 20 minutos
- Estiramientos profundos: 15 minutos
- Relajación: 5 minutos

Viernes: Yoga restaurativo
- Posturas de apoyo: 30 minutos
- Respiración profunda: 15 minutos
- Meditación guiada: 15 minutos

Sábado: Yoga al aire libre
- Caminata en naturaleza: 30 minutos
- Yoga en parque: 45 minutos
- Meditación: 15 minutos

Duración: 75-90 minutos por sesión
Frecuencia: 4-5 días/semana""",
            
            "3": """🧘‍♀️ RUTINA YOGA/PILATES AVANZADA
Lunes: Power Yoga
- Saludo al sol dinámico: 20 minutos
- Secuencias avanzadas: 40 minutos
- Posturas de equilibrio complejas: 25 minutos
- Inversiones: 15 minutos
- Meditación: 10 minutos

Miércoles: Pilates avanzado
- Calentamiento dinámico: 20 minutos
- Fortalecimiento core intenso: 30 minutos
- Movilidad avanzada: 25 minutos
- Posturas desafiantes: 20 minutos
- Relajación: 5 minutos

Viernes: Yoga terapéutico
- Posturas específicas: 45 minutos
- Respiración pranayama: 20 minutos
- Meditación profunda: 15 minutos

Sábado: Combinación
- Yoga matinal: 60 minutos
- Pilates tarde: 60 minutos
- Meditación: 15 minutos

Domingo: Regeneración
- Yoga suave: 45 minutos
- Masaje: 30 minutos
- Flotación: 30 minutos

Duración: 90-120 minutos por sesión
Frecuencia: 5-6 días/semana""",
            
            "4": """🧘‍♀️ RUTINA YOGA/PILATES PROFESIONAL
Lunes: Mañana intensiva
- Saludo al sol avanzado: 30 minutos
- Secuencias dinámicas: 60 minutos
- Posturas de equilibrio maestras: 30 minutos
- Inversiones avanzadas: 30 minutos
- Meditación: 15 minutos

Martes: Especialización
- Yoga terapéutico: 90 minutos
- Ajustes manuales: 30 minutos
- Anatomía aplicada: 30 minutos

Miércoles: Pilates de alto nivel
- Fortalecimiento core extremo: 45 minutos
- Movilidad articular máxima: 45 minutos
- Posturas maestras: 30 minutos
- Respiración avanzada: 15 minutos

Jueves: Enseñanza
- Clase guiada: 90 minutos
- Correcciones: 30 minutos
- Planificación: 30 minutos

Viernes: Práctica personal
- Secuencia personalizada: 120 minutos
- Meditación profunda: 30 minutos
- Autoanálisis: 30 minutos

Sábado: Comunidad
- Clase grupal: 120 minutos
- Talleres: 60 minutos
- Ceremonia: 30 minutos

Domingo: Integración
- Yoga silvestre: 120 minutos
- Retiro personal: 180 minutos
- Reflexión: 60 minutos

Duración: 180+ minutos por sesión
Frecuencia: 7 días/semana"""
        },
        
        "5": {  # Baile/Danza
            "1": """💃 RUTINA DE BAILE/DANZA PARA PRINCIPIANTES
Lunes: Baile urbano básico
- Calentamiento: 15 minutos
- Movimientos básicos: 30 minutos
- Secuencia simple: 20 minutos
- Coreografía: 15 minutos
- Enfriamiento: 10 minutos

Miércoles: Salsa básica
- Calentamiento: 15 minutos
- Pasos básicos: 30 minutos
- Giros simples: 20 minutos
- Coreografía: 20 minutos
- Enfriamiento: 10 minutos

Viernes: Bachata suave
- Calentamiento: 15 minutos
- Movimientos suaves: 30 minutos
- Posturas: 20 minutos
- Coreografía: 20 minutos
- Enfriamiento: 10 minutos

Sábado: Baile libre
- Música variada: 60 minutos
- Movimiento libre: 30 minutos
- Enfriamiento: 10 minutos

Duración: 75-90 minutos por sesión
Frecuencia: 3-4 días/semana""",
            
            "2": """💃 RUTINA DE BAILE/DANZA INTERMEDIA
Lunes: Baile urbano avanzado
- Calentamiento: 20 minutos
- Movimientos complejos: 40 minutos
- Secuencias dinámicas: 30 minutos
- Coreografía completa: 30 minutos
- Enfriamiento: 10 minutos

Miércoles: Salsa intermedia
- Calentamiento: 20 minutos
- Pasos avanzados: 40 minutos
- Giros complejos: 30 minutos
- Coreografía: 30 minutos
- Enfriamiento: 10 minutos

Viernes: Bachata con estilo
- Calentamiento: 20 minutos
- Movimientos expresivos: 40 minutos
- Improvisación: 30 minutos
- Coreografía: 30 minutos
- Enfriamiento: 10 minutos

Sábado: Baile de salón
- Tango: 30 minutos
- Vals: 30 minutos
- Cha-cha: 30 minutos

Domingo: Baile libre
- Música variada: 60 minutos
- Movimiento libre: 30 minutos

Duración: 90-120 minutos por sesión
Frecuencia: 4-5 días/semana""",
            
            "3": """💃 RUTINA DE BAILE/DANZA AVANZADA
Lunes: Baile urbano profesional
- Calentamiento: 30 minutos
- Movimientos maestros: 60 minutos
- Coreografía compleja: 45 minutos
- Improvisación avanzada: 30 minutos
- Enfriamiento: 15 minutos

Miércoles: Salsa de competición
- Calentamiento: 30 minutos
- Pasos de competencia: 60 minutos
- Giros extremos: 45 minutos
- Coreografía de show: 45 minutos
- Enfriamiento: 15 minutos

Viernes: Bachata sensual
- Calentamiento: 30 minutos
- Movimientos sensuales: 60 minutos
- Improvisación avanzada: 45 minutos
- Coreografía: 45 minutos
- Enfriamiento: 15 minutos

Sábado: Baile de salón avanzado
- Tango de salón: 45 minutos
- Vals vienés: 45 minutos
- Cha-cha profesional: 45 minutos

Domingo: Especialización
- Estilo específico: 120 minutos
- Coreografía personalizada: 60 minutos

Duración: 120-150 minutos por sesión
Frecuencia: 5-6 días/semana""",
            
            "4": """💃 RUTINA DE BAILE/DANZA PROFESIONAL
Lunes: Preparación física
- Fuerza explosiva: 45 minutos
- Agilidad: 45 minutos
- Resistencia: 45 minutos
- Flexibilidad: 30 minutos

Martes: Especialización urbana
- Movimientos maestros: 90 minutos
- Coreografía avanzada: 60 minutos
- Improvisación profesional: 45 minutos
- Enfriamiento: 15 minutos

Miércoles: Especialización latina
- Salsa de competición: 90 minutos
- Bachata sensual: 90 minutos
- Merengue avanzado: 45 minutos
- Enfriamiento: 15 minutos

Jueves: Baile de salón
- Tango profesional: 60 minutos
- Vals de competición: 60 minutos
- Cha-cha profesional: 60 minutos
- Enfriamiento: 15 minutos

Viernes: Coreografía de show
- Preparación: 60 minutos
- Coreografía completa: 120 minutos
- Repaso: 60 minutes
- Enfriamiento: 15 minutos

Sábado: Competición
- Calentamiento: 30 minutos
- Competición: 90 minutos
- Análisis: 30 minutos
- Recuperación: 30 minutos

Domingo: Integración
- Baile libre: 120 minutos
- Meditación: 30 minutos
- Planificación: 60 minutos

Duración: 180+ minutos por sesión
Frecuencia: 7 días/semana"""
        },
        
        "6": {  # Natación
            "1": """🏊‍♂️ RUTINA DE NATACIÓN PARA PRINCIPIANTES
Lunes: Técnica básica
- Calentamiento: 10 minutos (caminata ligera)
- Técnica de braza: 20 minutos
- Técnica de crol: 20 minutos
- Técnica de espalda: 15 minutos
- Enfriamiento: 5 minutos

Miércoles: Resistencia básica
- Calentamiento: 10 minutos
- Braza: 500m
- Crol: 500m
- Espalda: 300m
- Enfriamiento: 5 minutos

Viernes: Natación recreativa
- Calentamiento: 10 minutos
- Natación libre: 1000m
- Juegos acuáticos: 15 minutos
- Enfriamiento: 5 minutos

Sábado: Aguas abiertas
- Natación en playa: 30 minutos
- Aclimatación: 15 minutos
- Enfriamiento: 10 minutos

Duración: 45-60 minutos por sesión
Frecuencia: 3-4 días/semana""",
            
            "2": """🏊‍♂️ RUTINA DE NATACIÓN INTERMEDIA
Lunes: Técnica mejorada
- Calentamiento: 15 minutos
- Braza: 800m
- Crol: 800m
- Espalda: 500m
- Mariposa: 300m
- Enfriamiento: 10 minutos

Miércoles: Intervalos
- Calentamiento: 15 minutos
- Series 100m: 10x100m (descanso 30s)
- Series 200m: 5x200m (descanso 45s)
- Enfriamiento: 10 minutos

Viernes: Resistencia
- Calentamiento: 15 minutos
- Natación continua: 2000m
- Variación de estilos: 1000m
- Enfriamiento: 10 minutos

Sábado: Aguas abiertas
- Natación en lago: 1500m
- Técnicas de navegación: 30 minutos
- Enfriamiento: 15 minutos

Domingo: Descanso activo
- Caminata: 45 minutos
- Estiramientos: 15 minutos

Duración: 60-75 minutos por sesión
Frecuencia: 4-5 días/semana""",
            
            "3": """🏊‍♂️ RUTINA DE NATACIÓN AVANZADA
Lunes: Fuerza técnica
- Calentamiento: 20 minutos
- Palas: 1000m
- Remo con aletas: 800m
- Series cortas: 20x50m (descanso 20s)
- Enfriamiento: 15 minutos

Martes: Resistencia
- Calentamiento: 20 minutos
- Natación continua: 3000m
- Incluyendo todos los estilos: 2000m
- Enfriamiento: 15 minutos

Miércoles: Intervalos intensos
- Calentamiento: 20 minutos
- Series 100m: 20x100m (descanso 30s)
- Series 200m: 10x200m (descanso 45s)
- Enfriamiento: 15 minutos

Viernes: Competición simulada
- Calentamiento: 20 minutos
- 400m libre: 1
- 200m braza: 1
- 200m espalda: 1
- 200m mariposa: 1
- 100m libre: 1
- Enfriamiento: 15 minutos

Sábado: Aguas abiertas
- Natación en mar: 3000m
- Navegación: 30 minutos
- Enfriamiento: 20 minutos

Domingo: Recuperación
- Natación suave: 1500m
- Estiramientos: 30 minutos

Duración: 75-90 minutos por sesión
Frecuencia: 5-6 días/semana""",
            
            "4": """🏊‍♂️ RUTINA DE NATACIÓN PROFESIONAL
Lunes: Fuerza explosiva
- Calentamiento: 30 minutos
- Palas: 2000m
- Remo con aletas: 1500m
- Series cortas: 30x50m (descanso 15s)
- Enfriamiento: 20 minutos

Martes: Resistencia extrema
- Calentamiento: 30 minutos
- Natación continua: 5000m
- Variación de estilos: 3000m
- Enfriamiento: 20 minutos

Miércoles: Competición
- Calentamiento: 30 minutos
- 1500m libre: tiempo
- 400m individual: tiempo
- 100m libre: tiempo
- Enfriamiento: 20 minutos

Jueves: Especialización
- Calentamiento: 30 minutos
- Técnica de mariposa: 1000m
- Técnica de espalda: 1000m
- Técnica de braza: 1000m
- Enfriamiento: 20 minutos

Viernes: Preparación mental
- Visualización: 30 minutos
- Técnicas de relajación: 30 minutos
- Planificación: 60 minutos
- Enfriamiento: 20 minutos

Sábado: Competición real
- Calentamiento: 30 minutos
- Eventos: 90 minutos
- Recuperación: 60 minutos

Domingo: Descanso completo
- Masaje: 60 minutos
- Flotación: 30 minutos
- Nada programado

Duración: 120+ minutos por sesión
Frecuencia: 7 días/semana"""
        },
        
        "7": {  # Entrenamiento en casa
            "1": """🏠 RUTINA EN CASA PARA PRINCIPIANTES
Lunes: Fuerza corporal
- Sentadillas: 3x12
- Flexiones de rodillas: 3x10
- Plancha: 3x30 segundos
- Glúteos bridge: 3x15
- Abdominales: 3x15

Miércoles: Cardio ligero
- Jumping jacks: 3x30 segundos
- Zancadas: 3x12 por pierna
- Burpees modificados: 3x10
- Step en silla: 3x20
- Enfriamiento: 10 minutos

Viernes: Flexibilidad
- Estiramientos: 20 minutos
- Yoga básico: 15 minutos
- Respiración: 5 minutos
- Meditación: 10 minutos

Sábado: Movimiento libre
- Caminata: 45 minutos
- Estiramientos: 15 minutos

Duración: 30-45 minutos por sesión
Frecuencia: 3-4 días/semana""",
            
            "2": """🏠 RUTINA EN CASA INTERMEDIA
Lunes: Fuerza completa
- Sentadillas con peso: 4x15
- Flexiones: 4x12
- Plancha lateral: 3x45 segundos
- Glúteos bridge con elevación: 3x20
- Mountain climbers: 3x30 segundos

Miércoles: Cardio intenso
- Jumping jacks: 4x45 segundos
- Zancadas con salto: 3x15 por pierna
- Burpees: 4x15
- Escaleras imaginarias: 4x30 segundos
- Enfriamiento: 10 minutos

Viernes: Core y flexibilidad
- Plancha: 4x60 segundos
- Abdominales en V: 4x15
- Abdominales laterales: 4x20
- Estiramientos profundos: 20 minutos
- Yoga intermedio: 15 minutos

Sábado: HIIT en casa
- Tabata: 20 minutos
- Enfriamiento: 10 minutos
- Estiramientos: 10 minutos

Domingo: Descanso activo
- Caminata: 60 minutos
- Estiramientos: 15 minutos

Duración: 45-60 minutos por sesión
Frecuencia: 4-5 días/semana""",
            
            "3": """🏠 RUTINA EN CASA AVANZADA
Lunes: Fuerza intensa
- Sentadillas pistol: 4x10
- Flexiones explosivas: 4x15
- Plancha con movimiento: 4x45 segundos
- Glúteos bridge unilateral: 4x20
- Abdominales con rotación: 4x20

Miércoles: Cardio extremo
- HIIT: 30 minutos
- Burpees con salto: 5x20
- Zancadas con salto lateral: 5x20
- Escaleras con salto: 5x30 segundos
- Enfriamiento: 15 minutos

Viernes: Fuerza explosiva
- Saltos: 5x20
- Plancha con levantamiento: 5x30 segundos
- Abdominales con pesa: 5x20
- Flexiones con giro: 5x15
- Enfriamiento: 15 minutos

Sábado: Combinación
- Fuerza: 30 minutos
- Cardio: 30 minutos
- Core: 20 minutos
- Flexibilidad: 15 minutos

Domingo: Descanso activo
- Yoga avanzado: 45 minutos
- Meditación: 15 minutos

Duración: 60-75 minutos por sesión
Frecuencia: 5-6 días/semana""",
            
            "4": """🏠 RUTINA EN CASA PROFESIONAL
Lunes: Fuerza máxima
- Sentadillas con peso corporal: 6x8
- Flexiones explosivas: 6x12
- Plancha con peso: 6x45 segundos
- Glúteos bridge avanzado: 6x15
- Abdominales con resistencia: 6x20

Martes: Cardio extremo
- HIIT profesional: 45 minutos
- Burpees con salto: 8x25
- Zancadas con salto lateral: 8x25
- Escaleras con salto: 8x40 segundos
- Enfriamiento: 20 minutos

Miércoles: Fuerza funcional
- Movimiento compuesto: 40 minutos
- Circuitos: 30 minutos
- Resistencia: 30 minutos
- Enfriamiento: 20 minutos

Viernes: Preparación física
- Fuerza explosiva: 45 minutos
- Agilidad: 30 minutos
- Resistencia: 30 minutos
- Flexibilidad: 15 minutos

Sábado: Competición simulada
- Circuitos intensos: 60 minutos
- HIIT extremo: 30 minutos
- Fuerza máxima: 30 minutos
- Enfriamiento: 20 minutos

Domingo: Regeneración
- Yoga avanzado: 60 minutos
- Masaje: 30 minutos
- Meditación: 30 minutos

Duración: 90+ minutos por sesión
Frecuencia: 6-7 días/semana"""
        },
        
        "8": {  # Combinación de actividades
            "1": """🔄 RUTINA COMBINADA PARA PRINCIPIANTES
Lunes: Fuerza y cardio
- Calentamiento: 10 minutos
- Fuerza: 20 minutos
- Cardio: 20 minutos
- Core: 10 minutos
- Enfriamiento: 10 minutos

Miércoles: Flexibilidad y equilibrio
- Yoga básico: 30 minutos
- Estiramientos: 20 minutos
- Movimiento libre: 15 minutos
- Enfriamiento: 5 minutos

Viernes: Actividad recreativa
- Caminata: 45 minutos
- Estiramientos: 15 minutos
- Movimiento libre: 15 minutos

Sábado: Combinación ligera
- Fuerza ligera: 20 minutos
- Cardio ligero: 20 minutos
- Flexibilidad: 20 minutos
- Enfriamiento: 10 minutos

Domingo: Descanso activo
- Caminata: 60 minutos
- Estiramientos: 15 minutos

Duración: 45-60 minutos por sesión
Frecuencia: 3-4 días/semana""",
            
            "2": """🔄 RUTINA COMBINADA INTERMEDIA
Lunes: Fuerza y cardio
- Calentamiento: 15 minutos
- Fuerza: 30 minutos
- Cardio: 30 minutos
- Core: 15 minutos
- Enfriamiento: 10 minutos

Miércoles: Flexibilidad y fuerza
- Yoga intermedio: 30 minutos
- Fuerza con bandas: 30 minutos
- Core: 20 minutos
- Enfriamiento: 10 minutos

Viernes: Actividad específica
- Natación: 30 minutos
- Fuerza: 30 minutos
- Flexibilidad: 15 minutos
- Enfriamiento: 10 minutos

Sábado: HIIT y flexibilidad
- HIIT: 30 minutos
- Yoga: 30 minutos
- Enfriamiento: 15 minutos

Domingo: Descanso activo
- Caminata: 60 minutos
- Estiramientos: 20 minutos

Duración: 60-75 minutos por sesión
Frecuencia: 4-5 días/semana""",
            
            "3": """🔄 RUTINA COMBINADA AVANZADA
Lunes: Fuerza intensa
- Calentamiento: 20 minutos
- Fuerza con peso: 45 minutos
- Cardio: 30 minutos
- Core: 15 minutos
- Enfriamiento: 15 minutos

Martes: Cardio y flexibilidad
- HIIT: 45 minutos
- Yoga avanzado: 30 minutos
- Flexibilidad: 15 minutos
- Enfriamiento: 10 minutos

Miércoles: Fuerza funcional
- Movimiento compuesto: 45 minutos
- Resistencia: 30 minutos
- Flexibilidad: 15 minutos
- Enfriamiento: 15 minutos

Viernes: Especialización
- Natación: 45 minutos
- Fuerza: 30 minutos
- Flexibilidad: 20 minutos
- Enfriamiento: 15 minutos

Sábado: Competición simulada
- Circuitos intensos: 60 minutos
- HIIT extremo: 30 minutos
- Fuerza máxima: 30 minutos
- Enfriamiento: 20 minutos

Domingo: Regeneración
- Yoga avanzado: 45 minutos
- Masaje: 30 minutos
- Meditación: 15 minutos

Duración: 75-90 minutos por sesión
Frecuencia: 5-6 días/semana""",
            
            "4": """🔄 RUTINA COMBINADA PROFESIONAL
Lunes: Fuerza máxima
- Calentamiento: 30 minutos
- Fuerza con peso: 60 minutos
- Cardio: 45 minutos
- Core: 20 minutos
- Enfriamiento: 20 minutos

Martes: Cardio extremo
- HIIT profesional: 60 minutos
- Resistencia: 45 minutos
- Flexibilidad: 20 minutos
- Enfriamiento: 15 minutos

Miércoles: Especialización
- Natación: 60 minutos
- Fuerza: 45 minutos
- Flexibilidad: 30 minutos
- Enfriamiento: 15 minutos

Jueves: Fuerza funcional
- Movimiento compuesto: 60 minutos
- Resistencia: 45 minutos
- Agilidad: 30 minutos
- Enfriamiento: 20 minutos

Viernes: Competición simulada
- Circuitos intensos: 90 minutos
- HIIT extremo: 45 minutos
- Fuerza máxima: 45 minutos
- Enfriamiento: 30 minutos

Sábado: Preparación mental
- Visualización: 30 minutos
- Técnicas de relajación: 30 minutos
- Planificación: 60 minutos
- Enfriamiento: 20 minutos

Domingo: Regeneración completa
- Masaje: 60 minutos
- Flotación: 45 minutos
- Meditación: 30 minutos
- Descanso total

Duración: 120+ minutos por sesión
Frecuencia: 7 días/semana"""
        }
    }
    
    # Obtener la rutina según la actividad preferida y nivel de experiencia
    rutina_seleccionada = rutinas.get(actividad, {}).get(nivel, "Rutina no disponible para tu selección")
    
    return rutina_seleccionada

# Ejecutar la aplicación
if __name__ == "__main__":
    calcular_calorias()