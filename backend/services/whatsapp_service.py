import os
import requests
import logging

logger = logging.getLogger("WhatsAppService")

# ==========================================================
# CONFIGURACIÓN EVOLUTION API
# ==========================================================

EVOLUTION_API_URL = os.getenv(
    "EVOLUTION_API_URL",
    "https://evolution-api-production-a15fc.up.railway.app"
).rstrip("/")

EVOLUTION_API_KEY = os.getenv(
    "EVOLUTION_API_KEY",
    ""
)

WHATSAPP_INSTANCE = os.getenv(
    "WHATSAPP_INSTANCE",
    "entrenador_455cb715"
)

# ==========================================================
# NORMALIZAR TELÉFONO
# ==========================================================

def normalizar_telefono_whatsapp(numero: str) -> str:

    numero = str(numero)

    numero = (
        numero
        .replace("+", "")
        .replace(" ", "")
        .replace("-", "")
        .replace("(", "")
        .replace(")", "")
    )

    return numero

# ==========================================================
# VERIFICAR INSTANCIA
# ==========================================================

def verificar_instancia():

    try:

        url = (
            f"{EVOLUTION_API_URL}"
            f"/instance/connectionState/"
            f"{WHATSAPP_INSTANCE}"
        )

        headers = {
            "apikey": EVOLUTION_API_KEY
        }

        logger.info(f"🔍 Verificando instancia: {WHATSAPP_INSTANCE}")
        logger.info(f"🔗 URL VERIFICACIÓN: {url}")

        response = requests.get(
            url,
            headers=headers,
            timeout=15
        )

        logger.info(
            f"📡 STATUS INSTANCIA: "
            f"{response.status_code}"
        )

        logger.info(
            f"📡 RESPUESTA INSTANCIA: "
            f"{response.text}"
        )

        if response.status_code != 200:

            logger.error(
                "❌ La instancia no existe "
                "o no está conectada."
            )

            return False

        data = response.json()

        estado = (
            data.get("instance", {})
            .get("state", "")
        )

        logger.info(f"📶 ESTADO INSTANCIA: {estado}")

        return estado.lower() == "open"

    except Exception as e:

        logger.error(
            f"❌ Error verificando instancia: {str(e)}"
        )

        return False

# ==========================================================
# ENVIAR MENSAJE
# ==========================================================

def enviar_mensaje_texto_evolution(
    telefono: str,
    mensaje: str
):

    try:

        # ==================================================
        # VALIDAR INSTANCIA
        # ==================================================

        if not verificar_instancia():

            return {
                "exito": False,
                "error": "Instancia no conectada"
            }

        # ==================================================
        # NORMALIZAR TELÉFONO
        # ==================================================

        telefono_limpio = (
            normalizar_telefono_whatsapp(
                telefono
            )
        )

        logger.info(
            f"📲 Enviando WhatsApp a "
            f"{telefono_limpio}"
        )

        # ==================================================
        # URL ENVÍO
        # ==================================================

        url = (
            f"{EVOLUTION_API_URL}"
            f"/message/sendText/"
            f"{WHATSAPP_INSTANCE}"
        )

        logger.info(f"🔗 URL EVOLUTION: {url}")

        # ==================================================
        # HEADERS
        # ==================================================

        headers = {
            "Content-Type": "application/json",
            "apikey": EVOLUTION_API_KEY
        }

        # ==================================================
        # PAYLOAD
        # ==================================================

        payload = {
            "number": telefono_limpio,
            "text": mensaje.strip()
        }

        logger.info(
            f"📦 PAYLOAD: {payload}"
        )

        # ==================================================
        # REQUEST
        # ==================================================

        response = requests.post(
            url,
            headers=headers,
            json=payload,
            timeout=30
        )

        logger.info(
            f"📤 STATUS EVOLUTION: "
            f"{response.status_code}"
        )

        logger.info(
            f"📤 RESPUESTA EVOLUTION: "
            f"{response.text}"
        )

        # ==================================================
        # RESPUESTA EXITOSA
        # ==================================================

        if response.status_code in [200, 201]:

            return {
                "exito": True,
                "respuesta": response.json()
            }

        # ==================================================
        # ERROR EVOLUTION
        # ==================================================

        return {
            "exito": False,
            "error": response.text
        }

    except Exception as e:

        logger.error(
            f"❌ Error Evolution API: {str(e)}"
        )

        return {
            "exito": False,
            "error": str(e)
        }