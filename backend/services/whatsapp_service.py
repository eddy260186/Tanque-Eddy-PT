
import os
import requests

from utils.logger import obtener_logger
from database.queries import registrar_log_whatsapp

logger = obtener_logger("WhatsAppService")


class EvolutionAPI:

    def __init__(self):

        self.base_url = os.getenv(
            "EVOLUTION_API_URL",
            "https://evolution-api-production-a15fc.up.railway.app"
        ).rstrip("/")

        self.api_key = os.getenv(
            "EVOLUTION_API_KEY",
            ""
        )

        self.headers = {
            "Content-Type": "application/json",
            "apikey": self.api_key
        }

    def crear_instancia_y_obtener_qr(self, nombre_instancia):

        url = f"{self.base_url}/instance/create"

        payload = {
            "instanceName": nombre_instancia,
            "qrcode": True,
            "integration": "WHATSAPP-BAILEYS"
        }

        try:

            response = requests.post(
                url,
                headers=self.headers,
                json=payload,
                timeout=20
            )

            data = response.json()

            if response.status_code in [200, 201]:

                return {
                    "exito": True,
                    "qr_base64": data.get("qrcode", {}).get("base64")
                }

            return {
                "exito": False,
                "error": data.get("message", "Error desconocido")
            }

        except Exception as e:

            logger.error(f"❌ Error creando instancia: {str(e)}")

            return {
                "exito": False,
                "error": str(e)
            }


def normalizar_telefono_whatsapp(telefono: str) -> str:

    return "".join(
        filter(str.isdigit, str(telefono or ""))
    )


def enviar_mensaje_texto_evolution(
    nombre_instancia: str,
    alumno_id: str,
    entrenador_id: str,
    telefono: str,
    mensaje: str
):

    base_url = os.getenv(
        "EVOLUTION_API_URL",
        "https://evolution-api-production-a15fc.up.railway.app"
    ).rstrip("/")

    api_key = os.getenv(
        "EVOLUTION_API_KEY",
        ""
    )

    telefono_limpio = normalizar_telefono_whatsapp(telefono)

    url = f"{base_url}/message/sendText/{nombre_instancia}"

    headers = {
        "Content-Type": "application/json",
        "apikey": api_key
    }

    payload = {
        "number": telefono_limpio,
        "options": {
            "delay": 1200,
            "presence": "composing"
        },
        "text": mensaje.strip()
    }

    try:

        respuesta = requests.post(
            url,
            json=payload,
            headers=headers,
            timeout=20
        )

        if respuesta.status_code in [200, 201]:

            registrar_log_whatsapp(
                alumno_id=alumno_id,
                entrenador_id=entrenador_id,
                direccion="saliente",
                contenido=mensaje.strip()
            )

            return {
                "exito": True
            }

        return {
            "exito": False,
            "error": respuesta.text
        }

    except Exception as e:

        logger.error(f"❌ Error Evolution API: {str(e)}")

        return {
            "exito": False,
            "error": str(e)
        }


def enviar_mensaje_texto_whatsapp(*args, **kwargs):

    return enviar_mensaje_texto_evolution(*args, **kwargs)
