from fastapi import APIRouter, Query, HTTPException, Path, Body
from typing import List, Dict, Any, Optional
from app.services.tramites_service import TramitesService
from app.schemas.tramites_schema import TramiteCreateSchema, TramiteUpdateSchema

router = APIRouter()
service = TramitesService()

@router.get("/list")
async def list_tramites(
    client_id: Optional[int] = Query(None, description="ID de la entidad cliente")
):
    return await service.list_tramites(client_id)

@router.get("/get/{id}")
async def get_tramite(
    id: int = Path(..., description="ID único del trámite"),
    client_id: Optional[int] = Query(None, description="ID de la entidad cliente")
):
    return await service.get_tramite(id, client_id)

@router.post("/create")
async def create_tramite(
    data: TramiteCreateSchema = Body(...),
    client_id: Optional[int] = Query(None, description="ID de la entidad cliente")
):
    return await service.create_tramite(data, client_id)

@router.put("/update/{id}")
async def update_tramite(
    id: int = Path(..., description="ID único del trámite"),
    data: TramiteUpdateSchema = Body(...),
    client_id: Optional[int] = Query(None, description="ID de la entidad cliente")
):
    return await service.update_tramite(id, data, client_id)

@router.delete("/delete/{id}")
async def delete_tramite(
    id: int = Path(..., description="ID único del trámite"),
    client_id: Optional[int] = Query(None, description="ID de la entidad cliente")
):
    return await service.delete_tramite(id, client_id)
