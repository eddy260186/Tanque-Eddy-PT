from pydantic import BaseModel
from typing import Optional
from datetime import time, date

class AutomatizacionModel(BaseModel):
    id: Optional[str] = None
    alumno_id: str
    tipo_alerta: str # 'agua', 'comida', 'entrenamiento', 'suplementos', 'pesaje'
    hora_programada: time
    mensaje_plantilla: Optional[str] = None
    activo: bool = True
    ultima_ejecucion: Optional[date] = None # Evita envíos duplicados en el mismo día