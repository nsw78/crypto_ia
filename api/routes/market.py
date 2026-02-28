from fastapi import APIRouter, Depends

from api.core.deps import get_current_user
from api.services.analysis_service import analysis_service

router = APIRouter()


@router.get("/price/{coin_id}")
async def get_coin_price(
    coin_id: str,
    _user: dict = Depends(get_current_user),
):
    """Get current price and market data for a cryptocurrency."""
    data = await analysis_service.get_coin_price(coin_id)
    return {"data": data}


@router.get("/trending")
async def get_trending_coins(
    _user: dict = Depends(get_current_user),
):
    """Get currently trending cryptocurrencies."""
    coins = await analysis_service.get_trending_coins()
    return {"data": coins}
