"""Integration tests for full lifecycle workflow."""

import shutil
import tempfile
from pathlib import Path

import pytest

from octalume.core.engine import PhaseEngine
from octalume.core.gates import GateValidator
from octalume.core.models import Artifact, ArtifactType, ComplianceStandard
from octalume.core.orchestrator import AgentOrchestrator
from octalume.core.state import ProjectStateManager


@pytest.fixture
def temp_state_dir():
    temp_dir = Path(tempfile.mkdtemp())
    yield temp_dir
    shutil.rmtree(temp_dir, ignore_errors=True)


@pytest.fixture
async def setup_engine(temp_state_dir):
    manager = ProjectStateManager(state_dir=temp_state_dir)
    gate_validator = GateValidator(manager)
    orchestrator = AgentOrchestrator(manager)
    engine = PhaseEngine(manager, gate_validator, orchestrator)
    yield manager, engine, gate_validator


class TestFullLifecycleWorkflow:
    @pytest.mark.asyncio
    async def test_initialize_and_progress_through_phases(self, setup_engine):
        manager, engine, gate_validator = setup_engine

        state = await manager.create(
            name="test-lifecycle-project",
            description="Test full lifecycle",
            compliance_standards=["soc2"]
        )

        assert state.current_phase == 1
        assert len(state.phases) == 8

        state = await engine.start_phase(state, 1)
        assert state.phases[1].status.value == "in_progress"

        artifact = Artifact(
            id="P1-DOC-001",
            phase=1,
            name="Business Case",
            artifact_type=ArtifactType.DOCUMENT,
            content="Test business case",
        )
        state.artifacts[artifact.id] = artifact
        state.phases[1].artifacts.append(artifact.id)
        await manager.save(state)

        gate_result = await gate_validator.validate_exit(state, 1)
        assert gate_result is not None

    @pytest.mark.asyncio
    async def test_compliance_standards_are_configured(self, setup_engine):
        manager, engine, _ = setup_engine

        state = await manager.create(
            name="compliant-project",
            compliance_standards=["hipaa", "soc2", "gdpr"]
        )

        assert len(state.compliance_standards) == 3
        assert ComplianceStandard.HIPAA in state.compliance_standards
        assert ComplianceStandard.SOC2 in state.compliance_standards
        assert ComplianceStandard.GDPR in state.compliance_standards

    @pytest.mark.asyncio
    async def test_artifact_traceability(self, setup_engine):
        manager, engine, _ = setup_engine

        state = await manager.create(name="traceability-test")

        artifact1 = Artifact(
            id="P1-DOC-001",
            phase=1,
            name="PRD",
            artifact_type=ArtifactType.DOCUMENT,
        )
        artifact2 = Artifact(
            id="P2-DOC-001",
            phase=2,
            name="Requirements",
            artifact_type=ArtifactType.DOCUMENT,
        )

        state.artifacts[artifact1.id] = artifact1
        state.artifacts[artifact2.id] = artifact2

        artifact1.linked_artifacts.append(artifact2.id)

        await manager.save(state)

        loaded = await manager.load()
        assert artifact2.id in loaded.artifacts[artifact1.id].linked_artifacts

    @pytest.mark.asyncio
    async def test_phase_rollback(self, setup_engine):
        manager, engine, _ = setup_engine

        state = await manager.create(name="rollback-test")

        state = await engine.start_phase(state, 1)
        assert state.current_phase == 1

        state = await engine.rollback_phase(state, 1, "Test rollback")
        assert state.current_phase == 1


class TestAgentOrchestration:
    @pytest.mark.asyncio
    async def test_spawn_and_track_agent(self, setup_engine):
        manager, engine, _ = setup_engine

        state = await manager.create(name="agent-test")

        orchestrator = AgentOrchestrator(manager)

        agent_id = await orchestrator.spawn_agent(
            state=state,
            agent_type="vision",
            task="Create business case"
        )

        assert agent_id is not None
        assert agent_id in state.agents

    @pytest.mark.asyncio
    async def test_list_agents_by_phase(self, setup_engine):
        manager, engine, _ = setup_engine

        state = await manager.create(name="agent-list-test")
        orchestrator = AgentOrchestrator(manager)

        await orchestrator.spawn_agent(
            state=state,
            agent_type="vision",
            task="Task 1"
        )
        await orchestrator.spawn_agent(
            state=state,
            agent_type="architecture",
            task="Task 2"
        )

        agents = await orchestrator.list_agents(state)
        assert len(agents) >= 2


class TestQualityGates:
    @pytest.mark.asyncio
    async def test_entry_gate_validation(self, setup_engine):
        manager, engine, gate_validator = setup_engine

        state = await manager.create(name="gate-test")

        result = await gate_validator.validate_entry(state, 1)
        assert result.passed is True

    @pytest.mark.asyncio
    async def test_exit_gate_requires_artifacts(self, setup_engine):
        manager, engine, gate_validator = setup_engine

        state = await manager.create(name="exit-gate-test")

        result = await gate_validator.validate_exit(state, 1)
        assert result.passed is False
        assert len(result.missing_artifacts) > 0


class TestStatePersistence:
    @pytest.mark.asyncio
    async def test_state_persists_across_sessions(self, temp_state_dir):
        manager1 = ProjectStateManager(state_dir=temp_state_dir)

        state = await manager1.create(
            name="persistence-test",
            description="Testing persistence"
        )
        await manager1.save(state)

        manager2 = ProjectStateManager(state_dir=temp_state_dir)
        loaded = await manager2.load()

        assert loaded is not None
        assert loaded.name == "persistence-test"

    @pytest.mark.asyncio
    async def test_state_updates_persist(self, temp_state_dir):
        manager = ProjectStateManager(state_dir=temp_state_dir)

        state = await manager.create(name="update-test")
        state.description = "Updated description"
        await manager.save(state)

        loaded = await manager.load()
        assert loaded.description == "Updated description"
