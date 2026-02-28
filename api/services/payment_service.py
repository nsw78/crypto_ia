from typing import Dict, Optional

from sqlalchemy.ext.asyncio import AsyncSession

from api.core.config import get_settings
from api.core.logging import get_logger
from api.database import crud

from src.payment.stripe_integration import stripe_handler

settings = get_settings()
logger = get_logger(__name__)

PLANS = {
    "basic": {"price": 49.00, "credits": 20},
    "pro": {"price": 199.00, "credits": 100},
}


async def purchase_plan(
    db: AsyncSession, user_id: int, plan: str
) -> Optional[Dict]:
    if plan not in PLANS:
        return None

    plan_info = PLANS[plan]

    await crud.upgrade_plan(db, user_id, plan, plan_info["credits"])
    await crud.record_transaction(
        db,
        user_id=user_id,
        amount=plan_info["price"],
        plan=plan,
        credits_added=plan_info["credits"],
    )

    logger.info(
        "plan_purchased",
        user_id=user_id,
        plan=plan,
        credits=plan_info["credits"],
    )

    return {
        "plan": plan,
        "credits_added": plan_info["credits"],
        "amount": plan_info["price"],
    }
