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

        evento = payload.get("event", "")

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

            return "", ""

        data = payload.get("data", {})

        if not data:

            logger.warning(
                "⚠️ Payload sin data."
            )

            return "", ""

        key = data.get("key", {})

        remote_jid = key.get(
            "remoteJid",
            ""
        )

        if not remote_jid:

            logger.warning(
                "⚠️ remoteJid vacío."
            )

            return "", ""

        if "@g.us" in remote_jid:

            logger.info(
                "⚠️ Grupo ignorado."
            )

            return "", ""

        from_me = key.get(
            "fromMe",
            False
        )

        if from_me:

            logger.info(
                "⚠️ Mensaje propio ignorado."
            )

            return "", ""

        telefono = (
            remote_jid
            .replace("@s.whatsapp.net", "")
            .replace("@lid", "")
            .replace(":", "")
            .strip()
        )

        message = data.get("message", {})

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

            return "", ""

        logger.info(
            f"📲 TELEFONO EXTRAIDO: {telefono}"
        )

        logger.info(
            f"💬 MENSAJE EXTRAIDO: {texto}"
        )

        return telefono, texto

    except Exception as e:

        logger.error(
            f"❌ ERROR EXTRAYENDO MENSAJE: {str(e)}"
        )

        return "", ""

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

        logger.info(
            f"📞 Buscando teléfono: "
            f"{telefono_normalizado}"
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

                logger.info(
                    f"✅ Atleta encontrado: "
                    f"{perfil.get('nombre_completo')}"
                )

                return perfil

        logger.warning(
            f"❌ Número no encontrado: "
            f"{telefono_normalizado}"
        )

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

        telefono, texto = extraer_mensaje(payload)

        if not telefono:

            logger.warning(
                "⚠️ Teléfono vacío."
            )

            return

        if not texto:

            logger.warning(
                "⚠️ Texto vacío."
            )

            return

        logger.info(
            f"📩 MENSAJE ENTRANTE "
            f"[{telefono}]: {texto}"
        )

        atleta = buscar_atleta_por_telefono(
            telefono
        )

        if not atleta:

            logger.warning(
                f"⚠️ Usuario no registrado: "
                f"{telefono}"
            )

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

        logger.info(
            f"🤖 RESPUESTA IA: {respuesta_ia}"
        )

        # =================================================
        # INSTANCIA REAL DEL PAYLOAD
        # =================================================

        instancia_real = payload.get(
            "instance",
            ""
        )

        logger.info(
            f"📲 INSTANCIA PAYLOAD: "
            f"{instancia_real}"
        )

        if not instancia_real:

            instancia_real = (
                settings.WHATSAPP_INSTANCE
            )

            logger.warning(
                f"⚠️ Payload sin instancia. "
                f"Usando fallback: "
                f"{instancia_real}"
            )

        # =================================================
        # ENVIAR RESPUESTA
        # =================================================

        enviado = (
            enviar_mensaje_texto_evolution(
                nombre_instancia=instancia_real,
                alumno_id=alumno_id,
                entrenador_id=entrenador_id,
                telefono=telefono,
                mensaje=respuesta_ia
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