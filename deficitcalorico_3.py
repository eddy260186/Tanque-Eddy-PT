import math
import csv # Importamos el módulo csv para un posible futuro almacenamiento estructurado

# --- FUNCIONES DE CÁLCULO ---

def calcular_tmb(genero, peso, estatura_m, edad):
    """
    Calcula la Tasa Metabólica Basal (TMB) usando la fórmula de Mifflin-St Jeor.
    Parámetros:
    - genero (str): 'hombre' o 'mujer'.
    - peso (float): Peso en kilogramos.
    - estatura_m (float): Estatura en metros.
    - edad (int): Edad en años.
    Retorna:
    - float: La TMB en calorías.
    """
    estatura_cm = estatura_m * 100 # Convertir metros a centímetros para la fórmula
    if genero.lower() == 'hombre':
        tmb = (10 * peso) + (6.25 * estatura_cm) - (5 * edad) + 5
    else: # Mujer
        tmb = (10 * peso) + (6.25 * estatura_cm) - (5 * edad) - 161
    return tmb

def calcular_tdee(tmb, dias_ejercicio):
    """
    Calcula el Gasto Energético Diario Total (TDEE) basado en el nivel de actividad.
    Parámetros:
    - tmb (float): Tasa Metabólica Basal.
    - dias_ejercicio (int): Número de días por semana que se realiza ejercicio.
    Retorna:
    - float: El TDEE en calorías.
    """
    if dias_ejercicio <= 0:
        factor_actividad = 1.2  # Sedentario (poco o ningún ejercicio)
    elif 1 <= dias_ejercicio <= 3:
        factor_actividad = 1.375 # Actividad ligera (ejercicio ligero 1-3 días/semana)
    elif 4 <= dias_ejercicio <= 5:
        factor_actividad = 1.55  # Actividad moderada (ejercicio moderado 3-5 días/semana)
    else: # 6-7 días
        factor_actividad = 1.725 # Actividad alta (ejercicio intenso 6-7 días/semana)
    return tmb * factor_actividad

def calcular_macros(calorias, opcion_macros):
    """
    Calcula los gramos de macronutrientes según el plan elegido.
    Parámetros:
    - calorias (float): Calorías totales objetivo.
    - opcion_macros (str): Opción de distribución de macronutrientes ('1', '2', '3').
    Retorna:
    - tuple: Gramos de proteínas, carbohidratos, grasas y el nombre del plan de macros.
    """
    # Calorías por gramo: Proteína=4 kcal, Carbs=4 kcal, Grasa=9 kcal
    distribuciones = {
        '1': {"p": 0.30, "c": 0.40, "g": 0.30, "nombre": "Balanceada"},        # 30% Proteína / 40% Carbs / 30% Grasa
        '2': {"p": 0.40, "c": 0.25, "g": 0.35, "nombre": "Baja en Carbohidratos"}, # 40% Proteína / 25% Carbs / 35% Grasa
        '3': {"p": 0.25, "c": 0.55, "g": 0.20, "nombre": "Alta en Carbohidratos (Deportista)"} # 25% Proteína / 55% Carbs / 20% Grasa
    }
    plan = distribuciones[opcion_macros]

    proteinas_gr = (calorias * plan["p"]) / 4
    carbs_gr = (calorias * plan["c"]) / 4
    grasas_gr = (calorias * plan["g"]) / 9

    return proteinas_gr, carbs_gr, grasas_gr, plan["nombre"]

# --- FUNCIONES DE UTILIDAD PARA VALIDACIÓN DE ENTRADA ---

def solicitar_numero(mensaje, tipo=float, minimo=0, maximo=None):
    """
    Solicita un número al usuario con validación de tipo y rango.
    Parámetros:
    - mensaje (str): Mensaje a mostrar al usuario.
    - tipo (type): Tipo de dato esperado (int o float).
    - minimo (int/float): Valor mínimo permitido.
    - maximo (int/float, opcional): Valor máximo permitido.
    Retorna:
    - int/float: El valor numérico validado.
    """
    while True:
        try:
            valor = tipo(input(mensaje))
            if valor < minimo:
                print(f"❌ Error: El valor debe ser como mínimo {minimo}.")
            elif maximo is not None and valor > maximo:
                print(f"❌ Error: El valor no puede exceder {maximo}.")
            else:
                return valor
        except ValueError:
            print(f"❌ Error: Por favor, introduce un número válido.")

