from fastapi import APIRouter

from api.routes.auth import router as auth_router
from api.routes.analysis import router as analysis_router
from api.routes.market import router as market_router
from api.routes.user import router as user_router
from api.routes.health import router as health_router
from api.routes.webhooks import router as webhooks_router

api_router = APIRouter()

api_router.include_router(health_router, tags=["Health"])
api_router.include_router(auth_router, prefix="/auth", tags=["Authentication"])
api_router.include_router(analysis_router, prefix="/analysis", tags=["Analysis"])
api_router.include_router(market_router, prefix="/market", tags=["Market Data"])
api_router.include_router(user_router, prefix="/user", tags=["User Management"])
api_router.include_router(webhooks_router, prefix="/webhooks", tags=["Webhooks"])
