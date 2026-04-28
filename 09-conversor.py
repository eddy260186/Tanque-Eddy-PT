temperatura = float (input ("Ingrese Temperatura:"))
escala = input ("Es Fahrenheit(F) o es Celsius (C) ?:").lower()
if escala == "f":
    Celsius = (temperatura - 32) * 5/9
    print(Celsius)
elif escala == "c":
    Fahrenheit = temperatura * 1.8 + 32
    print (Fahrenheit)
else:
    print("Escala Incorreta")
    
