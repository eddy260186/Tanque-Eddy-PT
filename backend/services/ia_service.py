import google.generativeai as genai
import datetime as dt
from datetime import datetime, date
from config.settings import settings
from database.conexion import supabase
from utils.logger import obtener_logger

logger = obtener_logger("IAServiceMaster")

# Inicialización oficial de la API de Google Gemini
if settings.GEMINI_API_KEY:
    genai.configure(api_key=settings.GEMINI_API_KEY)
else:
    logger.warning("⚠️ GEMINI_API_KEY no encontrada en la configuración centralizada.")


# =========================================================================
# 🎯 APARTADO A: LOGICA DE CRÉDITOS PARA CONSULTORÍA WEB (Tu código original)
# =========================================================================

def gestionar_ia_con_creditos(email_usuario: str) -> tuple[bool, int]:
    """
    Valida y administra los créditos de la consulta web del Team Eddy.
    Maneja la renovación automática de 30 créditos cada 30 días si compró la guía.
    """
    try:
        res = supabase.table("perfiles_atletas")\
            .select("creditos_ia, guia_comprada, fecha_ultima_recarga")\
            .eq("email", email_usuario)\
            .execute()
        
        if res.data:
            perfil = res.data[0]
            compro_guia = perfil.get('guia_comprada', False)
            valor_db = perfil.get('creditos_ia')
            creditos_actuales = 0 if valor_db is None else int(valor_db)
            ultima_recarga_str = perfil.get('fecha_ultima_recarga')

            if compro_guia:
                hoy = dt.date.today()
                try:
                    ultima_recarga = dt.datetime.strptime(ultima_recarga_str, '%Y-%m-%d').date() if ultima_recarga_str else None
                except:
                    ultima_recarga = None

                # Si pasaron 30 días o nunca se recargó, renovamos los 30 créditos elite
                if ultima_recarga is None or (hoy - ultima_recarga).days >= 30:
                    creditos_actuales = 30
                    supabase.table("perfiles_atletas").update({
                        "creditos_ia": 30,
                        "fecha_ultima_recarga": str(hoy)
                    }).eq("email", email_usuario).execute()
                    logger.info(f"🔄 Créditos renovados automáticamente para el usuario: {email_usuario}")

            if creditos_actuales > 0:
                return True, creditos_actuales
                
    except Exception as e:
        logger.error(f"❌ Error al gestionar créditos de IA web para {email_usuario}: {str(e)}")
        
    return False, 0


def descontar_credito(email_usuario: str, creditos_actuales: int) -> int:
    """
    Resta un crédito en la base de datos tras una consulta exitosa en la web.
    """
    try:
        nuevo_saldo = creditos_actuales - 1
        supabase.table("perfiles_atletas").update({"creditos_ia": nuevo_saldo}).eq("email", email_usuario).execute()
        return nuevo_saldo
    except Exception as e:
        logger.error(f"❌ Error al descontar crédito web para {email_usuario}: {str(e)}")
        return creditos_actuales


# =========================================================================
# 🧠 APARTADO B: MOTOR DE IA CON MEMORIA Y RATE LIMITS (Para WhatsApp)
# =========================================================================

def procesar_consulta_ia_con_memoria(alumno_id: str, mensaje_alumno: str) -> str:
    """
    Procesador inteligente de IA para el flujo asíncrono de WhatsApp.
    Aplica límites duros de 10 mensajes diarios y consume historial_ia.
    """
    try:
        fecha_hoy = date.today().isoformat()

        # RATE LIMITER: Máximo 10 mensajes diarios por WhatsApp
        conteo_hoy = supabase.table("historial_ia")\
            .select("id", count="exact")\
            .eq("alumno_id", alumno_id)\
            .eq("rol_mensaje", "user")\
            .gte("fecha_creacion", f"{fecha_hoy}T00:00:00Z")\
            .execute()
        
        if (conteo_hoy.count or 0) >= 10:
            return "⚠️ ¡Hola! Has alcanzado tu límite de 10 consultas diarias de IA por WhatsApp. Hablemos mañana de nuevo. ¡A seguir entrenando fuerte! 💪"

        # EXTRACCIÓN DE CONTEXTO BIOMÉTRICO
        atleta_query = supabase.table("perfiles_atletas").select("nombre_completo, genero, objetivo_principal").eq("id", alumno_id).execute()
        if not atleta_query.data:
            return "Error: No se encontró el perfil del atleta."
            
        atleta_data = atleta_query.data[0]
        nombre = atleta_data.get("nombre_completo", "Atleta")
        genero = atleta_data.get("genero", "No definido")
        objetivo = atleta_data.get("objective_principal", "Mantenerse saludable")

        # RECUPERACIÓN DE MEMORIA CONVERSACIONAL (Últimos 6 mensajes)
        historial_query = supabase.table("historial_ia").select("rol_mensaje, contenido").eq("alumno_id", alumno_id).order("fecha_creacion", desc=True).limit(6).execute()
        mensajes_pasados = list(reversed(historial_query.data)) if historial_query.data else []

        # SYSTEM INSTRUCTION CORPORATIVO
        system_instruction = (
            f"Sos el asistente virtual e IA de la plataforma 'Eddy Personal Trainer: Software Elite'.\n"
            f"Tu rol es responder dudas de fitness, motivación y nutrición de manera profesional, concisa y directa.\n"
            f"Datos del cliente actual:\n"
            f"- Nombre: {nombre}\n"
            f"- Género: {genero}\n"
            f"- Objetivo principal: {objetivo}\n\n"
            f"Reglas estrictas:\n"
            f"1. Sé breve. Las respuestas por WhatsApp deben leerse en menos de 30 segundos.\n"
            f"2. Usá modismos argentinos amigables pero profesionales (voseo, che, dale).\n"
            f"3. Si te preguntan algo fuera de fitness o nutrición, deciles amablemente que solo estás capacitado para el área de entrenamiento."
        )

        contents = []
        for msg in mensajes_pasados:
            contents.append({
                "role": "user" if msg["rol_mensaje"] == "user" else "model",
                "parts": [msg["contenido"]]
            })
        contents.append({"role": "user", "parts": [mensaje_alumno]})

        model = genai.GenerativeModel(model_name="gemini-1.5-pro", system_instruction=system_instruction)
        response = model.generate_content(contents)
        respuesta_texto = response.text.strip()

        # PERSISTENCIA EN LA BASE DE DATOS
        supabase.table("historial_ia").insert({"alumno_id": alumno_id, "rol_mensaje": "user", "contenido": mensaje_alumno}).execute()
        supabase.table("historial_ia").insert({"alumno_id": alumno_id, "rol_mensaje": "model", "contenido": respuesta_texto}).execute()

        return respuesta_texto

    except Exception as e:
        logger.error(f"❌ Error crítico en el motor de procesamiento de IA: {str(e)}")
        return "👋 ¡Hola! Estoy experimentando una pequeña actualización en mis servidores de inteligencia artificial. En unos minutos vuelvo a estar al 100% para ayudarte."