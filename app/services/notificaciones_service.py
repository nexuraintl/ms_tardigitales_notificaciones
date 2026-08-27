from typing import List, Dict, Any, Optional
from fastapi import HTTPException
from app.repositories.notificaciones_repository import NotificacionesRepository
from app.schemas.notificaciones_schema import NotificacionCreateSchema

class NotificacionesService:

    def __init__(self):
        self.repository = NotificacionesRepository()

    async def list_notificaciones(self, client_id: Optional[int] = None) -> List[Dict[str, Any]]:
        try:
            return await self.repository.get_all(client_id)
        except HTTPException:
            raise
        except Exception as e:
            print(f"[NotificacionesService] Error al listar notificaciones: {e}")
            raise HTTPException(
                status_code=500,
                detail="No fue posible consultar el historial de notificaciones (MS-3820)."
            )

    async def create_notificacion(self, data: NotificacionCreateSchema, client_id: Optional[int] = None) -> Dict[str, Any]:
        try:
            notif_dict = data.dict()
            new_id = await self.repository.create(notif_dict, client_id)
            return {
                "id": new_id,
                "status": "success",
                "message": "Notificación programada exitosamente."
            }
        except HTTPException:
            raise
        except Exception as e:
            print(f"[NotificacionesService] Error al crear notificación: {e}")
            raise HTTPException(
                status_code=500,
                detail="No fue posible registrar la notificación (MS-3821)."
            )
