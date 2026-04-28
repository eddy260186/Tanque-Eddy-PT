def contar_palabras(texto):
    """Función para contar el número de palabras en el texto."""
    return len(texto.split())

def contar_letras(texto, letra):
    """Función para contar la cantidad de veces que una letra aparece en el texto."""
    return texto.count(letra)

def primera_letra(texto):
    """Función para encontrar la primera letra del texto."""
    return texto[0] if texto else None

def ultima_letra(texto):
    """Función para encontrar la última letra del texto."""
    return texto[-1] if texto else None

def buscar_palabra(texto, palabra):
    """Función para buscar una palabra en el texto."""
    return palabra.lower() in texto.lower().split()

def mostrar_menu():
    """Función para mostrar el menú de opciones."""
    print("¿Qué deseas hacer?")
    print("1. Terminar")
    print("2. Buscar una palabra en el texto")
    opcion = input("Ingresa tu opción: ")
    return opcion

# Solicitar al usuario que ingrese un texto y convertirlo a minúsculas
texto = input("Por favor, ingresa un texto: ").lower()

# Contar el número de palabras en el texto
numero_palabras = contar_palabras(texto)

# Solicitar al usuario que ingrese tres letras y convertirlas a minúsculas
letra1 = input("Ingresa la primera letra: ").lower()
letra2 = input("Ingresa la segunda letra: ").lower()
letra3 = input("Ingresa la tercera letra: ").lower()

# Convertir el texto ingresado y las letras a minúsculas
texto = texto.lower()

# Contar la cantidad de veces que se repite cada letra en el texto
repeticiones_letra1 = contar_letras(texto, letra1)
repeticiones_letra2 = contar_letras(texto, letra2)
repeticiones_letra3 = contar_letras(texto, letra3)

# Imprimir el número de palabras en el texto
print("Número de palabras en el texto:", numero_palabras)

# Imprimir la primera y última letra del texto
print("Primera letra del texto:", primera_letra(texto))
print("Última letra del texto:", ultima_letra(texto))

# Imprimir la cantidad de veces que se repite cada letra en el texto
print(f"La letra '{letra1}' aparece {repeticiones_letra1} veces en el texto.")
print(f"La letra '{letra2}' aparece {repeticiones_letra2} veces en el texto.")
print(f"La letra '{letra3}' aparece {repeticiones_letra3} veces en el texto.")

# Preguntar al usuario si desea realizar alguna otra acción
opcion = mostrar_menu()

# Realizar la acción correspondiente según la opción seleccionada
while opcion != "1":
    if opcion == "2":
        palabra_a_buscar = input("Ingresa una palabra para buscar en el texto: ")
        palabra_encontrada = buscar_palabra(texto, palabra_a_buscar)
        if palabra_encontrada:
            print(f"La palabra '{palabra_a_buscar}' fue encontrada en el texto.")
        else:
            print(f"La palabra '{palabra_a_buscar}' no fue encontrada en el texto.")
    else:
        print("Opción inválida. Por favor, ingresa una opción válida.")

    opcion = mostrar_menu()

print("¡Hasta luego!")
