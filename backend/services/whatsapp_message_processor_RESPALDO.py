import re

from utils.logger import obtener_logger
from database.conexion import supabase
from backend.services.entrenamiento_service import guardar_entrenamiento_estructurado

logger = obtener_logger("WhatsAppMessageProcessor")


def detectar_intencion_mensaje(
    mensaje: str
):

    """
    Detecta qué quiso decir el alumno.
    """

    texto = mensaje.lower().strip()

    # =====================================================
    # CHECKIN NOCTURNO (respuesta 1 / 2 / 3)
    # =====================================================

    if texto in ("1", "2", "3"):

        mapa = {
            "1": "si",
            "2": "parcial",
            "3": "no"
        }

        return {
            "tipo": "checkin",
            "valor": mapa[texto]
        }

    # =====================================================
    # ENTRENAMIENTO
    # (se evalúa ANTES que el peso corporal, porque
    # "sentadilla 60kg" tiene kg pero es entrenamiento)
    # =====================================================

    palabras_entreno = [
        "entrene",
        "entrené",
        "gym",
        "piernas",
        "pecho",
        "espalda",
        "sentadilla",
        "press",
        "prensa",
        "remo",
        "curl",
        "dominadas",
        "peso muerto",
        "hice",
        "series",
        "repeticiones",
        "reps"
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
    # PESO CORPORAL
    # =====================================================

    patron_peso = r"(\d+(?:\.\d+)?)\s?kg"

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
        # GUARDAR CHECKIN NOCTURNO
        # =====================================================

        elif tipo == "checkin":

            supabase.table(
                "checkins_diarios"
            ).insert({
                "alumno_id": alumno_id,
                "respuesta": resultado.get("valor"),
                "detalle": mensaje
            }).execute()

            logger.info(
                f"✅ Checkin guardado: "
                f"{resultado.get('valor')}"
            )

        # =====================================================
        # GUARDAR ENTRENAMIENTO
        # (extrae con IA: ejercicio, peso, series, reps
        # y los guarda en ejercicios_realizados)
        # =====================================================

        elif tipo == "entrenamiento":

            cantidad = guardar_entrenamiento_estructurado(
                alumno_id,
                mensaje
            )

            logger.info(
                f"✅ Entrenamiento guardado "
                f"({cantidad} ejercicios)."
            )

        # =====================================================
        # REGISTRAR MENSAJE ENTRANTE
        # (en tu tabla mensajes_whatsapp existente)
        # =====================================================

        supabase.table(
            "mensajes_whatsapp"
        ).insert({
            "alumno_id": alumno_id,
            "direccion": "entrante",
            "tipo_mensaje": tipo,
            "contenido": mensaje,
            "estado_envio": "recibido"
        }).execute()

        logger.info(
            "✅ Mensaje registrado."
        )

        return resultado

    except Exception as e:

        logger.error(
            f"❌ Error procesando mensaje: {str(e)}"
        )

        return {
            "tipo": "error"
        }