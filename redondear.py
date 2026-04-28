# EJERCICIO 1
# Realizar la división
resultado = 10 / 3

# Redondear el resultado a 2 decimales
resultado_redondeado = round(resultado, 2)

# Mostrar el valor redondeado en pantalla
print(resultado_redondeado)

# EJERCICIO 2
# Redondear el número al entero más próximo
resultado_redondeado = round(10.676767)

# Mostrar el resultado en pantalla
print(resultado_redondeado)

# EJERCICIO 3
import math

# Calcular la raíz cuadrada de 5
raiz_cuadrada = math.sqrt(5)

# Redondear el resultado con 4 posiciones decimales
resultado_redondeado = round(raiz_cuadrada, 4)

# Mostrar el resultado en pantalla
print(resultado_redondeado)

# ejercicios 4
num1 = 13.87

#Las siguientes líneas en Python, arrojarían el mismo resultado:

print(round(num1))
print(int(num1))

#Ejercicios 5
num1 = round(13 / 2, 0)
tipo_de_dato = type(num1)
print(tipo_de_dato)
