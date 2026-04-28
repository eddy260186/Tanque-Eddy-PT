def calcular_tmb(genero, peso, estatura_m, edad):
    """Calcula la Tasa Metabólica Basal (TMB) usando la fórmula de Mifflin-St Jeor."""
    estatura_cm = estatura_m * 100
    if genero.lower() == 'hombre':
        # Fórmula para hombres: 10 * peso (kg) + 6.25 * estatura (cm) - 5 * edad (años) + 5
        tmb = (10 * peso) + (6.25 * estatura_cm) - (5 * edad) + 5
    elif genero.lower() == 'mujer':
        # Fórmula para mujeres: 10 * peso (kg) + 6.25 * estatura (cm) - 5 * edad (años) - 161
        tmb = (10 * peso) + (6.25 * estatura_cm) - (5 * edad) - 161
    else:
        # Un promedio si el género no es especificado
        tmb = (10 * peso) + (6.25 * estatura_cm) - (5 * edad) - 78
    return tmb

def calcular_tdee(tmb, dias_ejercicio):
    """Calcula el Gasto Energético Diario Total (TDEE) basado en la actividad."""
    if dias_ejercicio <= 0:
        factor_actividad = 1.2  # Sedentario
    elif 1 <= dias_ejercicio <= 3:
        factor_actividad = 1.375 # Actividad ligera
    elif 4 <= dias_ejercicio <= 5:
        factor_actividad = 1.55  # Actividad moderada
    else: # 6-7 días
        factor_actividad = 1.725 # Actividad alta
    
    return tmb * factor_actividad

def registrar_usuario():
    """Función para registrar un nuevo usuario, calcular su plan y guardar los datos."""

    print("--- 📝 Formulario de Registro y Plan Nutricional ---")

    # --- DATOS PERSONALES ---
    nombre = input("Nombre: ")
    apellido = input("Apellido: ")
    while True:
        genero = input("Género (Hombre / Mujer): ")
        if genero.lower() in ['hombre', 'mujer']:
            break
        else:
            print("Por favor, introduce 'Hombre' o 'Mujer'.")

    # --- DATOS FÍSICOS ---
    while True:
        try:
            edad = int(input("Edad: "))
            break
        except ValueError:
            print("❌ Error: Por favor, introduce un número válido para la edad.")

    while True:
        try:
            peso = float(input("Peso actual en kg (ej: 70.5): "))
            break
        except ValueError:
            print("❌ Error: Por favor, introduce un número válido para el peso.")

    while True:
        try:
            estatura = float(input("Estatura en metros (ej: 1.75): "))
            break
        except ValueError:
            print("❌ Error: Por favor, introduce un número válido para la estatura.")

    while True:
        try:
            dias_ejercicio = int(input("¿Cuántos días por semana realizas ejercicio (0-7)?: "))
            if 0 <= dias_ejercicio <= 7:
                break
            else:
                print("❌ Error: Por favor, introduce un número de días entre 0 y 7.")
        except ValueError:
            print("❌ Error: Por favor, introduce un número válido.")
    
    # --- OBJETIVOS ---
    while True:
        try:
            kilos_a_bajar = float(input("¿Cuántos kg quieres bajar?: "))
            if kilos_a_bajar > 0:
                break
            else:
                print("El objetivo debe ser mayor a 0.")
        except ValueError:
            print("❌ Error: Por favor, introduce un número válido.")

    while True:
        try:
            tiempo_semanas = int(input("¿En cuántas semanas quieres lograrlo?: "))
            if tiempo_semanas > 0:
                break
            else:
                print("El tiempo debe ser de al menos 1 semana.")
        except ValueError:
            print("❌ Error: Por favor, introduce un número válido.")
    
    # --- CÁLCULOS ---
    tmb_calculada = calcular_tmb(genero, peso, estatura, edad)
    tdee_calculado = calcular_tdee(tmb_calculada, dias_ejercicio)
    
    # Cálculo del déficit calórico
    calorias_totales_a_quemar = kilos_a_bajar * 7700  # 1 kg de grasa ≈ 7700 kcal
    dias_totales = tiempo_semanas * 7
    deficit_diario = calorias_totales_a_quemar / dias_totales
    
    calorias_objetivo = tdee_calculado - deficit_diario

    # --- MOSTRAR RESULTADOS ---
    print("\n" + "="*40)
    print(f"✅ ¡Hola, {nombre}! Aquí está tu plan personalizado:")
    print("="*40)
    print(f"🔥 Tu Metabolismo Basal (TMB) es de: {tmb_calculada:.0f} kcal/día.")
    print(f"🏃 Tu Gasto Calórico de Mantenimiento (TDEE) es de: {tdee_calculado:.0f} kcal/día.")
    print(f"🎯 Para bajar {kilos_a_bajar} kg en {tiempo_semanas} semanas, tu objetivo es:")
    print(f"🥗 Consumir aproximadamente {calorias_objetivo:.0f} kcal/día.")
    print("="*40 + "\n")

    # --- AVISO DE SEGURIDAD ---
    if deficit_diario > 1000:
        print("⚠️ ¡Atención! El déficit calórico es muy agresivo (>1000 kcal/día).")
        print("Esto puede ser perjudicial para tu salud. Considera extender el plazo.")
    elif deficit_diario < 300:
        print("💡 Nota: El déficit calórico es muy ligero (<300 kcal/día).")
        print("La pérdida de peso será lenta pero sostenible. ¡Paciencia!")
    else:
        print("👍 Tu plan de déficit calórico es saludable y sostenible. ¡Mucho éxito!")


    # --- GUARDAR DATOS ---
    try:
        with open("registros_usuarios.txt", "a", encoding='utf-8') as archivo:
            archivo.write(f"Nombre: {nombre}, Apellido: {apellido}, Genero: {genero}, Edad: {edad}, "
                        f"Peso: {peso} kg, Estatura: {estatura} m, Dias Ejercicio: {dias_ejercicio}, "
                        f"Objetivo: Bajar {kilos_a_bajar} kg en {tiempo_semanas} semanas, "
                        f"TMB: {tmb_calculada:.0f}, TDEE: {tdee_calculado:.0f}, "
                        f"Calorías Objetivo: {calorias_objetivo:.0f}\n")
        print("\n💾 ¡Registro exitoso! Todos tus datos y tu plan han sido guardados.")
    except IOError as e:
        print(f"\n❌ Error al guardar el archivo: {e}")

# --- Iniciar la aplicación ---
if __name__ == "__main__":
    registrar_usuario()