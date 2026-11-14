from fastapi import APIRouter, Query
from psycopg.rows import dict_row

from api.database import pool
from api.models import RecurringBill

router = APIRouter(prefix="/bills", tags=["bills"])


@router.get("", response_model=list[RecurringBill])
async def recurring_bills_list(user_id: int = Query(...)):
    """List a user's recurring bills, with whether each is paid this month."""
    async with pool.connection() as conn:
        async with conn.cursor(row_factory=dict_row) as cur:
            await cur.execute(
                """
                SELECT b.bill_id,
                       c.name AS counterparty,
                       c.slug AS counterparty_slug,
                       c.avatar_url,
                       b.category,
                       b.amount,
                       b.due_day,
                       EXISTS (
                           SELECT 1
                           FROM public.transactions t
                           WHERE t.user_id = b.user_id
                             AND t.counterparty_id = b.counterparty_id
                             AND t.occurred_at >= date_trunc('month', now())
                       ) AS paid
                FROM public.recurring_bills b
                JOIN public.counterparties c USING (counterparty_id)
                WHERE b.user_id = %s
                ORDER BY b.due_day
                """,
                (user_id,),
            )
            return await cur.fetchall()
