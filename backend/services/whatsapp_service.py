
import os
import requests

from utils.logger import obtener_logger
from database.queries import registrar_log_whatsapp

logger = obtener_logger("WhatsAppService")

# =========================================================
# CLIENTE EVOLUTION API
# =========================================================

class EvolutionAPI:

    def __init__(self):

        self.base_url = os.getenv("EVOLUTION_API_URL", "https://evolution-api-production-a15fc.up.railway.app").rstrip("/")

        self.api_key = os.getenv("EVOLUTION_API_KEY", "").strip()

        self.headers = {
            "apikey": self.api_key,
            "Content-Type": "application/json"
        }

    # =====================================================
    # CREAR INSTANCIA
    # =====================================================

    def crear_instancia_y_obtener_qr(self, nombre_instancia):

        try:

            url = f"{self.base_url}/instance/create"

            payload = {
                "instanceName": nombre_instancia,
                "qrcode": True,
                "integration": "WHATSAPP-BAILEYS"
            }

            response = requests.post(
                url,
                headers=self.headers,
                json=payload,
                timeout=30
            )

            logger.info(f"📡 CREATE INSTANCE STATUS: {response.status_code}")

            data = response.json()

            logger.info(f"📦 CREATE INSTANCE RESPONSE: {data}")

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

# =========================================================
# NORMALIZAR TELEFONO
# =========================================================

def normalizar_telefono_whatsapp(telefono: str) -> str:

    return "".join(filter(str.isdigit, str(telefono or "")))

# =========================================================
# VERIFICAR INSTANCIA
# =========================================================

def verificar_instancia(nombre_instancia: str):

    try:

        base_url = os.getenv("EVOLUTION_API_URL", "").rstrip("/")

        api_key = os.getenv("EVOLUTION_API_KEY", "").strip()

        url = f"{base_url}/instance/connectionState/{nombre_instancia}"

        headers = {
            "apikey": api_key
        }

        response = requests.get(
            url,
            headers=headers,
            timeout=15
        )

        logger.info(f"📡 VERIFY INSTANCE STATUS: {response.status_code}")

        logger.info(f"📦 VERIFY INSTANCE RESPONSE: {response.text}")

        return response.status_code == 200

    except Exception as e:

        logger.error(f"❌ Error verificando instancia: {str(e)}")

        return False

# =========================================================
# ENVIAR MENSAJE WHATSAPP
# =========================================================

def enviar_mensaje_texto_evolution(nombre_instancia: str, alumno_id: str, entrenador_id: str, telefono: str, mensaje: str):

    try:

        # =================================================
        # VARIABLES
        # =================================================

        base_url = os.getenv("EVOLUTION_API_URL", "https://evolution-api-production-a15fc.up.railway.app").rstrip("/")

        api_key = os.getenv("EVOLUTION_API_KEY", "").strip()

        instancia_global = os.getenv("WHATSAPP_INSTANCE", "entrenador_455cb715").strip()

        # =================================================
        # VALIDACIONES
        # =================================================

        if not api_key:

            logger.error("❌ EVOLUTION_API_KEY no configurada.")

            return {
                "exito": False,
                "error": "EVOLUTION_API_KEY faltante"
            }

        if not verificar_instancia(instancia_global):

            logger.error(f"❌ La instancia '{instancia_global}' no existe o no está conectada.")

            return {
                "exito": False,
                "error": "Instancia no conectada"
            }

        # =================================================
        # TELEFONO
        # =================================================

        telefono_limpio = normalizar_telefono_whatsapp(telefono)

        # =================================================
        # URL
        # =================================================

        url = f"{base_url}/message/sendText/{instancia_global}"

        # =================================================
        # HEADERS
        # =================================================

        headers = {
            "apikey": api_key,
            "Content-Type": "application/json"
        }

        # =================================================
        # PAYLOAD EVOLUTION 2.3.7
        # =================================================

        payload = {
            "number": telefono_limpio,
            "text": mensagem.strip() if 'mensagem' in locals() else mensaje.strip()
        }

        logger.info(f"📤 Enviando WhatsApp a {telefono_limpio}")

        logger.info(f"📡 URL Evolution: {url}")

        logger.info(f"📦 PAYLOAD: {payload}")

        # =================================================
        # REQUEST
        # =================================================

        respuesta = requests.post(
            url,
            json=payload,
            headers=headers,
            timeout=30
        )

        logger.info(f"📥 STATUS EVOLUTION: {respuesta.status_code}")

        logger.info(f"📦 RESPUESTA EVOLUTION: {respuesta.text}")

        # =================================================
        # EXITO
        # =================================================

        if respuesta.status_code in [200, 201]:

            registrar_log_whatsapp(
                alumno_id=alumno_id,
                entrenador_id=entrenador_id,
                direccion="saliente",
                contenido=mensaje.strip()
            )

            logger.info("✅ WhatsApp enviado correctamente.")

            return {
                "exito": True
            }

        # =================================================
        # ERROR API
        # =================================================

        logger.error(f"❌ Error Evolution API: {respuesta.text}")

        return {
            "exito": False,
            "error": respuesta.text
        }

    except Exception as e:

        logger.error(f"❌ Error enviando WhatsApp: {str(e)}")

        return {
            "exito": False,
            "error": str(e)
        }

# =========================================================
# WRAPPER LEGACY
# =========================================================

def enviar_mensaje_texto_whatsapp(*args, **kwargs):

    return enviar_mensaje_texto_evolution(*args, **kwargs)

