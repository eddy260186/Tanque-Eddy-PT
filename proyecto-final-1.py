# Solicitar al usuario que ingrese un texto y convertirlo a minúsculas
texto = input("Por favor, ingresa un texto: ").lower()

# Contar el número de palabras en el texto
numero_palabras = len(texto.split())

# Solicitar al usuario que ingrese tres letras y convertirlas a minúsculas
letra1 = input("Ingresa la primera letra: ").lower()
letra2 = input("Ingresa la segunda letra: ").lower()
letra3 = input("Ingresa la tercera letra: ").lower()

# Convertir el texto ingresado y las letras a minúsculas
texto = texto.lower()

# Contar la cantidad de veces que se repite cada letra en el texto
repeticiones_letra1 = texto.count(letra1)
repeticiones_letra2 = texto.count(letra2)
repeticiones_letra3 = texto.count(letra3)

# Imprimir el número de palabras en el texto
print("Número de palabras en el texto:", numero_palabras)

# Imprimir la cantidad de veces que se repite cada letra en el texto
print(f"La letra '{letra1}' aparece {repeticiones_letra1} veces en el texto.")
print(f"La letra '{letra2}' aparece {repeticiones_letra2} veces en el texto.")
print(f"La letra '{letra3}' aparece {repeticiones_letra3} veces en el texto.")
