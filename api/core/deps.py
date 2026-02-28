from typing import Optional

from fastapi import Depends, Header, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from api.core.config import get_settings
from api.core.exceptions import ForbiddenError, InsufficientCreditsError, UnauthorizedError
from api.core.security import decode_token
from api.database.session import get_db
from api.database import crud

settings = get_settings()
security_scheme = HTTPBearer(auto_error=False)


async def get_current_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Security(security_scheme),
    x_api_key: Optional[str] = Header(None),
    db=Depends(get_db),
) -> dict:
    # Try API key auth first
    if x_api_key:
        user = await crud.get_user_by_api_key(db, x_api_key)
        if user:
            await crud.increment_api_key_usage(db, x_api_key)
            return user
        raise UnauthorizedError("Invalid API key")

    # Then try JWT
    if not credentials:
        raise UnauthorizedError("Missing authentication token")

    payload = decode_token(credentials.credentials)
    if not payload:
        raise UnauthorizedError("Invalid or expired token")

    if payload.get("type") != "access":
        raise UnauthorizedError("Invalid token type")

    user_id = payload.get("sub")
    if not user_id:
        raise UnauthorizedError("Invalid token payload")

    user = await crud.get_user_by_id(db, int(user_id))
    if not user:
        raise UnauthorizedError("User not found")

    return user


async def require_credits(
    user: dict = Depends(get_current_user),
    db=Depends(get_db),
) -> dict:
    credits = await crud.get_user_credits(db, user["id"])
    if credits <= 0:
        raise InsufficientCreditsError()
    return user


async def require_plan(
    allowed_plans: list[str],
):
    async def _check(user: dict = Depends(get_current_user)):
        if user["plan"] not in allowed_plans:
            raise ForbiddenError(
                f"This feature requires one of these plans: {', '.join(allowed_plans)}"
            )
        return user

    return _check
