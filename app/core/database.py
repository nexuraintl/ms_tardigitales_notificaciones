import os
import aiomysql
from fastapi import HTTPException
from app.core.mysql import get_mysql_connection

async def get_client_mysql_config(client_id: int):
    # Si no se configuró DB1_HOST, no intentamos consultar la central
    if not os.getenv("DB1_HOST"):
        return None
        
    try:
        connection = await get_mysql_connection()
    except Exception as e:
        print(f"[Database Manager] Error al conectar con la base de datos central: {e}")
        return None

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
        print(f"[Database Manager] Error al consultar la tabla tn_gestion_bdconex para cliente {client_id}: {e}")
        return None
    finally:
        connection.close()

async def get_client_connection(client_id: int | None = None):
    # 1. Resolver el client_id (del parámetro o de la variable de entorno por defecto)
    if not client_id:
        default_id = os.getenv("CLIENT_ID")
        client_id = int(default_id) if default_id else None

    # 2. Intentar obtener configuración dinámica desde la base de datos central
    if client_id:
        config = await get_client_mysql_config(client_id)
        if config:
            try:
                print(f"[Database Manager] Conectando dinámicamente a {config['nombreBaseDeDatos']} en {config['hosting']}")
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
                print(f"[Database Manager] Error al conectar a la BD dinámica del cliente {client_id}: {e}")
                # Si falla, podemos continuar y usar el fallback local

    # 3. Fallback: Conexión directa a base de datos de Laragon/desarrollo local
    fallback_host = os.getenv("DB_HOST", "127.0.0.1")
    fallback_port = int(os.getenv("DB_PORT", 3306))
    fallback_user = os.getenv("DB_USER", "root")
    fallback_pass = os.getenv("DB_PASS", "")
    fallback_name = os.getenv("DB_NAME", "producto9_base")

    try:
        print(f"[Database Manager] Usando conexión local de respaldo (fallback): {fallback_name} en {fallback_host}")
        connection = await aiomysql.connect(
            host=fallback_host,
            port=fallback_port,
            user=fallback_user,
            password=fallback_pass,
            db=fallback_name,
            autocommit=True
        )
        return connection
    except Exception as e:
        print(f"[Database Manager] Error crítico de conexión en fallback: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error al establecer conexión con la base de datos local ({fallback_name})."
        )
