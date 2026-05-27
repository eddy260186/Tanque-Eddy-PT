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
    enviar_mensaje_texto_whatsapp,
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
            f"PAYLOAD COMPLETO: {payload}"
        )

        # =====================================================
        # VALIDAR EVENTO
        # =====================================================

        evento = payload.get("event", "")

        if evento != "messages.upsert":

            logger.info(
                f"Evento ignorado: {evento}"
            )

            return "", ""

        # =====================================================
        # DATA
        # =====================================================

        data = payload.get("data", {})

        if not data:

            logger.warning(
                "Payload sin data."
            )

            return "", ""

        # =====================================================
        # KEY
        # =====================================================

        key = data.get("key", {})

        remote_jid = key.get(
            "remoteJid",
            ""
        )

        if not remote_jid:

            logger.warning(
                "remoteJid vacío."
            )

            return "", ""

        telefono = (
            remote_jid
            .replace("@s.whatsapp.net", "")
            .replace("@g.us", "")
        )

        # =====================================================
        # IGNORAR GRUPOS
        # =====================================================

        if "@g.us" in remote_jid:

            logger.info(
                "Mensaje grupal ignorado."
            )

            return "", ""

        # =====================================================
        # IGNORAR MENSAJES PROPIOS
        # =====================================================

        from_me = key.get("fromMe", False)

        if from_me:

            logger.info(
                "Mensaje propio ignorado."
            )

            return "", ""

        # =====================================================
        # MENSAJE
        # =====================================================

        message = data.get("message", {})

        texto = ""

        # TEXTO SIMPLE

        if "conversation" in message:

            texto = (
                message.get(
                    "conversation",
                    ""
                )
            )

        # TEXTO EXTENDIDO

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

        # IMAGEN CON TEXTO

        elif "imageMessage" in message:

            texto = (
                message
                .get(
                    "imageMessage",
                    {}
                )
                .get(
                    "caption",
                    ""
                )
            )

        # VIDEO CON TEXTO

        elif "videoMessage" in message:

            texto = (
                message
                .get(
                    "videoMessage",
                    {}
                )
                .get(
                    "caption",
                    ""
                )
            )

        texto = texto.strip()

        logger.info(
            f"Mensaje extraído "
            f"telefono={telefono} "
            f"texto={texto}"
        )

        return telefono, texto

    except Exception as e:

        logger.error(
            f"Error extrayendo mensaje: {str(e)}"
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
                    f"Atleta encontrado: "
                    f"{perfil.get('nombre_completo')}"
                )

                return perfil

        logger.warning(
            f"Número no encontrado: "
            f"{telefono_normalizado}"
        )

        return None

    except Exception as e:

        logger.error(
            f"Error buscando atleta: {str(e)}"
        )

        return None

# =========================================================
# PROCESADOR PRINCIPAL
# =========================================================

def procesar_mensaje(payload: dict):

    try:

        telefono, texto = extraer_mensaje(payload)

        if not telefono:

            logger.warning(
                "Mensaje ignorado: teléfono vacío."
            )

            return

        if not texto:

            logger.warning(
                "Mensaje ignorado: texto vacío."
            )

            return

        logger.info(
            f"Mensaje entrante "
            f"[{telefono}]: {texto}"
        )

        atleta = buscar_atleta_por_telefono(
            telefono
        )

        if not atleta:

            logger.warning(
                f"Número no registrado: "
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

        # =================================================
        # LOG ENTRANTE
        # =================================================

        registrar_log_whatsapp(
            alumno_id=alumno_id,
            entrenador_id=entrenador_id,
            direccion="entrante",
            contenido=texto
        )

        # =================================================
        # IA
        # =================================================

        logger.info(
            f"Procesando IA para {nombre}"
        )

        respuesta_ia = (
            procesar_consulta_ia_con_memoria(
                alumno_id=alumno_id,
                mensaje_alumno=texto
            )
        )

        if not respuesta_ia:

            respuesta_ia = (
                "No pude procesar tu mensaje."
            )

        logger.info(
            f"Respuesta IA: {respuesta_ia}"
        )

        # =================================================
        # ENVIAR RESPUESTA
        # =================================================

        enviado = (
            enviar_mensaje_texto_whatsapp(
                nombre_instancia="eddypt",
                alumno_id=alumno_id,
                entrenador_id=entrenador_id,
                telefono=telefono,
                mensaje=respuesta_ia
            )
        )

        logger.info(
            f"Mensaje enviado "
            f"a {nombre}. "
            f"Estado={enviado}"
        )

    except Exception as e:

        logger.error(
            f"Error procesando mensaje: {str(e)}"
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
            "Webhook recibido correctamente."
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
            f"Error webhook: {str(e)}"
        )

        return {
            "status": "error",
            "message": str(e)
        }