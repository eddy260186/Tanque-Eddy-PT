# ai/nutrition_ai.py
from ai.providers.gemini_provider import generar_texto

def redactar_receta_inteligente(nombre_alumno: str, dieta_activa: str, objetivo: str) -> str:
    """
    Analiza la dieta actual del alumno y le inventa una receta rápida 
    con los ingredientes que ya tiene permitidos.
    """
    prompt = f"""
    Actuá como un Nutricionista Deportivo de Élite. 
    Tu alumno se llama {nombre_alumno} y su objetivo es: {objetivo}.
    Su plan de alimentación actual contiene esto: {dieta_activa}
    
    Instrucción:
    Inventá una receta rápida y deliciosa (desayuno o almuerzo) usando PRINCIPALMENTE los ingredientes mencionados en su plan.
    El tono debe ser motivador, profesional y estilo "Personal Trainer argentino" (usá palabras como 'Tanque', 'campeón', 'metele').
    Estructura:
    - 🍳 Nombre de la receta (atractivo)
    - 🛒 Ingredientes
    - ⚡ Preparación rápida (3 pasos cortos)
    
    Máximo 150 palabras. Formato ideal para enviar por WhatsApp.
    """
    
    # Usamos temperatura 0.8 para que sea más creativo con las recetas
    return generar_texto(prompt=prompt, temperatura=0.8)