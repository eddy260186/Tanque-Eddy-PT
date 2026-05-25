from fastapi import APIRouter, Request, Response, HTTPException, status
from config.settings import settings
from utils.logger import obtener_logger
from database.conexion import supabase
from database.queries import registrar_log_whatsapp
from backend.services.ia_service import procesar_consulta_ia_con_memoria
from backend.services.whatsapp_service import enviar_mensaje_texto_whatsapp, normalizar_telefono_whatsapp

logger = obtener_logger("WhatsAppWebhookMaster")
router = APIRouter()


@router.get("/whatsapp")
def verificar_webhook_meta(request: Request):
    """
    Verifica el webhook desde Meta Developers.
    Usa WHATSAPP_VERIFY_TOKEN, no el token privado de la API.
    """
    params = request.query_params
    mode = params.get("hub.mode")
    token = params.get("hub.verify_token")
    challenge = params.get("hub.challenge")

    if mode == "subscribe" and token == settings.WHATSAPP_VERIFY_TOKEN:
        logger.info("Webhook de WhatsApp validado correctamente.")
        return Response(content=challenge or "", media_type="text/plain")

    if mode or token:
        logger.warning("Intento de verificacion de webhook con token incorrecto.")
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Token mismatch")

    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Missing parameters")


def _extraer_mensaje_texto(payload: dict) -> tuple[str, str]:
    entry = payload.get("entry") or []
    changes = (entry[0].get("changes") if entry else []) or []
    value = changes[0].get("value", {}) if changes else {}
    messages = value.get("messages") or []

    if not messages:
        return "", ""

    msg = messages[0]
    telefono = msg.get("from", "")
    texto = (msg.get("text") or {}).get("body", "").strip()
    return telefono, texto


def _buscar_atleta_por_telefono(telefono_meta: str) -> dict:
    telefono_normalizado = normalizar_telefono_whatsapp(telefono_meta)
    if not telefono_normalizado:
        return {}

    try:
        exacto = supabase.table("perfiles_atletas")\
            .select("id, entrenador_id, nombre_completo, telefono")\
            .eq("telefono", telefono_meta)\
            .limit(1)\
            .execute()
        if exacto.data:
            return exacto.data[0]

        con_mas = supabase.table("perfiles_atletas")\
            .select("id, entrenador_id, nombre_completo, telefono")\
            .eq("telefono", f"+{telefono_normalizado}")\
            .limit(1)\
            .execute()
        if con_mas.data:
            return con_mas.data[0]

        # Fallback tolerante: cubre telefonos guardados con espacios, guiones o parentesis.
        perfiles = supabase.table("perfiles_atletas")\
            .select("id, entrenador_id, nombre_completo, telefono")\
            .execute()
        for perfil in perfiles.data or []:
            if normalizar_telefono_whatsapp(perfil.get("telefono")) == telefono_normalizado:
                return perfil
    except Exception as e:
        logger.error(f"Error buscando atleta por telefono: {e}")

    return {}


@router.post("/whatsapp")
async def recibir_interaccion_alumno(request: Request):
    """
    Recibe mensajes de WhatsApp, identifica al alumno, responde con IA y guarda historial.
    """
    try:
        payload = await request.json()
        telefono_original, texto_recibido = _extraer_mensaje_texto(payload)

        if not telefono_original:
            return {"status": "ignored", "reason": "sin_mensaje"}

        if not texto_recibido:
            return {"status": "ignored", "reason": "sin_texto"}

        logger.info(f"WhatsApp entrante de [{telefono_original}]: {texto_recibido}")

        atleta = _buscar_atleta_por_telefono(telefono_original)
        if not atleta:
            logger.warning(f"Mensaje recibido de numero no registrado: {telefono_original}")
            return {"status": "unregistered_user"}

        alumno_id = atleta["id"]
        entrenador_id = atleta.get("entrenador_id")
        nombre_alumno = atleta.get("nombre_completo", "Atleta")

        registrar_log_whatsapp(
            alumno_id=alumno_id,
            entrenador_id=entrenador_id,
            direccion="entrante",
            contenido=texto_recibido,
        )

        respuesta_ia = procesar_consulta_ia_con_memoria(
            alumno_id=alumno_id,
            mensaje_alumno=texto_recibido,
        )

        enviado = enviar_mensaje_texto_whatsapp(
            alumno_id=alumno_id,
            entrenador_id=entrenador_id,
            telefono=telefono_original,
            mensaje=respuesta_ia,
        )

        logger.info(f"Circuito WhatsApp cerrado para {nombre_alumno}. Enviado={enviado}")
        return {"status": "success", "processed": True, "sent": enviado}

    except Exception as e:
        logger.error(f"Fallo critico en webhook WhatsApp: {str(e)}")
        return {"status": "error", "message": str(e)}

