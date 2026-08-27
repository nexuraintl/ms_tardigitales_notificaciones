from pydantic import BaseModel, Field
from typing import Optional

class TramiteCreateSchema(BaseModel):
    nombre: str
    tipo: Optional[str] = "General"
    costo: Optional[float] = 0.0
    estado: Optional[str] = "Activo"
    descripcion: Optional[str] = None

class TramiteUpdateSchema(BaseModel):
    nombre: Optional[str] = None
    tipo: Optional[str] = None
    costo: Optional[float] = None
    estado: Optional[str] = None
    descripcion: Optional[str] = None

class TramiteItemSchema(BaseModel):
    id: int
    nombre: str
    tipo: str
    costo: float
    estado: str
    descripcion: Optional[str] = None
