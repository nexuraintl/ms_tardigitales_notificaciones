import os
import aiomysql
from fastapi import HTTPException
from app.core.mysql import get_mysql_connection

async def get_client_mysql_config(client_id: int):
    if not os.getenv("DB1_HOST"):
        return None
        
    try:
        connection = await get_mysql_connection()
    except Exception as e:
        print(f"[Database Manager] Error de conexión al servidor central de base de datos: {e}")
        raise HTTPException(
            status_code=500,
            detail="No fue posible establecer conexión con el repositorio de datos (MS-3804)."
        )

    try:
        async with connection.cursor(aiomysql.DictCursor) as cursor:
            await cursor.execute(
                """
                SELECT
                    nombreBaseDeDatos,
                    usuario,
                    contrasena,
                    hosting,
                    puerto,
                    tipoDeBaseDeDatos
                FROM tn_gestion_bdconex
                WHERE idCliente = %s
                AND tipoDeBaseDeDatos = 'mysql'
                LIMIT 1
                """,
                (client_id,)
            )
            result = await cursor.fetchone()
            return result
    except Exception as e:
        print(f"[Database Manager] Error al consultar configuración de entidad {client_id}: {e}")
        raise HTTPException(
            status_code=500,
            detail="Error al consultar los parámetros de configuración de la entidad (MS-3805)."
        )
    finally:
        connection.close()

async def get_client_connection(client_id: int | None = None):
    # 1. Resolver el client_id
    if not client_id:
        default_id = os.getenv("CLIENT_ID")
        client_id = int(default_id) if default_id else None

    if not client_id:
        raise HTTPException(
            status_code=400,
            detail="Identificador de entidad no especificado en la solicitud (MS-3803)."
        )

    # 2. Obtener configuración dinámica desde la base de datos central
    config = await get_client_mysql_config(client_id)
    if not config:
        raise HTTPException(
            status_code=500,
            detail="Configuración de entidad no localizada en el repositorio central (MS-3805)."
        )

    try:
        connection = await aiomysql.connect(
            host=config["hosting"],
            port=int(config["puerto"] or 3306),
            user=config["usuario"],
            password=config["contrasena"],
            db=config["nombreBaseDeDatos"],
            autocommit=True
        )
        return connection
    except Exception as e:
        print(f"[Database Manager] Error al conectar a la base de datos de la entidad {client_id}: {e}")
        raise HTTPException(
            status_code=500,
            detail="No fue posible establecer conexión con el repositorio de datos de la entidad (MS-3804)."
        )
