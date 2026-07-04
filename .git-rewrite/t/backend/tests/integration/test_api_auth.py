"""Integration tests for authentication API."""
import pytest
from fastapi.testclient import TestClient


@pytest.mark.asyncio
async def test_register_user(test_client: TestClient):
    """Test user registration."""
    response = test_client.post(
        "/api/auth/register",
        json={
            "email": "newuser@example.com",
            "username": "newuser",
            "password": "SecurePass123!"
        }
    )

    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data


@pytest.mark.asyncio
async def test_register_duplicate_email(test_client: TestClient):
    """Test registration with duplicate email."""
    # Register first user
    test_client.post(
        "/api/auth/register",
        json={
            "email": "user@example.com",
            "username": "user1",
            "password": "Pass123!"
        }
    )

    # Try to register with same email
    response = test_client.post(
        "/api/auth/register",
        json={
            "email": "user@example.com",
            "username": "user2",
            "password": "Pass123!"
        }
    )

    assert response.status_code == 400


@pytest.mark.asyncio
async def test_login_success(test_client: TestClient):
    """Test successful login."""
    # Register user
    test_client.post(
        "/api/auth/register",
        json={
            "email": "user@example.com",
            "username": "user",
            "password": "TestPass123!"
        }
    )

    # Login
    response = test_client.post(
        "/api/auth/login",
        json={
            "email": "user@example.com",
            "password": "TestPass123!"
        }
    )

    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data


@pytest.mark.asyncio
async def test_login_invalid_credentials(test_client: TestClient):
    """Test login with invalid credentials."""
    response = test_client.post(
        "/api/auth/login",
        json={
            "email": "nonexistent@example.com",
            "password": "WrongPass123!"
        }
    )

    assert response.status_code in [400, 401, 500]


@pytest.mark.asyncio
async def test_refresh_token(test_client: TestClient, auth_headers: dict):
    """Test token refresh."""
    response = test_client.post(
        "/api/auth/refresh",
        headers=auth_headers
    )

    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
