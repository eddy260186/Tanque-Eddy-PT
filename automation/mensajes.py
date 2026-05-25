import random

def obtener_plantilla_mensaje(tipo_alerta: str, nombre_alumno: str, detalle: str = "") -> str:
    """
    Centraliza los copies de la marca. Evita que la app se sienta robótica 
    usando variaciones motivacionales de alto nivel.
    """
    plantillas = {
        "agua": [
            f"💧 ¡Hola {nombre_alumno}! Tu cuerpo necesita combustible limpio. Es momento de tomar un vaso de agua de 350ml. No te descuides. ⚡",
            f"💧 Hidratación Elite, {nombre_alumno}. Recordá cumplir con tu meta de agua en este momento. Mantené el metabolismo arriba. 🔥"
        ],
        "comida": [
            f"🍏 Horario de Nutrición, {nombre_alumno}. Te toca tu próxima comida programada: {detalle}. Respetá los macros para ver los resultados esperados. 🥩",
            f"🥗 Disciplina alimentaria, {nombre_alumno}. Es hora de tu comida: {detalle}. Prepará tus alimentos con precisión. 🎯"
        ],
        "pre_entrenamiento": [
            f"⏰ ¡Arriba {nombre_alumno}! Estás a 1 hora de arrancar tu sesión de entrenamiento programada (7:00 AM). Momento de levantarse, activar el cuerpo y preparar tu indumentaria. Hoy se entrena fuerte. 💪🏆",
            f"⚡ Cuenta regresiva, {nombre_alumno}. En 1 hora comienza tu zona de entrenamiento. Empezá a mentalizarte y prepará tu rutina. El éxito se construye temprano. 🔥"
        ],
        "suplementos": [
            f"💊 Recordatorio de Suplementación, {nombre_alumno}. Momento de tomar: {detalle}. La constancia en los micronutrientes acelera tu recuperación. 🧠",
        ],
        "pesaje": [
            f"⚖️ Control de Progreso, {nombre_alumno}. Mañana al despertarte, recordá pesarte en ayunas y registrarlo en la app. Los números no mienten. 📊"
        ]
    }
    
    # Retorna una plantilla aleatoria para que el alumno no se aburra de leer siempre lo mismo
    opciones = plantillas.get(tipo_alerta, [f"👋 Hola {nombre_alumno}, tenés un recordatorio programado."])
    return random.choice(opciones)