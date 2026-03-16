"""Project state management for OCTALUME."""

import json
from datetime import datetime
from pathlib import Path
from typing import Any
from uuid import UUID, uuid4

from pydantic import ValidationError

from octalume.core.models import (
    PHASE_DEFINITIONS,
    Phase,
    PhaseStatus,
    ProjectState,
)
from octalume.utils.logging import get_logger

logger = get_logger(__name__)


class ProjectStateManager:
    """Manages project state persistence and retrieval."""

    def __init__(self, state_dir: Path | None = None):
        self.state_dir = state_dir or Path.cwd() / ".octalume"
        self.state_file = self.state_dir / "project-state.json"
        self._ensure_state_dir()

    def _ensure_state_dir(self) -> None:
        """Ensure state directory exists."""
        self.state_dir.mkdir(parents=True, exist_ok=True)

    async def create(
        self,
        name: str,
        description: str | None = None,
        compliance_standards: list[str] | None = None,
    ) -> ProjectState:
        """Create a new project state."""
        state = ProjectState(
            id=uuid4(),
            name=name,
            description=description,
            current_phase=1,
            phase_status=PhaseStatus.NOT_STARTED,
            compliance_standards=compliance_standards or [],
        )

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

        await self.save(state)

        logger.info(
            "project_created",
            project_id=str(state.id),
            name=name,
            phases=len(state.phases),
        )

        return state

    async def load(self, project_id: UUID | None = None) -> ProjectState | None:
        """Load project state from disk."""
        if not self.state_file.exists():
            return None

        try:
            with open(self.state_file) as f:
                data = json.load(f)

            state = ProjectState.model_validate(data)

            logger.debug("project_state_loaded", project_id=str(state.id))
            return state

        except (json.JSONDecodeError, ValidationError) as e:
            logger.error("project_state_load_error", error=str(e))
            return None

    async def save(self, state: ProjectState) -> None:
        """Save project state to disk."""
        state.updated_at = datetime.utcnow()

        with open(self.state_file, "w") as f:
            json.dump(state.model_dump(mode="json"), f, indent=2, default=str)

        logger.debug("project_state_saved", project_id=str(state.id))

    async def delete(self, project_id: UUID) -> bool:
        """Delete project state."""
        if self.state_file.exists():
            self.state_file.unlink()
            logger.info("project_state_deleted", project_id=str(project_id))
            return True
        return False

    async def get_or_create(
        self,
        name: str = "default",
        description: str | None = None,
    ) -> ProjectState:
        """Get existing state or create new."""
        state = await self.load()
        if state:
            return state
        return await self.create(name=name, description=description)

    async def update_phase(
        self,
        state: ProjectState,
        phase_num: int,
        status: PhaseStatus,
        **kwargs: Any,
    ) -> ProjectState:
        """Update a phase in the state."""
        if phase_num not in state.phases:
            raise ValueError(f"Phase {phase_num} not found")

        phase = state.phases[phase_num]
        phase.status = status

        if status == PhaseStatus.IN_PROGRESS:
            phase.started_at = datetime.utcnow()
        elif status == PhaseStatus.COMPLETED:
            phase.completed_at = datetime.utcnow()

        for key, value in kwargs.items():
            if hasattr(phase, key):
                setattr(phase, key, value)

        await self.save(state)
        return state

    async def add_artifact_ref(
        self,
        state: ProjectState,
        phase_num: int,
        artifact_id: str,
    ) -> ProjectState:
        """Add artifact reference to a phase."""
        if phase_num not in state.phases:
            raise ValueError(f"Phase {phase_num} not found")

        if artifact_id not in state.phases[phase_num].artifacts:
            state.phases[phase_num].artifacts.append(artifact_id)
            await self.save(state)

        return state

    async def get_summary(self, state: ProjectState) -> dict[str, Any]:
        """Get project state summary."""
        phases_summary = []

        for phase_num in sorted(state.phases.keys()):
            phase = state.phases[phase_num]
            phases_summary.append(
                {
                    "number": phase.number,
                    "name": phase.name,
                    "status": phase.status.value,
                    "owner": phase.owner,
                    "artifacts_count": len(phase.artifacts),
                }
            )

        return {
            "id": str(state.id),
            "name": state.name,
            "description": state.description,
            "current_phase": state.current_phase,
            "phase_status": state.phase_status.value,
            "total_artifacts": len(state.artifacts),
            "total_agents": len(state.agents),
            "compliance_standards": [s.value for s in state.compliance_standards],
            "created_at": state.created_at.isoformat(),
            "updated_at": state.updated_at.isoformat(),
            "phases": phases_summary,
        }

    def state_exists(self) -> bool:
        """Check if state file exists."""
        return self.state_file.exists()

    def get_state_path(self) -> Path:
        """Get path to state file."""
        return self.state_file
