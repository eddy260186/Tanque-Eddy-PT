import math

def calcular_tmb(genero, peso, estatura_m, edad):
    """Calcula la Tasa Metabólica Basal (TMB) usando la fórmula de Mifflin-St Jeor."""
    estatura_cm = estatura_m * 100
    if genero.lower() == 'hombre':
        # Fórmula para hombres: 10 * peso (kg) + 6.25 * estatura (cm) - 5 * edad (años) + 5
        tmb = (10 * peso) + (6.25 * estatura_cm) - (5 * edad) + 5
    else: # Se asume mujer por defecto si no es 'hombre'
        # Fórmula para mujeres: 10 * peso (kg) + 6.25 * estatura (cm) - 5 * edad (años) - 161
        tmb = (10 * peso) + (6.25 * estatura_cm) - (5 * edad) - 161
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
    """Función mejorada para registrar un usuario, crear un plan flexible y guardar los datos."""

    print("--- 📝 Formulario de Registro y Plan Nutricional Avanzado ---")

    # --- DATOS PERSONALES Y FÍSICOS ---
    nombre = input("Nombre: ")
    apellido = input("Apellido: ")
    while True:
        genero = input("Género (Hombre / Mujer): ")
        if genero.lower() in ['hombre', 'mujer']:
            break
        else:
            print("❌ Error: Por favor, introduce 'Hombre' o 'Mujer'.")
    
    # Bloques de validación para datos numéricos
    def solicitar_numero(mensaje, tipo=int, minimo=0):
        while True:
            try:
                valor = tipo(input(mensaje))
                if valor >= minimo:
                    return valor
                else:
                    print(f"❌ Error: El valor debe ser como mínimo {minimo}.")
            except ValueError:
                print(f"❌ Error: Por favor, introduce un número válido.")

    edad = solicitar_numero("Edad: ", tipo=int, minimo=1)
    peso = solicitar_numero("Peso actual en kg (ej: 70.5): ", tipo=float, minimo=1)
    estatura = solicitar_numero("Estatura en metros (ej: 1.75): ", tipo=float, minimo=0.5)
    dias_ejercicio = solicitar_numero("¿Cuántos días por semana realizas ejercicio (0-7)?: ", tipo=int, minimo=0)
    kilos_a_bajar = solicitar_numero("¿Cuántos kg quieres bajar?: ", tipo=float, minimo=0.1)

    # --- CÁLCULOS BASE ---
    tmb_calculada = calcular_tmb(genero, peso, estatura, edad)
    tdee_calculado = calcular_tdee(tmb_calculada, dias_ejercicio)

    # --- SELECCIÓN DE OBJETIVO Y RITMO ---
    print("\n--- Elige un ritmo de pérdida de peso ---")
    print("1. Ligero (Recomendado para empezar, ~0.25 kg/semana)")
    print("2. Moderado (Sostenible y efectivo, ~0.5 kg/semana)")
    print("3. Intenso (Exigente, requiere supervisión, ~1.0 kg/semana)")
    
    ritmos_deficit = {'1': 275, '2': 550, '3': 1100}
    ritmos_nombre = {'1': "Ligero", '2': "Moderado", '3': "Intenso"}
    
    while True:
        opcion = input("Selecciona una opción (1, 2, o 3): ")
        if opcion in ritmos_deficit:
            deficit_diario = ritmos_deficit[opcion]
            ritmo_elegido = ritmos_nombre[opcion]
            break
        else:
            print("❌ Opción no válida. Inténtalo de nuevo.")

    calorias_objetivo = tdee_calculado - deficit_diario

    # --- AJUSTE DE SEGURIDAD ---
    # Evitar que las calorías bajen de un umbral peligroso
    min_calorias = 1500 if genero.lower() == 'hombre' else 1200
    if calorias_objetivo < min_calorias:
        print("\n⚠️ ¡ATENCIÓN! El ritmo 'Intenso' resulta en una ingesta calórica demasiado baja para ti.")
        calorias_objetivo = min_calorias
        deficit_diario = tdee_calculado - calorias_objetivo
        ritmo_elegido = "Ajustado por Seguridad"
        print(f"Hemos ajustado tu plan para no bajar de {min_calorias} kcal/día.")
        print("Esto es para proteger tu salud. La pérdida de peso será más lenta pero segura.")

    # --- CÁLCULO DE PROYECCIONES ---
    # Basado en que 1 kg de grasa corporal son ~7700 kcal
    perdida_diaria_kg = deficit_diario / 7700
    perdida_semanal_kg = perdida_diaria_kg * 7
    perdida_mensual_kg = perdida_diaria_kg * 30.44  # Promedio de días en un mes
    
    dias_necesarios = math.ceil(kilos_a_bajar / perdida_diaria_kg) if perdida_diaria_kg > 0 else float('inf')
    semanas_necesarias = dias_necesarios / 7
    meses_necesarios = dias_necesarios / 30.44

    # --- MOSTRAR RESULTADOS DETALLADOS ---
    print("\n" + "="*50)
    print(f"✅ ¡Excelente, {nombre}! Aquí está tu plan detallado:")
    print("="*50)
    print(f"🔥 Tu Metabolismo Basal (TMB) es: {tmb_calculada:.0f} kcal/día.")
    print(f"🏃 Tu Mantenimiento Calórico (TDEE) es: {tdee_calculado:.0f} kcal/día.")
    print(f"🎯 Has elegido un ritmo: '{ritmo_elegido}'")
    print(f"🥗 Tu consumo calórico diario objetivo es: {calorias_objetivo:.0f} kcal/día.")
    print("-"*50)
    print("🗓️ Con este plan, tu pérdida de peso proyectada es:")
    print(f"   - Por día: {perdida_diaria_kg * 1000:.0f} gramos")
    print(f"   - Por semana: {perdida_semanal_kg:.2f} kg")
    print(f"   - Por mes: {perdida_mensual_kg:.2f} kg")
    print("-"*50)
    print(f"🏁 Para alcanzar tu meta de bajar {kilos_a_bajar} kg, necesitarás aproximadamente:")
    print(f"   - {dias_necesarios} días")
    print(f"   - O {semanas_necesarias:.1f} semanas")
    print(f"   - O {meses_necesarios:.1f} meses")
    print("="*50)
    print("\n💡 Recuerda: la consistencia es clave. ¡Mucho éxito en tu camino!")


    # --- GUARDAR DATOS EN ARCHIVO ---
    try:
        with open("registros_usuarios_avanzado.txt", "a", encoding='utf-8') as archivo:
            archivo.write(f"Nombre: {nombre} {apellido}, Genero: {genero}, Edad: {edad}, "
                        f"Peso: {peso} kg, Estatura: {estatura} m, Dias Ejercicio: {dias_ejercicio}, "
                        f"Objetivo: Bajar {kilos_a_bajar} kg, Ritmo: {ritmo_elegido}, "
                        f"TMB: {tmb_calculada:.0f}, TDEE: {tdee_calculado:.0f}, "
                        f"Calorías Objetivo: {calorias_objetivo:.0f}\n")
        print("\n💾 ¡Registro y plan detallado guardados con éxito!")
    except IOError as e:
        print(f"\n❌ Error al guardar el archivo: {e}")

# --- Iniciar la aplicación ---
if __name__ == "__main__":
    registrar_usuario()