from pydantic import BaseModel
from typing import Optional

class TarjetaBase(BaseModel):
    tipo_tarjeta: str
    codigo: str
    expediente: int
    solicitante: str
    documento: str
    matricula: str
    correo: Optional[str] = None
    representante: Optional[str] = None
    tarjeta: str
    fecha: str

class TarjetaCreate(TarjetaBase):
    pass

class TarjetaResponse(TarjetaBase):
    id: int

    class Config:
        from_attributes = True
