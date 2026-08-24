from fastapi import APIRouter, Query, HTTPException, Path
from typing import List, Optional
import aiomysql
from app.core.database import get_client_connection
from app.schemas.tarjetas import (
    TarjetaCreate, TarjetaResponse, HistorialTarjetaResponse,
    ValidadorConfigSave, ValidadorConfigResponse, CertificadoResponse
)
from app.schemas.tramites import StandardMessageResponse

router = APIRouter()

@router.get(
    "/tarjetas",
    response_model=List[TarjetaResponse],
    tags=["Tarjetas Digitales"],
    summary="Listar tarjetas digitales emitidas",
    description="Consulta las tarjetas digitales emitidas para la entidad, permitiendo filtrar por tipo (contadores / sociedades)."
)
async def get_tarjetas(
    client_id: int = Query(..., description="ID de la entidad cliente (ej. 20001)"),
    tipo_tarjeta: Optional[str] = Query(None, description="Filtro por tipo de tarjeta: 'contadores' o 'sociedades'")
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
            detail="Error al consultar las tarjetas en la base de datos (MS-3830)."
        )
    finally:
        connection.close()

@router.get(
    "/tarjetas/{id}",
    response_model=TarjetaResponse,
    tags=["Tarjetas Digitales"],
    summary="Consultar detalle de una tarjeta",
    description="Obtiene los datos completos de una credencial digital por su ID."
)
async def get_tarjeta_by_id(
    id: int = Path(..., description="ID de la tarjeta"),
    client_id: int = Query(..., description="ID de la entidad cliente")
):
    connection = await get_client_connection(client_id)
    try:
        async with connection.cursor(aiomysql.DictCursor) as cursor:
            query = """
                SELECT id, tipo_tarjeta, codigo, expediente, solicitante, documento, matricula, correo, representante, tarjeta, DATE_FORMAT(fecha, '%%Y-%%m-%%d') as fecha
                FROM tn_tarjetavirtual_tarjetas
                WHERE id = %s
                LIMIT 1;
            """
            await cursor.execute(query, (id,))
            record = await cursor.fetchone()
            if not record:
                raise HTTPException(status_code=404, detail="Tarjeta digital no encontrada (MS-3806).")
            return record
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error al consultar tarjeta {id}: {e}")
        raise HTTPException(
            status_code=500,
            detail="Error al consultar la tarjeta en la base de datos (MS-3830)."
        )
    finally:
        connection.close()

@router.post(
    "/tarjetas",
    status_code=201,
    response_model=TarjetaResponse,
    tags=["Tarjetas Digitales"],
    summary="Emisión y registro de nueva tarjeta digital",
    description="Registra una nueva tarjeta profesional y genera el primer evento de trazabilidad en su historial."
)
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
            
            # Insertar registro de estado histórico inicial
            query_hist = """
                INSERT INTO tn_tarjetavirtual_estados_historial (
                    tarjeta_id, estado, descripcion, realizado_por
                ) VALUES (%s, %s, %s, %s);
            """
            await cursor.execute(query_hist, (new_id, 'Creada', 'Creación e inicio de emisión de credencial.', 'Sistema'))
            
            return {
                "id": new_id,
                **data.dict()
            }
    except Exception as e:
        print(f"Error al registrar tarjeta: {e}")
        raise HTTPException(
            status_code=500,
            detail="Error al registrar la tarjeta en la base de datos (MS-3831)."
        )
    finally:
        connection.close()

@router.get(
    "/tarjetas/{id}/historial",
    response_model=HistorialTarjetaResponse,
    tags=["Tarjetas Digitales"],
    summary="Consultar trazabilidad de una tarjeta",
    description="Obtiene el historial cronológico de cambios de estado y registro de lecturas públicas QR."
)
async def get_tarjeta_historial(
    id: int = Path(..., description="ID de la tarjeta"),
    client_id: int = Query(..., description="ID de la entidad cliente")
):
    connection = await get_client_connection(client_id)
    try:
        async with connection.cursor(aiomysql.DictCursor) as cursor:
            # 1. Consultar estados
            await cursor.execute(
                """
                SELECT id, tarjeta_id, estado, descripcion, DATE_FORMAT(fecha, '%%Y-%%m-%%d %%H:%%i:%%s') as fecha, realizado_por
                FROM tn_tarjetavirtual_estados_historial
                WHERE tarjeta_id = %s
                ORDER BY fecha ASC;
                """,
                (id,)
            )
            estados = await cursor.fetchall()

            # 2. Consultar lecturas QR
            await cursor.execute(
                """
                SELECT id, tarjeta_id, DATE_FORMAT(fecha, '%%Y-%%m-%%d %%H:%%i:%%s') as fecha, endpoint, metodo, codigo_http, ip
                FROM tn_tarjetavirtual_lecturas_historial
                WHERE tarjeta_id = %s
                ORDER BY fecha DESC;
                """,
                (id,)
            )
            lecturas = await cursor.fetchall()

            return {
                "estados": estados,
                "lecturas": lecturas
            }
    except Exception as e:
        print(f"Error al consultar historial: {e}")
        raise HTTPException(
            status_code=500,
            detail="Error al consultar el historial de la tarjeta en la base de datos (MS-3832)."
        )
    finally:
        connection.close()

