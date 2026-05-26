# application/actualizar_plan.py
from database.repositories import AtletaRepository
from backend.services.whatsapp_service import enviar_mensaje_texto_evolution
from utils.logger import obtener_logger

logger = obtener_logger("AppLayer")

def ejecutar_actualizacion_plan(entrenador_id: str, alumno_id: str, alumno_data: dict, nueva_rutina: str, nueva_dieta: str, nuevo_peso_obj: float, nuevo_plazo: int) -> dict:
    """
    Caso de Uso Central: Orquesta la BD y la mensajería.
    El frontend solo llama a esta función y espera la respuesta.
    """
    # 1. Guardar en Base de Datos a través del Repositorio
    exito_db = AtletaRepository.actualizar_plan_y_metas(
        alumno_id=alumno_id,
        rutina=nueva_rutina,
        dieta=nueva_dieta,
        peso_obj=nuevo_peso_obj,
        plazo=nuevo_plazo
    )

    if not exito_db:
        return {"exito": False, "error": "Falla interna al intentar guardar en la base de datos."}

    # 2. Preparar el envío de WhatsApp
    telefono_alumno = str(alumno_data.get("telefono", "")).strip()
    nombre_alumno = str(alumno_data.get('nombre_completo', 'campeón')).split()[0]

    if not telefono_alumno:
        return {"exito": True, "ws_enviado": False, "mensaje": "Ficha actualizada. (El alumno no tiene teléfono configurado)."}

    # Recreamos el nombre de la instancia del coach para el API
    instancia_nombre = f"coach_{str(entrenador_id)[:8]}"
    mensaje_whatsapp = f"¡Hola {nombre_alumno}! 🚀\n\nTu Coach acaba de actualizar tu plan de entrenamiento en la plataforma.\n\n🎯 Nueva meta fijada: {nuevo_peso_obj} Kg.\n\nEntrá a la app para ver tu nueva rutina y plan nutricional. ¡A romperla esta semana!"

    # 3. Disparar Mensaje
    resultado_ws = enviar_mensaje_texto_evolution(
        nombre_instancia=instancia_nombre,
        alumno_id=alumno_id,
        entrenador_id=entrenador_id,
        telefono=telefono_alumno,
        mensaje=mensaje_whatsapp
    )

    # 4. Retornar resultado limpio al Frontend para que pinte el cartel de éxito o error
    if isinstance(resultado_ws, dict) and resultado_ws.get("exito"):
        return {"exito": True, "ws_enviado": True, "mensaje": f"Plan guardado y WhatsApp entregado al {telefono_alumno}."}
    else:
        error_ws = resultado_ws.get("error") if isinstance(resultado_ws, dict) else "Error desconocido"
        return {"exito": True, "ws_enviado": False, "mensaje": f"BD Guardada, pero WhatsApp falló: {error_ws}"}