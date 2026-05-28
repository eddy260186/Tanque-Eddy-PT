
import os
import requests

from utils.logger import obtener_logger
from database.queries import registrar_log_whatsapp

logger = obtener_logger("WhatsAppService")


# =========================================================
# EVOLUTION API CLIENT
# =========================================================

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

    # =====================================================
    # CREAR INSTANCIA
    # =====================================================

    def crear_instancia_y_obtener_qr(
        self,
        nombre_instancia
    ):

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

            logger.info(
                f"📦 RESPUESTA CREATE INSTANCE: {data}"
            )

            if response.status_code in [200, 201]:

                return {
                    "exito": True,
                    "qr_base64": (
                        data.get("qrcode", {})
                        .get("base64")
                    )
                }

            return {
                "exito": False,
                "error": data.get(
                    "message",
                    "Error desconocido"
                )
            }

        except Exception as e:

            logger.error(
                f"❌ Error creando instancia: {str(e)}"
            )

            return {
                "exito": False,
                "error": str(e)
            }


# =========================================================
# NORMALIZAR TELÉFONO
# =========================================================

def normalizar_telefono_whatsapp(
    telefono: str
) -> str:

    return "".join(
        filter(
            str.isdigit,
            str(telefono or "")
        )
    )


# =========================================================
# ENVIAR MENSAJE WHATSAPP
# =========================================================

def enviar_mensaje_texto_evolution(
    nombre_instancia: str,
    alumno_id: str,
    entrenador_id: str,
    telefono: str,
    mensaje: str
):

    try:

        # =================================================
        # VARIABLES ENTORNO
        # =================================================

        base_url = os.getenv(
            "EVOLUTION_API_URL",
            "https://evolution-api-production-a15fc.up.railway.app"
        ).rstrip("/")

        api_key = os.getenv(
            "EVOLUTION_API_KEY",
            ""
        )

        instancia_global = os.getenv(
            "WHATSAPP_INSTANCE",
            "entrenador_455cb715"
        )

        # =================================================
        # VALIDACIONES
        # =================================================

        if not api_key:

            logger.error(
                "❌ EVOLUTION_API_KEY no configurada."
            )

            return {
                "exito": False,
                "error": "EVOLUTION_API_KEY faltante"
            }

        if not base_url:

            logger.error(
                "❌ EVOLUTION_API_URL no configurada."
            )

            return {
                "exito": False,
                "error": "EVOLUTION_API_URL faltante"
            }

        # =================================================
        # TELEFONO
        # =================================================

        telefono_limpio = (
            normalizar_telefono_whatsapp(
                telefono
            )
        )

        # =================================================
        # USAR INSTANCIA GLOBAL
        # =================================================

        nombre_instancia = instancia_global

        # =================================================
        # URL
        # =================================================

        url = (
            f"{base_url}"
            f"/message/sendText/"
            f"{nombre_instancia}"
        )

        # =================================================
        # HEADERS
        # =================================================

        headers = {
            "Content-Type": "application/json",
            "apikey": api_key
        }

        # =================================================
        # PAYLOAD
        # =================================================

        payload = {
            "number": telefono_limpio,
            "options": {
                "delay": 1200,
                "presence": "composing"
            },
            "text": mensaje.strip()
        }

        logger.info(
            f"📤 Enviando WhatsApp "
            f"a {telefono_limpio}"
        )

        logger.info(
            f"📡 URL Evolution: {url}"
        )

        # =================================================
        # REQUEST
        # =================================================

        respuesta = requests.post(
            url,
            json=payload,
            headers=headers,
            timeout=20
        )

        logger.info(
            f"📥 STATUS EVOLUTION: "
            f"{respuesta.status_code}"
        )

        logger.info(
            f"📦 RESPUESTA EVOLUTION: "
            f"{respuesta.text}"
        )

        # =================================================
        # ÉXITO
        # =================================================

        if respuesta.status_code in [200, 201]:

            registrar_log_whatsapp(
                alumno_id=alumno_id,
                entrenador_id=entrenador_id,
                direccion="saliente",
                contenido=mensaje.strip()
            )

            logger.info(
                "✅ WhatsApp enviado correctamente."
            )

            return {
                "exito": True
            }

        # =================================================
        # ERROR EVOLUTION
        # =================================================

        logger.error(
            f"❌ Error Evolution API: "
            f"{respuesta.text}"
        )

        return {
            "exito": False,
            "error": respuesta.text
        }

    except Exception as e:

        logger.error(
            f"❌ Error enviando WhatsApp: {str(e)}"
        )

        return {
            "exito": False,
            "error": str(e)
        }


# =========================================================
# WRAPPER LEGACY
# =========================================================

def enviar_mensaje_texto_whatsapp(
    *args,
    **kwargs
):

    return enviar_mensaje_texto_evolution(
        *args,
        **kwargs
    )

