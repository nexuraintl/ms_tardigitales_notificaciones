from pydantic import BaseModel, Field
from typing import Optional

class TramiteBase(BaseModel):
    nombre: str = Field(..., example="Inscripción de Tarjeta Profesional", description="Nombre oficial del trámite")
    tipo: str = Field(..., example="Contador Público", description="Tipo de solicitante: 'Contador Público' o 'Sociedad'")
    costo: float = Field(..., example=412000.0, description="Valor del trámite en pesos colombianos (COP)")
    estado: str = Field(..., example="Activo", description="Estado de vigencia: 'Activo' o 'Inactivo'")
    descripcion: Optional[str] = Field(None, example="Trámite oficial para solicitud de tarjeta por primera vez.", description="Detalles o requisitos del trámite")

class TramiteCreate(TramiteBase):
    pass

class TramiteUpdate(TramiteBase):
    pass

class TramiteResponse(TramiteBase):
    id: int = Field(..., example=1, description="Identificador único del trámite")

    class Config:
        from_attributes = True

class StandardMessageResponse(BaseModel):
    status: str = Field(..., example="success")
    message: str = Field(..., example="Operación realizada correctamente.")
