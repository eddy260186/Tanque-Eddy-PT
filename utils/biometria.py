# utils/biometria.py

def calcular_biometria(genero, estatura, cintura, peso_actual):
    if cintura > 0:
        if genero == "m":
            rfm = round(64 - (20 * (estatura / cintura)), 1)
        else:
            rfm = round(76 - (20 * (estatura / cintura)), 1)
        
        rfm = max(5.0, min(rfm, 60.0))
        masa_magra = peso_actual * (1 - (rfm / 100))
        tmb = 370 + (21.6 * masa_magra)
    else:
        # Valores por defecto si no hay cintura ingresada
        rfm = 0.0
        masa_magra = 0.0
        tmb = 0.0 
        
    return rfm, masa_magra, tmb