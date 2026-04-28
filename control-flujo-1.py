# Solicitar al usuario que ingrese los valores de num1 y num2
num1 = float(input("Ingresa el valor de num1: "))
num2 = float(input("Ingresa el valor de num2: "))

# Comparar los valores de num1 y num2
if num1 > num2:
    print(f"{num1} es mayor que {num2}")
elif num2 > num1:
    print(f"{num2} es mayor que {num1}")
else:
    print(f"{num1} y {num2} son iguales")
