import requests
import streamlit as st
from config.settings import settings
from utils.logger import obtener_logger
from database.queries import registrar_log_whatsapp

logger = obtener_logger("WhatsAppService")

class EvolutionAPI:
    """
    Conector de Alta Gama para el motor Evolution API alojado en Railway.
    Gobierna la creación de instancias dinámicas y el despacho de flujos de IA.
    """
    def __init__(self):
        # Extraemos las credenciales guardadas de forma segura en los secretos del SaaS
        self.base_url = st.secrets.get("EVOLUTION_API_URL", "https://evolution-api-production-a15fc.up.railway.app").rstrip("/")
        self.api_key = st.secrets.get("EVOLUTION_API_KEY", "")
        
        self.headers = {
            "Content-Type": "application/json",
            "apikey": self.api_key
        }

    def crear_instancia_y_obtener_qr(self, nombre_instancia):
        """
        Inicializa un contenedor virtual para el profesor en el cluster de Railway.
        Devuelve el QR de emparejamiento Base64 listo para inyección en la UI de Streamlit.
        """
        url = f"{self.base_url}/instance/create"
        payload = {
            "instanceName": nombre_instancia,
            "qrcode": True,
            "integration": "WHATSAPP-BAILEYS"
        }
        
        try:
            response = requests.post(url, headers=self.headers, json=payload, timeout=15)
            data = response.json()
            
            if response.status_code in [200, 201]:
                return {"exito": True, "qr_base64": data.get("qrcode", {}).get("base64")}
            elif response.status_code == 403 or "already exists" in str(data.get("message", "")):
                return self.conectar_instancia(nombre_instancia)
            else:
                return {"exito": False, "error": data.get("message", "Falla de comunicación con el servidor.")}
        except Exception as e:
            return {"exito": False, "error": f"Error de conexión de red: {str(e)}"}

    def conectar_instancia(self, nombre_instancia):
        """
        Intenta recuperar el flujo del código QR si la instancia ya existe pero no está vinculada.
        """
        url = f"{self.base_url}/instance/connect/{nombre_instancia}"
        try:
            response = requests.get(url, headers=self.headers, timeout=15)
            data = response.json()
            if "base64" in data:
                return {"exito": True, "qr_base64": data["base64"]}
            elif data.get("code") == "instance_already_connected":
                return {"exito": False, "error": "CONNECTED_ALREADY"}
            return {"exito": False, "error": "No se pudo recuperar el flujo del código QR."}
        except Exception as e:
            return {"exito": False, "error": str(e)}

def normalizar_telefono_whatsapp(telefono: str) -> str:
    """
    Limpia el string del teléfono dejando únicamente los dígitos numéricos.
    Elimina signos +, espacios, guiones y previene errores de tipeo.
    """
    return "".join(filter(str.isdigit, str(telefono or "")))

def enviar_mensaje_texto_evolution(nombre_instancia: str, alumno_id: str, entrenador_id: str, telefono: str, mensaje: str) -> dict:
    """
    Despacha un mensaje de texto automatizado en tiempo real usando la línea del Coach.
    Elimina el sufijo obsoleto de WhatsApp para acoplarse al estándar moderno de Evolution.
    """
    base_url = st.secrets.get("EVOLUTION_API_URL", "https://evolution-api-production-a15fc.up.railway.app").rstrip("/")
    api_key = st.secrets.get("EVOLUTION_API_KEY", "")
    
    telefono_limpio = normalizar_telefono_whatsapp(telefono)
    if not telefono_limpio or not mensaje or not mensaje.strip():
        logger.error("Envío cancelado: Parámetros de teléfono o mensaje inválidos.")
        return {"exito": False, "error": "El número de teléfono o el mensaje están vacíos."}

    url = f"{base_url}/message/sendText/{nombre_instancia}"
    headers = {
        "Content-Type": "application/json",
        "apikey": api_key
    }
    
    # Formato universal limpio exigido por la API de Railway
    payload = {
        "number": telefono_limpio,
        "options": {
            "delay": 1200,
            "presence": "composing"
        },
        "textMessage": {
            "text": mensaje.strip()
        }
    }

    try:
        respuesta = requests.post(url, json=payload, headers=headers, timeout=15)
        if respuesta.status_code in [200, 201]:
            try:
                registrar_log_whatsapp(
                    alumno_id=alumno_id,
                    entrenador_id=entrenador_id,
                    direccion="saliente",
                    contenido=mensaje.strip()
                )
            except Exception as log_err:
                logger.warning(f"No se pudo registrar el log en la BD: {log_err}")
                
            logger.info(f"Mensaje de Evolution enviado correctamente a {telefono_limpio}.")
            return {"exito": True, "error": None}
        
        # Atrapamos la respuesta exacta del servidor si rebota (ej: instancia desconectada)
        error_msg = f"Railway HTTP {respuesta.status_code}: {respuesta.text}"
        logger.error(error_msg)
        return {"exito": False, "error": error_msg}
        
    except Exception as e:
        error_msg = f"Error crítico de red conectando con Evolution API: {str(e)}"
        logger.error(error_msg)
        return {"exito": False, "error": error_msg}