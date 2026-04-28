# Pedir al usuario su nombre
nombre = input("Por favor, introduce tu nombre: ")

# Pedir al usuario el monto de las ventas
ventas = float(input("Hola {}, ¿cuál fue el monto de tus ventas?: ".format(nombre)))

# Calcular el 13% de las ventas
comision = ventas * 0.13

# Redondear la comisión a no más de dos decimales
comision_redondeada = round(comision, 2)

# Combinar el nombre y la comisión utilizando format
mensaje = "¡Hola {}, tu comisión del 13% es de ${:.2f}!".format(nombre, comision)

# Imprimir el mensaje
print(mensaje)