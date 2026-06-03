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
            f"/instance/fetchInstances"
        )

        headers = {
            "apikey": EVOLUTION_API_KEY
        }

        logger.info(
            f"🔍 Verificando instancia: "
            f"{WHATSAPP_INSTANCE}"
        )

        logger.info(
            f"🔗 URL VERIFICACIÓN: "
            f"{url}"
        )

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
                "❌ Error obteniendo instancias"
            )

            return False

        data = response.json()

        # ==================================================
        # EVOLUTION PUEDE DEVOLVER:
        # LISTA o {"instance": [...]}
        # ==================================================

        if isinstance(data, dict):

            data = data.get("instance", [])

        if not isinstance(data, list):

            logger.error(
                "❌ Evolution no devolvió lista"
            )

            return False

        for instancia in data:

            nombre = (
                instancia
                .get("name", "")
            )

            conexion = (
                instancia
                .get("connectionStatus", "")
            )

            logger.info(
                f"📲 Instancia encontrada: "
                f"{nombre} -> {conexion}"
            )

            if nombre == WHATSAPP_INSTANCE:

                if conexion.lower() in [
                    "open",
                    "connected",
                    "online"
                ]:

                    logger.info(
                        "✅ Instancia conectada"
                    )

                    return True

        logger.error(
            "❌ La instancia no existe "
            "o no está conectada."
        )

        return False

    except Exception as e:

        logger.error(
            f"❌ Error verificando instancia: "
            f"{str(e)}"
        )

        return False

# ==========================================================
# FUNCIÓN PRINCIPAL
# ==========================================================

def enviar_mensaje_texto_whatsapp(
    nombre_instancia: str = None,
    alumno_id: str = None,
    entrenador_id: str = None,
    telefono: str = "",
    mensaje: str = ""
):

    try:

        # ==================================================
        # VALIDAR MENSAJE
        # ==================================================

        if not mensaje:

            return {
                "exito": False,
                "error": "Mensaje vacío"
            }

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

        instancia_final = (
            nombre_instancia
            if nombre_instancia
            else WHATSAPP_INSTANCE
        )

        url = (
            f"{EVOLUTION_API_URL}"
            f"/message/sendText/"
            f"{instancia_final}"
        )

        logger.info(
            f"🔗 URL EVOLUTION: "
            f"{url}"
        )

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
            f"📦 PAYLOAD: "
            f"{payload}"
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

            try:

                resposta_json = response.json()

            except:

                resposta_json = response.text

            return {
                "exito": True,
                "respuesta": resposta_json
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
            f"❌ Error Evolution API: "
            f"{str(e)}"
        )

        return {
            "exito": False,
            "error": str(e)
        }

# ==========================================================
# COMPATIBILIDAD TOTAL
# ==========================================================

def enviar_mensaje_texto_evolution(
    nombre_instancia: str = None,
    alumno_id: str = None,
    entrenador_id: str = None,
    telefono: str = "",
    mensaje: str = ""
):

    return enviar_mensaje_texto_whatsapp(
        nombre_instancia=nombre_instancia,
        alumno_id=alumno_id,
        entrenador_id=entrenador_id,
        telefono=telefono,
        mensaje=mensaje
    )
# ==========================================================
# COMPATIBILIDAD PANEL ENTRENADOR
# ==========================================================

class EvolutionAPI:

    @staticmethod
    def enviar_mensaje(
        telefono: str,
        mensaje: str,
        nombre_instancia: str = None
    ):

        return enviar_mensaje_texto_whatsapp(
            telefono=telefono,
            mensaje=mensaje,
            nombre_instancia=nombre_instancia
        )