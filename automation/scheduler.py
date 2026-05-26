# automation/scheduler.py
from apscheduler.schedulers.background import BackgroundScheduler
from automation.daily_jobs import disparar_rutinas_y_agua_matutina, ejecutar_ciclo_automatizacion
from utils.logger import obtener_logger

logger = obtener_logger("Scheduler")

def iniciar_scheduler():
    """
    Arranca el motor de automatizaciones en segundo plano.
    Orquesta la IA y las alertas personalizadas.
    """
    scheduler = BackgroundScheduler()
    
    # ⏰ 1. TAREA IA: Todos los días a las 08:00 AM exactas
    scheduler.add_job(
        disparar_rutinas_y_agua_matutina, 
        'cron', 
        hour=8, 
        minute=0,
        id='job_motivacion_matutina',
        replace_existing=True
    )
    
    # 🔄 2. TAREA TABLA: Revisa la base de datos cada 1 minuto (Reemplaza el viejo while True)
    scheduler.add_job(
        ejecutar_ciclo_automatizacion,
        'interval',
        minutes=1,
        id='job_alertas_programadas',
        replace_existing=True
    )
    
    scheduler.start()
    logger.info("⏰ Reloj Maestro (APScheduler) INICIADO. Procesando IA diaria y alertas por minuto.")