def convertir_tiempo(cantidad, unidad_origen, unidad_destino):
    # Definir los factores de conversión para diferentes unidades de tiempo
    omvandlingsfaktorer = {
        "milisegundo": 0.001,
        "segundo": 1,
        "minuto": 60,
        "hora": 3600,
        "dia": 86400,
        "semana": 604800,
        "mes": 2629800,
        "año": 31557600,
        "década": 315576000,
        "siglo": 3155760000
    }

    try:
        # Convertir la cantidad desde la unidad de origen a la unidad de destino
        resultado = cantidad * omvandlingsfaktorer[unidad_origen] / omvandlingsfaktorer[unidad_destino]
        return resultado
    except KeyError:
        return "Las unidades proporcionadas no son válidas."


# Solicitar al usuario que ingrese la cantidad y las unidades de origen y destino
cantidad = float(input("Ingrese la cantidad de tiempo a convertir: "))
unidad_origen = input("Ingrese la unidad de tiempo de origen (milisegundo, segundo, hora, día, semana, mes, año, decada, siglo): ").lower()
unidad_destino = input("Ingrese la unidad de tiempo de destino (milisegundo, segundo, hora, día, semana, mes, año, decada, siglo): ").lower()

# Verificar la conversión y mostrar el resultado
resultado = convertir_tiempo(cantidad, unidad_origen, unidad_destino)
if isinstance(resultado, str):
    print(resultado)
else:
    print(f"{cantidad} {unidad_origen} es igual a {resultado} {unidad_destino}")

