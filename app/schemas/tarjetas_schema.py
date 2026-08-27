from pydantic import BaseModel, Field
from typing import Optional, Dict, Any

class TarjetaCreateSchema(BaseModel):
    tipo_tarjeta: Optional[str] = "contadores"
    tipoTarjeta: Optional[str] = None
    codigo: Optional[str] = None
    expediente: Optional[int] = 0
    solicitante: Optional[str] = None
    nombreTitular: Optional[str] = None
    documento: Optional[str] = None
    identificacion: Optional[str] = None
    matricula: Optional[str] = None
    numeroTarjeta: Optional[str] = None
    correo: Optional[str] = None
    representante: Optional[str] = None
    tarjeta: Optional[str] = "Activa"
    estado: Optional[str] = None
    fecha: Optional[str] = None

class ValidadorConfigSchema(BaseModel):
    val_foto: Optional[bool] = True
    val_nombres: Optional[bool] = True
    val_matricula: Optional[bool] = True
    val_numero_identificacion: Optional[bool] = True
    val_codigo_tarjeta: Optional[bool] = True
    val_estado: Optional[bool] = True
