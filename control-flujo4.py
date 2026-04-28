# Definir las respuestas válidas para sí y no
respuestas_si = {"s", "si"}
respuestas_no = {"n", "no"}

# Solicitar al usuario que ingrese su información
respuesta_sabe_programar = input("¿Sabes programar en Python? (Sí/No): ").strip().lower()
respuesta_conoce_ingles = input("¿Tienes conocimientos de inglés? (Sí/No): ").strip().lower()

# Verificar si las respuestas del usuario están dentro de las respuestas válidas
sabe_programar_python = respuesta_sabe_programar in respuestas_si
conoce_ingles = respuesta_conoce_ingles in respuestas_si

# Evaluar las condiciones y mostrar el mensaje correspondiente
if sabe_programar_python and conoce_ingles:
    print("Cumples con los requisitos para postularte")
elif sabe_programar_python:
    print("Para postularte, necesitas tener conocimientos de inglés")
elif conoce_ingles:
    print("Para postularte, necesitas saber programar en Python")
else:
    print("Para postularte, necesitas saber programar en Python y tener conocimientos de inglés")
