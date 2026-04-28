frase = "En teoría, la teoría y la práctica son los mismos. En la práctica, no lo son."

# Encontrar el índice de la primera aparición de "práctica"
primer_indice = frase.find("práctica")

# Encontrar el índice de la segunda aparición de "práctica"
segundo_indice = frase.find("práctica", primer_indice + 1)

# Mostrar el índice de la segunda aparición
print("El índice de la segunda aparición de 'práctica' es:", segundo_indice)
