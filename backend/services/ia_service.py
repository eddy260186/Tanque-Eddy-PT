import google.generativeai as genai
import datetime as dt
from datetime import date

from config.settings import settings
from database.conexion import supabase
from utils.logger import obtener_logger

logger = obtener_logger("IAServiceMaster")

# =========================================================
# CONFIGURAR GEMINI
# =========================================================

client = None

if settings.GEMINI_API_KEY:

    try:

        genai.configure(
            api_key=settings.GEMINI_API_KEY
        )

        client = genai.GenerativeModel(
            "gemini-2.0-flash"
        )

        logger.info("✅ Gemini configurado correctamente.")

    except Exception as e:

        logger.error(
            f"❌ Error configurando Gemini: {str(e)}"
        )

else:

    logger.warning("⚠️ GEMINI_API_KEY no encontrada.")

# =========================================================
# GESTION CREDITOS IA
# =========================================================

def gestionar_ia_con_creditos(email_usuario: str):

    try:

        res = (
            supabase
            .table("perfiles_atletas")
            .select(
                "creditos_ia, guia_comprada, fecha_ultima_recarga"
            )
            .eq("email", email_usuario)
            .execute()
        )

        if not res.data:

            return False, 0

        perfil = res.data[0]

        compro_guia = perfil.get(
            "guia_comprada",
            False
        )

        creditos_actuales = int(
            perfil.get("creditos_ia") or 0
        )

        ultima_recarga_str = perfil.get(
            "fecha_ultima_recarga"
        )

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

                (
                    supabase
                    .table("perfiles_atletas")
                    .update({
                        "creditos_ia": 30,
                        "fecha_ultima_recarga": str(hoy)
                    })
                    .eq("email", email_usuario)
                    .execute()
                )

                logger.info(
                    f"🔄 Créditos renovados: {email_usuario}"
                )

        return creditos_actuales > 0, creditos_actuales

    except Exception as e:

        logger.error(
            f"❌ Error créditos IA: {str(e)}"
        )

        return False, 0

# =========================================================
# DESCONTAR CREDITOS
# =========================================================

def descontar_credito(
    email_usuario: str,
    creditos_actuales: int
):

    try:

        nuevo_saldo = max(
            creditos_actuales - 1,
            0
        )

        (
            supabase
            .table("perfiles_atletas")
            .update({
                "creditos_ia": nuevo_saldo
            })
            .eq("email", email_usuario)
            .execute()
        )

        return nuevo_saldo

    except Exception as e:

        logger.error(
            f"❌ Error descontando crédito: {str(e)}"
        )

        return creditos_actuales

# =========================================================
# MOTOR IA WHATSAPP
# =========================================================

