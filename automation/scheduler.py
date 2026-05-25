import time
from datetime import datetime, timedelta, date
from database.conexion import supabase
from backend.services.whatsapp_service import enviar_mensaje_texto_whatsapp
from automation.mensajes import obtener_plantilla_mensaje
from utils.logger import obtener_logger

logger = obtener_logger("SaaS_Scheduler_Master")

def ejecutar_ciclo_automatizacion():
    """
    El motor principal que revisa, calcula tiempos dinámicos, aplica filtros anti-spam 
    y dispara el CRM de WhatsApp en piloto automático.
    """
    logger.info("⏰ Iniciando ciclo de escaneo de automatizaciones activas...")
    
    ahora = datetime.now()
    hora_actual_str = ahora.strftime("%H:%M:00") # Formato hh:mm:00 para comparar con SQL
    fecha_hoy = date.today()

    try:
        # 1. TRACCIÓN COMPLETA DE DATOS: Trae automatizaciones activas cruzando los datos del atleta
        # Evitamos mandar mensajes duplicados validando que 'ultima_ejecucion' no sea HOY
        query = supabase.table("automatizaciones")\
            .select("id, tipo_alerta, hora_programada, mensaje_plantilla, ultima_ejecucion, alumno_id, perfiles_atletas(nombre_completo, telefono, entrenador_id)")\
            .eq("activo", True)\
            .neq("ultima_ejecucion", fecha_hoy.isoformat())\
            .execute()

        automatizaciones = query.data

        if not automatizaciones:
            logger.info("☕ No hay tareas pendientes para disparar en este minuto.")
            return

        for tarea in automatizaciones:
            # Desempaquetar datos relacionales seguros de la base de datos
            alumno = tarea.get("perfiles_atletas", {})
            if not alumno:
                continue
                
            nombre_alumno = alumno.get("nombre_completo", "Atleta")
            telefono_alumno = alumno.get("telefono")
            entrenador_id = alumno.get("entrenador_id")
            alumno_id = tarea.get("alumno_id")
            
            hora_programada_raw = tarea["hora_programada"] # Ej: "07:00:00"
            tipo = tarea["tipo_alerta"]
            detalle_especifico = tarea.get("mensaje_plantilla", "") # Macros o nombres de suplemento

            # 2. CÁLCULO DE TIEMPOS DINÁMICOS (Pensar en Grande / Estructura Gigante)
            # Convertimos la cadena de texto de la base de datos en objeto de tiempo analizable
            hora_objeto = datetime.strptime(hora_programada_raw, "%H:%M:%S")
            
            hora_disparo_real = hora_programada_raw # Por defecto, se dispara a la hora exacta
            
            # REGLA DE NEGOCIO: Si es entrenamiento, calculamos el despliegue 1 hora antes obligatoriamente
            if tipo == "entrenamiento":
                hora_un_hora_antes = (hora_objeto - timedelta(hours=1)).time()
                hora_disparo_real = hora_un_hora_antes.strftime("%H:%M:00")
                tipo_ajustado = "pre_entrenamiento"
            else:
                tipo_ajustado = tipo

            # 3. FILTRO DE COINCIDENCIA TEMPORAL CRÍTICA
            # Verificamos si el minuto actual del servidor coincide con la hora calculada para el alumno
            if hora_actual_str == hora_disparo_real:
                if not telefono_alumno:
                    logger.warning(f"⚠️ Alumno {nombre_alumno} no tiene teléfono registrado. Tarea omitida.")
                    continue

                # 4. CONSTRUCCIÓN DEL COPY ELITE DESDE LA CENTRAL
                mensaje_final = obtener_plantilla_mensaje(
                    tipo_alerta=tipo_ajustado,
                    nombre_alumno=nombre_alumno,
                    detalle=detalle_especifico
                )

                # 5. DISPARO INMEDIATO HACIA META CLOUD API
                exito = enviar_mensaje_texto_whatsapp(
                    alumno_id=alumno_id,
                    entrenador_id=entrenador_id,
                    telefono=telefono_alumno,
                    mensaje=mensaje_final
                )

                # 6. BLINDAJE ANTI-SPAM (Escribimos la fecha de hoy para congelar re-envíos)
                if exito:
                    supabase.table("automatizaciones")\
                        .update({"ultima_ejecucion": fecha_hoy.isoformat()})\
                        .eq("id", tarea["id"])\
                        .execute()
                    logger.info(f"✅ Alerta [{tipo_ajustado}] enviada y blindada para {nombre_alumno}.")

    except Exception as e:
        logger.error(f"❌ Error crítico en el motor del Scheduler: {str(e)}")

def iniciar_loop_eterno_scheduler():
    """
    Mantiene el proceso vivo en el servidor de fondo. Revisa la base de datos cada 60 segundos.
    No interfiere con Streamlit porque corre en un hilo de ejecución independiente.
    """
    logger.info("🚀 El Reloj Maestro SaaS Automatizado está encendido y operando...")
    while True:
        ejecutar_ciclo_automatizacion()
        time.sleep(60) # Espera exactamente 1 minuto antes de volver a escanear

if __name__ == "__main__":
    # Permite ejecutar este archivo de forma solitaria en la consola con: python automation/scheduler.py
    iniciar_loop_eterno_scheduler()