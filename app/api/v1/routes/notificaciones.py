from fastapi import APIRouter, Query, HTTPException
from typing import List
import aiomysql
from app.core.database import get_client_connection
from app.schemas.notificaciones import NotificationResponse, NotificationCreate

router = APIRouter()

@router.get("/notificaciones", response_model=List[NotificationResponse])
async def get_notificaciones(client_id: int | None = Query(default=None)):
    connection = await get_client_connection(client_id)
    
    try:
        async with connection.cursor(aiomysql.DictCursor) as cursor:
            query = """
                SELECT id, titulo, canal, audiencia, destinatarios, fecha, estado, creado_por, mensaje 
                FROM tn_tarjetavirtual_notificaciones 
                ORDER BY id ASC;
            """
            await cursor.execute(query)
            records = await cursor.fetchall()
            
            mapped_records = []
            for row in records:
                mapped_records.append({
                    "id": row["id"],
                    "titulo": row["titulo"],
                    "canal": row["canal"],
                    "audiencia": row["audiencia"],
                    "destinatarios": row["destinatarios"],
                    "fecha": row["fecha"],
                    "estado": row["estado"],
                    "creadoPor": row["creado_por"],
                    "mensaje": row["mensaje"]
                })
            return mapped_records
            
    except Exception as e:
        print(f"Error al consultar notificaciones: {e}")
        raise HTTPException(
            status_code=500,
            detail="Error al realizar la consulta en la base de datos."
        )
    finally:
        connection.close()

@router.post("/notificaciones", status_code=201, response_model=NotificationResponse)
async def create_notification(data: NotificationCreate, client_id: int | None = Query(default=None)):
    connection = await get_client_connection(client_id)
    try:
        async with connection.cursor() as cursor:
            query = """
                INSERT INTO tn_tarjetavirtual_notificaciones (
                    titulo, canal, audiencia, destinatarios, fecha, estado, creado_por, mensaje
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
            """
            params = (
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
                "titulo": data.titulo,
                "canal": data.canal,
                "audiencia": data.audiencia,
                "destinatarios": data.destinatarios,
                "fecha": data.fecha,
                "estado": data.estado,
                "creadoPor": data.creadoPor,
                "mensaje": data.mensaje
            }
    except Exception as e:
        print(f"Error al crear notificación: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error al registrar la notificación en la base de datos."
        )
    finally:
        connection.close()