def solicitar_opcion_str(mensaje, opciones_validas):
    """
    Solicita una opción de cadena al usuario con validación contra una lista de opciones válidas.
    Parámetros:
    - mensaje (str): Mensaje a mostrar al usuario.
    - opciones_validas (list): Lista de cadenas válidas permitidas.
    Retorna:
    - str: La opción de cadena validada (en minúsculas).
    """
    while True:
        valor = input(mensaje).lower() # Convertimos a minúsculas para una comparación flexible
        if valor in opciones_validas:
            return valor
        else:
            print(f"❌ Error: Por favor, elige una de las siguientes opciones: {', '.join(opciones_validas)}.")

# --- FUNCIÓN PRINCIPAL DE REGISTRO Y PLANIFICACIÓN ---

def registrar_usuario():
    """
    Guía al usuario a través del registro, calcula su plan nutricional
    y guarda los datos.
    """
    print("--- 📝 Formulario de Registro y Plan Nutricional Completo ---")

    # --- DATOS PERSONALES Y FÍSICOS ---
    nombre = input("Nombre: ").strip().title() # Elimina espacios extra y pone la primera letra en mayúscula
    apellido = input("Apellido: ").strip().title()
    genero = solicitar_opcion_str("Género (Hombre / Mujer): ", ['hombre', 'mujer'])

    edad = solicitar_numero("Edad (años): ", tipo=int, minimo=1, maximo=120) # Límite de edad razonable
    peso = solicitar_numero("Peso actual en kg (ej: 70.5): ", tipo=float, minimo=1.0, maximo=300.0) # Límite de peso razonable
    estatura = solicitar_numero("Estatura en metros (ej: 1.75): ", tipo=float, minimo=0.50, maximo=2.50) # Límite de estatura razonable

    print("\n--- Nivel de Actividad Física (basado en días de ejercicio por semana) ---")
    print("  0 días/semana: Sedentario (poco o ningún ejercicio)")
    print("  1-3 días/semana: Actividad ligera (ejercicio ligero 1-3 días/semana)")
    print("  4-5 días/semana: Actividad moderada (ejercicio moderado 3-5 días/semana)")
    print("  6-7 días/semana: Actividad alta (ejercicio intenso 6-7 días/semana)")
    dias_ejercicio = solicitar_numero("¿Cuántos días por semana realizas ejercicio (0-7)?: ", tipo=int, minimo=0, maximo=7)

    kilos_a_bajar = solicitar_numero("¿Cuántos kg quieres bajar? (ej: 5.0): ", tipo=float, minimo=0.1)

    # --- CÁLCULOS DE CALORÍAS ---
    tmb_calculada = calcular_tmb(genero, peso, estatura, edad)
    tdee_calculado = calcular_tdee(tmb_calculada, dias_ejercicio)

    print("\n--- Elige un ritmo de pérdida de peso ---")
    print("  1. Ligero: ~0.25 kg/semana (déficit de 275 kcal/día)")
    print("  2. Moderado: ~0.5 kg/semana (déficit de 550 kcal/día)")
    print("  3. Intenso: ~1.0 kg/semana (déficit de 1100 kcal/día)")
    # Mapeo de opciones a déficit calórico diario
    ritmos_deficit = {'1': 275, '2': 550, '3': 1100}
    opcion_ritmo = solicitar_opcion_str("Selecciona una opción de ritmo (1, 2, o 3): ", ['1', '2', '3'])
    deficit_diario = ritmos_deficit[opcion_ritmo]

    calorias_objetivo = tdee_calculado - deficit_diario
    # Establecer un límite mínimo de calorías por seguridad y salud
    min_calorias = 1500 if genero.lower() == 'hombre' else 1200
    if calorias_objetivo < min_calorias:
        print(f"\n⚠️ ¡ATENCIÓN! El ritmo de pérdida de peso elegido es muy agresivo.")
        print(f"   Se ha ajustado tu plan para no bajar de {min_calorias:.0f} kcal y proteger tu salud.")
        calorias_objetivo = min_calorias

    # --- SELECCIÓN DE DISTRIBUCIÓN DE MACRONUTRIENTES ---
    print("\n--- Elige una distribución de macronutrientes ---")
    print("  1. Balanceada: 30% Proteína, 40% Carbs, 30% Grasa")
    print("  2. Baja en Carbohidratos: 40% Proteína, 25% Carbs, 35% Grasa (ideal para ciertas dietas)")
    print("  3. Alta en Carbohidratos: 25% Proteína, 55% Carbs, 20% Grasa (ideal para deportistas de resistencia)")

    opcion_macros = solicitar_opcion_str("Selecciona una opción de macros (1, 2, o 3): ", ['1', '2', '3'])
    proteinas, carbohidratos, grasas, nombre_plan_macros = calcular_macros(calorias_objetivo, opcion_macros)

    # --- MOSTRAR RESULTADOS FINALES ---
    print("\n" + "="*60)
    print(f"✅ ¡Plan Nutricional Completo para {nombre} {apellido}!")
    print("="*60)
    print(f"🔥 Tu Tasa Metabólica Basal (TMB) es: {tmb_calculada:.0f} kcal/día.")
    print(f"📊 Tu Gasto Energético Diario Total (TDEE) es: {tdee_calculado:.0f} kcal/día.")
    print(f"🎯 Tu consumo calórico diario objetivo es: {calorias_objetivo:.0f} kcal/día para perder {kilos_a_bajar:.1f} kg.")
    print("-" * 60)
    print(f"🍽️ Distribución de Macronutrientes (Plan '{nombre_plan_macros}')")
    print(f"   💪 Proteínas:  {proteinas:.0f} gramos/día")
    print(f"   🍞 Carbohidratos: {carbohidratos:.0f} gramos/día")
    print(f"   🥑 Grasas:     {grasas:.0f} gramos/día")
    print("=" * 60)

    # --- Guardar datos ---
    try:
        # Opción 1: Guardar en archivo de texto simple (como lo tenías, con mejoras de formato)
        with open("registros_nutricionales.txt", "a", encoding='utf-8') as archivo:
            archivo.write(f"--- REGISTRO DE USUARIO ---\n")
            archivo.write(f"Fecha/Hora: {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            archivo.write(f"Nombre: {nombre} {apellido}\n")
            archivo.write(f"Género: {genero.capitalize()}\n")
            archivo.write(f"Edad: {edad} años\n")
            archivo.write(f"Peso: {peso} kg\n")
            archivo.write(f"Estatura: {estatura} m\n")
            archivo.write(f"Días de ejercicio/semana: {dias_ejercicio}\n")
            archivo.write(f"Kilos a bajar: {kilos_a_bajar} kg\n")
            archivo.write(f"TMB Calculada: {tmb_calculada:.0f} kcal\n")
            archivo.write(f"TDEE Calculado: {tdee_calculado:.0f} kcal\n")
            archivo.write(f"Calorías Objetivo: {calorias_objetivo:.0f} kcal\n")
            archivo.write(f"Plan de Macronutrientes: {nombre_plan_macros}\n")
            archivo.write(f"  Proteínas: {proteinas:.0f}g\n")
            archivo.write(f"  Carbohidratos: {carbohidratos:.0f}g\n")
            archivo.write(f"  Grasas: {grasas:.0f}g\n")
            archivo.write("-" * 30 + "\n\n") # Separador entre registros

        # Opción 2: Considera guardar en un archivo CSV para un manejo más estructurado
        # Esto sería útil si quieres analizar los datos con Excel o herramientas similares.
        # Descomenta y adapta si quieres probarlo:
        """
        encabezados_csv = ["Fecha", "Nombre", "Apellido", "Genero", "Edad", "Peso_kg", "Estatura_m",
                           "Dias_Ejercicio", "Kilos_a_Bajar", "TMB", "TDEE", "Calorias_Objetivo",
                           "Plan_Macros", "Proteinas_g", "Carbohidratos_g", "Grasas_g"]
        datos_usuario = {
            "Fecha": __import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "Nombre": nombre,
            "Apellido": apellido,
            "Genero": genero,
            "Edad": edad,
            "Peso_kg": peso,
            "Estatura_m": estatura,
            "Dias_Ejercicio": dias_ejercicio,
            "Kilos_a_Bajar": kilos_a_bajar,
            "TMB": f"{tmb_calculada:.0f}",
            "TDEE": f"{tdee_calculado:.0f}",
            "Calorias_Objetivo": f"{calorias_objetivo:.0f}",
            "Plan_Macros": nombre_plan_macros,
            "Proteinas_g": f"{proteinas:.0f}",
            "Carbohidratos_g": f"{carbohidratos:.0f}",
            "Grasas_g": f"{grasas:.0f}"
        }

        with open("registros_nutricionales.csv", "a", newline='', encoding='utf-8') as archivo_csv:
            writer = csv.DictWriter(archivo_csv, fieldnames=encabezados_csv)
            # Si el archivo está vacío, escribe los encabezados
            if archivo_csv.tell() == 0:
                writer.writeheader()
            writer.writerow(datos_usuario)
        """
        print("\n💾 ¡Registro y plan completo guardados con éxito!")
    except IOError as e:
        print(f"\n❌ Error al guardar el archivo: {e}")
    except Exception as e: # Captura cualquier otro error inesperado al guardar
        print(f"\n❌ Ocurrió un error inesperado al guardar: {e}")

# --- Iniciar la aplicación ---
if __name__ == "__main__":
    registrar_usuario()