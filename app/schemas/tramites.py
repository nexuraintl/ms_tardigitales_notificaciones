from pydantic import BaseModel

class TramiteBase(BaseModel):
    nombre: str
    tipo: str
    costo: float
    estado: str
    descripcion: str

class TramiteCreate(TramiteBase):
    client_id: int

class TramiteResponse(TramiteBase):
    id: int

    class Config:
        from_attributes = True
