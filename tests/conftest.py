"""Pytest configuration and fixtures for OCTALUME tests."""

import asyncio
from collections.abc import AsyncGenerator, Generator
from pathlib import Path
from uuid import uuid4

import pytest
import pytest_asyncio

from octalume.core.engine import PhaseEngine
from octalume.core.gates import GateValidator
from octalume.core.memory import MemoryBank
from octalume.core.models import (
    Agent,
    AgentStatus,
    AgentType,
    Artifact,
    ArtifactType,
    ComplianceStandard,
    GateResult,
    Phase,
    PhaseStatus,
    ProjectState,
)
from octalume.core.orchestrator import AgentOrchestrator
from octalume.core.state import ProjectStateManager


# Configure asyncio for pytest
@pytest.fixture(scope="session")
def event_loop() -> Generator[asyncio.AbstractEventLoop, None, None]:
    """Create an event loop for async tests."""
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def temp_state_dir(tmp_path: Path) -> Path:
    """Create a temporary state directory."""
    state_dir = tmp_path / ".octalume"
    state_dir.mkdir(parents=True, exist_ok=True)
    return state_dir


@pytest_asyncio.fixture
async def state_manager(temp_state_dir: Path) -> AsyncGenerator[ProjectStateManager, None]:
    """Create a ProjectStateManager with temporary storage."""
    manager = ProjectStateManager(state_dir=temp_state_dir)
    yield manager


@pytest_asyncio.fixture
async def memory_bank(temp_state_dir: Path) -> AsyncGenerator[MemoryBank, None]:
    """Create a MemoryBank with temporary storage."""
    memory_dir = temp_state_dir / "memory"
    memory_dir.mkdir(parents=True, exist_ok=True)
    bank = MemoryBank(state_dir=memory_dir)
    yield bank


@pytest_asyncio.fixture
async def gate_validator(state_manager: ProjectStateManager) -> AsyncGenerator[GateValidator, None]:
    """Create a GateValidator."""
    validator = GateValidator(state_manager)
    yield validator


@pytest_asyncio.fixture
async def orchestrator(
    state_manager: ProjectStateManager,
) -> AsyncGenerator[AgentOrchestrator, None]:
    """Create an AgentOrchestrator."""
    orch = AgentOrchestrator(state_manager)
    yield orch


@pytest_asyncio.fixture
async def engine(
    state_manager: ProjectStateManager,
    gate_validator: GateValidator,
    orchestrator: AgentOrchestrator,
) -> AsyncGenerator[PhaseEngine, None]:
    """Create a PhaseEngine with all dependencies."""
    eng = PhaseEngine(state_manager, gate_validator, orchestrator)
    yield eng


@pytest.fixture
def sample_phase() -> Phase:
    """Create a sample Phase instance."""
    return Phase(
        number=1,
        name="Vision and Strategy",
        description="Define product vision and business case",
        owner="Product Owner",
        status=PhaseStatus.NOT_STARTED,
        artifacts=[],
        entry_criteria=["business_idea_identified"],
        exit_criteria=["business_case_approved", "prd_completed"],
    )


@pytest.fixture
def sample_artifact() -> Artifact:
    """Create a sample Artifact instance."""
    return Artifact(
        id="P1-DOC-001",
        phase=1,
        name="Product Requirements Document",
        artifact_type=ArtifactType.DOCUMENT,
        content="# PRD\n\nThis is the product requirements document.",
        file_path="docs/prd.md",
        compliance_tags=[ComplianceStandard.SOC2],
        linked_artifacts=[],
    )


@pytest.fixture
def sample_agent() -> Agent:
    """Create a sample Agent instance."""
    return Agent(
        id=f"agent-vision-{uuid4().hex[:8]}",
        name="Vision Agent",
        agent_type=AgentType.VISION,
        phase=1,
        status=AgentStatus.IDLE,
        current_task="Create business case and PRD",
        capabilities=["business_analysis", "market_research"],
        config={"max_iterations": 10},
    )


