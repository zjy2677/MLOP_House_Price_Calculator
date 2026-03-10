from fastapi import FastAPI

from api.routes.analysis import router as analysis_router
from api.routes.health import router as health_router

app = FastAPI(
    title="Real Estate Analysis API",
    version="0.1.0",
    description="Starter backend for the real-estate prototype project.",
)

app.include_router(health_router)
app.include_router(analysis_router, prefix="/api/v1")