@router.get(
    "/validador-qr/config",
    response_model=ValidadorConfigResponse,
    tags=["Configuración y Utilidades"],
    summary="Consultar configuración del validador público QR",
    description="Obtiene los flags de visibilidad de campos en la pantalla de verificación pública."
)
async def get_validador_config(client_id: int = Query(..., description="ID de la entidad cliente")):
    connection = await get_client_connection(client_id)
    try:
        async with connection.cursor(aiomysql.DictCursor) as cursor:
            await cursor.execute(
                """
                SELECT val_foto, val_nombres, val_matricula, val_numero_identificacion, val_codigo_tarjeta, val_estado
                FROM tn_tarjetavirtual_validador_config
                WHERE client_id = %s
                LIMIT 1;
                """,
                (client_id,)
            )
            result = await cursor.fetchone()
            if not result:
                return {
                    "val_foto": 1,
                    "val_nombres": 1,
                    "val_matricula": 1,
                    "val_numero_identificacion": 0,
                    "val_codigo_tarjeta": 1,
                    "val_estado": 1
                }
            return result
    except Exception as e:
        print(f"Error al consultar config de validador: {e}")
        raise HTTPException(
            status_code=500,
            detail="Error al consultar la configuración del validador (MS-3850)."
        )
    finally:
        connection.close()

@router.post(
    "/validador-qr/config",
    response_model=StandardMessageResponse,
    tags=["Configuración y Utilidades"],
    summary="Guardar configuración del validador QR",
    description="Actualiza qué campos son visibles en la consulta pública del código QR."
)
async def save_validador_config(data: ValidadorConfigSave):
    connection = await get_client_connection(data.client_id)
    try:
        async with connection.cursor() as cursor:
            query = """
                INSERT INTO tn_tarjetavirtual_validador_config (
                    client_id, val_foto, val_nombres, val_matricula, val_numero_identificacion, val_codigo_tarjeta, val_estado
                ) VALUES (%s, %s, %s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE
                    val_foto = VALUES(val_foto),
                    val_nombres = VALUES(val_nombres),
                    val_matricula = VALUES(val_matricula),
                    val_numero_identificacion = VALUES(val_numero_identificacion),
                    val_codigo_tarjeta = VALUES(val_codigo_tarjeta),
                    val_estado = VALUES(val_estado);
            """
            params = (
                data.client_id,
                data.val_foto,
                data.val_nombres,
                data.val_matricula,
                data.val_numero_identificacion,
                data.val_codigo_tarjeta,
                data.val_estado
            )
            await cursor.execute(query, params)
            return {"status": "success", "message": "Configuración guardada correctamente."}
    except Exception as e:
        print(f"Error al guardar config de validador: {e}")
        raise HTTPException(
            status_code=500,
            detail="Error al guardar la configuración del validador (MS-3851)."
        )
    finally:
        connection.close()

@router.get(
    "/certificados",
    response_model=List[CertificadoResponse],
    tags=["Configuración y Utilidades"],
    summary="Consultar certificados emitidos",
    description="Obtiene la lista de certificados generados para los contadores y sociedades."
)
async def get_certificados(client_id: int = Query(..., description="ID de la entidad cliente")):
    connection = await get_client_connection(client_id)
    try:
        async with connection.cursor(aiomysql.DictCursor) as cursor:
            await cursor.execute(
                """
                SELECT id, client_id, expediente, titular, documento, matricula, correo, archivo_pdf, DATE_FORMAT(fecha_generacion, '%%Y-%%m-%%d') as fecha_generacion
                FROM tn_tarjetavirtual_certificados
                WHERE client_id = %s
                ORDER BY id ASC;
                """,
                (client_id,)
            )
            records = await cursor.fetchall()
            return records
    except Exception as e:
        print(f"Error al consultar certificados: {e}")
        raise HTTPException(
            status_code=500,
            detail="Error al consultar los certificados en la base de datos (MS-3860)."
        )
    finally:
        connection.close()
