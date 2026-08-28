from typing import List, Dict, Any, Optional
from fastapi import HTTPException
from app.repositories.tarjetas_repository import TarjetasRepository
from app.schemas.tarjetas_schema import TarjetaCreateSchema, ValidadorConfigSchema, ConsultaMatriculaResponseSchema
from app.integrations.jcc_client import JccClient

class TarjetasService:

    def __init__(self):
        self.repository = TarjetasRepository()
        self.jcc_client = JccClient()

    async def consult_registry(
        self,
        documento: str,
        tipo_tarjeta: str = "contadores",
        tipo: str = "",
        client_id: Optional[int] = None
    ) -> Dict[str, Any]:
        try:
            if not documento or not str(documento).strip():
                raise HTTPException(
                    status_code=400,
                    detail="El número de documento o NIT es requerido para la consulta (MS-3833)."
                )

            # Consultar API de la JCC a través del módulo de integraciones
            result = await self.jcc_client.consultar_registro(
                documento=documento,
                tipo_tarjeta=tipo_tarjeta,
                tipo=tipo
            )
            return result
        except HTTPException:
            raise
        except Exception as e:
            print(f"[TarjetasService] Error al consultar matrícula/registro JCC: {e}")
            raise HTTPException(
                status_code=500,
                detail="Error al consultar el registro institucional en la API de la JCC (MS-3834)."
            )

    async def list_tarjetas(self, tipo_tarjeta: Optional[str] = None, client_id: Optional[int] = None) -> List[Dict[str, Any]]:
        try:
            return await self.repository.get_all(tipo_tarjeta, client_id)
        except HTTPException:
            raise
        except Exception as e:
            print(f"[TarjetasService] Error al listar tarjetas: {e}")
            raise HTTPException(
                status_code=500,
                detail="No fue posible cargar el listado de tarjetas (MS-3830)."
            )

    async def get_tarjeta(self, tarjeta_id: int, client_id: Optional[int] = None) -> Dict[str, Any]:
        try:
            tarjeta = await self.repository.get_by_id(tarjeta_id, client_id)
            if not tarjeta:
                raise HTTPException(
                    status_code=404,
                    detail="Tarjeta digital no encontrada (MS-3806)."
                )
            return tarjeta
        except HTTPException:
            raise
        except Exception as e:
            print(f"[TarjetasService] Error al obtener tarjeta {tarjeta_id}: {e}")
            raise HTTPException(
                status_code=500,
                detail="No fue posible consultar la tarjeta solicitada (MS-3830)."
            )

    async def create_tarjeta(self, data: TarjetaCreateSchema, client_id: Optional[int] = None) -> Dict[str, Any]:
        try:
            new_id = await self.repository.create(data.dict(), client_id)
            return {
                "id": new_id,
                "status": "success",
                "message": "Tarjeta digital emitida exitosamente."
            }
        except HTTPException:
            raise
        except Exception as e:
            print(f"[TarjetasService] Error al crear tarjeta: {e}")
            raise HTTPException(
                status_code=500,
                detail="No fue posible completar la emisión de la tarjeta (MS-3831)."
            )

    async def get_historial(self, tarjeta_id: int, client_id: Optional[int] = None) -> List[Dict[str, Any]]:
        try:
            return await self.repository.get_historial(tarjeta_id, client_id)
        except HTTPException:
            raise
        except Exception as e:
            print(f"[TarjetasService] Error al obtener historial de tarjeta {tarjeta_id}: {e}")
            raise HTTPException(
                status_code=500,
                detail="No fue posible obtener el historial de la tarjeta (MS-3832)."
            )

    async def get_validador_config(self, client_id: Optional[int] = None) -> Dict[str, Any]:
        try:
            return await self.repository.get_validador_config(client_id)
        except HTTPException:
            raise
        except Exception as e:
            print(f"[TarjetasService] Error al cargar configuración de validador: {e}")
            raise HTTPException(
                status_code=500,
                detail="No fue posible cargar la configuración del validador (MS-3850)."
            )

    async def save_validador_config(self, data: ValidadorConfigSchema, client_id: Optional[int] = None) -> Dict[str, Any]:
        try:
            await self.repository.save_validador_config(data.dict(), client_id)
            return {
                "status": "success",
                "message": "Configuración del validador guardada exitosamente."
            }
        except HTTPException:
            raise
        except Exception as e:
            print(f"[TarjetasService] Error al guardar configuración de validador: {e}")
            raise HTTPException(
                status_code=500,
                detail="No fue posible guardar la configuración del validador (MS-3851)."
            )

