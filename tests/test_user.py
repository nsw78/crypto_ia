import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_get_profile(auth_client: AsyncClient):
    response = await auth_client.get("/api/v1/user/me")
    assert response.status_code == 200
    data = response.json()
    assert data["user"]["email"] == "test@example.com"
    assert data["user"]["plan"] == "free"
    assert data["user"]["credits"] == 3


@pytest.mark.asyncio
async def test_get_credits(auth_client: AsyncClient):
    response = await auth_client.get("/api/v1/user/credits")
    assert response.status_code == 200
    data = response.json()
    assert data["credits"] == 3
    assert data["plan"] == "free"


@pytest.mark.asyncio
async def test_create_api_key(auth_client: AsyncClient):
    response = await auth_client.post(
        "/api/v1/user/api-keys",
        json={"name": "my-key"},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "my-key"
    assert data["api_key"].startswith("cia_")
    assert data["is_active"] is True


@pytest.mark.asyncio
async def test_list_api_keys(auth_client: AsyncClient):
    await auth_client.post("/api/v1/user/api-keys", json={"name": "key-1"})
    await auth_client.post("/api/v1/user/api-keys", json={"name": "key-2"})

    response = await auth_client.get("/api/v1/user/api-keys")
    assert response.status_code == 200
    keys = response.json()
    assert len(keys) >= 2


@pytest.mark.asyncio
async def test_purchase_plan(auth_client: AsyncClient):
    response = await auth_client.post(
        "/api/v1/user/purchase",
        json={"plan": "basic"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "20 credits added" in data["message"]


@pytest.mark.asyncio
async def test_purchase_invalid_plan(auth_client: AsyncClient):
    response = await auth_client.post(
        "/api/v1/user/purchase",
        json={"plan": "super_duper"},
    )
    assert response.status_code == 422
