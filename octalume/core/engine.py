"""Phase execution engine for OCTALUME."""

import asyncio
from datetime import datetime
from typing import Any

from octalume.core.models import (
    PHASE_DEFINITIONS,
    Artifact,
    ArtifactType,
    GateResult,
    Phase,
    PhaseStatus,
    ProjectState,
)
from octalume.core.gates import GateValidator
from octalume.core.orchestrator import AgentOrchestrator
from octalume.core.state import ProjectStateManager
from octalume.utils.logging import get_logger

logger = get_logger(__name__)


class PhaseEngine:
    """Executes and manages lifecycle phases."""

    def __init__(
        self,
        state_manager: ProjectStateManager,
        gate_validator: GateValidator | None = None,
        orchestrator: AgentOrchestrator | None = None,
    ):
        self.state_manager = state_manager
        self.gate_validator = gate_validator or GateValidator(state_manager)
        self.orchestrator = orchestrator or AgentOrchestrator(state_manager)

    async def initialize_project(self, state: ProjectState) -> ProjectState:
        """Initialize all 8 phases for a project."""
        for phase_num, definition in PHASE_DEFINITIONS.items():
            phase = Phase(
                number=phase_num,
                name=definition["name"],
                description=definition["description"],
                owner=definition["owner"],
                duration_estimate_days=definition["duration_estimate_days"],
                exit_criteria=definition["exit_criteria"],
                status=PhaseStatus.NOT_STARTED,
            )
            state.phases[phase_num] = phase

        state.phases[1].status = PhaseStatus.NOT_STARTED
        state.current_phase = 1
        state.phase_status = PhaseStatus.NOT_STARTED

        await self.state_manager.save(state)
        logger.info("project_initialized", project_id=str(state.id), phases=8)
        return state

    async def start_phase(self, state: ProjectState, phase_num: int) -> ProjectState:
        """Start a specific phase."""
        if phase_num < 1 or phase_num > 8:
            raise ValueError(f"Invalid phase number: {phase_num}")

        if phase_num not in state.phases:
            raise ValueError(f"Phase {phase_num} not initialized")

        phase = state.phases[phase_num]

        if phase_num > 1:
            prev_phase = state.phases[phase_num - 1]
            if prev_phase.status != PhaseStatus.COMPLETED:
                raise RuntimeError(
                    f"Cannot start phase {phase_num}: phase {phase_num - 1} not completed"
                )

        gate_result = await self.gate_validator.validate_entry(state, phase_num)
        if not gate_result.passed:
            phase.status = PhaseStatus.BLOCKED
            phase.blockers = gate_result.missing_artifacts
            await self.state_manager.save(state)
            logger.warning(
                "phase_blocked",
                phase=phase_num,
                blockers=gate_result.missing_artifacts,
            )
            return state

        phase.status = PhaseStatus.IN_PROGRESS
        phase.started_at = datetime.utcnow()
        state.current_phase = phase_num
        state.phase_status = PhaseStatus.IN_PROGRESS

        await self.state_manager.save(state)
        logger.info("phase_started", phase=phase_num, name=phase.name)
        return state

    async def complete_phase(
        self,
        state: ProjectState,
        phase_num: int,
        artifacts: list[Artifact] | None = None,
    ) -> tuple[ProjectState, GateResult]:
        """Complete a phase and run exit gate validation."""
        if phase_num not in state.phases:
            raise ValueError(f"Phase {phase_num} not initialized")

        phase = state.phases[phase_num]

        if phase.status != PhaseStatus.IN_PROGRESS:
            raise RuntimeError(f"Phase {phase_num} is not in progress")

        if artifacts:
            for artifact in artifacts:
                state.artifacts[artifact.id] = artifact
                phase.artifacts.append(artifact.id)
                self._increment_artifact_counter(state, artifact)

        gate_result = await self.gate_validator.validate_exit(state, phase_num)

        if gate_result.passed:
            phase.status = PhaseStatus.COMPLETED
            phase.completed_at = datetime.utcnow()
            state.gate_results.append(gate_result)
            logger.info("phase_completed", phase=phase_num, name=phase.name)
        else:
            phase.blockers = gate_result.missing_artifacts + gate_result.compliance_issues
            logger.warning(
                "phase_exit_failed",
                phase=phase_num,
                issues=phase.blockers,
            )

        await self.state_manager.save(state)
        return state, gate_result

    async def transition_phase(
        self,
        state: ProjectState,
        from_phase: int,
        to_phase: int,
    ) -> tuple[ProjectState, GateResult]:
        """Transition from one phase to another."""
        if to_phase != from_phase + 1:
            raise ValueError(f"Can only transition to next phase (from {from_phase} to {from_phase + 1})")

        state, gate_result = await self.complete_phase(state, from_phase)

        if gate_result.passed:
            state = await self.start_phase(state, to_phase)

        return state, gate_result

    async def rollback_phase(
        self,
        state: ProjectState,
        to_phase: int,
        reason: str,
    ) -> ProjectState:
        """Rollback to a previous phase."""
        if to_phase >= state.current_phase:
            raise ValueError(f"Can only rollback to earlier phase (current: {state.current_phase})")

        for phase_num in range(to_phase + 1, state.current_phase + 1):
            phase = state.phases[phase_num]
            phase.status = PhaseStatus.NOT_STARTED
            phase.started_at = None
            phase.completed_at = None
            phase.blockers = []

        state.current_phase = to_phase
        state.phase_status = PhaseStatus.NOT_STARTED
        state.phases[to_phase].status = PhaseStatus.NOT_STARTED

        await self.state_manager.save(state)
        logger.warning(
            "phase_rollback",
            to_phase=to_phase,
            reason=reason,
        )
        return state

    async def spawn_phase_agent(
        self,
        state: ProjectState,
        phase_num: int,
        task: str,
    ) -> str:
        """Spawn an agent for a phase-specific task."""
        agent_type = self._get_agent_type_for_phase(phase_num)
        agent_id = await self.orchestrator.spawn_agent(
            state=state,
            agent_type=agent_type,
            task=task,
        )
        return agent_id

    async def get_phase_status(
        self,
        state: ProjectState,
        phase_num: int,
    ) -> dict[str, Any]:
        """Get detailed status of a phase."""
        phase = state.phases.get(phase_num)
        if not phase:
            raise ValueError(f"Phase {phase_num} not found")

        artifacts = [
            state.artifacts[aid].model_dump()
            for aid in phase.artifacts
            if aid in state.artifacts
        ]

        agents = [
            a.model_dump()
            for a in state.agents.values()
            if a.phase == phase_num
        ]

        return {
            "phase": phase.model_dump(),
            "artifacts": artifacts,
            "agents": agents,
            "can_proceed": phase.status == PhaseStatus.COMPLETED,
            "next_phase_available": (
                phase_num < 8 and
                phase.status == PhaseStatus.COMPLETED
            ),
        }

    def _increment_artifact_counter(self, state: ProjectState, artifact: Artifact) -> None:
        """Increment artifact counter for traceability."""
        section = artifact.id.split("-")[1]
        state.artifact_counter[section] = state.artifact_counter.get(section, 0) + 1

    def _get_agent_type_for_phase(self, phase_num: int) -> str:
        """Map phase number to agent type."""
        mapping = {
            1: "vision",
            2: "requirements",
            3: "architecture",
            4: "planning",
            5: "development",
            6: "quality",
            7: "deployment",
            8: "operations",
        }
        return mapping.get(phase_num, "generic")
