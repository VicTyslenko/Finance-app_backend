from fastapi import APIRouter, HTTPException, Query
from psycopg import errors
from psycopg.rows import dict_row

from api.database import pool
from api.models import Pot, PotCreate, PotMove

router = APIRouter(prefix="/pots", tags=["pots"])

POT_COLUMNS = "pot_id, name, target, total, theme, created_at"


@router.get("", response_model=list[Pot])
async def pots_list(
    user_id: int = Query(..., description="Whose pots; becomes the JWT subject once auth lands"),
):
    """List a user's pots."""
    async with pool.connection() as conn:
        async with conn.cursor(row_factory=dict_row) as cur:
            await cur.execute(
                f"""
                SELECT {POT_COLUMNS}
                FROM public.pots
                WHERE user_id = %s
                ORDER BY created_at
                """,
                (user_id,),
            )
            return await cur.fetchall()


@router.post("", response_model=Pot, status_code=201)
async def create_pot(
    body: PotCreate,
    user_id: int = Query(..., description="Whose pot; becomes the JWT subject once auth lands"),
):
    """Create an empty pot for a user. Names are unique per user."""
    async with pool.connection() as conn:
        async with conn.cursor(row_factory=dict_row) as cur:
            try:
                await cur.execute(
                    f"""
                    INSERT INTO public.pots (user_id, name, target, theme)
                    VALUES (%s, %s, %s, %s)
                    RETURNING {POT_COLUMNS}
                    """,
                    (user_id, body.name, body.target, body.theme),
                )
            except errors.UniqueViolation:
                raise HTTPException(409, f"A pot named {body.name} already exists")
            except errors.ForeignKeyViolation:
                raise HTTPException(404, "User not found")

            return await cur.fetchone()


@router.put("/{pot_id}", response_model=Pot)
async def update_pot(
    pot_id: int,
    body: PotCreate,
    user_id: int = Query(..., description="Whose pot; becomes the JWT subject once auth lands"),
):
    """Replace a pot's name, target and theme. The total only moves via deposit/withdraw."""
    async with pool.connection() as conn:
        async with conn.cursor(row_factory=dict_row) as cur:
            try:
                await cur.execute(
                    f"""
                    UPDATE public.pots
                    SET name = %s, target = %s, theme = %s
                    WHERE pot_id = %s AND user_id = %s
                    RETURNING {POT_COLUMNS}
                    """,
                    (body.name, body.target, body.theme, pot_id, user_id),
                )
            except errors.UniqueViolation:
                raise HTTPException(409, f"A pot named {body.name} already exists")

            row = await cur.fetchone()
            if row is None:
                raise HTTPException(404, "Pot not found")
            return row


@router.delete("/{pot_id}", status_code=204)
async def delete_pot(
    pot_id: int,
    user_id: int = Query(..., description="Whose pot; becomes the JWT subject once auth lands"),
):
    """Delete a pot and return its money to the user's balance."""
    async with pool.connection() as conn:
        async with conn.transaction():
            async with conn.cursor() as cur:
                await cur.execute(
                    """
                    DELETE FROM public.pots
                    WHERE pot_id = %s AND user_id = %s
                    RETURNING total
                    """,
                    (pot_id, user_id),
                )
                row = await cur.fetchone()
                if row is None:
                    raise HTTPException(404, "Pot not found")

                await cur.execute(
                    "UPDATE public.users SET balance = balance + %s WHERE user_id = %s",
                    (row[0], user_id),
                )


@router.post("/{pot_id}/deposit", response_model=Pot)
async def deposit(
    pot_id: int,
    body: PotMove,
    user_id: int = Query(..., description="Whose pot; becomes the JWT subject once auth lands"),
):
    """Move money from the user's balance into a pot."""
    async with pool.connection() as conn:
        async with conn.transaction():
            async with conn.cursor(row_factory=dict_row) as cur:
                # The balance check lives in the WHERE, so two quick clicks can't overdraw.
                await cur.execute(
                    """
                    UPDATE public.users SET balance = balance - %s
                    WHERE user_id = %s AND balance >= %s
                    """,
                    (body.amount, user_id, body.amount),
                )
                if cur.rowcount == 0:
                    raise HTTPException(400, "Insufficient balance")

                await cur.execute(
                    f"""
                    UPDATE public.pots SET total = total + %s
                    WHERE pot_id = %s AND user_id = %s
                    RETURNING {POT_COLUMNS}
                    """,
                    (body.amount, pot_id, user_id),
                )
                row = await cur.fetchone()
                if row is None:
                    # Raising inside transaction() rolls back the balance change above.
                    raise HTTPException(404, "Pot not found")
                return row


@router.post("/{pot_id}/withdraw", response_model=Pot)
async def withdraw(
    pot_id: int,
    body: PotMove,
    user_id: int = Query(..., description="Whose pot; becomes the JWT subject once auth lands"),
):
    """Move money from a pot back to the user's balance."""
    async with pool.connection() as conn:
        async with conn.transaction():
            async with conn.cursor(row_factory=dict_row) as cur:
                await cur.execute(
                    f"""
                    UPDATE public.pots SET total = total - %s
                    WHERE pot_id = %s AND user_id = %s AND total >= %s
                    RETURNING {POT_COLUMNS}
                    """,
                    (body.amount, pot_id, user_id, body.amount),
                )
                row = await cur.fetchone()
                if row is None:
                    raise HTTPException(400, "Pot not found or not enough in it")

                await cur.execute(
                    "UPDATE public.users SET balance = balance + %s WHERE user_id = %s",
                    (body.amount, user_id),
                )
                return row