@pytest.fixture
def sample_project_state() -> ProjectState:
    """Create a sample ProjectState instance."""
    now = asyncio.get_event_loop().time() if asyncio.get_event_loop().is_running() else 0

    phases = {}
    for i in range(1, 9):
        phases[i] = Phase(
            number=i,
            name=f"Phase {i}",
            description=f"Description for phase {i}",
            owner="Owner",
            status=PhaseStatus.NOT_STARTED if i > 1 else PhaseStatus.IN_PROGRESS,
            artifacts=[],
            entry_criteria=[],
            exit_criteria=[],
        )

    return ProjectState(
        id=uuid4(),
        name="test-project",
        description="Test project for unit tests",
        current_phase=1,
        phases=phases,
        artifacts={},
        agents={},
        compliance_standards=[ComplianceStandard.SOC2, ComplianceStandard.HIPAA],
        artifact_counter={},
    )


@pytest_asyncio.fixture
async def initialized_project(
    state_manager: ProjectStateManager,
    sample_project_state: ProjectState,
) -> AsyncGenerator[ProjectState, None]:
    """Create and persist an initialized project state."""
    state = await state_manager.create(
        name=sample_project_state.name,
        description=sample_project_state.description,
        compliance_standards=["soc2", "hipaa"],
    )
    yield state


@pytest_asyncio.fixture
async def project_with_artifact(
    initialized_project: ProjectState,
    state_manager: ProjectStateManager,
    sample_artifact: Artifact,
) -> AsyncGenerator[ProjectState, None]:
    """Create a project state with an artifact."""
    state = initialized_project
    state.artifacts[sample_artifact.id] = sample_artifact
    state.phases[1].artifacts.append(sample_artifact.id)
    await state_manager.save(state)
    yield state


@pytest.fixture
def sample_gate_result() -> GateResult:
    """Create a sample GateResult instance."""
    return GateResult(
        passed=True,
        phase=1,
        missing_artifacts=[],
        failed_criteria=[],
        warnings=["Consider adding more detail to PRD"],
        reasons=["All required artifacts present"],
    )


# Test helpers
def create_artifact(
    phase: int,
    artifact_type: ArtifactType,
    name: str,
    counter: int = 1,
) -> Artifact:
    """Helper function to create artifacts with proper IDs."""
    section_map = {
        ArtifactType.DOCUMENT: "DOC",
        ArtifactType.CODE: "CODE",
        ArtifactType.TEST: "TEST",
        ArtifactType.CONFIGURATION: "CFG",
        ArtifactType.DESIGN: "DSN",
        ArtifactType.REPORT: "RPT",
        ArtifactType.DECISION: "DEC",
    }
    section = section_map[artifact_type]

    return Artifact(
        id=f"P{phase}-{section}-{counter:03d}",
        phase=phase,
        name=name,
        artifact_type=artifact_type,
    )


def create_agent(
    agent_type: AgentType,
    phase: int,
    task: str,
) -> Agent:
    """Helper function to create agents."""
    return Agent(
        id=f"agent-{agent_type.value}-{uuid4().hex[:8]}",
        agent_type=agent_type,
        phase=phase,
        task=task,
        status=AgentStatus.IDLE,
        config={},
        artifacts_created=[],
    )


# Pytest configuration
def pytest_configure(config: pytest.Config) -> None:
    """Configure pytest with custom markers."""
    config.addinivalue_line("markers", "asyncio: mark test as async")
    config.addinivalue_line("markers", "slow: mark test as slow")
    config.addinivalue_line("markers", "integration: mark test as integration test")


def pytest_collection_modifyitems(config: pytest.Config, items: list[pytest.Item]) -> None:
    """Skip slow tests by default unless --runslow is passed."""
    if not config.getoption("--runslow", default=False):
        skip_slow = pytest.mark.skip(reason="use --runslow to run")
        for item in items:
            if "slow" in item.keywords:
                item.add_marker(skip_slow)
