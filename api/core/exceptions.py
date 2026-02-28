from typing import Any, Optional

from fastapi import HTTPException, status


class APIError(HTTPException):
    def __init__(
        self,
        status_code: int,
        error_code: str,
        message: str,
        details: Optional[Any] = None,
    ):
        super().__init__(
            status_code=status_code,
            detail={
                "error_code": error_code,
                "message": message,
                "details": details,
            },
        )


class UnauthorizedError(APIError):
    def __init__(self, message: str = "Authentication required"):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            error_code="UNAUTHORIZED",
            message=message,
        )


class ForbiddenError(APIError):
    def __init__(self, message: str = "Insufficient permissions"):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            error_code="FORBIDDEN",
            message=message,
        )


class NotFoundError(APIError):
    def __init__(self, resource: str = "Resource"):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            error_code="NOT_FOUND",
            message=f"{resource} not found",
        )


class InsufficientCreditsError(APIError):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_402_PAYMENT_REQUIRED,
            error_code="INSUFFICIENT_CREDITS",
            message="You don't have enough credits. Please upgrade your plan.",
        )


class RateLimitError(APIError):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            error_code="RATE_LIMIT_EXCEEDED",
            message="Too many requests. Please try again later.",
        )


class ValidationError(APIError):
    def __init__(self, message: str, details: Any = None):
        super().__init__(
            status_code=422,
            error_code="VALIDATION_ERROR",
            message=message,
            details=details,
        )


class ExternalServiceError(APIError):
    def __init__(self, service: str, message: str = "External service error"):
        super().__init__(
            status_code=status.HTTP_502_BAD_GATEWAY,
            error_code="EXTERNAL_SERVICE_ERROR",
            message=f"{service}: {message}",
        )
