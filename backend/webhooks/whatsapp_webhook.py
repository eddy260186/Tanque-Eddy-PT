from fastapi import APIRouter, Request, Response, HTTPException, status
from config.settings import settings
from utils.logger import obtener_logger
from database.conexion import supabase
from backend.services.ia_service import procesar_consulta_ia_con_memoria
from backend.services.whatsapp_service import enviar_mensaje_texto_whatsapp

logger = obtener_logger("WhatsAppWebhookMaster")
router = APIRouter()

VERIFY_TOKEN = settings.WHATSAPP_TOKEN or "mi_token_secreto_eddy_pt_2026"

@router.get("/whatsapp")
def verificar_webhook_meta(request: Request):
    """
    Validador obligatorio para la consola de Meta Developers.
    """
    params = request.query_params
    mode = params.get("hub.mode")
    token = params.get("hub.verify_token")
    challenge = params.get("hub.challenge")

    if mode and token:
        if mode == "subscribe" and token == VERIFY_TOKEN:
            logger.info("✅ Servidor validado correctamente ante la Meta API.")
            return Response(content=challenge, media_type="text/plain")
        else:
            logger.warning("❌ Intento de hackeo o token incorrecto en webhook.")
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Token mismatch")
            
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Missing parameters")


@router.post("/whatsapp")
async def recibir_interaccion_alumno(request: Request):
    """
    EL INTERCEPTOR MÁGICO: Escucha, procesa con contexto e IA, y responde al instante.
    """
    try:
        payload = await request.json()
        
        # 1. Extracción segura de la estructura anidada de Meta Cloud API
        entry = payload.get("entry", [])[0]
        changes = entry.get("changes", [])[0]
        value = changes.get("value", {})
        messages = value.get("messages", [])

        if not messages:
            return {"status": "ignored", "reason": "No contiene estructura de mensajes (ej. fue un estado de entrega)."}

        msg = messages[0]
        telefono_original = msg.get("from") # El número de WhatsApp del alumno
        texto_recibido = msg.get("text", {}).get("body", "").strip()

        if not texto_recibido:
            return {"status": "ignored", "reason": "El mensaje no contiene texto plano."}

        logger.info(f"📩 WhatsApp entrante de [{telefono_original}]: '{texto_recibido}'")

        # 2. IDENTIFICACIÓN MULTI-INQUILINO (Cruzar teléfono con base de datos)
        # Buscamos quién es el atleta y quién es su entrenador asignado
        atleta_query = supabase.table("perfiles_atletas")\
            .select("id, entrenador_id, nombre_completo")\
            .eq("telefono", telefono_original)\
            .execute()

        if not atleta_query.data:
            logger.warning(f"⚠️ Mensaje recibido de un número no registrado en el SaaS: {telefono_original}")
            return {"status": "unregistered_user"}

        atleta = atleta_query.data[0]
        alumno_id = atleta["id"]
        entrenador_id = atleta["entrenador_id"]
        nombre_alumno = atleta["nombre_completo"]

        # 3. CONTEXTO E IA EN ACCIÓN
        # Mandamos el mensaje al módulo de ia_service que maneja la memoria y el rate limiter
        respuesta_ia = procesar_consulta_ia_con_memoria(
            alumno_id=alumno_id, 
            mensaje_alumno=texto_recibido
        )

        # 4. DISPARO DE RESPUESTA DE SALIDA
        # Usamos el motor de whatsapp_service para mandarle la respuesta de Gemini al alumno
        enviar_mensaje_texto_whatsapp(
            alumno_id=alumno_id,
            entrenador_id=entrenador_id,
            telefono=telefono_original,
            mensaje=respuesta_ia
        )

        logger.info(f"🚀 Circuito cerrado con éxito para el alumno: {nombre_alumno}")
        return {"status": "success", "processed": True}

    except Exception as e:
        logger.error(f"❌ Fallo crítico en el router del webhook: {str(e)}")
        return {"status": "error", "message": str(e)}