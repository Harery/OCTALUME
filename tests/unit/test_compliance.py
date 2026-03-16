"""Tests for compliance scanners."""

import pytest

from octalume.compliance.gdpr import GDPRCompliance
from octalume.compliance.hipaa import HIPAACompliance
from octalume.compliance.pci import PCICompliance
from octalume.compliance.soc2 import SOC2Compliance
from octalume.core.models import (
    Artifact,
    ArtifactType,
    Phase,
    PhaseStatus,
    ProjectState,
)


@pytest.fixture
def empty_state():
    from uuid import uuid4

    state = ProjectState(
        id=uuid4(),
        name="test",
        phases={},
        artifacts={},
        agents={},
    )
    for i in range(1, 9):
        state.phases[i] = Phase(
            number=i,
            name=f"Phase {i}",
            description="Test",
            owner="Test",
            status=PhaseStatus.NOT_STARTED,
        )
    return state


@pytest.fixture
def state_with_artifacts(empty_state):
    empty_state.artifacts["P3-SEC-001"] = Artifact(
        id="P3-SEC-001",
        phase=3,
        name="Security Architecture",
        artifact_type=ArtifactType.DOCUMENT,
    )
    empty_state.artifacts["P1-PRD-001"] = Artifact(
        id="P1-PRD-001",
        phase=1,
        name="PRD",
        artifact_type=ArtifactType.DOCUMENT,
    )
    return empty_state


class TestHIPAACompliance:
    async def test_scan_empty_project(self, empty_state):
        scanner = HIPAACompliance()
        result = await scanner.scan(empty_state)

        assert result["standard"] == "hipaa"
        assert result["status"] == "non-compliant"
        assert result["score"] < 100

    async def test_scan_with_artifacts(self, state_with_artifacts):
        scanner = HIPAACompliance()
        result = await scanner.scan(state_with_artifacts)

        assert result["score"] > 0

    async def test_scan_returns_findings(self, empty_state):
        scanner = HIPAACompliance()
        result = await scanner.scan(empty_state)

        assert isinstance(result["findings"], list)


class TestSOC2Compliance:
    async def test_scan_empty_project(self, empty_state):
        scanner = SOC2Compliance()
        result = await scanner.scan(empty_state)

        assert result["standard"] == "soc2"
        assert result["status"] in ["compliant", "partial", "non-compliant"]

    async def test_scan_with_artifacts(self, state_with_artifacts):
        scanner = SOC2Compliance()
        result = await scanner.scan(state_with_artifacts)

        assert result["score"] > 0


class TestGDPRCompliance:
    async def test_scan_empty_project(self, empty_state):
        scanner = GDPRCompliance()
        result = await scanner.scan(empty_state)

        assert result["standard"] == "gdpr"

    async def test_scan_returns_recommendations(self, empty_state):
        scanner = GDPRCompliance()
        result = await scanner.scan(empty_state)

        assert isinstance(result["recommendations"], list)


class TestPCICompliance:
    async def test_scan_empty_project(self, empty_state):
        scanner = PCICompliance()
        result = await scanner.scan(empty_state)

        assert result["standard"] == "pci_dss"

    async def test_all_checks_critical(self, empty_state):
        scanner = PCICompliance()
        result = await scanner.scan(empty_state)

        for finding in result["findings"]:
            assert finding["severity"] == "critical"
