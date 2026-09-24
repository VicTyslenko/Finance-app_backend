from fastapi import APIRouter, HTTPException, Query
from psycopg import errors
from psycopg.rows import dict_row

from api.database import pool
from api.models import Budget, BudgetCreate

router = APIRouter(prefix="/budgets", tags=["budgets"])


@router.post("", response_model=Budget, status_code=201)
async def create_budget(
    body: BudgetCreate,
    user_id: int = Query(..., description="Whose budget; becomes the JWT subject once auth lands"),
):
    """Create one budget for a user. One per category."""
    async with pool.connection() as conn:
        async with conn.cursor(row_factory=dict_row) as cur:
            try:
                await cur.execute(
                    """
                    INSERT INTO public.budgets (user_id, category, maximum_spend, theme)
                    VALUES (%s, %s, %s, %s)
                    RETURNING budget_id, category, maximum_spend, theme, created_at
                    """,
                    (user_id, body.category, body.maximum_spend, body.theme),
                )
            except errors.UniqueViolation:
                raise HTTPException(409, f"A budget for {body.category} already exists")
            except errors.ForeignKeyViolation:
                raise HTTPException(404, "User not found")
            except errors.CheckViolation:
                raise HTTPException(422, f"'{body.category}' is not a valid category")

            return await cur.fetchone()
