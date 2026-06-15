import random


def obtener_plantilla_mensaje(tipo_alerta: str, nombre_alumno: str, detalle: str = "") -> str:
    """
    Centraliza los copies de la marca. Evita que la app se sienta robótica
    usando variaciones motivacionales de alto nivel.

    Usa solo el PRIMER nombre (mas natural por WhatsApp) y ofrece
    muchas variantes para que el alumno no lea siempre lo mismo.
    """

    # Solo el primer nombre, se ve mas natural y cercano
    primer_nombre = str(nombre_alumno or "").split()[0] if nombre_alumno else "campeón/a"

    plantillas = {
        "agua": [
            f"💧 {primer_nombre}, momento de hidratarte. Un vaso de agua ahora y seguimos. 💪",
            f"💧 Pausa de agua, {primer_nombre}. Tu cuerpo te lo agradece. 🙌",
            f"💧 ¡A tomar agua, {primer_nombre}! La hidratación es parte del entrenamiento. 🔥",
            f"💧 Recordá tu vaso de agua, {primer_nombre}. Pequeños hábitos, grandes resultados. ✨",
            f"💧 {primer_nombre}, un vaso de agua ahora mismo. Mantené el ritmo. ⚡",
            f"💧 Hora de hidratarse, {primer_nombre}. No lo dejes pasar. 💦",
            f"💧 Tu recordatorio de agua, {primer_nombre}. Cada sorbo suma. 🌊",
            f"💧 {primer_nombre}, ¿ya tomaste agua? Es el momento. 😉",
        ],
        "comida": [
            f"🍽️ {primer_nombre}, te toca tu comida: {detalle}. Respetá los macros. 🎯",
            f"🥗 Hora de comer, {primer_nombre}: {detalle}. Disciplina = resultados. 🥩",
            f"🍴 {primer_nombre}, llegó tu comida programada: {detalle}. ¡A disfrutarla! 😋",
        ],
        "pre_entrenamiento": [
            f"⏰ {primer_nombre}, en 1 hora arranca tu entrenamiento. Prepará todo y mentalizate. 💪",
            f"⚡ Cuenta regresiva, {primer_nombre}. En 60 min a darle con todo. 🔥",
            f"🏋️ {primer_nombre}, falta poco para tu sesión. Hidratate y preparate. 🏆",
        ],
        "pesaje": [
            f"⚖️ {primer_nombre}, mañana en ayunas pesate y registralo. Los números guían el camino. 📊",
        ],
    }

    opciones = plantillas.get(tipo_alerta)

    # Si no hay plantilla para este tipo, NO mandamos un generico vacio.
    # Devolvemos None para que el agente decida no enviar nada.
    if not opciones:
        return None

    return random.choice(opciones)