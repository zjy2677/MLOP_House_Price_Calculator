import os

import psycopg2


def check_db_connection() -> bool:
    """Health helper only; this is intentionally minimal.

    TODO (Person 2): move to pooled connections + repository layer.
    """
    try:
        conn = psycopg2.connect(
            host=os.getenv("POSTGRES_HOST", "db"),
            port=os.getenv("POSTGRES_PORT", "5432"),
            dbname=os.getenv("POSTGRES_DB", "realestate"),
            user=os.getenv("POSTGRES_USER", "realestate_user"),
            password=os.getenv("POSTGRES_PASSWORD", "realestate_pass"),
            connect_timeout=2,
        )
        conn.close()
        return True
    except Exception:
        return False
