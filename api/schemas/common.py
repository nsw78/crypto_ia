from typing import Any, Optional

from pydantic import BaseModel


class HealthResponse(BaseModel):
    status: str = "healthy"
    version: str
    environment: str
    uptime_seconds: float


class ErrorResponse(BaseModel):
    error_code: str
    message: str
    details: Optional[Any] = None


class SuccessResponse(BaseModel):
    message: str
    data: Optional[Any] = None


class PaginatedResponse(BaseModel):
    items: list
    total: int
    limit: int
    offset: int
    has_more: bool


class ApiKeyCreateRequest(BaseModel):
    name: str = "default"


class ApiKeyResponse(BaseModel):
    id: int
    name: str
    api_key: str
    is_active: bool
    requests_count: int
    last_used: str | None
    created_at: str


class CreditsPurchaseRequest(BaseModel):
    plan: str
