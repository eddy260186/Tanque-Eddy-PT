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
        "webhook": "online"
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
# EXTRAER MENSAJE
# =========================================================

def extraer_mensaje(payload: dict):

    try:

        entry = payload.get("entry", [])

        if not entry:
            return "", ""

        changes = entry[0].get("changes", [])

        if not changes:
            return "", ""

        value = changes[0].get("value", {})

        messages = value.get("messages", [])

        if not messages:
            return "", ""

        msg = messages[0]

        telefono = msg.get("from", "")

        texto = (
            msg.get("text", {})
            .get("body", "")
            .strip()
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
                return perfil

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
            return

        if not texto:
            return

        logger.info(
            f"Mensaje entrante [{telefono}]: {texto}"
        )

        atleta = buscar_atleta_por_telefono(
            telefono
        )

        if not atleta:

            logger.warning(
                f"Número no registrado: {telefono}"
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

        respuesta_ia = (
            procesar_consulta_ia_con_memoria(
                alumno_id=alumno_id,
                mensaje_alumno=texto
            )
        )

        # =================================================
        # RESPUESTA
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
            f"Flujo completado para {nombre}. "
            f"Enviado={enviado}"
        )

    except Exception as e:

        logger.error(
            f"Error procesando mensaje: {str(e)}"
        )

# =========================================================
# WEBHOOK
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