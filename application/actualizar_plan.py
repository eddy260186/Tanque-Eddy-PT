# application/actualizar_plan.py
from database.repositories import AtletaRepository
from events.event_handler import EventBus
from utils.logger import obtener_logger

logger = obtener_logger("AppLayer")

def ejecutar_actualizacion_plan(entrenador_id: str, alumno_id: str, alumno_data: dict, nueva_rutina: str, nueva_dieta: str, nuevo_peso_obj: float, nuevo_plazo: int) -> dict:
    """
    Caso de Uso Central Orquestado.
    1. Guarda en BD.
    2. Grita (Emite) el evento.
    No espera a WhatsApp, la pantalla se libera en 0.1 segundos.
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

    # 2. Emitir el evento de que el plan se actualizó
    datos_evento = {
        "entrenador_id": entrenador_id,
        "alumno_id": alumno_id,
        "alumno_data": alumno_data,
        "nuevo_peso_obj": nuevo_peso_obj
    }
    EventBus.emit("PLAN_ACTUALIZADO", datos_evento)

    # 3. Retornar éxito inmediato al Frontend
    return {"exito": True, "ws_enviado": True, "mensaje": "Ficha guardada. Sincronización en segundo plano iniciada."}