def procesar_consulta_ia_con_memoria(
    alumno_id: str,
    mensaje_alumno: str
):

    try:

        logger.info(
            f"🧠 Procesando IA para alumno: {alumno_id}"
        )

        if client is None:

            return "❌ Gemini no configurado."

        fecha_hoy = date.today().isoformat()

        # =====================================================
        # RATE LIMIT
        # =====================================================

        conteo_hoy = (
            supabase
            .table("historial_ia")
            .select("id", count="exact")
            .eq("alumno_id", alumno_id)
            .eq("rol_mensaje", "user")
            .gte(
                "fecha_creacion",
                f"{fecha_hoy}T00:00:00Z"
            )
            .execute()
        )

        if (conteo_hoy.count or 0) >= 10:

            return (
                "⚠️ Alcanzaste el límite diario "
                "de consultas IA 💪"
            )

        # =====================================================
        # PERFIL CLIENTE
        # =====================================================

        atleta_query = (
            supabase
            .table("perfiles_atletas")
            .select("""
                nombre_completo,
                genero,
                objetivo_principal,
                telefono,
                tipo_plan,
                entrenador_id
            """)
            .eq("id", alumno_id)
            .execute()
        )

        if not atleta_query.data:

            return "❌ No encontré tu perfil."

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
            "Mantenerse saludable"
        )

        telefono = atleta_data.get(
            "telefono",
            "No definido"
        )

        tipo_plan = atleta_data.get(
            "tipo_plan",
            "Plan general"
        )

        logger.info(
            f"✅ Perfil encontrado: {nombre}"
        )

        # =====================================================
        # BIOMETRIA
        # =====================================================

        biometria_query = (
            supabase
            .table("evaluaciones_biometricas")
            .select("*")
            .eq("alumno_id", alumno_id)
            .limit(1)
            .execute()
        )

        biometria = {}

        if biometria_query.data:

            biometria = biometria_query.data[0]

        peso = biometria.get(
            "peso_actual",
            "No definido"
        )

        edad = biometria.get(
            "edad",
            "No definida"
        )

        experiencia = biometria.get(
            "experiencia_entrenamiento",
            "No definida"
        )

        objetivo_biometrico = biometria.get(
            "objetivo_fisico",
            "No definido"
        )

        # =====================================================
        # HISTORIAL IA
        # =====================================================

        historial_query = (
            supabase
            .table("historial_ia")
            .select(
                "rol_mensaje, contenido"
            )
            .eq("alumno_id", alumno_id)
            .order("fecha_creacion", desc=True)
            .limit(6)
            .execute()
        )

        historial_texto = ""

        if historial_query.data:

            historial_query.data.reverse()

            for item in historial_query.data:

                rol = item.get(
                    "rol_mensaje",
                    "user"
                )

                contenido = item.get(
                    "contenido",
                    ""
                )

                historial_texto += (
                    f"{rol}: {contenido}\n"
                )

        # =====================================================
        # PROMPT FINAL
        # =====================================================

        prompt_final = f"""
Sos la IA oficial de Eddy Personal Trainer.

Especialista en:
- fitness
- hipertrofia
- pérdida de grasa
- nutrición
- recomposición corporal
- hábitos saludables

INFORMACIÓN DEL CLIENTE:

Nombre: {nombre}
Genero: {genero}
Objetivo principal: {objetivo}
Objetivo físico: {objetivo_biometrico}
Peso actual: {peso}
Edad: {edad}
Experiencia: {experiencia}
Tipo de plan: {tipo_plan}

HISTORIAL RECIENTE:
{historial_texto}

INSTRUCCIONES:

- Respuestas personalizadas.
- Habla como entrenador profesional argentino.
- Máximo 6 líneas.
- Sé claro y práctico.
- Da ejercicios específicos.
- Da recomendaciones útiles.
- No repitas frases genéricas.
- Motiva sin exagerar.
- Si el usuario es principiante explicá simple.

MENSAJE DEL CLIENTE:
{mensaje_alumno}
"""

        logger.info(
            "🚀 Enviando prompt a Gemini..."
        )

        response = client.generate_content(
            prompt_final
        )

        respuesta_texto = response.text

        logger.info(
            "✅ Respuesta Gemini recibida."
        )

        if not respuesta_texto:

            respuesta_texto = (
                "⚠️ Gemini no devolvió texto."
            )

        respuesta_texto = str(
            respuesta_texto
        ).strip()

        # =====================================================
        # GUARDAR HISTORIAL
        # =====================================================

        (
            supabase
            .table("historial_ia")
            .insert({
                "alumno_id": alumno_id,
                "rol_mensaje": "user",
                "contenido": mensaje_alumno
            })
            .execute()
        )

        (
            supabase
            .table("historial_ia")
            .insert({
                "alumno_id": alumno_id,
                "rol_mensaje": "model",
                "contenido": respuesta_texto
            })
            .execute()
        )

        logger.info(
            "✅ Historial guardado."
        )

        return respuesta_texto

    except Exception as e:

        error_real = str(e)

        logger.error(
            f"❌ ERROR REAL GEMINI: {error_real}"
        )

        return (
            f"❌ ERROR IA:\n{error_real}"
        )