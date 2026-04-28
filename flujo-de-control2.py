# Solicitar al usuario que ingrese su edad y si tiene licencia
edad = int(input("Ingresa tu edad: "))
tiene_licencia = input("¿Tienes licencia para conducir? (Sí/No): ").strip().lower()

# Definir las respuestas válidas para tener licencia
respuestas_validas = {"sí", "si", "yes", "no"}

if edad < 18:
    print("No puedes conducir aún. Debes tener 18 años y contar con una licencia")
elif edad >= 18 and tiene_licencia in respuestas_validas:
    if tiene_licencia in {"sí", "si", "yes"}:
        print("Puedes conducir")
    else:
        print("No puedes conducir. Necesitas contar con una licencia")
else:
    print("Entrada inválida. Por favor, ingresa 'Sí' o 'No' para indicar si tienes licencia.")




