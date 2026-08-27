import aiomysql
from typing import List, Dict, Any, Optional
from app.core.database import get_client_connection

class NotificacionesRepository:

    async def get_all(self, client_id: Optional[int] = None) -> List[Dict[str, Any]]:
        conn = await get_client_connection(client_id)
        try:
            async with conn.cursor(aiomysql.DictCursor) as cursor:
                await cursor.execute(
                    """
                    SELECT
                        id,
                        titulo,
                        canal,
                        audiencia,
                        destinatarios,
                        fecha,
                        estado,
                        creado_por AS creadoPor,
                        mensaje
                    FROM tn_tarjetavirtual_notificaciones
                    ORDER BY id DESC
                    """
                )
                return await cursor.fetchall()
        finally:
            conn.close()

    async def create(self, notif_data: Dict[str, Any], client_id: Optional[int] = None) -> int:
        conn = await get_client_connection(client_id)
        try:
            async with conn.cursor() as cursor:
                await cursor.execute(
                    """
                    INSERT INTO tn_tarjetavirtual_notificaciones (
                        titulo, canal, audiencia, destinatarios, fecha, estado, creado_por, mensaje
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    """,
                    (
                        notif_data.get("titulo", ""),
                        notif_data.get("canal", "Push"),
                        notif_data.get("audiencia", "Todos"),
                        notif_data.get("destinatarios", 0),
                        notif_data.get("fecha", ""),
                        notif_data.get("estado", "Entregada"),
                        notif_data.get("creadoPor") or notif_data.get("creado_por") or "Administrador",
                        notif_data.get("mensaje", "")
                    )
                )
                return cursor.lastrowid
        finally:
            conn.close()
