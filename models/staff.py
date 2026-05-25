from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class StaffModel(BaseModel):
    id: Optional[str] = None
    perfil_id: str
    rol: str # 'admin', 'entrenador', 'nutricionista'
    whatsapp_comercial: Optional[str] = None
    matricula: Optional[str] = None
    plan_saas: str = "basico" # 'basico', 'pro', 'elite'
    limite_alumnos: int = 10
    activo: bool = True
    fecha_alta: Optional[datetime] = None