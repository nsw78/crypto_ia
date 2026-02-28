from fastapi import APIRouter, Depends, Query
from typing import Optional

from api.core.deps import get_current_user, require_credits
from api.core.exceptions import InsufficientCreditsError, NotFoundError
from api.database import crud
from api.database.session import get_db
from api.schemas.analysis import (
    AnalysisListResponse,
    AnalysisResult,
    AnalysisTypeEnum,
    ContractAnalysisRequest,
    RiskLevelEnum,
    SentimentAnalysisRequest,
    WalletAnalysisRequest,
)
from api.services.analysis_service import analysis_service

router = APIRouter()


@router.post("/contract", response_model=AnalysisResult, status_code=201)
async def analyze_contract(
    body: ContractAnalysisRequest,
    user: dict = Depends(require_credits),
    db=Depends(get_db),
):
    """Analyze a smart contract for vulnerabilities, rug pull patterns, and risk scoring."""
    if not await crud.use_credit(db, user["id"]):
        raise InsufficientCreditsError()

    try:
        result = await analysis_service.analyze_contract(
            body.contract_address, body.network.value
        )

        analysis = await crud.save_analysis(
            db,
            user_id=user["id"],
            analysis_type="contract_analysis",
            target_address=body.contract_address,
            result=result["analysis_text"],
            risk_score=result["risk_score"],
            risk_level=result["risk_level"],
            risk_factors=result.get("risk_factors", []),
            network=body.network.value,
            processing_time_ms=result.get("processing_time_ms"),
        )

        return AnalysisResult(
            id=analysis.id,
            analysis_type=analysis.analysis_type,
            target_address=analysis.target_address,
            network=analysis.network,
            result=analysis.result,
            risk_score=analysis.risk_score,
            risk_level=analysis.risk_level,
            risk_factors=result.get("risk_factors", []),
            processing_time_ms=analysis.processing_time_ms,
            status=analysis.status,
            created_at=analysis.created_at.isoformat() if analysis.created_at else None,
        )
    except InsufficientCreditsError:
        raise
    except Exception as e:
        # Refund credit on failure
        await crud.add_credits(db, user["id"], 1)
        raise


@router.post("/wallet", response_model=AnalysisResult, status_code=201)
async def analyze_wallet(
    body: WalletAnalysisRequest,
    user: dict = Depends(require_credits),
    db=Depends(get_db),
):
    """Analyze a wallet's on-chain behavior for suspicious patterns."""
    if not await crud.use_credit(db, user["id"]):
        raise InsufficientCreditsError()

    try:
        result = await analysis_service.analyze_wallet(
            body.wallet_address, body.network.value
        )

        analysis = await crud.save_analysis(
            db,
            user_id=user["id"],
            analysis_type="wallet_analysis",
            target_address=body.wallet_address,
            result=result["analysis_text"],
            risk_score=result["risk_score"],
            risk_level=result["risk_level"],
            risk_factors=result.get("risk_factors", []),
            network=body.network.value,
            processing_time_ms=result.get("processing_time_ms"),
        )

        return AnalysisResult(
            id=analysis.id,
            analysis_type=analysis.analysis_type,
            target_address=analysis.target_address,
            network=analysis.network,
            result=analysis.result,
            risk_score=analysis.risk_score,
            risk_level=analysis.risk_level,
            risk_factors=result.get("risk_factors", []),
            processing_time_ms=analysis.processing_time_ms,
            status=analysis.status,
            created_at=analysis.created_at.isoformat() if analysis.created_at else None,
        )
    except InsufficientCreditsError:
        raise
    except Exception as e:
        await crud.add_credits(db, user["id"], 1)
        raise


@router.post("/sentiment", response_model=AnalysisResult, status_code=201)
async def analyze_sentiment(
    body: SentimentAnalysisRequest,
    user: dict = Depends(require_credits),
    db=Depends(get_db),
):
    """Analyze market sentiment for a crypto asset using news and AI."""
    if not await crud.use_credit(db, user["id"]):
        raise InsufficientCreditsError()

    try:
        result = await analysis_service.analyze_sentiment(body.asset.upper())

        analysis = await crud.save_analysis(
            db,
            user_id=user["id"],
            analysis_type="sentiment_analysis",
            target_address=body.asset.upper(),
            result=result["analysis_text"],
            risk_score=result["risk_score"],
            risk_level=result["risk_level"],
            risk_factors=result.get("risk_factors", []),
            processing_time_ms=result.get("processing_time_ms"),
        )

        return AnalysisResult(
            id=analysis.id,
            analysis_type=analysis.analysis_type,
            target_address=analysis.target_address,
            network=analysis.network,
            result=analysis.result,
            risk_score=analysis.risk_score,
            risk_level=analysis.risk_level,
            risk_factors=result.get("risk_factors", []),
            processing_time_ms=analysis.processing_time_ms,
            status=analysis.status,
            created_at=analysis.created_at.isoformat() if analysis.created_at else None,
        )
    except InsufficientCreditsError:
        raise
    except Exception as e:
        await crud.add_credits(db, user["id"], 1)
        raise


@router.get("/history", response_model=AnalysisListResponse)
async def get_analysis_history(
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    analysis_type: Optional[AnalysisTypeEnum] = None,
    risk_level: Optional[RiskLevelEnum] = None,
    user: dict = Depends(get_current_user),
    db=Depends(get_db),
):
    """Get the authenticated user's analysis history with filters and pagination."""
    analyses = await crud.get_user_analyses(
        db,
        user_id=user["id"],
        limit=limit,
        offset=offset,
        analysis_type=analysis_type.value if analysis_type else None,
        risk_level=risk_level.value if risk_level else None,
    )
    total = await crud.count_user_analyses(db, user["id"])

    items = [AnalysisResult(**a) for a in analyses]

    return AnalysisListResponse(
        items=items,
        total=total,
        limit=limit,
        offset=offset,
    )


@router.get("/{analysis_id}", response_model=AnalysisResult)
async def get_analysis_detail(
    analysis_id: int,
    user: dict = Depends(get_current_user),
    db=Depends(get_db),
):
    """Get a specific analysis by ID."""
    analysis = await crud.get_analysis_by_id(db, analysis_id, user["id"])
    if not analysis:
        raise NotFoundError("Analysis")

    return AnalysisResult(**analysis)
