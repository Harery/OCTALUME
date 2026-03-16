"""Integration tests for OCTALUME API."""

import shutil
import tempfile
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from web.backend.main import app


@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c


@pytest.fixture
def temp_project_dir():
    temp_dir = Path(tempfile.mkdtemp())
    yield temp_dir
    shutil.rmtree(temp_dir, ignore_errors=True)


class TestHealthEndpoints:
    def test_root_returns_api_info(self, client):
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "OCTALUME"
        assert data["version"] == "2.0.0"
        assert data["status"] == "running"

    def test_health_returns_services_status(self, client):
        response = client.get("/health")
        assert response.status_code in [200, 503]
        data = response.json()
        assert "status" in data
        assert "services" in data

    def test_readiness_check(self, client):
        response = client.get("/ready")
        assert response.status_code == 200
        data = response.json()
        assert "ready" in data


class TestPhaseEndpoints:
    def test_list_phases(self, client):
        response = client.get("/api/phases")
        assert response.status_code == 200
        data = response.json()
        assert "phases" in data
        assert "current_phase" in data

    def test_get_phase_status(self, client):
        response = client.get("/api/phases/1")
        assert response.status_code == 200

    def test_start_phase(self, client):
        response = client.post("/api/phases/1/start")
        assert response.status_code in [200, 400]

    def test_complete_phase(self, client):
        response = client.post("/api/phases/1/complete")
        assert response.status_code in [200, 400, 422]

    def test_invalid_phase_number(self, client):
        response = client.get("/api/phases/99")
        assert response.status_code in [400, 404, 422]


class TestAgentEndpoints:
    def test_list_agents(self, client):
        response = client.get("/api/agents")
        assert response.status_code == 200
        data = response.json()
        assert "agents" in data

    def test_list_agents_with_filter(self, client):
        response = client.get("/api/agents?status=running")
        assert response.status_code == 200

    def test_spawn_agent_validation(self, client):
        response = client.post(
            "/api/agents/spawn",
            json={"agent_type": "vision", "task": "Create business case"}
        )
        assert response.status_code in [200, 400, 422]


class TestArtifactEndpoints:
    def test_list_artifacts(self, client):
        response = client.get("/api/artifacts")
        assert response.status_code == 200
        data = response.json()
        assert "artifacts" in data

    def test_create_artifact_validation(self, client):
        response = client.post(
            "/api/artifacts",
            json={
                "phase": 1,
                "artifact_type": "document",
                "name": "Test Artifact"
            }
        )
        assert response.status_code in [200, 201, 400, 422]

    def test_search_artifacts(self, client):
        response = client.get("/api/artifacts?search_term=test")
        assert response.status_code == 200


class TestComplianceEndpoints:
    def test_list_compliance_standards(self, client):
        response = client.get("/api/compliance/standards")
        assert response.status_code == 200
        data = response.json()
        assert "standards" in data

    def test_compliance_status(self, client):
        response = client.get("/api/compliance/status")
        assert response.status_code == 200

    def test_run_compliance_scan(self, client):
        response = client.post(
            "/api/compliance/scan",
            json={"standards": ["hipaa"]}
        )
        assert response.status_code in [200, 400, 422]


class TestDashboardEndpoints:
    def test_dashboard_summary(self, client):
        response = client.get("/api/dashboard/summary")
        assert response.status_code == 200

    def test_dashboard_metrics(self, client):
        response = client.get("/api/dashboard/metrics")
        assert response.status_code == 200

    def test_dashboard_timeline(self, client):
        response = client.get("/api/dashboard/timeline")
        assert response.status_code == 200
