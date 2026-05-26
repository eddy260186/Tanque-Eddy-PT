# events/services.py
from backend.services.whatsapp_service import enviar_mensaje_texto_evolution
from utils.logger import obtener_logger

logger = obtener_logger("EventServices")

def notificar_whatsapp_plan_actualizado(data: dict):
    """
    Listener: Escucha el evento PLAN_ACTUALIZADO y dispara el WhatsApp.
    Opera de forma independiente a la interfaz visual para no congelar la pantalla.
    """
    try:
        entrenador_id = data.get("entrenador_id")
        alumno_id = data.get("alumno_id")
        alumno_data = data.get("alumno_data", {})
        nuevo_peso_obj = data.get("nuevo_peso_obj")

        telefono_alumno = str(alumno_data.get("telefono", "")).strip()
        nombre_alumno = str(alumno_data.get('nombre_completo', 'campeón')).split()[0]

        if not telefono_alumno:
            logger.info("Ficha actualizada: El alumno no tiene teléfono. No se envía WS.")
            return

        instancia_nombre = f"coach_{str(entrenador_id)[:8]}"
        mensaje_whatsapp = f"¡Hola {nombre_alumno}! 🚀\n\nTu Coach acaba de actualizar tu plan de entrenamiento en la plataforma.\n\n🎯 Nueva meta fijada: {nuevo_peso_obj} Kg.\n\nEntrá a la app para ver tu nueva rutina y plan nutricional. ¡A romperla esta semana!"

        # Disparar Mensaje a través de Evolution API
        enviar_mensaje_texto_evolution(
            nombre_instancia=instancia_nombre,
            alumno_id=alumno_id,
            entrenador_id=entrenador_id,
            telefono=telefono_alumno,
            mensaje=mensaje_whatsapp
        )
        logger.info(f"✅ WhatsApp automático despachado a {telefono_alumno} por evento PLAN_ACTUALIZADO.")
        
    except Exception as e:
        logger.error(f"❌ Error en el listener de WhatsApp: {e}")