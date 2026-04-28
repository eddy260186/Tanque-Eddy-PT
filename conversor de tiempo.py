def convertir_tiempo(cantidad, unidad_origen, unidad_destino):
    # Definir los factores de conversión para diferentes unidades de tiempo
    omvandlingsfaktorer = {
        "1. milisegundo": 0.001,
        "2. segundo": 1,
        "3. minuto": 60,
        "4. hora": 3600,
        "5. día": 86400,
        "6. semana": 604800,
        "7. mes": 2629800,
        "8. año": 31557600,
        "9. década": 315576000,
        "10. siglo": 3155760000
    }

    try:
        # Convertir la cantidad desde la unidad de origen a la unidad de destino
        resultado = cantidad * omvandlingsfaktorer[unidad_origen] / omvandlingsfaktorer[unidad_destino]
        if unidad_origen == "10. siglo" and unidad_destino == "6. semana":
            resultado = round(resultado)  # Redondear el resultado al convertir siglos a semanas
        return resultado
    except KeyError:
        return "Las unidades proporcionadas no son válidas."


# Solicitar al usuario que ingrese la cantidad y las unidades de origen y destino
cantidad = float(input("Ingrese la cantidad de tiempo a convertir: "))
print("Unidades de tiempo disponibles para la conversión:")
print("1. milisegundo\n2. segundo\n3. minuto\n4. hora\n5. día\n6. semana\n7. mes\n8. año\n9. década\n10. siglo")
unidad_origen = input("Ingrese el número correspondiente a la unidad de tiempo de origen: ")
unidad_destino = input("Ingrese el número correspondiente a la unidad de tiempo de destino: ")

# Mapear el número de unidad elegido por el usuario a la unidad de tiempo correspondiente
unidades = {
    "1": "1. milisegundo",
    "2": "2. segundo",
    "3": "3. minuto",
    "4": "4. hora",
    "5": "5. día",
    "6": "6. semana",
    "7": "7. mes",
    "8": "8. año",
    "9": "9. década",
    "10": "10. siglo"
}

unidad_origen = unidades.get(unidad_origen)
unidad_destino = unidades.get(unidad_destino)

# Verificar la conversión y mostrar el resultado
resultado = convertir_tiempo(cantidad, unidad_origen, unidad_destino)
if isinstance(resultado, str):
    print(resultado)
else:
    print(f"{cantidad} {unidad_origen} es igual a {resultado} {unidad_destino}")
 