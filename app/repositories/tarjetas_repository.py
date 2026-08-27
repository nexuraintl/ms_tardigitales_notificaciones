import aiomysql
from typing import List, Dict, Any, Optional
from app.core.database import get_client_connection

class TarjetasRepository:

    async def get_all(self, tipo_tarjeta: Optional[str] = None, client_id: Optional[int] = None) -> List[Dict[str, Any]]:
        conn = await get_client_connection(client_id)
        try:
            async with conn.cursor(aiomysql.DictCursor) as cursor:
                if tipo_tarjeta:
                    await cursor.execute(
                        """
                        SELECT
                            id,
                            tipo_tarjeta,
                            codigo,
                            expediente,
                            solicitante,
                            documento,
                            matricula,
                            correo,
                            representante,
                            tarjeta,
                            DATE_FORMAT(fecha, '%%Y-%%m-%%d') AS fecha
                        FROM tn_tarjetavirtual_tarjetas
                        WHERE tipo_tarjeta = %s
                        ORDER BY id DESC
                        """,
                        (tipo_tarjeta,)
                    )
                else:
                    await cursor.execute(
                        """
                        SELECT
                            id,
                            tipo_tarjeta,
                            codigo,
                            expediente,
                            solicitante,
                            documento,
                            matricula,
                            correo,
                            representante,
                            tarjeta,
                            DATE_FORMAT(fecha, '%%Y-%%m-%%d') AS fecha
                        FROM tn_tarjetavirtual_tarjetas
                        ORDER BY id DESC
                        """
                    )
                return await cursor.fetchall()
        finally:
            conn.close()

    async def get_by_id(self, tarjeta_id: int, client_id: Optional[int] = None) -> Optional[Dict[str, Any]]:
        conn = await get_client_connection(client_id)
        try:
            async with conn.cursor(aiomysql.DictCursor) as cursor:
                await cursor.execute(
                    """
                    SELECT
                        id,
                        tipo_tarjeta,
                        codigo,
                        expediente,
                        solicitante,
                        documento,
                        matricula,
                        correo,
                        representante,
                        tarjeta,
                        DATE_FORMAT(fecha, '%%Y-%%m-%%d') AS fecha
                    FROM tn_tarjetavirtual_tarjetas
                    WHERE id = %s
                    LIMIT 1
                    """,
                    (tarjeta_id,)
                )
                return await cursor.fetchone()
        finally:
            conn.close()

    async def create(self, tarjeta_data: Dict[str, Any], client_id: Optional[int] = None) -> int:
        conn = await get_client_connection(client_id)
        try:
            async with conn.cursor() as cursor:
                await cursor.execute(
                    """
                    INSERT INTO tn_tarjetavirtual_tarjetas (
                        tipo_tarjeta, codigo, expediente, solicitante, documento,
                        matricula, correo, representante, tarjeta, fecha
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """,
                    (
                        tarjeta_data.get("tipo_tarjeta") or tarjeta_data.get("tipoTarjeta", "contadores"),
                        tarjeta_data.get("codigo", ""),
                        tarjeta_data.get("expediente", 0),
                        tarjeta_data.get("solicitante") or tarjeta_data.get("nombreTitular", ""),
                        tarjeta_data.get("documento") or tarjeta_data.get("identificacion", ""),
                        tarjeta_data.get("matricula") or tarjeta_data.get("numeroTarjeta", ""),
                        tarjeta_data.get("correo", ""),
                        tarjeta_data.get("representante", None),
                        tarjeta_data.get("tarjeta") or tarjeta_data.get("estado", "Activa"),
                        tarjeta_data.get("fecha", None)
                    )
                )
                return cursor.lastrowid
        finally:
            conn.close()

    async def get_historial(self, tarjeta_id: int, client_id: Optional[int] = None) -> List[Dict[str, Any]]:
        conn = await get_client_connection(client_id)
        try:
            async with conn.cursor(aiomysql.DictCursor) as cursor:
                await cursor.execute(
                    """
                    SELECT
                        id,
                        tarjeta_id,
                        estado,
                        descripcion,
                        DATE_FORMAT(fecha, '%%Y-%%m-%%d %%H:%%i') AS fecha,
                        realizado_por
                    FROM tn_tarjetavirtual_estados_historial
                    WHERE tarjeta_id = %s
                    ORDER BY id DESC
                    """,
                    (tarjeta_id,)
                )
                return await cursor.fetchall()
        finally:
            conn.close()

    async def get_validador_config(self, client_id: Optional[int] = None) -> Dict[str, Any]:
        conn = await get_client_connection(client_id)
        try:
            async with conn.cursor(aiomysql.DictCursor) as cursor:
                await cursor.execute(
                    """
                    SELECT
                        id,
                        client_id,
                        val_foto,
                        val_nombres,
                        val_matricula,
                        val_numero_identificacion,
                        val_codigo_tarjeta,
                        val_estado
                    FROM tn_tarjetavirtual_validador_config
                    WHERE client_id = %s
                    LIMIT 1
                    """,
                    (client_id,)
                )
                row = await cursor.fetchone()
                if row:
                    row["val_foto"] = bool(row["val_foto"])
                    row["val_nombres"] = bool(row["val_nombres"])
                    row["val_matricula"] = bool(row["val_matricula"])
                    row["val_numero_identificacion"] = bool(row["val_numero_identificacion"])
                    row["val_codigo_tarjeta"] = bool(row["val_codigo_tarjeta"])
                    row["val_estado"] = bool(row["val_estado"])
                    return row
                return {
                    "val_foto": True,
                    "val_nombres": True,
                    "val_matricula": True,
                    "val_numero_identificacion": True,
                    "val_codigo_tarjeta": True,
                    "val_estado": True
                }
        finally:
            conn.close()

    async def save_validador_config(self, config_data: Dict[str, Any], client_id: Optional[int] = None) -> bool:
        conn = await get_client_connection(client_id)
        try:
            async with conn.cursor() as cursor:
                await cursor.execute(
                    "SELECT id FROM tn_tarjetavirtual_validador_config WHERE client_id = %s LIMIT 1",
                    (client_id,)
                )
                exists = await cursor.fetchone()
                
                vf = 1 if config_data.get("val_foto") else 0
                vn = 1 if config_data.get("val_nombres") else 0
                vm = 1 if config_data.get("val_matricula") else 0
                vnum = 1 if config_data.get("val_numero_identificacion") else 0
                vc = 1 if config_data.get("val_codigo_tarjeta") else 0
                ve = 1 if config_data.get("val_estado") else 0

                if exists:
                    await cursor.execute(
                        """
                        UPDATE tn_tarjetavirtual_validador_config SET
                            val_foto = %s,
                            val_nombres = %s,
                            val_matricula = %s,
                            val_numero_identificacion = %s,
                            val_codigo_tarjeta = %s,
                            val_estado = %s,
                            fecha_actualizacion = CURRENT_TIMESTAMP
                        WHERE client_id = %s
                        """,
                        (vf, vn, vm, vnum, vc, ve, client_id)
                    )
                else:
                    await cursor.execute(
                        """
                        INSERT INTO tn_tarjetavirtual_validador_config (
                            client_id, val_foto, val_nombres, val_matricula,
                            val_numero_identificacion, val_codigo_tarjeta, val_estado
                        ) VALUES (%s, %s, %s, %s, %s, %s, %s)
                        """,
                        (client_id, vf, vn, vm, vnum, vc, ve)
                    )
                return True
        finally:
            conn.close()
