import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_analysis_history_empty(auth_client: AsyncClient):
    response = await auth_client.get("/api/v1/analysis/history")
    assert response.status_code == 200
    data = response.json()
    assert data["items"] == []
    assert data["total"] == 0


@pytest.mark.asyncio
async def test_analysis_history_pagination(auth_client: AsyncClient):
    response = await auth_client.get(
        "/api/v1/analysis/history",
        params={"limit": 10, "offset": 0},
    )
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert "total" in data
    assert "limit" in data
    assert "offset" in data


@pytest.mark.asyncio
async def test_analysis_detail_not_found(auth_client: AsyncClient):
    response = await auth_client.get("/api/v1/analysis/99999")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_contract_analysis_invalid_address(auth_client: AsyncClient):
    response = await auth_client.post(
        "/api/v1/analysis/contract",
        json={"contract_address": "not-valid", "network": "eth"},
    )
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_wallet_analysis_invalid_address(auth_client: AsyncClient):
    response = await auth_client.post(
        "/api/v1/analysis/wallet",
        json={"wallet_address": "invalid", "network": "eth"},
    )
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_sentiment_analysis_empty_asset(auth_client: AsyncClient):
    response = await auth_client.post(
        "/api/v1/analysis/sentiment",
        json={"asset": ""},
    )
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_analysis_requires_auth(client: AsyncClient):
    response = await client.post(
        "/api/v1/analysis/contract",
        json={
            "contract_address": "0x1f9840a85d5aF5bf1D1762F925BDADdC4201F984",
            "network": "eth",
        },
    )
    assert response.status_code == 401
