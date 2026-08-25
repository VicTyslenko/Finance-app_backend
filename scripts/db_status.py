"""Show which migrations are applied and how many rows each table holds."""

import os

import psycopg
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise SystemExit("DATABASE_URL is not set — check your .env")

with psycopg.connect(DATABASE_URL) as conn, conn.cursor() as cur:
    cur.execute("""
        SELECT table_name
        FROM information_schema.tables
        WHERE table_schema = 'public' AND table_type = 'BASE TABLE'
        ORDER BY table_name
    """)
    tables = [row[0] for row in cur.fetchall()]

    print("Tables:")
    for table in tables:
        # table names come from information_schema, not user input
        cur.execute(f'SELECT count(*) FROM public."{table}"')
        print(f"  {table:<20} {cur.fetchone()[0]:>6} rows")

    if "migration_log" in tables:
        cur.execute("SELECT filename FROM public.migration_log ORDER BY filename")
        print("\nApplied migrations:")
        for (filename,) in cur.fetchall():
            print(f"  \u00b7 {filename}")
