# ai/workout_ai.py
from ai.providers.gemini_provider import generar_texto

def redactar_motivacion_matutina(nombre_alumno: str, rutina_activa: str, agua_litros: float) -> str:
    """
    Genera el mensaje de "Buenos Días" resumiendo la rutina y recordando el agua.
    """
    prompt = f"""
    Actuá como Eddy, un Personal Trainer de Élite argentino.
    Escribile un mensaje corto de WhatsApp de buenos días a tu alumno/a {nombre_alumno}.
    
    Datos para usar:
    - Su rutina asignada actual es: {rutina_activa}. (Resumí en 1 oración qué músculos le toca destruir hoy).
    - Su meta estricta de hidratación de hoy es de {agua_litros} Litros.
    
    Instrucción:
    Usá un tono muy motivador, directo, rudo pero profesional. Usá modismos argentinos ('metele mecha', 'romperla hoy').
    No te excedas de 4 o 5 renglones cortos. Usá emojis de fuego, pesas y agua.
    """
    
    # Usamos temperatura 0.6 para que no alucine y respete los músculos exactos de la rutina
    return generar_texto(prompt=prompt, temperatura=0.6)