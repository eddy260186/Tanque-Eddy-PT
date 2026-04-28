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
    
    # Desglose nutricional completo
    print("\n🥗 DESGLOSE NUTRICIONAL COMPLETO:")
    
    # Macronutrientes
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
    
    print("\n🍖 MACRONUTRIENTES:")
    print(f"🥩 Proteínas: {proteinas_g}g ({round(proteinas_g * 4)} kcal) - {round(proteinas_g * 4 / calorias_diarias * 100)}%")
    print(f"🍞 Carbohidratos: {carbohidratos_g}g ({round(carbohidratos_g * 4)} kcal) - {round(carbohidratos_g * 4 / calorias_diarias * 100)}%")
    print(f"🥑 Grasas: {grasas_g}g ({round(grasas_g * 9)} kcal) - {round(grasas_g * 9 / calorias_diarias * 100)}%")
    
    # Micronutrientes clave según objetivo
    print("\n🍅 MICRONUTRIENTES CLAVE PARA TU OBJETIVO:")
    
    if objetivo_opcion == '2':  # Perder peso
        print("🌟 Para perder peso, enfócate en estos micronutrientes:")
        print("   • VITAMINA D: Regula el metabolismo y ayuda a quemar grasa")
        print("   • VITAMINA B12: Aumenta la energía y metabolismo")
        print("   • VITAMINA C: Ayuda a la oxidación de grasas y formación de colágeno")
        print("   • MAGNESIO: Controla el azúcar en sangre y reduce antojos")
        print("   • HIERRO: Previene fatiga y mantiene energía")
        print("   • CALCIO: Ayuda a la quema de grasa abdominal")
        
        print("\n🥗 ALIMENTOS RICOS EN ESTOS NUTRIENTES:")
        print("   • VITAMINA D: Pescado graso (salmón, atún), yemas de huevo, sol")
        print("   • VITAMINA B12: Carnes rojas, pescado, lácteos, huevos")
        print("   • VITAMINA C: Frutas cítricas, kiwi, fresas, pimientos, brócoli")
        print("   • MAGNESIO: Semillas de calabaza, almendras, espinacas, aguacate")
        print("   • HIERRO: Carne roja, lentejas, espinacas, quinoa")
        print("   • CALCIO: Lácteos sin grasa, tofu, brócoli, almendras")
        
    elif objetivo_opcion == '3':  # Ganar músculo
        print("🌟 Para ganar músculo, enfócate en estos micronutrientes:")
        print("   • VITAMINA D: Mejora la fuerza y función muscular")
        print("   • VITAMINA B6: Ayuda en la síntesis de proteínas")
        print("   • VITAMINA C: Produce colágeno para tejidos conectivos")
        print("   • ZINC: Importante para la síntesis de proteínas")
        print("   • MAGNESIO: Relajación muscular y previene calambres")
        print("   • FÓLICO: Ayuda en la reparación celular muscular")
        
        print("\n🥗 ALIMENTOS RICOS EN ESTOS NUTRIENTES:")
        print("   • VITAMINA D: Pescado graso, yemas de huevo, sol")
        print("   • VITAMINA B6: Pollo, pavo, plátanos, aguacate")
        print("   • VITAMINA C: Frutas cítricas, kiwi, pimientos, brócoli")
        print("   • ZINC: Carne roja, mariscos, legumbres, semillas")
        print("   • MAGNESIO: Chocolate oscuro, almendras, espinacas, aguacate")
        print("   • FÓLICO: Espinacas, brócoli, lentejas, aguacate")
        
    else:  # Mantener
        print("🌟 Para mantener salud, enfócate en estos micronutrientes:")
        print("   • VITAMINA A: Para la visión y sistema inmunológico")
        print("   • VITAMINA E: Antioxidante para células")
        print("   • VITAMINA K: Para la coagulación y huesos")
        print("   • SELENIO: Antioxidante y sistema inmunológico")
        print("   • POTASIO: Regula la presión arterial")
        print("   • FÓSFORO: Para huesos y energía celular")
        
        print("\n🥗 ALIMENTOS RICOS EN ESTOS NUTRIENTES:")
        print("   • VITAMINA A: Zanahorias, batatas, espinacas, hígado")
        print("   • VITAMINA E: Semillas, aceites vegetales, nueces")
        print("   • VITAMINA K: Brócoli, espinacas, col rizada")
        print("   • SELENIO: Mariscos, carne, nueces, semillas")
        print("   • POTASIO: Plátanos, patatas, espinacas, frijoles")
        print("   • FÓSFORO: Lácteos, carne, pescado, legumbres")
    
    # Suplementación recomendada
    print("\n💊 SUPLEMENTACIÓN RECOMENDADA:")
    if objetivo_opcion == '2':  # Perder peso
        print("• Si no consumes pescado 3 veces/semana: Omega-3 (1000mg)")
        print("• Si no te expones al sol: Vitamina D (1000-2000 IU)")
        print("• Si consumes pocos vegetales: Multivitamínico básico")
        print("• Pre-entrenamiento (si entrenas por la mañana): Cafeína (100-200mg)")
        
    elif objetivo_opcion == '3':  # Ganar músculo
        print("• Proteína en polvo (1-2 scoops al día, post-entrenamiento)")
        print("• Creatina monohidrato (3-5g al día)")
        print("• Si no consumes suficiente proteína: BCAA")
        print("• Si no te expones al sol: Vitamina D (2000-3000 IU)")
        print("• Multivitamínico para cubrir necesidades aumentadas")
        
    else:  # Mantener
        print("• Multivitamínico básico si consumes pocas frutas y verduras")
        print("• Omega-3 si no consumes pescado regularmente")
        print("• Vitamina D si no te expones al sol")
    
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
    print("• Los suplementos son complementos, no reemplazos de una buena alimentación")

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
- Glúteos: 5x15
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
        # ... (resto de las rutinas como en la versión anterior)
    }
    
    # Obtener la rutina según la actividad preferida y nivel de experiencia
    rutina_seleccionada = rutinas.get(actividad, {}).get(nivel, "Rutina no disponible para tu selección")
    
    return rutina_seleccionada

# Ejecutar la aplicación
if __name__ == "__main__":
    calcular_calorias()