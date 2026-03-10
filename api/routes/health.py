from fastapi import APIRouter

from api.services.db import check_db_connection

router = APIRouter(tags=["health"])


@router.get("/health")
def health() -> dict:
    db_ok = check_db_connection()
    return {
        "status": "ok",
        "db_connected": db_ok,
    }
