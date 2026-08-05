from pydantic import BaseModel

class NotificationResponse(BaseModel):
    id: int
    titulo: str
    canal: str
    audiencia: str
    destinatarios: int
    fecha: str
    estado: str
    creadoPor: str
    mensaje: str

    class Config:
        from_attributes = True

class NotificationCreate(BaseModel):
    client_id: int
    titulo: str
    canal: str
    audiencia: str
    destinatarios: int
    fecha: str
    estado: str
    creadoPor: str
    mensaje: str

