import asyncio
import time
from typing import Dict

from api.core.config import get_settings
from api.core.exceptions import ExternalServiceError
from api.core.logging import get_logger

from src.analysis.contract_analyzer import analyze_contract
from src.analysis.onchain_analyzer import analyze_wallet
from src.analysis.sentiment_analyzer import analyze_sentiment
from src.connectors.coingecko_api import coingecko

settings = get_settings()
logger = get_logger(__name__)


class AnalysisService:
    """Async wrapper around the existing analysis modules."""

    @staticmethod
    async def analyze_contract(
        contract_address: str, network: str = "eth"
    ) -> Dict:
        start = time.perf_counter()
        try:
            result = await asyncio.to_thread(
                analyze_contract, contract_address, network
            )
            elapsed_ms = int((time.perf_counter() - start) * 1000)
            result["processing_time_ms"] = elapsed_ms

            logger.info(
                "contract_analysis_completed",
                address=contract_address,
                network=network,
                risk_score=result.get("risk_score"),
                duration_ms=elapsed_ms,
            )
            return result
        except Exception as e:
            logger.error(
                "contract_analysis_failed",
                address=contract_address,
                error=str(e),
            )
            raise ExternalServiceError("ContractAnalyzer", str(e))

    @staticmethod
    async def analyze_wallet(
        wallet_address: str, network: str = "eth"
    ) -> Dict:
        start = time.perf_counter()
        try:
            result = await asyncio.to_thread(
                analyze_wallet, wallet_address, network
            )
            elapsed_ms = int((time.perf_counter() - start) * 1000)
            result["processing_time_ms"] = elapsed_ms

            logger.info(
                "wallet_analysis_completed",
                address=wallet_address,
                network=network,
                risk_score=result.get("risk_score"),
                duration_ms=elapsed_ms,
            )
            return result
        except Exception as e:
            logger.error(
                "wallet_analysis_failed",
                address=wallet_address,
                error=str(e),
            )
            raise ExternalServiceError("WalletAnalyzer", str(e))

    @staticmethod
    async def analyze_sentiment(asset: str) -> Dict:
        start = time.perf_counter()
        try:
            result_text = await asyncio.to_thread(analyze_sentiment, asset)
            elapsed_ms = int((time.perf_counter() - start) * 1000)

            logger.info(
                "sentiment_analysis_completed",
                asset=asset,
                duration_ms=elapsed_ms,
            )
            return {
                "analysis_text": result_text,
                "risk_score": 50,
                "risk_level": "MÉDIO",
                "risk_factors": [],
                "processing_time_ms": elapsed_ms,
            }
        except Exception as e:
            logger.error(
                "sentiment_analysis_failed",
                asset=asset,
                error=str(e),
            )
            raise ExternalServiceError("SentimentAnalyzer", str(e))

    @staticmethod
    async def get_coin_price(coin_id: str) -> Dict:
        try:
            result = await asyncio.to_thread(coingecko.get_coin_data, coin_id)
            if not result:
                return {"error": "Coin not found"}
            return result
        except Exception as e:
            raise ExternalServiceError("CoinGecko", str(e))

    @staticmethod
    async def get_trending_coins() -> list:
        try:
            return await asyncio.to_thread(coingecko.get_trending_coins)
        except Exception as e:
            raise ExternalServiceError("CoinGecko", str(e))


analysis_service = AnalysisService()
