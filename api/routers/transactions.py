from fastapi import APIRouter, Query
from psycopg.rows import dict_row

from api.database import pool
from api.models import Transaction

router = APIRouter(prefix="/transactions", tags=["transactions"])


@router.get("", response_model=list[Transaction])
async def list_transactions(
    user_id: int = Query(..., description="Whose ledger; becomes the JWT subject once auth lands"),
    limit: int | None = Query(None, ge=1, le=200, description="Omit for the full history"),
):
    """A user's transactions, newest first."""
    async with pool.connection() as conn:
        async with conn.cursor(row_factory=dict_row) as cur:
            await cur.execute(
                """
                SELECT t.transaction_id,
                       c.name AS counterparty,
                       c.slug AS counterparty_slug,
                       c.avatar_url,
                       t.category,
                       t.amount,
                       t.occurred_at
                FROM public.transactions t
                JOIN public.counterparties c USING (counterparty_id)
                WHERE t.user_id = %s
                ORDER BY t.occurred_at DESC, t.transaction_id DESC
                LIMIT %s
                """,
                (user_id, limit),
            )
            return await cur.fetchall()
