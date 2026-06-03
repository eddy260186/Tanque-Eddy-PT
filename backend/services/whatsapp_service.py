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

EVOLUTION_API_KEY = os.getenv("EVOLUTION_API_KEY", "")
WHATSAPP_INSTANCE = os.getenv("WHATSAPP_INSTANCE", "entrenador_455cb715")

# ==========================================================
# NORMALIZAR TELÉFONO
# ==========================================================
def normalizar_telefono_whatsapp(numero: str) -> str:
    numero = str(numero)
    for char in ["+", " ", "-", "(", ")"]:
        numero = numero.replace(char, "")
    return numero

# ==========================================================
# VERIFICAR INSTANCIA
# ==========================================================
def verificar_instancia():
    try:
        url = f"{EVOLUTION_API_URL}/instance/fetchInstances"
        headers = {"apikey": EVOLUTION_API_KEY}

        logger.info(f"🔍 Verificando instancia: {WHATSAPP_INSTANCE}")
        response = requests.get(url, headers=headers, timeout=15)
        logger.info(f"📡 STATUS INSTANCIA: {response.status_code}")

        if response.status_code != 200:
            logger.error("❌ Error obteniendo instancias")
            return False

        data = response.json()
        if isinstance(data, dict):
            data = data.get("instance", [])

        if not isinstance(data, list):
            logger.error("❌ Evolution no devolvió lista")
            return False

        for instancia in data:
            nombre = instancia.get("name", "")
            conexion = instancia.get("connectionStatus", "")
            logger.info(f"📲 Instancia encontrada: {nombre} -> {conexion}")

            if nombre == WHATSAPP_INSTANCE:
                if conexion.lower() in ["open", "connected", "online"]:
                    logger.info("✅ Instancia conectada")
                    return True

        logger.warning("⚠️ Instancia no conectada.")
        return False

    except Exception as e:
        logger.error(f"❌ Error verificando instancia: {str(e)}")
        return False

# ==========================================================
# ENVIAR MENSAJE
# ==========================================================
def enviar_mensaje_texto_whatsapp(nombre_instancia: str = None, alumno_id: str = None, entrenador_id: str = None, telefono: str = "", mensaje: str = ""):
    try:
        if not mensaje:
            return {"exito": False, "error": "Mensaje vacío"}

        telefono_limpio = normalizar_telefono_whatsapp(telefono)
        instancia_final = nombre_instancia if nombre_instancia else WHATSAPP_INSTANCE

        logger.info(f"📲 Enviando WhatsApp a {telefono_limpio}")

        url = f"{EVOLUTION_API_URL}/message/sendText/{instancia_final}"
        headers = {
            "Content-Type": "application/json",
            "apikey": EVOLUTION_API_KEY
        }
        payload = {
            "number": telefono_limpio,
            "text": mensaje.strip()
        }

        logger.info(f"📦 PAYLOAD: {payload}")
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        
        logger.info(f"📤 STATUS EVOLUTION: {response.status_code}")
        logger.info(f"📤 RESPUESTA EVOLUTION: {response.text}")

        if response.status_code in [200, 201]:
            try:
                resposta_json = response.json()
            except Exception:
                resposta_json = response.text
            return {"exito": True, "respuesta": resposta_json}

        return {"exito": False, "error": response.text}

    except Exception as e:
        logger.error(f"❌ Error Evolution API: {str(e)}")
        return {"exito": False, "error": str(e)}

# ==========================================================
# COMPATIBILIDAD LEGACY (Automatizaciones y Tareas Diarias)
# ==========================================================
def enviar_mensaje_texto_evolution(nombre_instancia: str = None, alumno_id: str = None, entrenador_id: str = None, telefono: str = "", mensaje: str = ""):
    return enviar_mensaje_texto_whatsapp(
        nombre_instancia=nombre_instancia,
        alumno_id=alumno_id,
        entrenador_id=entrenador_id,
        telefono=telefono,
        mensaje=mensaje
    )

# ==========================================================
# EVOLUTION API MULTI-ENTRENADOR (Panel Web y QR)
# ==========================================================
class EvolutionAPI:
    def __init__(self):
        self.base_url = EVOLUTION_API_URL
        self.api_key = EVOLUTION_API_KEY

    @staticmethod
    def enviar_mensaje(telefono: str, mensaje: str, nombre_instancia: str = None):
        return enviar_mensaje_texto_whatsapp(
            telefono=telefono,
            mensaje=mensaje,
            nombre_instancia=nombre_instancia
        )

    def crear_instancia_y_obtener_qr(self, nombre_instancia: str):
        try:
            headers = {
                "Content-Type": "application/json",
                "apikey": self.api_key
            }
            payload = {
                "instanceName": nombre_instancia,
                "qrcode": True,
                "integration": "WHATSAPP-BAILEYS"
            }
            url_create = f"{self.base_url}/instance/create"

            logger.info(f"🚀 Creando instancia: {nombre_instancia}")
            response = requests.post(url_create, headers=headers, json=payload, timeout=30)
            logger.info(f"📡 RESPONSE CREATE: {response.text}")
            
            data = response.json()

            if isinstance(data, dict) and "qrcode" in data and isinstance(data["qrcode"], dict) and data["qrcode"].get("base64"):
                return {"exito": True, "qr_base64": data["qrcode"]["base64"]}

            if isinstance(data, dict) and data.get("base64"):
                return {"exito": True, "qr_base64": data["base64"]}

            logger.info("♻️ Instancia ya existe. Intentando reconectar...")
            url_connect = f"{self.base_url}/instance/connect/{nombre_instancia}"
            resp_connect = requests.get(url_connect, headers=headers, timeout=30)
            logger.info(f"📡 RESPONSE CONNECT: {resp_connect.text}")
            
            data_connect = resp_connect.json()

            if data_connect.get("base64"):
                return {"exito": True, "qr_base64": data_connect["base64"]}

            return {"exito": False, "error": "La instancia ya está conectada o el QR expiró."}

        except Exception as e:
            logger.error(f"❌ Error creando instancia: {str(e)}")
            return {"exito": False, "error": str(e)}

    def obtener_estado_instancia(self, nombre_instancia: str):
        try:
            headers = {"apikey": self.api_key}
            url = f"{self.base_url}/instance/connectionState/{nombre_instancia}"
            
            response = requests.get(url, headers=headers, timeout=20)
            if response.status_code != 200:
                return {"conectado": False}

            data = response.json()
            estado = str(data.get("instance", {}).get("state", "")).lower()

            return {
                "conectado": estado in ["open", "connected"],
                "estado": estado
            }

        except Exception as e:
            logger.error(f"❌ Error estado instancia: {str(e)}")
            return {"conectado": False, "error": str(e)}