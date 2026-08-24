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
    client_id: int

class TarjetaResponse(TarjetaBase):
    id: int

    class Config:
        from_attributes = True

class TarjetaHistorialRequest(BaseModel):
    tarjeta_id: int
    client_id: int

class ValidadorConfigSave(BaseModel):
    client_id: int
    val_foto: int
    val_nombres: int
    val_matricula: int
    val_numero_identificacion: int
    val_codigo_tarjeta: int
    val_estado: int
