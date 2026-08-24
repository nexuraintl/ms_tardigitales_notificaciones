from pydantic import BaseModel
from typing import Optional

class TramiteBase(BaseModel):
    nombre: str
    tipo: str
    costo: float
    estado: str
    descripcion: Optional[str] = ""

class TramiteCreate(TramiteBase):
    client_id: int

class TramiteUpdate(TramiteBase):
    id: int
    client_id: int

class TramiteIdPayload(BaseModel):
    id: int
    client_id: int

class TramiteResponse(TramiteBase):
    id: int

    class Config:
        from_attributes = True
