from fastapi import APIRouter, HTTPException, Query
from psycopg import errors
from psycopg.rows import dict_row

from api.database import pool
from api.models import Budget, BudgetCreate

router = APIRouter(prefix="/budgets", tags=["budgets"])

@router.get("/{user_id}", response_model=list[Budget])
async def budgets_list(user_id: int
):
    """List of budgets per user."""
    async with pool.connection() as conn:
        async with conn.cursor(row_factory=dict_row) as cur:
            await cur.execute(
                """
                  SELECT budget_id, category, maximum_spend, theme, created_at
                  FROM public.budgets
                  WHERE user_id = %s
                  ORDER BY created_at
            """,
            (user_id,),
            )
            return await cur.fetchall() 




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


@router.delete("/{budget_id}", status_code=204)
async def delete_budget(
    budget_id: int,
    user_id: int = Query(..., description="Whose budget; becomes the JWT subject once auth lands"),
):
    """Delete one of the user's budgets."""
    async with pool.connection() as conn:
        async with conn.cursor() as cur:
            await cur.execute(
                """
                DELETE FROM public.budgets
                WHERE budget_id = %s AND user_id = %s
                """,
                (budget_id, user_id),
            )
            if cur.rowcount == 0:
                raise HTTPException(404, "Budget not found")


@router.put("/{budget_id}", response_model=Budget)
async def update_budget(
    budget_id: int,
    body: BudgetCreate,
    user_id: int = Query(..., description="Whose budget; becomes the JWT subject once auth lands"),
):
    """Replace one of the user's budgets."""
    async with pool.connection() as conn:
        async with conn.cursor(row_factory=dict_row) as cur:
            try:
                await cur.execute(
                    """
                    UPDATE public.budgets
                    SET category = %s, maximum_spend = %s, theme = %s
                    WHERE budget_id = %s AND user_id = %s
                    RETURNING budget_id, category, maximum_spend, theme, created_at
                    """,
                    (body.category, body.maximum_spend, body.theme, budget_id, user_id),
                )
            except errors.UniqueViolation:
                raise HTTPException(409, f"A budget for {body.category} already exists")
            except errors.CheckViolation:
                raise HTTPException(422, f"'{body.category}' is not a valid category")

            row = await cur.fetchone()
            if row is None:
                raise HTTPException(404, "Budget not found")
            return row


          