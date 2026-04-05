"""
Tests for project CRUD and API endpoints.
"""
import pytest
from httpx import AsyncClient, ASGITransport
from services.core.main import app


@pytest.fixture
async def authed_client():
    """Register, login, and return an authenticated client."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        await ac.post(
            "/api/v1/auth/register",
            json={"email": "projuser@guild.ai", "password": "pass123"},
        )
        login = await ac.post(
            "/api/v1/auth/login",
            data={"username": "projuser@guild.ai", "password": "pass123"},
        )
        token = login.json()["access_token"]
        ac.headers["Authorization"] = f"Bearer {token}"
        yield ac


@pytest.mark.skip(reason="Requires valid GCP/Firebase credentials in CI")
class TestProjectEndpoints:
    @pytest.mark.asyncio
    async def test_create_project(self, authed_client):
        response = await authed_client.post(
            "/api/v1/projects",
            json={"goal": "Launch MVP"},
        )
        assert response.status_code == 200
        data = response.json()
        assert data["goal"] == "Launch MVP"
        assert data["status"] == "pending"

    @pytest.mark.asyncio
    async def test_list_projects(self, authed_client):
        await authed_client.post("/api/v1/projects", json={"goal": "Goal A"})
        await authed_client.post("/api/v1/projects", json={"goal": "Goal B"})

        response = await authed_client.get("/api/v1/projects")
        assert response.status_code == 200
        data = response.json()
        assert len(data["projects"]) >= 2

    @pytest.mark.asyncio
    async def test_list_agents(self, authed_client):
        response = await authed_client.get("/api/v1/agents")
        assert response.status_code == 200
        assert "agents" in response.json()
