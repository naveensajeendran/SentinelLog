"""
Integration tests for FastAPI endpoints.
"""
import pytest
from fastapi.testclient import TestClient
from sentinellog.api.main import app


@pytest.fixture
def client():
    """Fixture to provide test client."""
    return TestClient(app)


class TestHealthEndpoints:
    """Test health and metadata endpoints."""
    
    def test_health_check(self, client):
        """Test /health endpoint returns 200."""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["service"] == "sentinellog"
        assert data["version"] == "1.0.0"
    
    def test_root_endpoint(self, client):
        """Test root / endpoint provides API metadata."""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert data["service"] == "SentinelLog API"
        assert "endpoints" in data
        assert "docs" in data["endpoints"]
    
    def test_api_info_endpoint(self, client):
        """Test /api/v1/info endpoint."""
        response = client.get("/api/v1/info")
        assert response.status_code == 200
        data = response.json()
        assert data["service_name"] == "SentinelLog"
        assert "capabilities" in data
        assert "endpoints" in data


class TestScanEndpoints:
    """Test threat scanning endpoints."""
    
    def test_scan_with_content(self, client):
        """Test POST /api/v1/scan with inline content."""
        payload = {
            "content": "ERROR Failed login attempt from 192.168.1.100"
        }
        response = client.post("/api/v1/scan", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert "count" in data
        assert "data" in data
        assert isinstance(data["data"], list)
    
    def test_scan_without_content_or_filepath(self, client):
        """Test POST /api/v1/scan without required fields returns 400."""
        payload = {}
        response = client.post("/api/v1/scan", json=payload)
        assert response.status_code == 400
        assert "detail" in response.json()
    
    def test_scan_with_empty_content(self, client):
        """Test POST /api/v1/scan with empty content."""
        payload = {"content": ""}
        response = client.post("/api/v1/scan", json=payload)
        assert response.status_code == 400


class TestRulesEndpoints:
    """Test rule management endpoints."""
    
    def test_list_rules(self, client):
        """Test GET /api/v1/rules/list returns rules."""
        response = client.get("/api/v1/rules/list")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert "rules" in data
        assert "count" in data
    
    def test_reload_rules(self, client):
        """Test POST /api/v1/rules/reload reloads rules."""
        response = client.post("/api/v1/rules/reload")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert "message" in data


class TestOpenAPISchema:
    """Test OpenAPI schema generation."""
    
    def test_openapi_schema_available(self, client):
        """Test /openapi.json returns valid schema."""
        response = client.get("/openapi.json")
        assert response.status_code == 200
        schema = response.json()
        assert "openapi" in schema
        assert "info" in schema
        assert "paths" in schema
    
    def test_swagger_ui_available(self, client):
        """Test /docs (Swagger UI) is available."""
        response = client.get("/docs")
        assert response.status_code == 200
        assert "swagger-ui" in response.text.lower() or "swagger" in response.text.lower()
