from typing import List, Dict, Any, Optional
from fastapi import HTTPException
from app.repositories.tramites_repository import TramitesRepository
from app.schemas.tramites_schema import TramiteCreateSchema, TramiteUpdateSchema

class TramitesService:

    def __init__(self):
        self.repository = TramitesRepository()

    async def list_tramites(self, client_id: Optional[int] = None) -> List[Dict[str, Any]]:
        try:
            return await self.repository.get_all(client_id)
        except HTTPException:
            raise
        except Exception as e:
            print(f"[TramitesService] Error al listar trámites: {e}")
            raise HTTPException(
                status_code=500,
                detail="No fue posible consultar el catálogo de trámites (MS-3810)."
            )

    async def get_tramite(self, tramite_id: int, client_id: Optional[int] = None) -> Dict[str, Any]:
        try:
            tramite = await self.repository.get_by_id(tramite_id, client_id)
            if not tramite:
                raise HTTPException(
                    status_code=404,
                    detail="Trámite no encontrado en el sistema (MS-3811)."
                )
            return tramite
        except HTTPException:
            raise
        except Exception as e:
            print(f"[TramitesService] Error al obtener trámite {tramite_id}: {e}")
            raise HTTPException(
                status_code=500,
                detail="No fue posible consultar la información del trámite (MS-3810)."
            )

    async def create_tramite(self, data: TramiteCreateSchema, client_id: Optional[int] = None) -> Dict[str, Any]:
        try:
            new_id = await self.repository.create(data.dict(), client_id)
            return {
                "id": new_id,
                "status": "success",
                "message": "Trámite registrado exitosamente."
            }
        except HTTPException:
            raise
        except Exception as e:
            print(f"[TramitesService] Error al crear trámite: {e}")
            raise HTTPException(
                status_code=500,
                detail="No fue posible registrar el nuevo trámite (MS-3812)."
            )

    async def update_tramite(self, tramite_id: int, data: TramiteUpdateSchema, client_id: Optional[int] = None) -> Dict[str, Any]:
        try:
            existing = await self.repository.get_by_id(tramite_id, client_id)
            if not existing:
                raise HTTPException(
                    status_code=404,
                    detail="Trámite no encontrado para actualizar (MS-3811)."
                )
            await self.repository.update(tramite_id, data.dict(exclude_none=True), client_id)
            return {
                "id": tramite_id,
                "status": "success",
                "message": "Trámite actualizado exitosamente."
            }
        except HTTPException:
            raise
        except Exception as e:
            print(f"[TramitesService] Error al actualizar trámite {tramite_id}: {e}")
            raise HTTPException(
                status_code=500,
                detail="No fue posible actualizar la información del trámite (MS-3813)."
            )

    async def delete_tramite(self, tramite_id: int, client_id: Optional[int] = None) -> Dict[str, Any]:
        try:
            existing = await self.repository.get_by_id(tramite_id, client_id)
            if not existing:
                raise HTTPException(
                    status_code=404,
                    detail="Trámite no encontrado para eliminar (MS-3811)."
                )
            await self.repository.delete(tramite_id, client_id)
            return {
                "id": tramite_id,
                "status": "success",
                "message": "Trámite eliminado exitosamente."
            }
        except HTTPException:
            raise
        except Exception as e:
            print(f"[TramitesService] Error al eliminar trámite {tramite_id}: {e}")
            raise HTTPException(
                status_code=500,
                detail="No fue posible eliminar el trámite seleccionado (MS-3814)."
            )
