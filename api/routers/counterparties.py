from fastapi import APIRouter
from psycopg.rows import dict_row

from api.database import pool
from api.models import Counterparty

router = APIRouter(prefix="/counterparties", tags=["counterparties"])


@router.get("", response_model=list[Counterparty])
async def list_counterparties():
    """Every counterparty, alphabetically."""
    async with pool.connection() as conn:
        async with conn.cursor(row_factory=dict_row) as cur:
            await cur.execute("""
                SELECT counterparty_id, name, slug, avatar_url, kind, created_at
                FROM public.counterparties
                ORDER BY name
            """)
            return await cur.fetchall()
