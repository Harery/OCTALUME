"""Tests for OCTALUME core engine."""


import pytest

from octalume.core.engine import PhaseEngine
from octalume.core.gates import GateValidator
from octalume.core.models import (
    Artifact,
    ArtifactType,
    Phase,
    PhaseStatus,
    ProjectState,
)
from octalume.core.state import ProjectStateManager


@pytest.fixture
async def state_manager(tmp_path):
    manager = ProjectStateManager(state_dir=tmp_path / ".octalume")
    yield manager


@pytest.fixture
async def project_state(state_manager):
    state = await state_manager.create(
        name="test-project",
        description="Test project",
    )
    yield state


class TestProjectStateManager:
    async def test_create_project(self, state_manager):
        state = await state_manager.create(
            name="my-project",
            description="Test",
        )

        assert state.name == "my-project"
        assert state.description == "Test"
        assert state.current_phase == 1
        assert len(state.phases) == 8

    async def test_load_project(self, state_manager, project_state):
        loaded = await state_manager.load()

        assert loaded is not None
        assert loaded.name == project_state.name
        assert str(loaded.id) == str(project_state.id)

    async def test_save_project(self, state_manager, project_state):
        project_state.description = "Updated"
        await state_manager.save(project_state)

        loaded = await state_manager.load()
        assert loaded.description == "Updated"


class TestPhaseEngine:
    async def test_initialize_project(self, state_manager):
        engine = PhaseEngine(state_manager)
        state = ProjectState(
            id=project_state.id,
            name="test",
            phases={},
            artifacts={},
            agents={},
        )

        state = await engine.initialize_project(state)

        assert len(state.phases) == 8
        assert state.phases[1].status == PhaseStatus.NOT_STARTED

    async def test_start_phase(self, state_manager, project_state):
        gate_validator = GateValidator(state_manager)
        from octalume.core.orchestrator import AgentOrchestrator
        orchestrator = AgentOrchestrator(state_manager)
        engine = PhaseEngine(state_manager, gate_validator, orchestrator)

        state = await engine.start_phase(project_state, 1)

        assert state.phases[1].status == PhaseStatus.IN_PROGRESS
        assert state.current_phase == 1

    async def test_cannot_start_phase_out_of_order(self, state_manager, project_state):
        gate_validator = GateValidator(state_manager)
        from octalume.core.orchestrator import AgentOrchestrator
        orchestrator = AgentOrchestrator(state_manager)
        engine = PhaseEngine(state_manager, gate_validator, orchestrator)

        with pytest.raises(RuntimeError):
            await engine.start_phase(project_state, 3)


class TestGateValidator:
    async def test_validate_entry_first_phase(self, state_manager, project_state):
        validator = GateValidator(state_manager)

        result = await validator.validate_entry(project_state, 1)

        assert result.passed is True

    async def test_validate_exit_without_artifacts(self, state_manager, project_state):
        validator = GateValidator(state_manager)

        result = await validator.validate_exit(project_state, 1)

        assert result.passed is False
        assert len(result.missing_artifacts) > 0


class TestModels:
    def test_phase_creation(self):
        phase = Phase(
            number=1,
            name="Vision",
            description="Test phase",
            owner="Product Owner",
        )

        assert phase.number == 1
        assert phase.status == PhaseStatus.NOT_STARTED
        assert phase.duration_estimate_days == 7

    def test_artifact_creation(self):
        artifact = Artifact(
            id="P1-DOC-001",
            phase=1,
            name="Test Artifact",
            artifact_type=ArtifactType.DOCUMENT,
        )

        assert artifact.id == "P1-DOC-001"
        assert artifact.phase == 1
        assert artifact.artifact_type == ArtifactType.DOCUMENT

    def test_artifact_id_pattern(self):
        with pytest.raises(ValueError):
            Artifact(
                id="invalid-id",
                phase=1,
                name="Test",
                artifact_type=ArtifactType.DOCUMENT,
            )
