from fastapi import APIRouter, Depends

from api.core.config import get_settings
from api.core.exceptions import UnauthorizedError, ValidationError
from api.core.security import create_access_token, create_refresh_token, decode_token
from api.database import crud
from api.database.session import get_db
from api.schemas.auth import (
    LoginRequest,
    RefreshTokenRequest,
    RegisterRequest,
    TokenResponse,
    UserResponse,
)

router = APIRouter()
settings = get_settings()


@router.post("/register", response_model=UserResponse, status_code=201)
async def register(body: RegisterRequest, db=Depends(get_db)):
    user = await crud.create_user(db, body.email, body.password, body.full_name)
    if not user:
        raise ValidationError("Email already registered")

    return UserResponse(
        id=user.id,
        email=user.email,
        full_name=user.full_name or "",
        plan=user.plan,
        credits=user.credits,
        is_active=user.is_active,
        created_at=user.created_at.isoformat() if user.created_at else None,
        last_login=None,
    )


@router.post("/login", response_model=TokenResponse)
async def login(body: LoginRequest, db=Depends(get_db)):
    user = await crud.authenticate_user(db, body.email, body.password)
    if not user:
        raise UnauthorizedError("Invalid email or password")

    access_token = create_access_token(data={"sub": str(user.id)})
    refresh_token = create_refresh_token(data={"sub": str(user.id)})

    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        expires_in=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    )


@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(body: RefreshTokenRequest, db=Depends(get_db)):
    payload = decode_token(body.refresh_token)
    if not payload or payload.get("type") != "refresh":
        raise UnauthorizedError("Invalid refresh token")

    user_id = payload.get("sub")
    user = await crud.get_user_by_id(db, int(user_id))
    if not user:
        raise UnauthorizedError("User not found")

    access_token = create_access_token(data={"sub": str(user_id)})
    refresh_token = create_refresh_token(data={"sub": str(user_id)})

    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        expires_in=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    )
