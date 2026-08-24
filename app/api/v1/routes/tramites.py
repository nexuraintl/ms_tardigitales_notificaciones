from fastapi import APIRouter, Query, HTTPException, Path
from typing import List
import aiomysql
from app.core.database import get_client_connection
from app.schemas.tramites import TramiteCreate, TramiteUpdate, TramiteResponse, StandardMessageResponse

router = APIRouter()

@router.get(
    "/tramites",
    response_model=List[TramiteResponse],
    tags=["Gestión de Trámites"],
    summary="Listar catálogo de trámites oficiales",
    description="Retorna el listado completo de trámites registrados para la entidad especificada."
)
async def get_tramites(client_id: int = Query(..., description="Identificador único de la entidad / cliente (ej. 20001)")):
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

@router.get(
    "/tramites/{id}",
    response_model=TramiteResponse,
    tags=["Gestión de Trámites"],
    summary="Consultar detalle de un trámite por ID",
    description="Obtiene la información detallada de un trámite oficial específico mediante su identificador."
)
async def get_tramite(
    id: int = Path(..., description="ID numérico del trámite"),
    client_id: int = Query(..., description="ID de la entidad cliente")
):
    connection = await get_client_connection(client_id)
    try:
        async with connection.cursor(aiomysql.DictCursor) as cursor:
            query = "SELECT id, nombre, tipo, costo, estado, descripcion FROM tn_tarjetavirtual_tramites WHERE id = %s;"
            await cursor.execute(query, (id,))
            record = await cursor.fetchone()
            if not record:
                raise HTTPException(status_code=404, detail="Trámite no encontrado en el sistema (MS-3811).")
            return record
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error al consultar trámite {id}: {e}")
        raise HTTPException(
            status_code=500,
            detail="Error al buscar el trámite en la base de datos (MS-3810)."
        )
    finally:
        connection.close()

@router.post(
    "/tramites",
    response_model=TramiteResponse,
    status_code=201,
    tags=["Gestión de Trámites"],
    summary="Registrar nuevo trámite oficial",
    description="Crea y publica un nuevo trámite oficial en el catálogo de la entidad."
)
async def create_tramite(
    tramite: TramiteCreate,
    client_id: int = Query(..., description="ID de la entidad cliente")
):
    connection = await get_client_connection(client_id)
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

@router.put(
    "/tramites/{id}",
    response_model=TramiteResponse,
    tags=["Gestión de Trámites"],
    summary="Actualizar información de un trámite",
    description="Modifica los costos, nombre, estado o requisitos de un trámite existente."
)
async def update_tramite(
    id: int = Path(..., description="ID del trámite a actualizar"),
    tramite: TramiteUpdate = ...,
    client_id: int = Query(..., description="ID de la entidad cliente")
):
    connection = await get_client_connection(client_id)
    try:
        async with connection.cursor() as cursor:
            check_query = "SELECT id FROM tn_tarjetavirtual_tramites WHERE id = %s;"
            await cursor.execute(check_query, (id,))
            if not await cursor.fetchone():
                raise HTTPException(status_code=404, detail="Trámite no encontrado para actualizar (MS-3811).")
                
            query = """
                UPDATE tn_tarjetavirtual_tramites
                SET nombre = %s, tipo = %s, costo = %s, estado = %s, descripcion = %s
                WHERE id = %s;
            """
            params = (tramite.nombre, tramite.tipo, tramite.costo, tramite.estado, tramite.descripcion, id)
            await cursor.execute(query, params)
            
            return {
                "id": id,
                "nombre": tramite.nombre,
                "tipo": tramite.tipo,
                "costo": tramite.costo,
                "estado": tramite.estado,
                "descripcion": tramite.descripcion
            }
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error al actualizar trámite {id}: {e}")
        raise HTTPException(
            status_code=500,
            detail="Error al actualizar el trámite en la base de datos (MS-3813)."
        )
    finally:
        connection.close()

@router.delete(
    "/tramites/{id}",
    response_model=StandardMessageResponse,
    tags=["Gestión de Trámites"],
    summary="Eliminar trámite del catálogo",
    description="Remueve un trámite del catálogo oficial de la entidad."
)
async def delete_tramite(
    id: int = Path(..., description="ID del trámite a eliminar"),
    client_id: int = Query(..., description="ID de la entidad cliente")
):
    connection = await get_client_connection(client_id)
    try:
        async with connection.cursor() as cursor:
            check_query = "SELECT id FROM tn_tarjetavirtual_tramites WHERE id = %s;"
            await cursor.execute(check_query, (id,))
            if not await cursor.fetchone():
                raise HTTPException(status_code=404, detail="Trámite no encontrado para eliminar (MS-3811).")
                
            query = "DELETE FROM tn_tarjetavirtual_tramites WHERE id = %s;"
            await cursor.execute(query, (id,))
            
            return {"status": "success", "message": f"Trámite #{id} eliminado correctamente."}
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error al eliminar trámite {id}: {e}")
        raise HTTPException(
            status_code=500,
            detail="Error al eliminar el trámite en la base de datos (MS-3814)."
        )
    finally:
        connection.close()
