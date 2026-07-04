"""Integration tests for projects API."""
import pytest
from fastapi.testclient import TestClient


@pytest.mark.asyncio
async def test_create_project(test_client: TestClient, auth_headers: dict):
    """Test creating a project."""
    response = test_client.post(
        "/api/projects",
        json={
            "name": "Test Project",
            "description": "A test project",
            "test_framework": "pytest"
        },
        headers=auth_headers
    )

    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Project"


@pytest.mark.asyncio
async def test_create_project_unauthorized(test_client: TestClient):
    """Test creating project without auth."""
    response = test_client.post(
        "/api/projects",
        json={
            "name": "Test Project",
            "description": "A test project"
        }
    )

    assert response.status_code == 403


@pytest.mark.asyncio
async def test_list_projects(test_client: TestClient, auth_headers: dict):
    """Test listing projects."""
    # Create a project first
    test_client.post(
        "/api/projects",
        json={
            "name": "Project 1",
            "description": "First project"
        },
        headers=auth_headers
    )

    response = test_client.get("/api/projects", headers=auth_headers)

    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1


@pytest.mark.asyncio
async def test_get_project(test_client: TestClient, auth_headers: dict):
    """Test getting a project by ID."""
    # Create project
    create_response = test_client.post(
        "/api/projects",
        json={
            "name": "Test Project",
            "description": "A test project"
        },
        headers=auth_headers
    )
    project_id = create_response.json()["id"]

    # Get project
    response = test_client.get(f"/api/projects/{project_id}", headers=auth_headers)

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == project_id


@pytest.mark.asyncio
async def test_update_project(test_client: TestClient, auth_headers: dict):
    """Test updating a project."""
    # Create project
    create_response = test_client.post(
        "/api/projects",
        json={
            "name": "Original Name",
            "description": "Original description"
        },
        headers=auth_headers
    )
    project_id = create_response.json()["id"]

    # Update project
    response = test_client.put(
        f"/api/projects/{project_id}",
        json={
            "name": "Updated Name",
            "description": "Updated description"
        },
        headers=auth_headers
    )

    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Updated Name"


@pytest.mark.asyncio
async def test_delete_project(test_client: TestClient, auth_headers: dict):
    """Test deleting a project."""
    # Create project
    create_response = test_client.post(
        "/api/projects",
        json={
            "name": "Project to Delete",
            "description": "Will be deleted"
        },
        headers=auth_headers
    )
    project_id = create_response.json()["id"]

    # Delete project
    response = test_client.delete(f"/api/projects/{project_id}", headers=auth_headers)

    assert response.status_code == 204

    # Verify deleted (soft delete - returns inactive)
    get_response = test_client.get(f"/api/projects/{project_id}", headers=auth_headers)
    assert get_response.status_code == 404 or get_response.json()["is_active"] is False
