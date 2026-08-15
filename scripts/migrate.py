"""Apply database/*.sql in filename order, once each.

Same model as MSO's osp-db-mgmt: numbered files, applied in order, each inside
one transaction, recorded in migration_log so it never runs twice.
"""

import os
import sys
from pathlib import Path

import psycopg
from dotenv import load_dotenv

load_dotenv()

DATABASE_DIR = Path(__file__).resolve().parent.parent / "database"
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    sys.exit("DATABASE_URL is not set — check your .env")


def main() -> None:
    files = sorted(DATABASE_DIR.glob("*.sql"))
    if not files:
        sys.exit(f"No .sql files in {DATABASE_DIR}")

    with psycopg.connect(DATABASE_URL) as conn:
        # Bootstrap: the log has to exist before we can ask what's applied.
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS public.migration_log (
                    filename   text PRIMARY KEY,
                    applied_at timestamptz NOT NULL DEFAULT now()
                )
            """)
            conn.commit()

            cur.execute("SELECT filename FROM public.migration_log")
            applied = {row[0] for row in cur.fetchall()}

        for path in files:
            if path.name in applied:
                print(f"  · {path.name} (already applied)")
                continue
            try:
                with conn.cursor() as cur:
                    cur.execute(path.read_text())
                    cur.execute(
                        "INSERT INTO public.migration_log (filename) VALUES (%s)",
                        (path.name,),
                    )
                conn.commit()
                print(f"  ✓ {path.name}")
            except Exception as e:
                conn.rollback()
                sys.exit(f"  ✗ {path.name}\n     {e}")

    print("Done.")


if __name__ == "__main__":
    main()
