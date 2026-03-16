"""Multi-agent orchestrator for OCTALUME."""

import asyncio
from datetime import datetime
from typing import Any
from uuid import uuid4

from octalume.a2a.messaging import MessageBus
from octalume.a2a.protocol import A2AProtocol
from octalume.core.models import (
    Agent,
    AgentStatus,
    ProjectState,
)
from octalume.core.state import ProjectStateManager
from octalume.utils.logging import get_logger

logger = get_logger(__name__)

AGENT_TYPES = {
    "vision": {
        "name": "Vision Agent",
        "phase": 1,
        "capabilities": ["prd", "business_case", "market_analysis", "stakeholder_alignment"],
        "timeout_seconds": 1800,
    },
    "requirements": {
        "name": "Requirements Agent",
        "phase": 2,
        "capabilities": ["functional_requirements", "nfr", "traceability", "use_cases"],
        "timeout_seconds": 3600,
    },
    "architecture": {
        "name": "Architecture Agent",
        "phase": 3,
        "capabilities": [
            "system_design",
            "security_architecture",
            "threat_modeling",
            "data_modeling",
        ],
        "timeout_seconds": 3600,
    },
    "planning": {
        "name": "Planning Agent",
        "phase": 4,
        "capabilities": ["wbs", "sprint_planning", "resource_allocation", "ci_cd_design"],
        "timeout_seconds": 1800,
    },
    "development": {
        "name": "Development Agent",
        "phase": 5,
        "capabilities": ["feature_implementation", "unit_testing", "code_review", "refactoring"],
        "timeout_seconds": 7200,
    },
    "quality": {
        "name": "Quality Agent",
        "phase": 6,
        "capabilities": ["testing", "security_scanning", "performance_testing", "uat"],
        "timeout_seconds": 5400,
    },
    "deployment": {
        "name": "Deployment Agent",
        "phase": 7,
        "capabilities": ["deployment", "smoke_testing", "rollback", "release_management"],
        "timeout_seconds": 3600,
    },
    "operations": {
        "name": "Operations Agent",
        "phase": 8,
        "capabilities": ["monitoring", "incident_management", "runbooks", "improvements"],
        "timeout_seconds": 1800,
    },
    "orchestrator": {
        "name": "Orchestrator Agent",
        "phase": None,
        "capabilities": ["coordination", "delegation", "monitoring", "escalation"],
        "timeout_seconds": 600,
    },
}


