from fastapi import APIRouter, Query, HTTPException
from typing import List
import aiomysql
from app.core.database import get_client_connection
from app.schemas.tramites import TramiteCreate, TramiteUpdate, TramiteIdPayload, TramiteResponse

router = APIRouter()

@router.get("/tramites", response_model=List[TramiteResponse])
async def get_tramites(client_id: int = Query(...)):
    connection = await get_client_connection(client_id)
    try:
        async with connection.cursor(aiomysql.DictCursor) as cursor:
            query = "SELECT id, nombre, tipo, costo, estado, descripcion FROM tn_tarjetavirtual_tramites ORDER BY id ASC;"
            await cursor.execute(query)
            records = await cursor.fetchall()
            return records
    except Exception as e:
        print(f"Error al consultar trámites: {e}")
        raise HTTPException(
            status_code=500,
            detail="Error al consultar los trámites en la base de datos (MS-3810)."
        )
    finally:
        connection.close()

@router.post("/tramites/detalle", response_model=TramiteResponse)
async def get_tramite_detalle(data: TramiteIdPayload):
    connection = await get_client_connection(data.client_id)
    try:
        async with connection.cursor(aiomysql.DictCursor) as cursor:
            query = "SELECT id, nombre, tipo, costo, estado, descripcion FROM tn_tarjetavirtual_tramites WHERE id = %s;"
            await cursor.execute(query, (data.id,))
            record = await cursor.fetchone()
            if not record:
                raise HTTPException(status_code=404, detail="Trámite no encontrado (MS-3811).")
            return record
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error al consultar trámite {data.id}: {e}")
        raise HTTPException(
            status_code=500,
            detail="Error al buscar el trámite en la base de datos (MS-3810)."
        )
    finally:
        connection.close()

@router.post("/tramites", response_model=TramiteResponse)
async def create_tramite(tramite: TramiteCreate):
    connection = await get_client_connection(tramite.client_id)
    try:
        async with connection.cursor() as cursor:
            query = """
                INSERT INTO tn_tarjetavirtual_tramites (nombre, tipo, costo, estado, descripcion)
                VALUES (%s, %s, %s, %s, %s);
            """
            params = (tramite.nombre, tramite.tipo, tramite.costo, tramite.estado, tramite.descripcion)
            await cursor.execute(query, params)
            new_id = cursor.lastrowid
            
            return {
                "id": new_id,
                "nombre": tramite.nombre,
                "tipo": tramite.tipo,
                "costo": tramite.costo,
                "estado": tramite.estado,
                "descripcion": tramite.descripcion
            }
    except Exception as e:
        print(f"Error al crear trámite: {e}")
        raise HTTPException(
            status_code=500,
            detail="Error al registrar el trámite en la base de datos (MS-3812)."
        )
    finally:
        connection.close()

@router.put("/tramites", response_model=TramiteResponse)
async def update_tramite(tramite: TramiteUpdate):
    connection = await get_client_connection(tramite.client_id)
    try:
        async with connection.cursor() as cursor:
            check_query = "SELECT id FROM tn_tarjetavirtual_tramites WHERE id = %s;"
            await cursor.execute(check_query, (tramite.id,))
            if not await cursor.fetchone():
                raise HTTPException(status_code=404, detail="Trámite no encontrado para actualizar (MS-3811).")
                
            query = """
                UPDATE tn_tarjetavirtual_tramites
                SET nombre = %s, tipo = %s, costo = %s, estado = %s, descripcion = %s
                WHERE id = %s;
            """
            params = (tramite.nombre, tramite.tipo, tramite.costo, tramite.estado, tramite.descripcion, tramite.id)
            await cursor.execute(query, params)
            
            return {
                "id": tramite.id,
                "nombre": tramite.nombre,
                "tipo": tramite.tipo,
                "costo": tramite.costo,
                "estado": tramite.estado,
                "descripcion": tramite.descripcion
            }
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error al actualizar trámite {tramite.id}: {e}")
        raise HTTPException(
            status_code=500,
            detail="Error al actualizar el trámite en la base de datos (MS-3813)."
        )
    finally:
        connection.close()

@router.post("/tramites/eliminar")
async def delete_tramite(data: TramiteIdPayload):
    connection = await get_client_connection(data.client_id)
    try:
        async with connection.cursor() as cursor:
            check_query = "SELECT id FROM tn_tarjetavirtual_tramites WHERE id = %s;"
            await cursor.execute(check_query, (data.id,))
            if not await cursor.fetchone():
                raise HTTPException(status_code=404, detail="Trámite no encontrado para eliminar (MS-3811).")
                
            query = "DELETE FROM tn_tarjetavirtual_tramites WHERE id = %s;"
            await cursor.execute(query, (data.id,))
            
            return {"status": "success", "message": f"Trámite #{data.id} eliminado correctamente."}
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error al eliminar trámite {data.id}: {e}")
        raise HTTPException(
            status_code=500,
            detail="Error al eliminar el trámite en la base de datos (MS-3814)."
        )
    finally:
        connection.close()
