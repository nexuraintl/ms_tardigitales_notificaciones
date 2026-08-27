import aiomysql
from typing import List, Dict, Any, Optional
from app.core.database import get_client_connection

class TramitesRepository:

    async def get_all(self, client_id: Optional[int] = None) -> List[Dict[str, Any]]:
        conn = await get_client_connection(client_id)
        try:
            async with conn.cursor(aiomysql.DictCursor) as cursor:
                await cursor.execute(
                    """
                    SELECT
                        id,
                        nombre,
                        tipo,
                        costo,
                        estado,
                        descripcion
                    FROM tn_tarjetavirtual_tramites
                    ORDER BY id ASC
                    """
                )
                rows = await cursor.fetchall()
                for r in rows:
                    if r.get("costo") is not None:
                        r["costo"] = float(r["costo"])
                return rows
        finally:
            conn.close()

    async def get_by_id(self, tramite_id: int, client_id: Optional[int] = None) -> Optional[Dict[str, Any]]:
        conn = await get_client_connection(client_id)
        try:
            async with conn.cursor(aiomysql.DictCursor) as cursor:
                await cursor.execute(
                    """
                    SELECT
                        id,
                        nombre,
                        tipo,
                        costo,
                        estado,
                        descripcion
                    FROM tn_tarjetavirtual_tramites
                    WHERE id = %s
                    LIMIT 1
                    """,
                    (tramite_id,)
                )
                row = await cursor.fetchone()
                if row and row.get("costo") is not None:
                    row["costo"] = float(row["costo"])
                return row
        finally:
            conn.close()

    async def create(self, tramite_data: Dict[str, Any], client_id: Optional[int] = None) -> int:
        conn = await get_client_connection(client_id)
        try:
            async with conn.cursor() as cursor:
                await cursor.execute(
                    """
                    INSERT INTO tn_tarjetavirtual_tramites (
                        nombre, tipo, costo, estado, descripcion
                    ) VALUES (%s, %s, %s, %s, %s)
                    """,
                    (
                        tramite_data.get("nombre", ""),
                        tramite_data.get("tipo", "General"),
                        tramite_data.get("costo", 0.0),
                        tramite_data.get("estado", "Activo"),
                        tramite_data.get("descripcion", "")
                    )
                )
                return cursor.lastrowid
        finally:
            conn.close()

    async def update(self, tramite_id: int, update_data: Dict[str, Any], client_id: Optional[int] = None) -> bool:
        conn = await get_client_connection(client_id)
        try:
            fields = []
            values = []
            
            allowed = ["nombre", "tipo", "costo", "estado", "descripcion"]
            for k in allowed:
                if k in update_data and update_data[k] is not None:
                    fields.append(f"{k} = %s")
                    values.append(update_data[k])
                    
            if not fields:
                return True
                
            values.append(tramite_id)
            sql = f"UPDATE tn_tarjetavirtual_tramites SET {', '.join(fields)} WHERE id = %s"
            
            async with conn.cursor() as cursor:
                await cursor.execute(sql, tuple(values))
                return cursor.rowcount > 0
        finally:
            conn.close()

    async def delete(self, tramite_id: int, client_id: Optional[int] = None) -> bool:
        conn = await get_client_connection(client_id)
        try:
            async with conn.cursor() as cursor:
                await cursor.execute("DELETE FROM tn_tarjetavirtual_tramites WHERE id = %s", (tramite_id,))
                return cursor.rowcount > 0
        finally:
            conn.close()
