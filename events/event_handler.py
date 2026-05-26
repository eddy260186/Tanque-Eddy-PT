# events/event_handler.py
from typing import Callable, Dict, List
from events.services import notificar_whatsapp_plan_actualizado

class EventBus:
    """Sistema central de eventos para desacoplar procesos y acelerar la interfaz."""
    _listeners: Dict[str, List[Callable]] = {}

    @classmethod
    def subscribe(cls, event_type: str, listener: Callable):
        if event_type not in cls._listeners:
            cls._listeners[event_type] = []
        cls._listeners[event_type].append(listener)

    @classmethod
    def emit(cls, event_type: str, data: dict = None):
        if data is None:
            data = {}
        if event_type in cls._listeners:
            for listener in cls._listeners[event_type]:
                # Ejecutamos a los trabajadores silenciosos
                listener(data)

def registrar_todos_los_eventos():
    """Conecta los cables del sistema. Se llama una sola vez al arrancar la app."""
    # Limpiamos para evitar duplicados si Streamlit recarga la página
    EventBus._listeners = {} 
    
    # Conectamos el evento con el trabajador de WhatsApp
    EventBus.subscribe("PLAN_ACTUALIZADO", notificar_whatsapp_plan_actualizado)