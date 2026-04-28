# Definir una lista con un elemento repetido varias veces
mi_lista = [1, 2, 3, 3, 4, 5, 3, 6, 7, 3, 8, 9, 3, 10, 11, 3]

# Elemento repetido que deseas eliminar
elemento_repetido = 3

# Eliminar todas las ocurrencias del elemento repetido de la lista
while elemento_repetido in mi_lista:
    mi_lista.remove(elemento_repetido)

print("Lista después de eliminar todas las ocurrencias del elemento repetido:")
print(mi_lista)
