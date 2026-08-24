from pydantic import BaseModel, Field
from typing import Optional

class NotificationCreate(BaseModel):
    client_id: int = Field(..., example=20001, description="ID de la entidad cliente")
    titulo: str = Field(..., example="Mantenimiento de plataforma", description="Título de la notificación")
    canal: str = Field(..., example="Push", description="Canal: 'Push', 'Alerta estándar' o 'Notificación interna'")
    audiencia: str = Field(..., example="Todos", description="Audiencia objetivo: 'Todos', 'Contadores' o 'Sociedades'")
    destinatarios: int = Field(..., example=12458, description="Cantidad estimada de destinatarios")
    fecha: str = Field(..., example="2026-05-26 09:00:00", description="Fecha programada de envío")
    estado: str = Field(..., example="Programada", description="Estado: 'Entregada', 'Programada', 'Fallida', 'En proceso'")
    creadoPor: str = Field(..., example="Administrador", description="Usuario emisor")
    mensaje: Optional[str] = Field(None, example="Se realizará una actualización programada.", description="Cuerpo del mensaje")

class NotificationResponse(NotificationCreate):
    id: int = Field(..., example=1, description="ID único de la notificación")

    class Config:
        from_attributes = True
