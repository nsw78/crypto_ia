import time

from fastapi import APIRouter

from api.core.config import get_settings
from api.schemas.common import HealthResponse

router = APIRouter()
settings = get_settings()

_start_time = time.time()


@router.get("/health", response_model=HealthResponse)
async def health_check():
    return HealthResponse(
        status="healthy",
        version=settings.APP_VERSION,
        environment=settings.ENVIRONMENT,
        uptime_seconds=round(time.time() - _start_time, 2),
    )


@router.get("/ready")
async def readiness_check():
    return {"status": "ready"}
