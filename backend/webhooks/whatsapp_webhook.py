
from fastapi import (
    APIRouter,
    Request,
    Response,
    HTTPException,
    status,
    BackgroundTasks
)

from config.settings import settings
from utils.logger import obtener_logger

from database.conexion import supabase
from database.queries import registrar_log_whatsapp

from backend.services.ia_service import (
    procesar_consulta_ia_con_memoria
)

from backend.services.whatsapp_service import (
    enviar_mensaje_texto_evolution,
    normalizar_telefono_whatsapp
)

from backend.services.whatsapp_message_processor import (
    guardar_interaccion_atleta
)

logger = obtener_logger("WhatsAppWebhook")

router = APIRouter()

# =========================================================
# ROOT
# =========================================================

@router.get("/")
def webhook_root():

    return {
        "webhook": "online",
        "status": "active"
    }

# =========================================================
# HEALTH
# =========================================================

@router.get("/health")
def health():

    return {
        "status": "ok",
        "service": "whatsapp_webhook"
    }

# =========================================================
# VERIFICACIÓN META
# =========================================================

@router.get("/whatsapp")
def verificar_webhook_meta(request: Request):

    params = request.query_params

    mode = params.get("hub.mode")
    token = params.get("hub.verify_token")
    challenge = params.get("hub.challenge")

    if (
        mode == "subscribe"
        and token == settings.WHATSAPP_VERIFY_TOKEN
    ):

        logger.info(
            "Webhook Meta validado correctamente."
        )

        return Response(
            content=challenge or "",
            media_type="text/plain"
        )

    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Token mismatch"
    )

# =========================================================
# EXTRAER MENSAJE EVOLUTION API
# =========================================================

def extraer_mensaje(payload: dict):

    try:

        logger.info(
            f"📦 PAYLOAD COMPLETO: {payload}"
        )

        evento = str(
            payload.get("event", "")
        ).strip()

        logger.info(
            f"📡 EVENTO RECIBIDO: {evento}"
        )

        eventos_validos = [
            "messages.upsert",
            "MESSAGES_UPSERT"
        ]

        if evento not in eventos_validos:

            logger.warning(
                f"⚠️ Evento ignorado: {evento}"
            )

            return None

        data = payload.get("data")

        if not isinstance(data, dict):

            logger.warning(
                "⚠️ Payload sin data válida."
            )

            return None

        key = data.get("key", {})

        if not isinstance(key, dict):

            logger.warning(
                "⚠️ Key inválida."
            )

            return None

        remote_jid = str(
            key.get("remoteJid", "")
        ).strip()

        if not remote_jid:

            logger.warning(
                "⚠️ remoteJid vacío."
            )

            return None

        if "@g.us" in remote_jid:

            logger.info(
                "⚠️ Grupo ignorado."
            )

            return None

        from_me = key.get(
            "fromMe",
            False
        )

        if from_me:

            logger.info(
                "⚠️ Mensaje propio ignorado."
            )

            return None

        telefono = (
            remote_jid
            .replace("@s.whatsapp.net", "")
            .replace("@lid", "")
            .replace(":", "")
            .strip()
        )

        if not telefono:

            logger.warning(
                "⚠️ Teléfono vacío."
            )

            return None

        message = data.get("message", {})

        if not isinstance(message, dict):

            logger.warning(
                "⚠️ Message inválido."
            )

            return None

        texto = ""

        if "conversation" in message:

            texto = (
                message.get(
                    "conversation",
                    ""
                )
            )

        elif "extendedTextMessage" in message:

            texto = (
                message
                .get(
                    "extendedTextMessage",
                    {}
                )
                .get(
                    "text",
                    ""
                )
            )

        elif "imageMessage" in message:

            texto = (
                message
                .get(
                    "imageMessage",
                    {}
                )
                .get(
                    "caption",
                    "[IMAGEN]"
                )
            )

        elif "videoMessage" in message:

            texto = (
                message
                .get(
                    "videoMessage",
                    {}
                )
                .get(
                    "caption",
                    "[VIDEO]"
                )
            )

        elif "audioMessage" in message:

            texto = "[AUDIO]"

        elif "documentMessage" in message:

            texto = "[DOCUMENTO]"

        texto = str(texto).strip()

        if not texto:

            logger.warning(
                "⚠️ Texto vacío."
            )

            return None

        logger.info(
            f"📲 TELEFONO EXTRAIDO: {telefono}"
        )

        logger.info(
            f"💬 MENSAJE EXTRAIDO: {texto}"
        )

        return {
            "telefono": telefono,
            "texto": texto
        }

    except Exception as e:

        logger.error(
            f"❌ ERROR EXTRAYENDO MENSAJE: {str(e)}"
        )

        return None

