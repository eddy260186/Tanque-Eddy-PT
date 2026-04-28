def obtener_temperatura_historica(ciudad, fecha):
    # Aquí simularemos la obtención de la temperatura histórica
    # en lugar de hacer una solicitud real a una API externa
    
    # En un escenario real, esta función debería hacer una solicitud
    # a una API o consultar una base de datos de registros climáticos históricos
    
    # Simulamos la obtención de la temperatura histórica como 25 grados Celsius
    temperatura = 25
    
    return temperatura

def estimar_temperatura_actual():
    ciudad = input("Ingrese su ubicación actual (ciudad): ")
    fecha = input("Ingrese la fecha exacta (YYYY-MM-DD): ")

    temperatura_historica = obtener_temperatura_historica(ciudad, fecha)

    if temperatura_historica is not None:
        print(f"Basado en registros históricos, se estima que la temperatura actual en {ciudad} para la fecha {fecha} es de {temperatura_historica} grados Celsius.")
    else:
        print("No se pudo obtener la temperatura histórica para la ubicación y fecha proporcionadas.")

# Ejemplo de uso
estimar_temperatura_actual()
