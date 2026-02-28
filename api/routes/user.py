from fastapi import APIRouter, Depends

from api.core.deps import get_current_user
from api.core.exceptions import NotFoundError, ValidationError
from api.core.security import generate_api_key
from api.database import crud
from api.database.session import get_db
from api.schemas.auth import UserProfileResponse, UserResponse
from api.schemas.common import ApiKeyCreateRequest, ApiKeyResponse, CreditsPurchaseRequest, SuccessResponse
from api.services import payment_service

router = APIRouter()


@router.get("/me", response_model=UserProfileResponse)
async def get_profile(
    user: dict = Depends(get_current_user),
    db=Depends(get_db),
):
    """Get the authenticated user's profile."""
    total = await crud.count_user_analyses(db, user["id"])
    keys = await crud.get_user_api_keys(db, user["id"])

    return UserProfileResponse(
        user=UserResponse(**user),
        total_analyses=total,
        api_keys_count=len(keys),
    )


@router.get("/credits")
async def get_credits(
    user: dict = Depends(get_current_user),
    db=Depends(get_db),
):
    """Get current credit balance."""
    credits = await crud.get_user_credits(db, user["id"])
    return {"credits": credits, "plan": user["plan"]}


@router.post("/purchase", response_model=SuccessResponse)
async def purchase_plan(
    body: CreditsPurchaseRequest,
    user: dict = Depends(get_current_user),
    db=Depends(get_db),
):
    """Upgrade plan and add credits."""
    result = await payment_service.purchase_plan(db, user["id"], body.plan)
    if not result:
        raise ValidationError("Invalid plan. Choose 'basic' or 'pro'.")

    return SuccessResponse(
        message=f"Plan upgraded to {body.plan}. {result['credits_added']} credits added.",
        data=result,
    )


# ─── API Keys ────────────────────────────────────────────────────────────────

@router.get("/api-keys", response_model=list[ApiKeyResponse])
async def list_api_keys(
    user: dict = Depends(get_current_user),
    db=Depends(get_db),
):
    """List all API keys for the authenticated user."""
    keys = await crud.get_user_api_keys(db, user["id"])
    return [ApiKeyResponse(**k) for k in keys]


@router.post("/api-keys", response_model=ApiKeyResponse, status_code=201)
async def create_api_key(
    body: ApiKeyCreateRequest,
    user: dict = Depends(get_current_user),
    db=Depends(get_db),
):
    """Generate a new API key. The full key is only shown once."""
    raw_key = generate_api_key()
    key = await crud.create_api_key(db, user["id"], raw_key, body.name)

    return ApiKeyResponse(
        id=key.id,
        name=key.name,
        api_key=raw_key,  # Show full key only on creation
        is_active=key.is_active,
        requests_count=0,
        last_used=None,
        created_at=key.created_at.isoformat(),
    )


@router.delete("/api-keys/{key_id}", response_model=SuccessResponse)
async def revoke_api_key(
    key_id: int,
    user: dict = Depends(get_current_user),
    db=Depends(get_db),
):
    """Revoke an API key."""
    success = await crud.revoke_api_key(db, key_id, user["id"])
    if not success:
        raise NotFoundError("API Key")

    return SuccessResponse(message="API key revoked successfully")
