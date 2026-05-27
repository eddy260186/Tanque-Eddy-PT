import google.generativeai as genai
import datetime as dt
from datetime import datetime, date
from config.settings import settings
from database.conexion import supabase
from utils.logger import obtener_logger

logger = obtener_logger("IAServiceMaster")

# =========================================================================
# CONFIGURACIÓN GEMINI
# =========================================================================

if settings.GEMINI_API_KEY:
    genai.configure(api_key=settings.GEMINI_API_KEY)
    logger.info("✅ Gemini configurado correctamente")
else:
    logger.warning("⚠️ GEMINI_API_KEY no encontrada")

# =========================================================================
# 🎯 CRÉDITOS IA WEB
# =========================================================================

def gestionar_ia_con_creditos(email_usuario: str) -> tuple[bool, int]:
    try:
        res = (
            supabase.table("perfiles_atletas")
            .select("creditos_ia, guia_comprada, fecha_ultima_recarga")
            .eq("email", email_usuario)
            .execute()
        )

        if res.data:
            perfil = res.data[0]

            compro_guia = perfil.get("guia_comprada", False)
            valor_db = perfil.get("creditos_ia")

            creditos_actuales = 0 if valor_db is None else int(valor_db)

            ultima_recarga_str = perfil.get("fecha_ultima_recarga")

            if compro_guia:

                hoy = dt.date.today()

                try:
                    ultima_recarga = (
                        dt.datetime.strptime(
                            ultima_recarga_str,
                            "%Y-%m-%d"
                        ).date()
                        if ultima_recarga_str
                        else None
                    )

                except:
                    ultima_recarga = None

                if (
                    ultima_recarga is None
                    or (hoy - ultima_recarga).days >= 30
                ):

                    creditos_actuales = 30

                    supabase.table("perfiles_atletas").update({
                        "creditos_ia": 30,
                        "fecha_ultima_recarga": str(hoy)
                    }).eq("email", email_usuario).execute()

                    logger.info(
                        f"🔄 Créditos renovados para: {email_usuario}"
                    )

            if creditos_actuales > 0:
                return True, creditos_actuales

    except Exception as e:
        logger.error(f"❌ Error créditos IA: {str(e)}")

    return False, 0


def descontar_credito(email_usuario: str, creditos_actuales: int) -> int:

    try:

        nuevo_saldo = creditos_actuales - 1

        supabase.table("perfiles_atletas").update({
            "creditos_ia": nuevo_saldo
        }).eq("email", email_usuario).execute()

        return nuevo_saldo

    except Exception as e:

        logger.error(f"❌ Error descontando crédito: {str(e)}")

        return creditos_actuales


# =========================================================================
# 🧠 IA WHATSAPP CON MEMORIA
# =========================================================================

def procesar_consulta_ia_con_memoria(
    alumno_id: str,
    mensaje_alumno: str
) -> str:

    try:

        logger.info(f"🧠 Procesando IA para alumno: {alumno_id}")

        fecha_hoy = date.today().isoformat()

        # =========================================================================
        # RATE LIMIT
        # =========================================================================

        conteo_hoy = (
            supabase.table("historial_ia")
            .select("id", count="exact")
            .eq("alumno_id", alumno_id)
            .eq("rol_mensaje", "user")
            .gte("fecha_creacion", f"{fecha_hoy}T00:00:00Z")
            .execute()
        )

        total_hoy = conteo_hoy.count or 0

        logger.info(f"📊 Mensajes hoy: {total_hoy}")

        if total_hoy >= 10:

            return (
                "⚠️ Alcanzaste el límite diario de consultas IA.\n\n"
                "Volvé mañana para seguir entrenando 💪"
            )

        # =========================================================================
        # PERFIL DEL ATLETA
        # =========================================================================

        atleta_query = (
            supabase.table("perfiles_atletas")
            .select(
                "nombre_completo, genero, objetivo_principal"
            )
            .eq("id", alumno_id)
            .execute()
        )

        if not atleta_query.data:

            logger.warning("⚠️ Atleta no encontrado")

            return "No encontré tu perfil."

        atleta_data = atleta_query.data[0]

        nombre = atleta_data.get(
            "nombre_completo",
            "Atleta"
        )

        genero = atleta_data.get(
            "genero",
            "No definido"
        )

        objetivo = atleta_data.get(
            "objetivo_principal",
            "Mejorar salud"
        )

        # =========================================================================
        # HISTORIAL
        # =========================================================================

        historial_query = (
            supabase.table("historial_ia")
            .select("rol_mensaje, contenido")
            .eq("alumno_id", alumno_id)
            .order("fecha_creacion", desc=True)
            .limit(6)
            .execute()
        )

        mensajes_pasados = (
            list(reversed(historial_query.data))
            if historial_query.data
            else []
        )

        # =========================================================================
        # PROMPT SISTEMA
        # =========================================================================

        system_instruction = f"""
Sos Eddy AI, entrenador virtual premium.

DATOS DEL CLIENTE:
- Nombre: {nombre}
- Género: {genero}
- Objetivo: {objetivo}

REGLAS:
- Respuestas cortas
- Máximo 3 párrafos
- Estilo motivador argentino
- Profesional
- Solo fitness/nutrición
- No inventar datos médicos
"""

        # =========================================================================
        # CONTENIDO CONVERSACIÓN
        # =========================================================================

        contents = []

        for msg in mensajes_pasados:

            contents.append({
                "role": (
                    "user"
                    if msg["rol_mensaje"] == "user"
                    else "model"
                ),
                "parts": [msg["contenido"]]
            })

        contents.append({
            "role": "user",
            "parts": [mensaje_alumno]
        })

        # =========================================================================
        # GEMINI NUEVO
        # =========================================================================

        model = genai.GenerativeModel(
            model_name="gemini-1.5-flash"
        )

        response = model.generate_content(
            contents,
            generation_config={
                "temperature": 0.7,
                "max_output_tokens": 300,
            }
        )

        respuesta_texto = response.text.strip()

        logger.info(f"🤖 RESPUESTA IA: {respuesta_texto}")

        # =========================================================================
        # GUARDAR MEMORIA
        # =========================================================================

        try:

            supabase.table("historial_ia").insert({
                "alumno_id": alumno_id,
                "rol_mensaje": "user",
                "contenido": mensaje_alumno
            }).execute()

            supabase.table("historial_ia").insert({
                "alumno_id": alumno_id,
                "rol_mensaje": "model",
                "contenido": respuesta_texto
            }).execute()

        except Exception as db_error:

            logger.error(
                f"❌ Error guardando historial: {db_error}"
            )

        return respuesta_texto

    except Exception as e:

        logger.error(
            f"❌ ERROR CRÍTICO IA: {str(e)}"
        )

        return (
            "👋 Estoy actualizando mis servidores IA.\n"
            "Probá nuevamente en unos segundos."
        )