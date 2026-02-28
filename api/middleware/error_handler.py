import traceback

from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from api.core.exceptions import APIError
from api.core.logging import get_logger

logger = get_logger(__name__)


class ErrorHandlerMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            return await call_next(request)
        except APIError:
            raise  # Let FastAPI handle our custom errors
        except Exception as e:
            logger.error(
                "unhandled_exception",
                path=request.url.path,
                method=request.method,
                error=str(e),
                traceback=traceback.format_exc(),
            )
            return JSONResponse(
                status_code=500,
                content={
                    "error_code": "INTERNAL_SERVER_ERROR",
                    "message": "An unexpected error occurred. Please try again later.",
                },
            )