# =========================================================
# BUSCAR ATLETA
# =========================================================

def buscar_atleta_por_telefono(telefono_meta: str):

    try:

        telefono_normalizado = (
            normalizar_telefono_whatsapp(
                telefono_meta
            )
        )

        perfiles = (
            supabase
            .table("perfiles_atletas")
            .select(
                "id, entrenador_id, nombre_completo, telefono"
            )
            .execute()
        )

        for perfil in perfiles.data or []:

            telefono_db = (
                normalizar_telefono_whatsapp(
                    perfil.get("telefono", "")
                )
            )

            if telefono_db == telefono_normalizado:

                return perfil

        return None

    except Exception as e:

        logger.error(
            f"❌ Error buscando atleta: {str(e)}"
        )

        return None

# =========================================================
# PROCESAR MENSAJE
# =========================================================

def procesar_mensaje(payload: dict):

    try:

        resultado = extraer_mensaje(payload)

        if not resultado:

            return

        telefono = resultado["telefono"]
        texto = resultado["texto"]

        atleta = buscar_atleta_por_telefono(
            telefono
        )

        if not atleta:

            return

        alumno_id = atleta["id"]

        entrenador_id = atleta.get(
            "entrenador_id"
        )

        nombre = atleta.get(
            "nombre_completo",
            "Atleta"
        )

        registrar_log_whatsapp(
            alumno_id=alumno_id,
            entrenador_id=entrenador_id,
            direccion="entrante",
            contenido=texto
        )

        # =================================================
        # PROCESADOR INTELIGENTE
        # =================================================

        guardar_interaccion_atleta(
            alumno_id=alumno_id,
            mensaje=texto
        )

        logger.info(
            f"🧠 Procesando IA para {nombre}"
        )

        respuesta_ia = (
            procesar_consulta_ia_con_memoria(
                alumno_id=alumno_id,
                mensaje_alumno=texto
            )
        )

        if not respuesta_ia:

            respuesta_ia = (
                "Estoy actualizando mis servidores IA. "
                "Probá nuevamente en unos minutos."
            )

        instancia_real = str(
            payload.get("instance", "")
        ).strip()

        if not instancia_real:

            instancia_real = (
                settings.WHATSAPP_INSTANCE
            )

        enviado = (
            enviar_mensaje_texto_evolution(
                telefono=telefono,
                mensaje=respuesta_ia,
                nombre_instancia=instancia_real
            )
        )

        logger.info(
            f"✅ Mensaje enviado "
            f"a {nombre} "
            f"estado={enviado}"
        )

    except Exception as e:

        logger.error(
            f"❌ ERROR PROCESANDO MENSAJE: {str(e)}"
        )

# =========================================================
# WEBHOOK PRINCIPAL
# =========================================================

@router.post("/webhook/evolution")
@router.post("/whatsapp")
async def recibir_interaccion_alumno(
    request: Request,
    background_tasks: BackgroundTasks
):

    try:

        payload = await request.json()

        logger.info(
            "✅ Webhook recibido correctamente."
        )

        background_tasks.add_task(
            procesar_mensaje,
            payload
        )

        return {
            "status": "accepted"
        }

    except Exception as e:

        logger.error(
            f"❌ Error webhook: {str(e)}"
        )

        return {
            "status": "error",
            "message": str(e)
        }

