from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class NetworkEnum(str, Enum):
    eth = "eth"
    bsc = "bsc"


class AnalysisTypeEnum(str, Enum):
    contract = "contract_analysis"
    wallet = "wallet_analysis"
    sentiment = "sentiment_analysis"


class RiskLevelEnum(str, Enum):
    BAIXO = "BAIXO"
    MEDIO = "MÉDIO"
    ALTO = "ALTO"
    CRITICO = "CRÍTICO"


# ─── Requests ────────────────────────────────────────────────────────────────

class ContractAnalysisRequest(BaseModel):
    contract_address: str = Field(
        ...,
        pattern=r"^0x[0-9a-fA-F]{40}$",
        description="Ethereum/BSC contract address",
        examples=["0x1f9840a85d5aF5bf1D1762F925BDADdC4201F984"],
    )
    network: NetworkEnum = NetworkEnum.eth


class WalletAnalysisRequest(BaseModel):
    wallet_address: str = Field(
        ...,
        pattern=r"^0x[0-9a-fA-F]{40}$",
        description="Ethereum/BSC wallet address",
        examples=["0xde0b295669a9fd93d5f28d9ec85e40f4cb697bae"],
    )
    network: NetworkEnum = NetworkEnum.eth


class SentimentAnalysisRequest(BaseModel):
    asset: str = Field(
        ...,
        min_length=1,
        max_length=20,
        description="Crypto asset ticker symbol",
        examples=["BTC", "ETH", "SOL"],
    )


# ─── Responses ───────────────────────────────────────────────────────────────

class AnalysisResult(BaseModel):
    id: int
    analysis_type: str
    target_address: str
    network: str | None = None
    result: str
    risk_score: int | None
    risk_level: str | None
    risk_factors: list[str] = []
    processing_time_ms: int | None
    status: str
    created_at: str | None


class AnalysisListResponse(BaseModel):
    items: list[AnalysisResult]
    total: int
    limit: int
    offset: int


class AnalysisHistoryParams(BaseModel):
    limit: int = Field(50, ge=1, le=100)
    offset: int = Field(0, ge=0)
    analysis_type: Optional[AnalysisTypeEnum] = None
    risk_level: Optional[RiskLevelEnum] = None
