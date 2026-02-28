"""
Crypto IA Auditor - Enterprise REST API
========================================
Production-grade API for intelligent smart contract & cryptocurrency analysis.

Run with:
    uvicorn api.main:app --reload --host 0.0.0.0 --port 8000

Or production:
    gunicorn api.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
"""

import os
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from api.core.config import get_settings
from api.core.logging import setup_logging, get_logger
from api.database.session import init_db
from api.middleware.error_handler import ErrorHandlerMiddleware
from api.middleware.rate_limiter import RateLimitMiddleware
from api.middleware.request_logging import RequestLoggingMiddleware
from api.routes import api_router

STATIC_DIR = Path(__file__).resolve().parent / "static"

settings = get_settings()
setup_logging()
logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info(
        "starting_api",
        app=settings.APP_NAME,
        version=settings.APP_VERSION,
        environment=settings.ENVIRONMENT,
    )
    await init_db()
    logger.info("database_initialized")
    yield
    logger.info("shutting_down_api")


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description=(
        "Enterprise-grade REST API for intelligent smart contract auditing, "
        "wallet forensics, and market sentiment analysis powered by AI. "
        "\n\n"
        "## Authentication\n"
        "Use JWT Bearer tokens or API keys (X-API-Key header).\n\n"
        "## Rate Limits\n"
        f"- {settings.RATE_LIMIT_PER_MINUTE} requests/minute\n"
        f"- {settings.RATE_LIMIT_PER_HOUR} requests/hour\n\n"
        "## Plans\n"
        "- **Free**: 3 analyses\n"
        "- **Basic** ($49/mo): 20 analyses + sentiment\n"
        "- **Pro** ($199/mo): 100 analyses + PDF + API + priority\n"
    ),
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan,
    openapi_tags=[
        {"name": "Health", "description": "Service health and readiness probes"},
        {"name": "Authentication", "description": "Register, login, and token management"},
        {"name": "Analysis", "description": "Smart contract, wallet, and sentiment analysis"},
        {"name": "Market Data", "description": "Cryptocurrency price and trending data"},
        {"name": "User Management", "description": "Profile, credits, and API key management"},
        {"name": "Webhooks", "description": "Payment webhook handlers"},
    ],
)

# ─── Middleware (order matters: last added = first executed) ─────────────────

app.add_middleware(ErrorHandlerMiddleware)
app.add_middleware(RequestLoggingMiddleware)
app.add_middleware(RateLimitMiddleware)
app.add_middleware(GZipMiddleware, minimum_size=1000)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=[
        "X-Request-ID",
        "X-Response-Time",
        "X-RateLimit-Limit",
        "X-RateLimit-Remaining",
    ],
)

# ─── Routes ──────────────────────────────────────────────────────────────────

app.include_router(api_router, prefix="/api/v1")

# ─── Static Files & Favicon ──────────────────────────────────────────────────

app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")


@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    ico_path = STATIC_DIR / "favicon.ico"
    if ico_path.exists():
        return FileResponse(str(ico_path), media_type="image/x-icon")
    return FileResponse(str(STATIC_DIR / "favicon.svg"), media_type="image/svg+xml")


@app.get("/", include_in_schema=False)
async def root():
    return {
        "name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "docs": "/docs",
        "health": "/api/v1/health",
    }
