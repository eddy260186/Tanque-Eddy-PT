# automation/daily_jobs.py
from datetime import datetime, timedelta, date, time as dt_time
from database.conexion import supabase
from backend.services.whatsapp_service import enviar_mensaje_texto_evolution
from automation.mensajes import obtener_plantilla_mensaje
from ai.workout_ai import redactar_motivacion_matutina
from utils.logger import obtener_logger

logger = obtener_logger("DailyJobs")

# ==========================================
# 1. TAREA DE INTELIGENCIA ARTIFICIAL (08:00 AM)
# ==========================================
def disparar_rutinas_y_agua_matutina():
    """
    Escanea a todos los atletas activos. Si no se les mandó el mensaje hoy,
    la IA les redacta su rutina + agua, se despacha y se anota en la memoria.
    """
    logger.info("🤖 Despertando IA: Escaneo de atletas para aviso matutino...")
    
    try:
        resp = supabase.table("perfiles_atletas").select("*").execute()
        atletas = resp.data if resp.data else []
    except Exception as e:
        logger.error(f"Falla al conectar con BD en el job matutino: {e}")
        return

    hoy = datetime.now().strftime("%Y-%m-%d")
    tipo_aviso = "motivacion_matutina"

    for atleta in atletas:
        alumno_id = str(atleta.get("id"))
        telefono = str(atleta.get("telefono", "")).strip()
        entrenador_id = str(atleta.get("entrenador_id", ""))
        nombre = str(atleta.get("nombre_completo", "Tanque")).split()[0]
        peso = float(atleta.get("peso", 75.0))
        rutina = atleta.get("rutina_activa", "Entrenamiento del día")
        dias_entreno = int(atleta.get("dias_entreno", 3))

        if not telefono or not entrenador_id:
            continue

        try:
            memoria = supabase.table("bot_memoria_ia")\
                .select("*")\
                .eq("alumno_id", alumno_id)\
                .eq("tipo_aviso", tipo_aviso)\
                .eq("fecha_envio", hoy)\
                .execute()
                
            if memoria.data:
                continue
        except Exception as e:
            logger.error(f"Error leyendo memoria de {nombre}: {e}")
            continue

        agua_total = round((peso * 0.035) + 0.75 + (0.5 if dias_entreno > 0 else 0), 1)

        try:
            mensaje_ia = redactar_motivacion_matutina(
                nombre_alumno=nombre, 
                rutina_activa=rutina, 
                agua_litros=agua_total
            )
            
            instancia_nombre = f"coach_{str(entrenador_id)[:8]}"
            
            exito_envio = enviar_mensaje_texto_evolution(
                nombre_instancia=instancia_nombre,
                alumno_id=alumno_id,
                entrenador_id=entrenador_id,
                telefono=telefono,
                mensaje=mensaje_ia
            )
            
            if isinstance(exito_envio, dict) and exito_envio.get("exito") or exito_envio is True:
                supabase.table("bot_memoria_ia").insert({
                    "alumno_id": alumno_id,
                    "tipo_aviso": tipo_aviso,
                    "fecha_envio": hoy,
                    "contenido_enviado": mensaje_ia
                }).execute()
                logger.info(f"✅ Motivación matutina despachada a {nombre}.")
                
        except Exception as e:
            logger.error(f"Falla crítica automatizando a {nombre}: {e}")

# ==========================================
# 2. TAREA DE TABLA DE AUTOMATIZACIONES (CADA MINUTO)
# ==========================================
def _parsear_hora(valor) -> dt_time:
    if isinstance(valor, dt_time):
        return valor
    texto = str(valor or "").strip()
    if not texto:
        raise ValueError("hora_programada vacia")
    texto = texto.split("+")[0].split(".")[0]
    for formato in ("%H:%M:%S", "%H:%M"):
        try:
            return datetime.strptime(texto, formato).time()
        except ValueError:
            pass
    raise ValueError(f"hora_programada invalida: {valor}")

def ejecutar_ciclo_automatizacion():
    """
    Revisa la tabla de automatizaciones activas y dispara recordatorios en el minuto exacto.
    """
    ahora = datetime.now()
    hora_actual_str = ahora.strftime("%H:%M:00")
    fecha_hoy = date.today()

    try:
        query = supabase.table("automatizaciones")\
            .select("id, tipo_alerta, hora_programada, mensaje_plantilla, ultima_ejecucion, alumno_id, perfiles_atletas(nombre_completo, telefono, entrenador_id)")\
            .eq("activo", True)\
            .or_(f"ultima_ejecucion.is.null,ultima_ejecucion.neq.{fecha_hoy.isoformat()}")\
            .execute()

        automatizaciones = query.data or []
        if not automatizaciones:
            return

        for tarea in automatizaciones:
            alumno = tarea.get("perfiles_atletas") or {}
            if not alumno:
                continue

            nombre_alumno = alumno.get("nombre_completo") or "Atleta"
            telefono_alumno = alumno.get("telefono")
            entrenador_id = alumno.get("entrenador_id")
            alumno_id = tarea.get("alumno_id")
            tipo = tarea.get("tipo_alerta")
            detalle_especifico = tarea.get("mensaje_plantilla") or ""

            try:
                hora_objeto = _parsear_hora(tarea.get("hora_programada"))
            except ValueError as e:
                logger.warning(f"Tarea {tarea.get('id')} omitida: {e}")
                continue

            hora_disparo_real = hora_objeto.strftime("%H:%M:00")
            tipo_ajustado = tipo

            # Lógica original: Si es entrenamiento, avisa 1 hora antes
            if tipo == "entrenamiento":
                hora_dt = datetime.combine(fecha_hoy, hora_objeto) - timedelta(hours=1)
                hora_disparo_real = hora_dt.strftime("%H:%M:00")
                tipo_ajustado = "pre_entrenamiento"

            if hora_actual_str != hora_disparo_real:
                continue

            if not telefono_alumno:
                continue

            mensaje_final = obtener_plantilla_mensaje(
                tipo_alerta=tipo_ajustado,
                nombre_alumno=nombre_alumno,
                detalle=detalle_especifico,
            )

            instancia_nombre = f"coach_{str(entrenador_id)[:8]}"
            
            exito = enviar_mensaje_texto_evolution(
                nombre_instancia=instancia_nombre,
                alumno_id=alumno_id,
                entrenador_id=entrenador_id,
                telefono=telefono_alumno,
                mensaje=mensaje_final,
            )

            if isinstance(exito, dict) and exito.get("exito") or exito is True:
                supabase.table("automatizaciones")\
                    .update({"ultima_ejecucion": fecha_hoy.isoformat()})\
                    .eq("id", tarea["id"])\
                    .execute()
                logger.info(f"✅ Alerta programada [{tipo_ajustado}] enviada a {nombre_alumno}.")

    except Exception as e:
        logger.error(f"Error crítico en scheduler de BD: {str(e)}")