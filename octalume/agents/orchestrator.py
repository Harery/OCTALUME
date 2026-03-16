"""Orchestrator agent for coordinating all phases."""

from typing import Any

from octalume.agents.base import BaseAgent
from octalume.core.memory import MemoryBank
from octalume.core.state import ProjectStateManager


class OrchestratorAgent(BaseAgent):
    def __init__(
        self,
        state_manager: ProjectStateManager,
        memory: MemoryBank,
        agent_id: str = "orchestrator-agent",
    ):
        super().__init__(
            agent_id=agent_id,
            name="Orchestrator Agent",
            phase=0,
            capabilities=[
                "phase_coordination",
                "agent_management",
                "workflow_orchestration",
                "cross_phase_communication",
                "resource_allocation",
                "progress_tracking",
            ],
            state_manager=state_manager,
            memory=memory,
        )

    async def _execute_task(
        self,
        task: str,
        context: dict[str, Any],
    ) -> dict[str, Any]:
        task_lower = task.lower()

        if "phase" in task_lower and ("transition" in task_lower or "start" in task_lower):
            return await self._coordinate_phase_transition(task, context)
        elif "agent" in task_lower:
            return await self._manage_agents(task, context)
        elif "workflow" in task_lower:
            return await self._orchestrate_workflow(task, context)
        elif "progress" in task_lower or "status" in task_lower:
            return await self._track_progress(task, context)
        else:
            return await self._general_orchestration_task(task, context)

    async def _coordinate_phase_transition(
        self,
        task: str,
        context: dict[str, Any],
    ) -> dict[str, Any]:
        from_phase = context.get("from_phase", 1)
        to_phase = context.get("to_phase", from_phase + 1)

        transition_plan = {
            "from_phase": from_phase,
            "to_phase": to_phase,
            "steps": [
                {"step": 1, "action": f"Validate exit criteria for Phase {from_phase}"},
                {"step": 2, "action": f"Archive Phase {from_phase} artifacts"},
                {"step": 3, "action": f"Initialize Phase {to_phase} agents"},
                {"step": 4, "action": f"Load Phase {to_phase} context"},
                {"step": 5, "action": f"Start Phase {to_phase} execution"},
            ],
            "artifacts_to_preserve": context.get("artifacts", []),
            "stakeholder_notifications": context.get("stakeholders", []),
        }

        return {
            "success": True,
            "artifact_type": "phase_transition_plan",
            "content": transition_plan,
        }

    async def _manage_agents(
        self,
        task: str,
        context: dict[str, Any],
    ) -> dict[str, Any]:
        agent_type = context.get("agent_type", "")
        action = context.get("action", "spawn")

        agent_management = {
            "action": action,
            "agent_type": agent_type,
            "available_agents": {
                "vision": {"phase": 1, "status": "available"},
                "requirements": {"phase": 2, "status": "available"},
                "architecture": {"phase": 3, "status": "available"},
                "planning": {"phase": 4, "status": "available"},
                "development": {"phase": 5, "status": "available"},
                "quality": {"phase": 6, "status": "available"},
                "deployment": {"phase": 7, "status": "available"},
                "operations": {"phase": 8, "status": "available"},
            },
            "current_active": context.get("active_agents", []),
        }

        return {
            "success": True,
            "artifact_type": "agent_management",
            "content": agent_management,
        }

    async def _orchestrate_workflow(
        self,
        task: str,
        context: dict[str, Any],
    ) -> dict[str, Any]:
        workflow = {
            "name": context.get("workflow_name", "lifecycle_workflow"),
            "stages": [
                {"stage": "init", "agents": [], "parallel": False},
                {"stage": "vision", "agents": ["vision"], "parallel": False},
                {"stage": "requirements", "agents": ["requirements"], "parallel": False},
                {"stage": "architecture", "agents": ["architecture"], "parallel": False},
                {"stage": "planning", "agents": ["planning"], "parallel": False},
                {"stage": "development", "agents": ["development"], "parallel": True},
                {"stage": "quality", "agents": ["quality"], "parallel": True},
                {"stage": "deployment", "agents": ["deployment"], "parallel": False},
                {"stage": "operations", "agents": ["operations"], "parallel": False},
            ],
            "current_stage": context.get("current_stage", "init"),
            "dependencies": context.get("dependencies", {}),
        }

        return {
            "success": True,
            "artifact_type": "workflow_orchestration",
            "content": workflow,
        }

    async def _track_progress(
        self,
        task: str,
        context: dict[str, Any],
    ) -> dict[str, Any]:
        progress = {
            "project": context.get("project", "current"),
            "phases": {
                1: {"status": "completed", "artifacts": 0},
                2: {"status": "completed", "artifacts": 0},
                3: {"status": "completed", "artifacts": 0},
                4: {"status": "completed", "artifacts": 0},
                5: {"status": "in_progress", "artifacts": 0},
                6: {"status": "pending", "artifacts": 0},
                7: {"status": "pending", "artifacts": 0},
                8: {"status": "pending", "artifacts": 0},
            },
            "overall_progress": "62.5%",
            "active_agents": context.get("active_agents", []),
            "blockers": context.get("blockers", []),
            "next_milestones": [
                "Complete Phase 5",
                "Start Quality Validation",
                "Prepare for Deployment",
            ],
        }

        return {
            "success": True,
            "artifact_type": "progress_report",
            "content": progress,
        }

    async def _general_orchestration_task(
        self,
        task: str,
        context: dict[str, Any],
    ) -> dict[str, Any]:
        return {
            "success": True,
            "task": task,
            "recommendations": [
                "Coordinate phase transitions",
                "Manage agent lifecycle",
                "Orchestrate cross-phase workflows",
                "Track overall progress",
                "Allocate resources across phases",
            ],
            "context_used": bool(context),
        }
