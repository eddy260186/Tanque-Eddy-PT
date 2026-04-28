def es_palindromo(palabra):
    # Convertir la palabra a minúsculas y eliminar espacios en blanco
    palabra = palabra.lower().replace(" ", "")
    
    # Verificar si la palabra es igual a su reverso
    return palabra == palabra[::-1]

# Solicitar al usuario que ingrese una palabra
palabra = input("Ingresa una palabra: ")

# Verificar si la palabra es un palíndromo
if es_palindromo(palabra):
    print(f"'{palabra}' es un palíndromo.")
else:
    print(f"'{palabra}' no es un palíndromo.")
