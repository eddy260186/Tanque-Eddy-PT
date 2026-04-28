def calcular_agua(peso, estatura_m, actividad, clima, genero):
    # Definir factores de conversión según el tipo de actividad física, clima y género
    if actividad == "sedentario":
        factor_actividad = 0.35
    elif actividad == "ligera":
        factor_actividad = 0.5
    elif actividad == "moderada":
        factor_actividad = 0.65
    elif actividad == "activa":
        factor_actividad = 0.8
    elif actividad == "muy activa":
        factor_actividad = 1
    
    # Factores de ajuste para diferentes climas
    if clima == "calido":
        factor_clima = 1.2
    elif clima == "templado":
        factor_clima = 1
    elif clima == "frio":
        factor_clima = 0.8
    
    # Factores de ajuste según el género
    if genero == "masculino":
        factor_genero = 1.1  # Hombres suelen necesitar más agua que mujeres
    elif genero == "femenino":
        factor_genero = 1

    agua_recomendada = ((peso * 0.033) + (estatura_m * 0.03) + factor_actividad) * factor_clima * factor_genero

    return agua_recomendada

# Lista de opciones para el nivel de actividad física, clima y género
opciones_actividad = ["sedentario", "ligera", "moderada", "activa", "muy activa"]
opciones_clima = ["calido", "templado", "frio"]
opciones_genero = ["masculino", "femenino"]

# Solicitar datos al usuario
nombre = input("Ingrese su nombre: ")
edad = int(input("Ingrese su edad: "))

print("\nSeleccione su género:")
for i, opcion in enumerate(opciones_genero, 1):
    print(f"{i}. {opcion}")

opcion_genero = int(input("Ingrese el número correspondiente a su género: "))
genero = opciones_genero[opcion_genero - 1]

peso = int(input("Ingrese su peso en kg: "))
estatura_cm = int(input("Ingrese su estatura en centímetros: "))  # Se ingresa en centímetros

# Convertir estatura de cm a m
estatura_m = estatura_cm / 100

print("\nSeleccione su nivel de actividad física:")
for i, opcion in enumerate(opciones_actividad, 1):
    print(f"{i}. {opcion}")

opcion_actividad = int(input("Ingrese el número correspondiente a su nivel de actividad física: "))
actividad = opciones_actividad[opcion_actividad - 1]

print("\nSeleccione el clima donde vive:")
for i, opcion in enumerate(opciones_clima, 1):
    print(f"{i}. {opcion}")

opcion_clima = int(input("Ingrese el número correspondiente al clima: "))
clima = opciones_clima[opcion_clima - 1]

cantidad_agua = calcular_agua(peso, estatura_m, actividad, clima, genero)
print("\nHola,", nombre + ",")
print("Basado en tus datos y el clima donde vives, la cantidad recomendada de agua a beber es:", round(cantidad_agua, 2), "litros por día.")
