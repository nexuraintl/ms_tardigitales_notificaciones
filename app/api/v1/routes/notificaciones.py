from fastapi import APIRouter, Query, HTTPException, Body
from typing import List, Dict, Any, Optional
from app.services.notificaciones_service import NotificacionesService
from app.schemas.notificaciones_schema import NotificacionCreateSchema

router = APIRouter()
service = NotificacionesService()

@router.get("/list")
async def list_notificaciones(
    client_id: Optional[int] = Query(None, description="ID de la entidad cliente")
):
    return await service.list_notificaciones(client_id)

@router.post("/create")
async def create_notificacion(
    data: NotificacionCreateSchema = Body(...),
    client_id: Optional[int] = Query(None, description="ID de la entidad cliente")
):
    return await service.create_notificacion(data, client_id)
