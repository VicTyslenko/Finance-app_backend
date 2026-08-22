from fastapi import APIRouter, HTTPException
from psycopg.rows import dict_row

from api.database import pool
from api.models import User

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/", response_model=list[User])
async def list_users():
    """Every user, alphabetically."""
    async with pool.connection() as conn:
        async with conn.cursor(row_factory=dict_row) as cur:
            await cur.execute("""
                SELECT user_id, email, full_name, created_at, avatar_url
                FROM public.users
                ORDER BY full_name
            """)
            return await cur.fetchall()


@router.get("/{user_id}", response_model=User)
async def get_user(user_id: int):
    """One user by id."""
    async with pool.connection() as conn:
        async with conn.cursor(row_factory=dict_row) as cur:
            await cur.execute(
                """
                SELECT user_id, email, full_name, created_at
                FROM public.users
                WHERE user_id = %s
                """,
                (user_id,),
            )
            row = await cur.fetchone()
            if row is None:
                raise HTTPException(status_code=404, detail="User not found")
            return row
