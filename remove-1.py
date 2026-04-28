# Definir una lista con elementos repetidos
mi_lista = [1, 2, 3, 3, 4, 5, 3, 6, 7, 3, 8, 9, 3, 10, 11, 3]

# Inicializar un conjunto para mantener un registro de los elementos únicos
elementos_unicos = set()

# Lista para almacenar los elementos sin repeticiones
lista_sin_repeticiones = []

# Recorrer la lista y agregar elementos únicos a la lista sin repeticiones
for elemento in mi_lista:
    if elemento not in elementos_unicos:
        lista_sin_repeticiones.append(elemento)
        elementos_unicos.add(elemento)

print("Lista después de eliminar repeticiones:")
print(lista_sin_repeticiones)
