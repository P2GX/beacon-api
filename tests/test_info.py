"""Tests for info endpoint."""

import pytest
from fastapi.testclient import TestClient

from fast_beacon.main import create_app


@pytest.fixture
def client() -> TestClient:
    """Create test client."""
    app = create_app()
    return TestClient(app)


def test_get_beacon_info(client: TestClient) -> None:
    """Test getting beacon info."""
    response = client.get("/api/info")
    assert response.status_code == 200

    data = response.json()
    assert "meta" in data
    assert "response" in data

    # Check meta structure
    meta = data["meta"]
    assert "beacon_id" in meta
    assert "api_version" in meta

    # Check response structure
    response_data = data["response"]
    assert "id" in response_data
    assert "name" in response_data
    assert "api_version" in response_data
    assert "environment" in response_data
    assert "organization" in response_data

    # Check organization structure
    org = response_data["organization"]
    assert "id" in org
    assert "name" in org
