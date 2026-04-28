import math
import csv
import datetime

# --- FUNCIONES DE CÁLCULO ---

def calcular_tmb(genero_simplificado, peso, estatura_cm, edad):
    """
    Calcula la Tasa Metabólica Basal (TMB) usando la fórmula de Mifflin-St Jeor.
    Parámetros:
    - genero_simplificado (str): 'm' para masculino o 'f' para femenino.
    - peso (float): Peso en kilogramos.
    - estatura_cm (float): Estatura en centímetros.
    - edad (int): Edad en años.
    Retorna:
    - float: La TMB en calorías.
    """
    genero_completo = 'hombre' if genero_simplificado.lower() == 'm' else 'mujer'

    if genero_completo == 'hombre':
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
        factor_actividad = 1.2
    elif 1 <= dias_ejercicio <= 3:
        factor_actividad = 1.375
    elif 4 <= dias_ejercicio <= 5:
        factor_actividad = 1.55
    else: # 6-7 días
        factor_actividad = 1.725
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
    distribuciones = {
        '1': {"p": 0.30, "c": 0.40, "g": 0.30, "nombre": "Balanceada"},
        '2': {"p": 0.40, "c": 0.25, "g": 0.35, "nombre": "Baja en Carbohidratos"},
        '3': {"p": 0.25, "c": 0.55, "g": 0.20, "nombre": "Alta en Carbohidratos (Deportista)"}
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
        valor = input(mensaje).lower()
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
    nombre = input("Nombre: ").strip().title()
    apellido = input("Apellido: ").strip().title()
    genero = solicitar_opcion_str("Género (M/F): ", ['m', 'f'])

    edad = solicitar_numero("Edad (años): ", tipo=int, minimo=1, maximo=120)
    peso = solicitar_numero("Peso actual en kg (ej: 70.5): ", tipo=float, minimo=1.0, maximo=300.0)
    estatura_cm = solicitar_numero("Estatura en cm (ej: 175): ", tipo=float, minimo=50.0, maximo=250.0)

    print("\n--- Nivel de Actividad Física (basado en días de ejercicio por semana) ---")
    print("   0 días/semana: Sedentario (poco o ningún ejercicio)")
    print("   1-3 días/semana: Actividad ligera (ejercicio ligero 1-3 días/semana)")
    print("   4-5 días/semana: Actividad moderada (ejercicio moderado 3-5 días/semana)")
    print("   6-7 días/semana: Actividad alta (ejercicio intenso 6-7 días/semana)")
    dias_ejercicio = solicitar_numero("¿Cuántos días por semana realizas ejercicio (0-7)?: ", tipo=int, minimo=0, maximo=7)

    # --- CÁLCULOS BASE ---
    tmb_calculada = calcular_tmb(genero, peso, estatura_cm, edad)
    tdee_calculado = calcular_tdee(tmb_calculada, dias_ejercicio)

    # --- SELECCIÓN DE OBJETIVO ---
    print("\n--- ¿Cuál es tu objetivo principal? ---")
    print("   1. Pérdida de Peso")
    print("   2. Mantenimiento de Peso")
    print("   3. Ganancia de Masa Muscular")
    opcion_objetivo = solicitar_opcion_str("Selecciona tu objetivo (1, 2, o 3): ", ['1', '2', '3'])

    calorias_objetivo = 0
    objetivo_texto = ""
    kilos_a_cambiar = 0
    plazo_cantidad_meses = 0 # Variable para almacenar el plazo en meses

    if opcion_objetivo == '1': # Pérdida de Peso
        objetivo_texto = "Pérdida de Peso"
        kilos_a_cambiar = solicitar_numero("¿Cuántos kg quieres bajar? (ej: 5.0): ", tipo=float, minimo=0.1)

        # Preguntar en cuánto tiempo (meses)
        plazo_cantidad_meses = solicitar_numero("¿En cuántos meses quieres lograr tu pérdida de peso? (ej: 3): ", tipo=int, minimo=1)
        
        total_dias = plazo_cantidad_meses * 30.437 # Promedio de días al mes
        
        # 1 kg de grasa equivale a aproximadamente 7700 kcal
        total_calorias_a_quemar = kilos_a_cambiar * 7700
        
        deficit_diario_requerido = 0
        if total_dias > 0:
            deficit_diario_requerido = total_calorias_a_quemar / total_dias
        
        calorias_objetivo = tdee_calculado - deficit_diario_requerido

        # Calcular ritmo de pérdida de peso por mes
        ritmo_mensual_kg = (deficit_diario_requerido * 30.437) / 7700

        print(f"\n📈 Para perder {kilos_a_cambiar:.1f} kg en {plazo_cantidad_meses} mes(es):")
        print(f"   Necesitas un déficit diario de aproximadamente {deficit_diario_requerido:.0f} kcal.")
        print(f"   Esto equivale a una pérdida de peso de aproximadamente {ritmo_mensual_kg:.2f} kg por mes.")


        # Establecer un límite mínimo de calorías por seguridad y salud
        min_calorias = 1500 if genero.lower() == 'm' else 1200
        if calorias_objetivo < min_calorias:
            print(f"\n⚠️ ¡ATENCIÓN! El plan de pérdida de peso es muy agresivo para el tiempo establecido.")
            print(f"   Se ha ajustado tu plan para no bajar de {min_calorias:.0f} kcal y proteger tu salud.")
            calorias_objetivo = min_calorias
            # Recalcular el ritmo de pérdida de peso con el nuevo objetivo calórico
            nuevo_deficit_diario = tdee_calculado - calorias_objetivo
            ritmo_mensual_kg_ajustado = (nuevo_deficit_diario * 30.437) / 7700
            print(f"   Con este ajuste, tu nueva estimación es perder {ritmo_mensual_kg_ajustado:.2f} kg por mes.")


    elif opcion_objetivo == '2': # Mantenimiento de Peso
        objetivo_texto = "Mantenimiento de Peso"
        calorias_objetivo = tdee_calculado
        print(f"\n✅ Tu objetivo es mantener tu peso. Tu consumo calórico diario será tu TDEE.")

    else: # Ganancia de Masa Muscular (opcion_objetivo == '3')
        objetivo_texto = "Ganancia de Masa Muscular"
        print("\n--- Elige un superávit calórico para la ganancia de masa muscular ---")
        print("   1. Moderado: +250 kcal/día (ganancia gradual, menos grasa)")
        print("   2. Alto: +500 kcal/día (ganancia más rápida, posible más grasa)")
        opcion_superavit = solicitar_opcion_str("Selecciona una opción de superávit (1 o 2): ", ['1', '2'])
        superavit_diario = 250 if opcion_superavit == '1' else 500
        calorias_objetivo = tdee_calculado + superavit_diario
        kilos_a_cambiar = solicitar_numero("¿Cuántos kg de masa muscular quieres ganar? (ej: 3.0): ", tipo=float, minimo=0.1)


    # --- SELECCIÓN DE DISTRIBUCIÓN DE MACRONUTRIENTES ---
    print("\n--- Elige una distribución de macronutrientes ---")
    print("   1. Balanceada: 30% Proteína, 40% Carbs, 30% Grasa")
    print("   2. Baja en Carbohidratos: 40% Proteína, 25% Carbs, 35% Grasa (ideal para ciertas dietas o control de insulina)")
    print("   3. Alta en Carbohidratos: 25% Proteína, 55% Carbs, 20% Grasa (ideal para deportistas de resistencia o alta energía)")

    opcion_macros = solicitar_opcion_str("Selecciona una opción de macros (1, 2, o 3): ", ['1', '2', '3'])
    proteinas, carbohidratos, grasas, nombre_plan_macros = calcular_macros(calorias_objetivo, opcion_macros)

    # --- MOSTRAR RESULTADOS FINALES ---
    print("\n" + "="*60)
    print(f"✅ ¡Plan Nutricional Completo para {nombre} {apellido}!")
    print("="*60)
    print(f"🔥 Tu Tasa Metabólica Basal (TMB) es: {tmb_calculada:.0f} kcal/día.")
    print(f"📊 Tu Gasto Energético Diario Total (TDEE) es: {tdee_calculado:.0f} kcal/día.")
    print(f"🎯 Tu objetivo es: {objetivo_texto}")

    if opcion_objetivo == '1':
        print(f"   Para perder {kilos_a_cambiar:.1f} kg en {plazo_cantidad_meses} mes(es),")
        print(f"   tu consumo calórico diario objetivo es: {calorias_objetivo:.0f} kcal/día.")
        print(f"   Esto implica un déficit diario de aproximadamente {deficit_diario_requerido:.0f} kcal.")
        print(f"   Podrías esperar perder aproximadamente {ritmo_mensual_kg:.2f} kg por mes.")
    elif opcion_objetivo == '3':
        print(f"   Para ganar {kilos_a_cambiar:.1f} kg de masa muscular, tu consumo calórico diario objetivo es: {calorias_objetivo:.0f} kcal/día.")
    else: # Mantenimiento
        print(f"   Tu consumo calórico diario objetivo para mantenimiento es: {calorias_objetivo:.0f} kcal/día.")

    print("-" * 60)
    print(f"🍽️ Distribución de Macronutrientes (Plan '{nombre_plan_macros}')")
    print(f"   💪 Proteínas:   {proteinas:.0f} gramos/día")
    print(f"   🍞 Carbohidratos: {carbohidratos:.0f} gramos/día")
    print(f"   🥑 Grasas:      {grasas:.0f} gramos/día")
    print("=" * 60)

    # --- GUÍA DE ALIMENTACIÓN POR COMIDA ---
    print("\n" + "="*60)
    print("📋 Guía de Alimentación por Comida (Estimado)")
    print("    *Distribución: Desayuno 25% | Almuerzo 35% | Merienda 15% | Cena 25%")
    print("="*60)

    distribucion_comidas = {
        "Desayuno": 0.25,
        "Almuerzo": 0.35,
        "Merienda": 0.15,
        "Cena": 0.25
    }

    for comida, porcentaje in distribucion_comidas.items():
        calorias_comida = calorias_objetivo * porcentaje
        proteinas_comida = proteinas * porcentaje
        carbohidratos_comida = carbohidratos * porcentaje
        grasas_comida = grasas * porcentaje

        print(f"--- {comida} ({porcentaje*100:.0f}%) ---")
        print(f"   Calorías: {calorias_comida:.0f} kcal")
        print(f"   Proteínas: {proteinas_comida:.0f} g")
        print(f"   Carbohidratos: {carbohidratos_comida:.0f} g")
        print(f"   Grasas: {grasas_comida:.0f} g")
        print("-" * 25)

    print("="*60)

    # --- Guardar datos ---
    try:
        with open("registros_nutricionales.txt", "a", encoding='utf-8') as archivo:
            archivo.write(f"--- REGISTRO DE USUARIO ---\n")
            archivo.write(f"Fecha/Hora: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            archivo.write(f"Nombre: {nombre} {apellido}\n")
            archivo.write(f"Género: {'Masculino' if genero == 'm' else 'Femenino'}\n")
            archivo.write(f"Edad: {edad} años\n")
            archivo.write(f"Peso: {peso} kg\n")
            archivo.write(f"Estatura: {estatura_cm} cm\n")
            archivo.write(f"Días de ejercicio/semana: {dias_ejercicio}\n")
            archivo.write(f"Objetivo: {objetivo_texto}\n")
            if opcion_objetivo == '1':
                archivo.write(f"Kilos a bajar: {kilos_a_cambiar} kg\n")
                archivo.write(f"Plazo para bajar peso: {plazo_cantidad_meses} mes(es)\n")
                archivo.write(f"Déficit diario requerido: {deficit_diario_requerido:.0f} kcal\n")
                archivo.write(f"Ritmo mensual estimado: {ritmo_mensual_kg:.2f} kg/mes\n")
            elif opcion_objetivo == '3':
                archivo.write(f"Kilos a ganar: {kilos_a_cambiar} kg\n")
            archivo.write(f"TMB Calculada: {tmb_calculada:.0f} kcal\n")
            archivo.write(f"TDEE Calculado: {tdee_calculado:.0f} kcal\n")
            archivo.write(f"Calorías Objetivo: {calorias_objetivo:.0f} kcal\n")
            archivo.write(f"Plan de Macronutrientes: {nombre_plan_macros}\n")
            archivo.write(f"   Proteínas: {proteinas:.0f}g\n")
            archivo.write(f"   Carbohidratos: {carbohidratos:.0f}g\n")
            archivo.write(f"   Grasas: {grasas:.0f}g\n")

            archivo.write("\n--- Guía de Alimentación por Comida ---\n")
            for comida, porcentaje in distribucion_comidas.items():
                calorias_comida = calorias_objetivo * porcentaje
                proteinas_comida = proteinas * porcentaje
                carbohidratos_comida = carbohidratos * porcentaje
                grasas_comida = grasas * porcentaje
                archivo.write(f"{comida}: {calorias_comida:.0f} kcal | P: {proteinas_comida:.0f}g | C: {carbohidratos_comida:.0f}g | G: {grasas_comida:.0f}g\n")
            archivo.write("-" * 30 + "\n\n")

        print("\n💾 ¡Registro y plan completo guardados con éxito!")
    except IOError as e:
        print(f"\n❌ Error al guardar el archivo: {e}")
    except Exception as e:
        print(f"\n❌ Ocurrió un error inesperado al guardar: {e}")

# --- Iniciar la aplicación ---
if __name__ == "__main__":
    registrar_usuario()