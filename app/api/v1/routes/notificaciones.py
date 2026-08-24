from fastapi import APIRouter, Query, HTTPException
from typing import List
import aiomysql
from app.core.database import get_client_connection
from app.schemas.notificaciones import NotificationCreate, NotificationResponse

router = APIRouter()

@router.get(
    "/notificaciones",
    response_model=List[NotificationResponse],
    tags=["Centro de Notificaciones"],
    summary="Listar historial de notificaciones emitidas",
    description="Obtiene todas las notificaciones emitidas o programadas para la entidad."
)
async def get_notificaciones(client_id: int = Query(..., description="ID de la entidad cliente")):
    connection = await get_client_connection(client_id)
    try:
        async with connection.cursor(aiomysql.DictCursor) as cursor:
            query = """
                SELECT id, client_id, titulo, canal, audiencia, destinatarios, DATE_FORMAT(fecha, '%%Y-%%m-%%d %%H:%%i:%%s') as fecha, estado, creadoPor, mensaje
                FROM tn_tarjetavirtual_notificaciones
                WHERE client_id = %s
                ORDER BY id DESC;
            """
            await cursor.execute(query, (client_id,))
            records = await cursor.fetchall()
            return records
    except Exception as e:
        print(f"Error al consultar notificaciones: {e}")
        raise HTTPException(
            status_code=500,
            detail="Error al consultar el historial de notificaciones (MS-3820)."
        )
    finally:
        connection.close()

@router.post(
    "/notificaciones",
    response_model=NotificationResponse,
    status_code=201,
    tags=["Centro de Notificaciones"],
    summary="Crear y programar nueva notificación",
    description="Registra una nueva notificación en el centro de alertas institucional."
)
async def create_notificacion(data: NotificationCreate):
    connection = await get_client_connection(data.client_id)
    try:
        async with connection.cursor() as cursor:
            query = """
                INSERT INTO tn_tarjetavirtual_notificaciones (
                    client_id, titulo, canal, audiencia, destinatarios, fecha, estado, creadoPor, mensaje
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);
            """
            params = (
                data.client_id,
                data.titulo,
                data.canal,
                data.audiencia,
                data.destinatarios,
                data.fecha,
                data.estado,
                data.creadoPor,
                data.mensaje
            )
            await cursor.execute(query, params)
            new_id = cursor.lastrowid
            
            return {
                "id": new_id,
                **data.dict()
            }
    except Exception as e:
        print(f"Error al crear notificación: {e}")
        raise HTTPException(
            status_code=500,
            detail="Error al registrar la notificación en la base de datos (MS-3821)."
        )
    finally:
        connection.close()
