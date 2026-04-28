import math

# --- FUNCIONES DE CÁLCULO ---

def calcular_tmb(genero, peso, estatura_m, edad):
    """Calcula la Tasa Metabólica Basal (TMB) usando la fórmula de Mifflin-St Jeor."""
    estatura_cm = estatura_m * 100
    if genero.lower() == 'hombre':
        tmb = (10 * peso) + (6.25 * estatura_cm) - (5 * edad) + 5
    else:
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

def calcular_macros(calorias, opcion):
    """Calcula los gramos de macronutrientes según el plan elegido."""
    # Calorías por gramo: Proteína=4, Carbs=4, Grasa=9
    distribuciones = {
        '1': {"p": 0.30, "c": 0.40, "g": 0.30, "nombre": "Balanceada"}, # 30P/40C/30G
        '2': {"p": 0.40, "c": 0.25, "g": 0.35, "nombre": "Baja en Carbs"}, # 40P/25C/35G
        '3': {"p": 0.25, "c": 0.55, "g": 0.20, "nombre": "Alta en Carbs (Deportista)"} # 25P/55C/20G
    }
    plan = distribuciones[opcion]
    
    proteinas_gr = (calorias * plan["p"]) / 4
    carbs_gr = (calorias * plan["c"]) / 4
    grasas_gr = (calorias * plan["g"]) / 9
    
    return proteinas_gr, carbs_gr, grasas_gr, plan["nombre"]

# --- FUNCIÓN PRINCIPAL DE REGISTRO ---

def registrar_usuario():
    """Registra un usuario, crea un plan de calorías y macros, y guarda los datos."""

    print("--- 📝 Formulario de Registro y Plan Nutricional Completo ---")

    # --- DATOS PERSONALES Y FÍSICOS ---
    nombre = input("Nombre: ")
    apellido = input("Apellido: ")
    while True:
        genero = input("Género (Hombre / Mujer): ")
        if genero.lower() in ['hombre', 'mujer']:
            break
        else:
            print("❌ Error: Por favor, introduce 'Hombre' o 'Mujer'.")
    
    def solicitar_numero(mensaje, tipo=int, minimo=0):
        while True:
            try:
                valor = tipo(input(mensaje))
                if valor >= minimo: return valor
                else: print(f"❌ Error: El valor debe ser como mínimo {minimo}.")
            except ValueError: print(f"❌ Error: Por favor, introduce un número válido.")

    edad = solicitar_numero("Edad: ", tipo=int, minimo=1)
    peso = solicitar_numero("Peso actual en kg (ej: 70.5): ", tipo=float, minimo=1)
    estatura = solicitar_numero("Estatura en metros (ej: 1.75): ", tipo=float, minimo=0.5)
    dias_ejercicio = solicitar_numero("¿Cuántos días por semana realizas ejercicio (0-7)?: ", tipo=int, minimo=0)
    kilos_a_bajar = solicitar_numero("¿Cuántos kg quieres bajar?: ", tipo=float, minimo=0.1)

    # --- CÁLCULOS DE CALORÍAS ---
    tmb_calculada = calcular_tmb(genero, peso, estatura, edad)
    tdee_calculado = calcular_tdee(tmb_calculada, dias_ejercicio)

    print("\n--- Elige un ritmo de pérdida de peso ---")
    print("1. Ligero (~0.25 kg/semana) \n2. Moderado (~0.5 kg/semana) \n3. Intenso (~1.0 kg/semana)")
    ritmos_deficit = {'1': 275, '2': 550, '3': 1100}
    while True:
        opcion_ritmo = input("Selecciona una opción de ritmo (1, 2, o 3): ")
        if opcion_ritmo in ritmos_deficit:
            deficit_diario = ritmos_deficit[opcion_ritmo]
            break
        else: print("❌ Opción no válida. Inténtalo de nuevo.")
    
    calorias_objetivo = tdee_calculado - deficit_diario
    min_calorias = 1500 if genero.lower() == 'hombre' else 1200
    if calorias_objetivo < min_calorias:
        print(f"\n⚠️ ¡ATENCIÓN! El ritmo elegido es muy agresivo. Se ha ajustado tu plan para no bajar de {min_calorias} kcal y proteger tu salud.")
        calorias_objetivo = min_calorias

    # --- SELECCIÓN DE DISTRIBUCIÓN DE MACRONUTRIENTES ---
    print("\n--- Elige una distribución de macronutrientes ---")
    print("1. Balanceada (30% Proteína, 40% Carbs, 30% Grasa)")
    print("2. Baja en Carbohidratos (40% Proteína, 25% Carbs, 35% Grasa)")
    print("3. Alta en Carbohidratos (25% Proteína, 55% Carbs, 20% Grasa) - Ideal para deportistas de resistencia")
    
    while True:
        opcion_macros = input("Selecciona una opción de macros (1, 2, o 3): ")
        if opcion_macros in ['1', '2', '3']:
            break
        else:
            print("❌ Opción no válida. Inténtalo de nuevo.")

    proteinas, carbohidratos, grasas, nombre_plan_macros = calcular_macros(calorias_objetivo, opcion_macros)
    
    # --- MOSTRAR RESULTADOS FINALES ---
    print("\n" + "="*55)
    print(f"✅ ¡Plan Nutricional Completo para {nombre}!")
    print("="*55)
    print(f"🔥 Tu Gasto Calórico de Mantenimiento (TDEE) es: {tdee_calculado:.0f} kcal/día.")
    print(f"🎯 Tu consumo calórico diario objetivo es: {calorias_objetivo:.0f} kcal/día.")
    print("-"*55)
    print(f"🍽️ Distribución de Macronutrientes (Plan '{nombre_plan_macros}')")
    print(f"   💪 Proteínas:  {proteinas:.0f} gramos/día")
    print(f"   🍞 Carbohidratos: {carbohidratos:.0f} gramos/día")
    print(f"   🥑 Grasas:     {grasas:.0f} gramos/día")
    print("="*55)
    
    # --- Guardar datos ---
    try:
        with open("registros_nutricionales.txt", "a", encoding='utf-8') as archivo:
            archivo.write(f"Nombre: {nombre} {apellido}, Genero: {genero}, Peso: {peso} kg, "
                        f"Calorías Objetivo: {calorias_objetivo:.0f}, Plan Macros: {nombre_plan_macros}, "
                        f"Proteínas: {proteinas:.0f}g, Carbs: {carbohidratos:.0f}g, Grasas: {grasas:.0f}g\n")
        print("\n💾 ¡Registro y plan completo guardados con éxito!")
    except IOError as e:
        print(f"\n❌ Error al guardar el archivo: {e}")

# --- Iniciar la aplicación ---
if __name__ == "__main__":
    registrar_usuario()