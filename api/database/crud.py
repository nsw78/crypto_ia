import json
from datetime import datetime, timezone
from typing import Optional

from sqlalchemy import select, update, func
from sqlalchemy.ext.asyncio import AsyncSession

from api.core.security import hash_password, verify_password
from api.database.models import Analysis, ApiKey, Transaction, User


# ─── Users ────────────────────────────────────────────────────────────────────

async def create_user(
    db: AsyncSession, email: str, password: str, full_name: str = ""
) -> Optional[User]:
    existing = await db.execute(select(User).where(User.email == email))
    if existing.scalar_one_or_none():
        return None

    user = User(
        email=email,
        password_hash=hash_password(password),
        full_name=full_name,
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


async def authenticate_user(
    db: AsyncSession, email: str, password: str
) -> Optional[User]:
    result = await db.execute(select(User).where(User.email == email))
    user = result.scalar_one_or_none()

    if not user or not verify_password(password, user.password_hash):
        return None

    user.last_login = datetime.now(timezone.utc)
    await db.commit()
    return user


async def get_user_by_id(db: AsyncSession, user_id: int) -> Optional[dict]:
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        return None
    return _user_to_dict(user)


async def get_user_by_email(db: AsyncSession, email: str) -> Optional[User]:
    result = await db.execute(select(User).where(User.email == email))
    return result.scalar_one_or_none()


async def get_user_credits(db: AsyncSession, user_id: int) -> int:
    result = await db.execute(select(User.credits).where(User.id == user_id))
    row = result.scalar_one_or_none()
    return row or 0


async def use_credit(db: AsyncSession, user_id: int) -> bool:
    result = await db.execute(
        select(User.credits).where(User.id == user_id)
    )
    credits = result.scalar_one_or_none()
    if not credits or credits <= 0:
        return False

    await db.execute(
        update(User).where(User.id == user_id).values(credits=User.credits - 1)
    )
    await db.commit()
    return True


async def add_credits(db: AsyncSession, user_id: int, amount: int) -> None:
    await db.execute(
        update(User).where(User.id == user_id).values(credits=User.credits + amount)
    )
    await db.commit()


async def upgrade_plan(
    db: AsyncSession, user_id: int, plan: str, credits: int
) -> None:
    await db.execute(
        update(User)
        .where(User.id == user_id)
        .values(plan=plan, credits=User.credits + credits)
    )
    await db.commit()


# ─── Analyses ─────────────────────────────────────────────────────────────────

async def save_analysis(
    db: AsyncSession,
    user_id: int,
    analysis_type: str,
    target_address: str,
    result: str,
    risk_score: int,
    risk_level: str,
    risk_factors: list = None,
    network: str = "eth",
    processing_time_ms: int = None,
) -> Analysis:
    analysis = Analysis(
        user_id=user_id,
        analysis_type=analysis_type,
        target_address=target_address,
        network=network,
        result=result,
        risk_score=risk_score,
        risk_level=risk_level,
        risk_factors=json.dumps(risk_factors or []),
        processing_time_ms=processing_time_ms,
    )
    db.add(analysis)
    await db.commit()
    await db.refresh(analysis)
    return analysis


async def get_user_analyses(
    db: AsyncSession,
    user_id: int,
    limit: int = 50,
    offset: int = 0,
    analysis_type: str = None,
    risk_level: str = None,
) -> list[dict]:
    query = select(Analysis).where(Analysis.user_id == user_id)

    if analysis_type:
        query = query.where(Analysis.analysis_type == analysis_type)
    if risk_level:
        query = query.where(Analysis.risk_level == risk_level)

    query = query.order_by(Analysis.created_at.desc()).offset(offset).limit(limit)
    result = await db.execute(query)
    analyses = result.scalars().all()

    return [_analysis_to_dict(a) for a in analyses]


async def get_analysis_by_id(
    db: AsyncSession, analysis_id: int, user_id: int
) -> Optional[dict]:
    result = await db.execute(
        select(Analysis).where(
            Analysis.id == analysis_id, Analysis.user_id == user_id
        )
    )
    analysis = result.scalar_one_or_none()
    if not analysis:
        return None
    return _analysis_to_dict(analysis)


async def count_user_analyses(db: AsyncSession, user_id: int) -> int:
    result = await db.execute(
        select(func.count(Analysis.id)).where(Analysis.user_id == user_id)
    )
    return result.scalar() or 0


# ─── API Keys ────────────────────────────────────────────────────────────────

async def create_api_key(
    db: AsyncSession, user_id: int, api_key: str, name: str = "default"
) -> ApiKey:
    key = ApiKey(user_id=user_id, api_key=api_key, name=name)
    db.add(key)
    await db.commit()
    await db.refresh(key)
    return key


async def get_user_by_api_key(db: AsyncSession, api_key: str) -> Optional[dict]:
    result = await db.execute(
        select(ApiKey)
        .where(ApiKey.api_key == api_key, ApiKey.is_active == True)
    )
    key = result.scalar_one_or_none()
    if not key:
        return None

    user_result = await db.execute(select(User).where(User.id == key.user_id))
    user = user_result.scalar_one_or_none()
    if not user:
        return None
    return _user_to_dict(user)


async def get_user_api_keys(db: AsyncSession, user_id: int) -> list[dict]:
    result = await db.execute(
        select(ApiKey).where(ApiKey.user_id == user_id).order_by(ApiKey.created_at.desc())
    )
    keys = result.scalars().all()
    return [
        {
            "id": k.id,
            "name": k.name,
            "api_key": k.api_key[:12] + "..." + k.api_key[-4:],
            "is_active": k.is_active,
            "requests_count": k.requests_count,
            "last_used": k.last_used.isoformat() if k.last_used else None,
            "created_at": k.created_at.isoformat(),
        }
        for k in keys
    ]


async def increment_api_key_usage(db: AsyncSession, api_key: str) -> None:
    await db.execute(
        update(ApiKey)
        .where(ApiKey.api_key == api_key)
        .values(
            requests_count=ApiKey.requests_count + 1,
            last_used=datetime.now(timezone.utc),
        )
    )
    await db.commit()


async def revoke_api_key(db: AsyncSession, key_id: int, user_id: int) -> bool:
    result = await db.execute(
        select(ApiKey).where(ApiKey.id == key_id, ApiKey.user_id == user_id)
    )
    key = result.scalar_one_or_none()
    if not key:
        return False
    key.is_active = False
    await db.commit()
    return True


# ─── Transactions ────────────────────────────────────────────────────────────

async def record_transaction(
    db: AsyncSession,
    user_id: int,
    amount: float,
    plan: str,
    credits_added: int,
    stripe_payment_id: str = None,
) -> Transaction:
    tx = Transaction(
        user_id=user_id,
        amount=amount,
        plan=plan,
        credits_added=credits_added,
        stripe_payment_id=stripe_payment_id,
    )
    db.add(tx)
    await db.commit()
    await db.refresh(tx)
    return tx


# ─── Helpers ─────────────────────────────────────────────────────────────────

def _user_to_dict(user: User) -> dict:
    return {
        "id": user.id,
        "email": user.email,
        "full_name": user.full_name,
        "plan": user.plan,
        "credits": user.credits,
        "is_active": user.is_active,
        "created_at": user.created_at.isoformat() if user.created_at else None,
        "last_login": user.last_login.isoformat() if user.last_login else None,
    }


def _analysis_to_dict(analysis: Analysis) -> dict:
    risk_factors = []
    if analysis.risk_factors:
        try:
            risk_factors = json.loads(analysis.risk_factors)
        except (json.JSONDecodeError, TypeError):
            risk_factors = []

    return {
        "id": analysis.id,
        "analysis_type": analysis.analysis_type,
        "target_address": analysis.target_address,
        "network": analysis.network,
        "result": analysis.result,
        "risk_score": analysis.risk_score,
        "risk_level": analysis.risk_level,
        "risk_factors": risk_factors,
        "processing_time_ms": analysis.processing_time_ms,
        "status": analysis.status,
        "created_at": analysis.created_at.isoformat() if analysis.created_at else None,
    }
