import time
from collections import defaultdict
from typing import Dict, Tuple

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

from api.core.config import get_settings
from api.core.logging import get_logger

settings = get_settings()
logger = get_logger(__name__)


class InMemoryRateLimiter:
    """Simple in-memory rate limiter. Replace with Redis for multi-instance deployments."""

    def __init__(self):
        self._requests: Dict[str, list[float]] = defaultdict(list)

    def _cleanup(self, key: str, window: float) -> None:
        now = time.time()
        self._requests[key] = [
            t for t in self._requests[key] if now - t < window
        ]

    def is_allowed(self, key: str, max_requests: int, window: float) -> Tuple[bool, int]:
        self._cleanup(key, window)
        count = len(self._requests[key])

        if count >= max_requests:
            return False, 0

        self._requests[key].append(time.time())
        return True, max_requests - count - 1


limiter = InMemoryRateLimiter()


class RateLimitMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        # Skip rate limiting for health checks
        if request.url.path in ("/health", "/ready", "/docs", "/openapi.json"):
            return await call_next(request)

        # Identify client by IP or API key
        client_id = request.headers.get("x-api-key") or request.client.host

        # Per-minute limit
        allowed, remaining = limiter.is_allowed(
            f"min:{client_id}",
            settings.RATE_LIMIT_PER_MINUTE,
            60.0,
        )

        if not allowed:
            logger.warning("rate_limit_exceeded", client=client_id, window="minute")
            return Response(
                content='{"error_code":"RATE_LIMIT_EXCEEDED","message":"Too many requests. Try again later."}',
                status_code=429,
                media_type="application/json",
                headers={
                    "Retry-After": "60",
                    "X-RateLimit-Limit": str(settings.RATE_LIMIT_PER_MINUTE),
                    "X-RateLimit-Remaining": "0",
                },
            )

        response = await call_next(request)

        response.headers["X-RateLimit-Limit"] = str(settings.RATE_LIMIT_PER_MINUTE)
        response.headers["X-RateLimit-Remaining"] = str(remaining)

        return response
