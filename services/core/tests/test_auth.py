"""
Tests for the Authentication flow — registration, login, JWT validation.
"""
import pytest
from httpx import AsyncClient, ASGITransport
from services.core.main import app


@pytest.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


@pytest.mark.skip(reason="Requires valid GCP/Firebase credentials in CI")
class TestAuthEndpoints:
    """Test the /api/v1/auth endpoints."""

    @pytest.mark.asyncio
    async def test_register_new_user(self, client):
        response = await client.post(
            "/api/v1/auth/register",
            json={"email": "newuser@guild.ai", "password": "strongpass123"},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["email"] == "newuser@guild.ai"
        assert data["tier"] == "free"
        assert data["is_active"] is True
        assert "id" in data

    @pytest.mark.asyncio
    async def test_register_duplicate_user(self, client):
        # Register once
        await client.post(
            "/api/v1/auth/register",
            json={"email": "dup@guild.ai", "password": "pass123"},
        )
        # Register again → 400
        response = await client.post(
            "/api/v1/auth/register",
            json={"email": "dup@guild.ai", "password": "pass123"},
        )
        assert response.status_code == 400

    @pytest.mark.asyncio
    async def test_login_valid_credentials(self, client):
        # Register first
        await client.post(
            "/api/v1/auth/register",
            json={"email": "login@guild.ai", "password": "pass123"},
        )
        # Login
        response = await client.post(
            "/api/v1/auth/login",
            data={"username": "login@guild.ai", "password": "pass123"},
        )
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"

    @pytest.mark.asyncio
    async def test_login_invalid_password(self, client):
        await client.post(
            "/api/v1/auth/register",
            json={"email": "badlogin@guild.ai", "password": "pass123"},
        )
        response = await client.post(
            "/api/v1/auth/login",
            data={"username": "badlogin@guild.ai", "password": "wrongpass"},
        )
        assert response.status_code == 401

    @pytest.mark.asyncio
    async def test_protected_endpoint_without_token(self, client):
        response = await client.get("/api/v1/dashboard/snapshot")
        assert response.status_code in [401, 403]

    @pytest.mark.asyncio
    async def test_protected_endpoint_with_token(self, client):
        # Register + login
        await client.post(
            "/api/v1/auth/register",
            json={"email": "authuser@guild.ai", "password": "pass123"},
        )
        login_response = await client.post(
            "/api/v1/auth/login",
            data={"username": "authuser@guild.ai", "password": "pass123"},
        )
        token = login_response.json()["access_token"]

        # Access protected endpoint
        response = await client.get(
            "/api/v1/dashboard/snapshot",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 200
        data = response.json()
        assert "projects_count" in data
        assert "tokens_used_this_month" in data

    @pytest.mark.asyncio
    async def test_health_check(self, client):
        response = await client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "ok"
