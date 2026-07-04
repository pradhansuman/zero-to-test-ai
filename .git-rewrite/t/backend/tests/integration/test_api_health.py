"""Integration tests for health check endpoints."""
import pytest
from fastapi.testclient import TestClient


@pytest.mark.asyncio
async def test_health_check(test_client: TestClient):
    """Test basic health check."""
    response = test_client.get("/health")

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "service" in data


@pytest.mark.asyncio
async def test_readiness_check(test_client: TestClient):
    """Test readiness check with database."""
    response = test_client.get("/health/ready")

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ready"


@pytest.mark.asyncio
async def test_liveness_check(test_client: TestClient):
    """Test liveness check."""
    response = test_client.get("/health/live")

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "alive"


@pytest.mark.asyncio
async def test_database_health(test_client: TestClient):
    """Test database health check."""
    response = test_client.get("/health/db")

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["database"] == "connected"
