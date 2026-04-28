def calcular_calorias():
    print("=== Calculadora de Calorías Personalizada ===\n")
    
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
    elif 18.5 <= imc < 25:
        clasificacion_imc = "Peso normal"
    elif 25 <= imc < 30:
        clasificacion_imc = "Sobrepeso"
    else:
        clasificacion_imc = "Obesidad"
    
    # Nivel de actividad física
    print("\nNivel de actividad física:")
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
    
    # Calcular metabolismo basal (Mifflin-St Jeor)
    if genero == 'H':
        mb = (10 * peso_actual) + (6.25 * altura) - (5 * edad) + 5
    else:
        mb = (10 * peso_actual) + (6.25 * altura) - (5 * edad) - 161
    
    # Calcular calorías de mantenimiento
    mantenimiento = round(mb * factores[actividad])
    
    # Objetivo de peso personalizado
    print("\n=== OBJETIVO DE PESO ===")
    print("1. Mantener peso actual")
    print("2. Bajar de peso")
    print("3. Subir de peso (ganar músculo)")
    
    objetivo_opcion = input("Selecciona tu objetivo (1-3): ")
    
    if objetivo_opcion == '1':
        peso_objetivo = peso_actual
        calorias_diarias = mantenimiento
        semanas_estimadas = 0
        cambio_calorias = 0
    elif objetivo_opcion == '2':
        peso_objetivo = float(input("¿Cuántos kg quieres bajar? "))
        semanas = int(input("¿En cuántas semanas quieres lograrlo? "))
        
        # Cálculo de déficit calórico (1 kg = 7700 kcal)
        total_calorias_necesarias = (peso_actual - peso_objetivo) * 7700
        cambio_calorias = -total_calorias_necesarias / (semanas * 7)
        calorias_diarias = round(mantenimiento + cambio_calorias)
        semanas_estimadas = semanas
    elif objetivo_opcion == '3':
        peso_objetivo = float(input("¿Cuántos kg quieres subir? "))
        semanas = int(input("¿En cuántas semanas quieres lograrlo? "))
        
        # Cálculo de superávit calórico (1 kg = 7700 kcal)
        total_calorias_necesarias = (peso_objetivo - peso_actual) * 7700
        cambio_calorias = total_calorias_necesarias / (semanas * 7)
        calorias_diarias = round(mantenimiento + cambio_calorias)
        semanas_estimadas = semanas
    else:
        print("Opción inválida")
        return
    
    # Información relevante por país
    info_pais = {
        "España": {
            "alimentos": "Prioriza aceite de oliva, pescado, frutas y verduras de temporada",
            "actividad": "Caminar, senderismo o deportes tradicionales como la pelota",
            "cultura": "Las comidas suelen ser en familia, intenta no saltarte comidas y controla porciones"
        },
        "México": {
            "alimentos": "Incorpora nopal, frijoles, chayote y aguacate en tu dieta",
            "actividad": "Caminata, fútbol o danzas tradicionales",
            "cultura": "Evita excesos de tortillas y salsas muy calóricas. Opta por preparaciones al vapor o a la plancha"
        },
        "Argentina": {
            "alimentos": "Aprovecha carne magra, legumbres y lácteos. Reduce asados frecuentes",
            "actividad": "Fútbol, ciclismo o correr en parques",
            "cultura": "Las asadas son tradicionales pero calóricas. Compensa con más vegetales"
        },
        "Colombia": {
            "alimentos": "Incluye granadilla, lulo, fríjoles y pescado fresco",
            "actividad": "Ciclismo, fútbol o senderismo en montañas",
            "cultura": "Las arepas y bandejas son calóricas. Opta por versiones más ligeras"
        },
        "Perú": {
            "alimentos": "Aprovecha quinoa, camote, kiwicha y pescado como trucha",
            "actividad": "Surf, senderismo o deportes acuáticos",
            "cultura": "Evita excesos de acevichado y lomo saltado. Prefiere platos a la plancha"
        },
        "Estados Unidos": {
            "alimentos": "Prioriza proteínas magras, vegetales y granos integrales. Evita comida procesada",
            "actividad": "Caminar, levantamiento de pesas o clases de HIIT",
            "cultura": "Controla porciones en restaurantes y evita bebidas azucaradas"
        },
        "Japón": {
            "alimentos": "Aprovecha pescado, algas, tofu y verduras. Reduce arroz blanco",
            "actividad": "Caminar, tai chi o karate",
            "cultura": "Come despacio y hasta el 80% de saciedad. Evita fritos"
        },
        "Brasil": {
            "alimentos": "Incorpora arroz integral, frijoles negros, frutas tropicales y pescado",
            "actividad": "Capoeira, fútbol o jiu-jitsu",
            "cultura": "Evita excesos de feijoada y carnes grasas. Prioriza preparaciones a la parrilla"
        }
    }
    
    # Obtener información del país si está disponible
    pais_info = info_pais.get(pais, {
        "alimentos": "Busca alimentos frescos y locales. Evita alimentos procesados",
        "actividad": "Realiza actividad física que disfrutes, al menos 30 minutos al día",
        "cultura": "Cada cultura tiene sus hábitos. Intenta adaptar tu dieta a tradiciones con porciones moderadas"
    })
    
    # Mostrar resultados
    print("\n=== RESULTADOS PERSONALIZADOS ===")
    print(f"IMC actual: {imc_redondeado} - {clasificacion_imc}")
    print(f"Metabolismo basal: {round(mb)} calorías/día")
    print(f"Calorías de mantenimiento: {mantenimiento} calorías/día")
    
    if objetivo_opcion == '1':
        print(f"\nTu objetivo: Mantener {peso_actual} kg")
        print(f"Recomendación diaria: {calorias_diarias} calorías")
    elif objetivo_opcion == '2':
        print(f"\nTu objetivo: Bajar de {peso_actual} kg a {peso_objetivo} kg")
        print(f"Duración estimada: {semanas} semanas")
        print(f"Déficit calórico diario: {abs(cambio_calorias)} calorías")
        print(f"Recomendación diaria: {calorias_diarias} calorías")
    else:
        print(f"\nTu objetivo: Subir de {peso_actual} kg a {peso_objetivo} kg")
        print(f"Duración estimada: {semanas} semanas")
        print(f"Superávit calórico diario: {cambio_calorias} calorías")
        print(f"Recomendación diaria: {calorias_diarias} calorías")
    
    # Consejos adicionales según el objetivo
    print("\n=== CONSEJOS PERSONALIZADOS ===")
    if objetivo_opcion == '1':
        print("Para mantener peso:")
        print("- Mantén una dieta equilibrada")
        print("- Realiza actividad física regular")
        print("- Monitorea tu peso semanalmente")
        print("- Ajusta calorías según cambios en la actividad")
    elif objetivo_opcion == '2':
        print("Para bajar de peso:")
        print("- Combina ejercicio cardiovascular con entrenamiento de fuerza")
        print("- Prioriza proteínas magras y vegetales")
        print("- Controla porciones y evita azúcares añadidos")
        print("- Bebe al menos 2 litros de agua al día")
        
        if imc_redondeado >= 30:
            print("\n¡CUIDADO! Tu IMC indica obesidad.")
            print("Consulta a un profesional antes de iniciar cualquier dieta intensiva.")
            
        if calorias_diarias < 1200:
            print("\n⚠️ ADVERTENCIA: Tu ingesta calórica es muy baja.")
            print("Puede afectar tu salud. Considera un déficit más moderado.")
    else:
        print("Para subir de peso (ganar músculo):")
        print("- Aumenta consumo de proteínas (1.6-2.2g/kg)")
        print("- Incluye snacks saludables entre comidas")
        print("- Realiza entrenamiento de fuerza 3-4 veces/semana")
        print("- Asegura descanso adecuado (7-9 horas de sueño)")
        
        if imc_redondeado < 18.5:
            print("\n¡ATENCIÓN! Tu IMC indica bajo peso.")
            print("Consulta a un nutricionista para un plan de ganancia de peso saludable.")
            
        if calorias_diarias > 4000:
            print("\n⚠️ ADVERTENCIA: Tu ingesta calórica es muy alta.")
            print("Puede resultar en ganancia de grasa. Considera un superávit más moderado.")
    
    # Información específica por país
    print(f"\n=== RECOMENDACIONES PARA {pais} ===")
    print(f"• Alimentos recomendados: {pais_info['alimentos']}")
    print(f"• Actividades sugeridas: {pais_info['actividad']}")
    print(f"• Aspecto cultural: {pais_info['cultura']}")
    
    # Consejos adicionales según el objetivo y país
    if objetivo_opcion == '2' and "Mediterráneo" in pais:
        print("\nConsejo adicional para {pais}:")
        print("La dieta mediterránea es ideal para la pérdida de peso sostenible.")
    elif objetivo_opcion == '3' and "Latino" in pais:
        print("\nConsejo adicional para {pais}:")
        print("Las legumbres son excelentes para ganar músculo de forma económica.")
    
    print("\n=== IMPORTANTE ===")
    print("Estos valores son estimaciones individuales.")
    print("Para un plan personalizado, consulta a un nutricionista o médico.")
    print("La pérdida o ganancia de peso saludable es de 0.5-1 kg por semana.")

# Ejecutar la aplicación
if __name__ == "__main__":
    calcular_calorias()