class AgentOrchestrator:
    """Orchestrates multi-agent execution across phases."""

    def __init__(
        self,
        state_manager: ProjectStateManager,
        message_bus: MessageBus | None = None,
        a2a_protocol: A2AProtocol | None = None,
    ):
        self.state_manager = state_manager
        self.message_bus = message_bus or MessageBus()
        self.a2a_protocol = a2a_protocol or A2AProtocol(self.message_bus)
        self._active_tasks: dict[str, asyncio.Task[Any]] = {}

    async def spawn_agent(
        self,
        state: ProjectState,
        agent_type: str,
        task: str,
        config: dict[str, Any] | None = None,
    ) -> str:
        """Spawn a new agent for a task."""
        if agent_type not in AGENT_TYPES:
            raise ValueError(f"Unknown agent type: {agent_type}")

        type_def = AGENT_TYPES[agent_type]
        agent_id = f"{agent_type}-{uuid4().hex[:8]}"

        agent = Agent(
            id=agent_id,
            name=type_def["name"],
            phase=type_def["phase"],
            status=AgentStatus.IDLE,
            current_task=task,
            capabilities=type_def["capabilities"],
            config=config or {},
            timeout_seconds=type_def["timeout_seconds"],
            last_heartbeat=datetime.utcnow(),
        )

        state.agents[agent_id] = agent
        await self.state_manager.save(state)

        logger.info(
            "agent_spawned",
            agent_id=agent_id,
            agent_type=agent_type,
            task=task,
        )

        return agent_id

    async def delegate_task(
        self,
        state: ProjectState,
        agent_id: str,
        task: str,
        context: dict[str, Any] | None = None,
    ) -> str:
        """Delegate a task to an existing agent."""
        if agent_id not in state.agents:
            raise ValueError(f"Agent not found: {agent_id}")

        agent = state.agents[agent_id]

        if agent.status == AgentStatus.RUNNING:
            raise RuntimeError(f"Agent {agent_id} is already running")

        agent.status = AgentStatus.RUNNING
        agent.current_task = task
        agent.last_heartbeat = datetime.utcnow()

        if context:
            agent.config.update(context)

        await self.state_manager.save(state)

        task_id = await self.a2a_protocol.send_message(
            sender="orchestrator",
            recipient=agent_id,
            message_type="task_delegation",
            payload={
                "task": task,
                "context": context or {},
                "phase": agent.phase,
            },
        )

        logger.info(
            "task_delegated",
            agent_id=agent_id,
            task=task,
            task_id=task_id,
        )

        return task_id

    async def get_agent_status(
        self,
        state: ProjectState,
        agent_id: str,
    ) -> dict[str, Any]:
        """Get status of a specific agent."""
        if agent_id not in state.agents:
            raise ValueError(f"Agent not found: {agent_id}")

        agent = state.agents[agent_id]

        return {
            "id": agent.id,
            "name": agent.name,
            "phase": agent.phase,
            "status": agent.status.value,
            "current_task": agent.current_task,
            "capabilities": agent.capabilities,
            "last_heartbeat": agent.last_heartbeat.isoformat() if agent.last_heartbeat else None,
            "timeout_seconds": agent.timeout_seconds,
            "retry_count": agent.retry_count,
            "is_healthy": self._check_agent_health(agent),
        }

    async def list_agents(
        self,
        state: ProjectState,
        phase: int | None = None,
        status: AgentStatus | None = None,
    ) -> list[dict[str, Any]]:
        """List all agents, optionally filtered."""
        agents = []

        for agent in state.agents.values():
            if phase is not None and agent.phase != phase:
                continue
            if status is not None and agent.status != status:
                continue

            agents.append(
                {
                    "id": agent.id,
                    "name": agent.name,
                    "phase": agent.phase,
                    "status": agent.status.value,
                    "current_task": agent.current_task,
                    "is_healthy": self._check_agent_health(agent),
                }
            )

        return agents

    async def terminate_agent(
        self,
        state: ProjectState,
        agent_id: str,
        reason: str = "manual_termination",
    ) -> bool:
        """Terminate an agent."""
        if agent_id not in state.agents:
            raise ValueError(f"Agent not found: {agent_id}")

        agent = state.agents[agent_id]

        if agent.id in self._active_tasks:
            task = self._active_tasks[agent.id]
            task.cancel()
            del self._active_tasks[agent.id]

        agent.status = AgentStatus.FAILED
        agent.current_task = None

        await self.state_manager.save(state)

        logger.warning(
            "agent_terminated",
            agent_id=agent_id,
            reason=reason,
        )

        return True

    async def send_agent_message(
        self,
        state: ProjectState,
        from_agent: str,
        to_agent: str,
        message_type: str,
        payload: dict[str, Any],
    ) -> str:
        """Send a message from one agent to another."""
        if from_agent not in state.agents:
            raise ValueError(f"Sender agent not found: {from_agent}")
        if to_agent not in state.agents and to_agent != "orchestrator":
            raise ValueError(f"Recipient agent not found: {to_agent}")

        message_id = await self.a2a_protocol.send_message(
            sender=from_agent,
            recipient=to_agent,
            message_type=message_type,
            payload=payload,
        )

        logger.info(
            "agent_message_sent",
            from_agent=from_agent,
            to_agent=to_agent,
            message_type=message_type,
            message_id=message_id,
        )

        return message_id

    async def broadcast_message(
        self,
        state: ProjectState,
        from_agent: str,
        message_type: str,
        payload: dict[str, Any],
        phase_filter: int | None = None,
    ) -> list[str]:
        """Broadcast a message to multiple agents."""
        message_ids = []

        for agent_id, agent in state.agents.items():
            if agent_id == from_agent:
                continue
            if phase_filter is not None and agent.phase != phase_filter:
                continue

            message_id = await self.a2a_protocol.send_message(
                sender=from_agent,
                recipient=agent_id,
                message_type=message_type,
                payload=payload,
            )
            message_ids.append(message_id)

        logger.info(
            "message_broadcast",
            from_agent=from_agent,
            message_type=message_type,
            recipient_count=len(message_ids),
        )

        return message_ids

    async def mark_agent_complete(
        self,
        state: ProjectState,
        agent_id: str,
        result: dict[str, Any] | None = None,
    ) -> bool:
        """Mark an agent as completed."""
        if agent_id not in state.agents:
            raise ValueError(f"Agent not found: {agent_id}")

        agent = state.agents[agent_id]
        agent.status = AgentStatus.COMPLETED
        agent.current_task = None
        agent.last_heartbeat = datetime.utcnow()

        if agent.id in self._active_tasks:
            del self._active_tasks[agent.id]

        await self.state_manager.save(state)

        logger.info(
            "agent_completed",
            agent_id=agent_id,
            result=result,
        )

        return True

    async def mark_agent_failed(
        self,
        state: ProjectState,
        agent_id: str,
        error: str,
        retry: bool = True,
    ) -> bool:
        """Mark an agent as failed, optionally retrying."""
        if agent_id not in state.agents:
            raise ValueError(f"Agent not found: {agent_id}")

        agent = state.agents[agent_id]

        if retry and agent.retry_count < agent.max_retries:
            agent.retry_count += 1
            agent.status = AgentStatus.IDLE
            logger.warning(
                "agent_retry",
                agent_id=agent_id,
                retry_count=agent.retry_count,
                error=error,
            )
        else:
            agent.status = AgentStatus.FAILED
            if agent.id in self._active_tasks:
                del self._active_tasks[agent.id]
            logger.error(
                "agent_failed",
                agent_id=agent_id,
                error=error,
                retries_exhausted=agent.retry_count >= agent.max_retries,
            )

        await self.state_manager.save(state)

        return True

    async def health_check(self, state: ProjectState) -> dict[str, Any]:
        """Perform health check on all agents."""
        healthy_count = 0
        unhealthy_agents = []

        for agent in state.agents.values():
            is_healthy = self._check_agent_health(agent)
            if is_healthy:
                healthy_count += 1
            else:
                unhealthy_agents.append(
                    {
                        "id": agent.id,
                        "status": agent.status.value,
                        "last_heartbeat": (
                            agent.last_heartbeat.isoformat() if agent.last_heartbeat else None
                        ),
                    }
                )

        return {
            "total_agents": len(state.agents),
            "healthy": healthy_count,
            "unhealthy": len(unhealthy_agents),
            "unhealthy_agents": unhealthy_agents,
            "timestamp": datetime.utcnow().isoformat(),
        }

    def _check_agent_health(self, agent: Agent) -> bool:
        """Check if an agent is healthy."""
        if agent.status == AgentStatus.FAILED:
            return False

        if agent.last_heartbeat:
            elapsed = (datetime.utcnow() - agent.last_heartbeat).total_seconds()
            if elapsed > agent.timeout_seconds * 2:
                return False

        return True

    def get_agent_type_definition(self, agent_type: str) -> dict[str, Any] | None:
        """Get definition for an agent type."""
        return AGENT_TYPES.get(agent_type)

    def list_agent_types(self) -> list[dict[str, Any]]:
        """List all available agent types."""
        return [
            {
                "type": type_name,
                "name": type_def["name"],
                "phase": type_def["phase"],
                "capabilities": type_def["capabilities"],
                "timeout_seconds": type_def["timeout_seconds"],
            }
            for type_name, type_def in AGENT_TYPES.items()
        ]
