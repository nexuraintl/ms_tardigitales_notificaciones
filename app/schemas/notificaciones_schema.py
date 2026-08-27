from pydantic import BaseModel, Field
from typing import Optional, Any

class NotificacionCreateSchema(BaseModel):
    titulo: str
    canal: Optional[str] = "Push"
    audiencia: Optional[str] = "Todos"
    destinatarios: Optional[int] = 0
    fecha: Optional[str] = None
    estado: Optional[str] = "Entregada"
    creadoPor: Optional[str] = "Administrador"
    mensaje: str

class NotificacionItemSchema(BaseModel):
    id: int
    titulo: str
    canal: str
    audiencia: str
    destinatarios: int
    fecha: str
    estado: str
    creadoPor: Optional[str] = None
    mensaje: Optional[str] = None
