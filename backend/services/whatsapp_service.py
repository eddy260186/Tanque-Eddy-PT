import requests
from config.settings import settings
from utils.logger import obtener_logger
from database.queries import registrar_log_whatsapp

logger = obtener_logger("WhatsAppService")

def enviar_mensaje_texto_whatsapp(alumno_id: str, entrenador_id: str, telefono: str, mensaje: str) -> bool:
    """
    Envía un mensaje de texto personalizado a un alumno utilizando la API en la Nube de Meta.
    """
    url = f"https://graph.facebook.com/v18.0/{settings.WHATSAPP_PHONE_NUMBER_ID}/messages"
    token = settings.WHATSAPP_TOKEN

    if not token or not settings.WHATSAPP_PHONE_NUMBER_ID:
        logger.error("❌ Error de configuración: Falta token o ID en settings.")
        return False

    telefono_limpio = "".join(filter(str.isdigit, telefono))

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    payload = {
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": telefono_limpio,
        "type": "text",
        "text": {"preview_url": False, "body": mensaje}
    }

    try:
        respuesta = requests.post(url, json=payload, headers=headers, timeout=10)
        if respuesta.status_code in [200, 201]:
            registrar_log_whatsapp(
                alumno_id=alumno_id,
                entrenador_id=entrenador_id,
                direccion="saliente",
                contenido=mensaje
            )
            return True
        else:
            logger.error(f"❌ Meta rechazó el mensaje: {respuesta.text}")
            return False
    except Exception as e:
        logger.error(f"🚨 Error de conexión con Meta: {str(e)}")
        return False