import requests
from config.settings import settings
from utils.logger import obtener_logger
from database.queries import registrar_log_whatsapp

logger = obtener_logger("WhatsAppService")


def normalizar_telefono_whatsapp(telefono: str) -> str:
    """Deja el numero en formato aceptado por Meta: solo digitos con codigo de pais."""
    return "".join(filter(str.isdigit, str(telefono or "")))


def enviar_mensaje_texto_whatsapp(alumno_id: str, entrenador_id: str, telefono: str, mensaje: str) -> bool:
    """
    Envia un mensaje de texto personalizado al alumno usando Meta Cloud API.
    """
    token = settings.WHATSAPP_TOKEN
    phone_number_id = settings.WHATSAPP_PHONE_NUMBER_ID

    if not token or not phone_number_id:
        logger.error("WhatsApp no configurado: faltan WHATSAPP_TOKEN o WHATSAPP_PHONE_NUMBER_ID.")
        return False

    telefono_limpio = normalizar_telefono_whatsapp(telefono)
    if not telefono_limpio:
        logger.error("WhatsApp no enviado: telefono vacio o invalido.")
        return False

    if not mensaje or not mensaje.strip():
        logger.error("WhatsApp no enviado: mensaje vacio.")
        return False

    url = f"https://graph.facebook.com/v18.0/{phone_number_id}/messages"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    payload = {
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": telefono_limpio,
        "type": "text",
        "text": {"preview_url": False, "body": mensaje.strip()},
    }

    try:
        respuesta = requests.post(url, json=payload, headers=headers, timeout=15)
        if respuesta.status_code in (200, 201):
            registrar_log_whatsapp(
                alumno_id=alumno_id,
                entrenador_id=entrenador_id,
                direccion="saliente",
                contenido=mensaje.strip(),
            )
            logger.info(f"WhatsApp enviado correctamente a {telefono_limpio}.")
            return True

        logger.error(f"Meta rechazo el mensaje ({respuesta.status_code}): {respuesta.text}")
        return False
    except Exception as e:
        logger.error(f"Error de conexion con Meta: {str(e)}")
        return False
