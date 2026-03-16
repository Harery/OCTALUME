"""Base agent class for all phase agents."""

from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any

from octalume.core.memory import MemoryBank
from octalume.core.models import Agent, AgentStatus
from octalume.core.state import ProjectStateManager
from octalume.utils.logging import get_logger

logger = get_logger(__name__)


class BaseAgent(ABC):
    """Base class for all phase-specific agents."""

    def __init__(
        self,
        agent_id: str,
        name: str,
        phase: int,
        capabilities: list[str],
        state_manager: ProjectStateManager,
        memory: MemoryBank,
    ):
        self.agent_id = agent_id
        self.name = name
        self.phase = phase
        self.capabilities = capabilities
        self.state_manager = state_manager
        self.memory = memory
        self._status = AgentStatus.IDLE
        self._current_task: str | None = None
        self._started_at: datetime | None = None

    @property
    def status(self) -> AgentStatus:
        return self._status

    @property
    def current_task(self) -> str | None:
        return self._current_task

    async def execute(self, task: str, context: dict[str, Any] | None = None) -> dict[str, Any]:
        """Execute a task with this agent."""
        self._status = AgentStatus.RUNNING
        self._current_task = task
        self._started_at = datetime.utcnow()

        logger.info(
            "agent_execution_started",
            agent_id=self.agent_id,
            task=task,
        )

        try:
            result = await self._execute_task(task, context or {})

            self._status = AgentStatus.COMPLETED

            await self.memory.save(
                category="progress",
                key=f"{self.agent_id}-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}",
                value={
                    "task": task,
                    "result": result,
                    "phase": self.phase,
                },
            )

            logger.info(
                "agent_execution_completed",
                agent_id=self.agent_id,
                task=task,
            )

            return result

        except Exception as e:
            self._status = AgentStatus.FAILED

            logger.error(
                "agent_execution_failed",
                agent_id=self.agent_id,
                task=task,
                error=str(e),
            )

            return {"success": False, "error": str(e)}

    @abstractmethod
    async def _execute_task(
        self,
        task: str,
        context: dict[str, Any],
    ) -> dict[str, Any]:
        """Execute the specific task. Override in subclasses."""
        pass

    def to_model(self) -> Agent:
        """Convert to Agent model."""
        return Agent(
            id=self.agent_id,
            name=self.name,
            phase=self.phase,
            status=self._status,
            current_task=self._current_task,
            capabilities=self.capabilities,
            last_heartbeat=datetime.utcnow(),
        )

    async def heartbeat(self) -> None:
        """Update agent heartbeat."""
        logger.debug("agent_heartbeat", agent_id=self.agent_id)
