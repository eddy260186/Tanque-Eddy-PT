import time
from datetime import datetime, timedelta, date, time as dt_time
from database.conexion import supabase
from backend.services.whatsapp_service import enviar_mensaje_texto_whatsapp
from automation.mensajes import obtener_plantilla_mensaje
from utils.logger import obtener_logger

logger = obtener_logger("SaaS_Scheduler_Master")


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
    Revisa automatizaciones activas y dispara recordatorios por WhatsApp.
    """
    logger.info("Iniciando ciclo de automatizaciones activas...")

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
            logger.info("No hay tareas pendientes para disparar en este minuto.")
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

            if tipo == "entrenamiento":
                hora_dt = datetime.combine(fecha_hoy, hora_objeto) - timedelta(hours=1)
                hora_disparo_real = hora_dt.strftime("%H:%M:00")
                tipo_ajustado = "pre_entrenamiento"

            if hora_actual_str != hora_disparo_real:
                continue

            if not telefono_alumno:
                logger.warning(f"Alumno {nombre_alumno} sin telefono. Tarea omitida.")
                continue

            mensaje_final = obtener_plantilla_mensaje(
                tipo_alerta=tipo_ajustado,
                nombre_alumno=nombre_alumno,
                detalle=detalle_especifico,
            )

            exito = enviar_mensaje_texto_whatsapp(
                alumno_id=alumno_id,
                entrenador_id=entrenador_id,
                telefono=telefono_alumno,
                mensaje=mensaje_final,
            )

            if exito:
                supabase.table("automatizaciones")\
                    .update({"ultima_ejecucion": fecha_hoy.isoformat()})\
                    .eq("id", tarea["id"])\
                    .execute()
                logger.info(f"Alerta [{tipo_ajustado}] enviada a {nombre_alumno}.")

    except Exception as e:
        logger.error(f"Error critico en scheduler: {str(e)}")


def iniciar_loop_eterno_scheduler():
    logger.info("Scheduler de WhatsApp iniciado.")
    while True:
        ejecutar_ciclo_automatizacion()
        time.sleep(60)


if __name__ == "__main__":
    iniciar_loop_eterno_scheduler()
