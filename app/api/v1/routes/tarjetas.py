from fastapi import APIRouter, Query, HTTPException
from typing import List, Optional
import aiomysql
from app.core.database import get_client_connection
from app.schemas.tarjetas import TarjetaResponse, TarjetaCreate

router = APIRouter()

@router.get("/tarjetas", response_model=List[TarjetaResponse])
async def get_tarjetas(
    tipo_tarjeta: Optional[str] = Query(default=None),
    client_id: int = Query(...)
):
    connection = await get_client_connection(client_id)
    try:
        async with connection.cursor(aiomysql.DictCursor) as cursor:
            if tipo_tarjeta:
                query = """
                    SELECT id, tipo_tarjeta, codigo, expediente, solicitante, documento, matricula, correo, representante, tarjeta, DATE_FORMAT(fecha, '%%Y-%%m-%%d') as fecha
                    FROM tn_tarjetavirtual_tarjetas
                    WHERE tipo_tarjeta = %s
                    ORDER BY id ASC;
                """
                await cursor.execute(query, (tipo_tarjeta,))
            else:
                query = """
                    SELECT id, tipo_tarjeta, codigo, expediente, solicitante, documento, matricula, correo, representante, tarjeta, DATE_FORMAT(fecha, '%%Y-%%m-%%d') as fecha
                    FROM tn_tarjetavirtual_tarjetas
                    ORDER BY id ASC;
                """
                await cursor.execute(query)
            
            records = await cursor.fetchall()
            return records
    except Exception as e:
        print(f"Error al consultar tarjetas: {e}")
        raise HTTPException(
            status_code=500,
            detail="Error al consultar las tarjetas en la base de datos."
        )
    finally:
        connection.close()

@router.post("/tarjetas", status_code=201, response_model=TarjetaResponse)
async def create_tarjeta(data: TarjetaCreate):
    connection = await get_client_connection(data.client_id)
    try:
        async with connection.cursor() as cursor:
            query = """
                INSERT INTO tn_tarjetavirtual_tarjetas (
                    tipo_tarjeta, codigo, expediente, solicitante, documento, matricula, correo, representante, tarjeta, fecha
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
            """
            params = (
                data.tipo_tarjeta,
                data.codigo,
                data.expediente,
                data.solicitante,
                data.documento,
                data.matricula,
                data.correo,
                data.representante,
                data.tarjeta,
                data.fecha
            )
            await cursor.execute(query, params)
            new_id = cursor.lastrowid
            
            return {
                "id": new_id,
                **data.dict()
            }
    except Exception as e:
        print(f"Error al registrar tarjeta: {e}")
        raise HTTPException(
            status_code=500,
            detail="Error al registrar la tarjeta en la base de datos."
        )
    finally:
        connection.close()
