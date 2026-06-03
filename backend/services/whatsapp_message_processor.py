
import re

from utils.logger import obtener_logger
from database.conexion import supabase

logger = obtener_logger("WhatsAppMessageProcessor")


def detectar_intencion_mensaje(
    mensaje: str
):

    """
    Detecta qué quiso decir el alumno.
    """

    texto = mensaje.lower().strip()

    # =====================================================
    # PESO CORPORAL
    # =====================================================

    patron_peso = r"(\d+)\s?kg"

    match_peso = re.search(
        patron_peso,
        texto
    )

    if match_peso:

        return {
            "tipo": "peso",
            "valor": float(
                match_peso.group(1)
            )
        }

    # =====================================================
    # ENTRENAMIENTO
    # =====================================================

    palabras_entreno = [
        "entrene",
        "entrené",
        "gym",
        "piernas",
        "pecho",
        "espalda",
        "sentadilla",
        "press"
    ]

    if any(
        palabra in texto
        for palabra in palabras_entreno
    ):

        return {
            "tipo": "entrenamiento",
            "detalle": mensaje
        }

    # =====================================================
    # COMIDA / REEMPLAZOS
    # =====================================================

    palabras_comida = [
        "no tengo",
        "reemplazo",
        "comer",
        "pollo",
        "atun",
        "atún",
        "arroz"
    ]

    if any(
        palabra in texto
        for palabra in palabras_comida
    ):

        return {
            "tipo": "nutricion",
            "detalle": mensaje
        }

    # =====================================================
    # AGUA
    # =====================================================

    palabras_agua = [
        "tomé agua",
        "tome agua",
        "agua"
    ]

    if any(
        palabra in texto
        for palabra in palabras_agua
    ):

        return {
            "tipo": "agua",
            "detalle": mensaje
        }

    # =====================================================
    # DEFAULT
    # =====================================================

    return {
        "tipo": "general",
        "detalle": mensaje
    }


def guardar_interaccion_atleta(
    alumno_id: str,
    mensaje: str
):

    """
    Guarda automáticamente
    información importante del atleta.
    """

    try:

        resultado = detectar_intencion_mensaje(
            mensaje
        )

        tipo = resultado.get("tipo")

        logger.info(
            f"🧠 Tipo detectado: {tipo}"
        )

        # =====================================================
        # ACTUALIZAR PESO
        # =====================================================

        if tipo == "peso":

            nuevo_peso = resultado.get(
                "valor"
            )

            supabase.table(
                "perfiles_atletas"
            ).update({
                "peso_actual": nuevo_peso
            }).eq(
                "id",
                alumno_id
            ).execute()

            logger.info(
                f"✅ Peso actualizado: "
                f"{nuevo_peso}kg"
            )

        # =====================================================
        # GUARDAR ENTRENAMIENTO
        # =====================================================

        elif tipo == "entrenamiento":

            supabase.table(
                "ejercicios_realizados"
            ).insert({
                "alumno_id": alumno_id,
                "descripcion": mensaje
            }).execute()

            logger.info(
                "✅ Entrenamiento guardado."
            )

        # =====================================================
        # GUARDAR HISTORIAL IA
        # =====================================================

        supabase.table(
            "historial_interacciones"
        ).insert({
            "alumno_id": alumno_id,
            "mensaje": mensaje,
            "tipo_detectado": tipo
        }).execute()

        logger.info(
            "✅ Historial guardado."
        )

        return resultado

    except Exception as e:

        logger.error(
            f"❌ Error procesando mensaje: {str(e)}"
        )

        return {
            "tipo": "error"
        }
