"""Connection pool, opened on startup and shared by every request."""

import os

from dotenv import load_dotenv
from psycopg_pool import AsyncConnectionPool

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL is not set — check your .env")

pool = AsyncConnectionPool(
    conninfo=DATABASE_URL,
    open=False,        # opened in main.py's lifespan, not at import time
    min_size=1,
    max_size=10,
    max_idle=300,
    check=AsyncConnectionPool.check_connection,   # discard dead connections
)
