"""Planning agent for Phase 4 - Development Planning."""

from typing import Any

from octalume.agents.base import BaseAgent
from octalume.core.memory import MemoryBank
from octalume.core.state import ProjectStateManager


class PlanningAgent(BaseAgent):
    """Agent for Phase 4: Development Planning.

    Responsibilities:
    - Work breakdown structure (WBS)
    - Resource planning
    - Sprint planning
    - Risk assessment
    - Timeline creation
    """

    def __init__(
        self,
        state_manager: ProjectStateManager,
        memory: MemoryBank,
        agent_id: str = "planning-agent",
    ):
        super().__init__(
            agent_id=agent_id,
            name="Planning Agent",
            phase=4,
            capabilities=[
                "wbs_creation",
                "resource_planning",
                "sprint_planning",
                "risk_assessment",
                "timeline_creation",
                "dependency_mapping",
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

        if "wbs" in task_lower or "work breakdown" in task_lower:
            return await self._create_wbs(task, context)
        elif "resource" in task_lower:
            return await self._plan_resources(task, context)
        elif "sprint" in task_lower:
            return await self._plan_sprints(task, context)
        elif "risk" in task_lower:
            return await self._assess_risks(task, context)
        elif "timeline" in task_lower or "schedule" in task_lower:
            return await self._create_timeline(task, context)
        else:
            return await self._general_planning_task(task, context)

    async def _create_wbs(
        self,
        task: str,
        context: dict[str, Any],
    ) -> dict[str, Any]:
        features = context.get("features", [])

        wbs = {
            "1.0": {"name": "Project", "children": {}},
        }

        for i, feature in enumerate(features, 1):
            feature_id = f"1.{i}"
            wbs["1.0"]["children"][feature_id] = {
                "name": feature.get("name", f"Feature {i}"),
                "children": {
                    f"{feature_id}.1": {"name": "Design", "effort_days": 2},
                    f"{feature_id}.2": {"name": "Development", "effort_days": 5},
                    f"{feature_id}.3": {"name": "Testing", "effort_days": 2},
                    f"{feature_id}.4": {"name": "Review", "effort_days": 1},
                },
            }

        return {
            "success": True,
            "artifact_type": "work_breakdown_structure",
            "content": wbs,
        }

    async def _plan_resources(
        self,
        task: str,
        context: dict[str, Any],
    ) -> dict[str, Any]:
        team = context.get("team", [])

        resource_plan = {
            "team_members": [],
            "allocations": {},
            "capacity": {
                "hours_per_sprint": 80,
                "sprints_planned": context.get("sprints", 6),
            },
        }

        for member in team:
            resource_plan["team_members"].append({
                "name": member.get("name", ""),
                "role": member.get("role", "Developer"),
                "allocation": member.get("allocation", "100%"),
            })

        return {
            "success": True,
            "artifact_type": "resource_plan",
            "content": resource_plan,
        }

    async def _plan_sprints(
        self,
        task: str,
        context: dict[str, Any],
    ) -> dict[str, Any]:
        sprint_duration = context.get("sprint_duration", 2)
        num_sprints = context.get("num_sprints", 6)

        sprints = []
        for i in range(1, num_sprints + 1):
            sprints.append({
                "sprint": i,
                "duration_weeks": sprint_duration,
                "goals": [],
                "capacity": context.get("capacity_per_sprint", 40),
                "features": [],
            })

        return {
            "success": True,
            "artifact_type": "sprint_plan",
            "content": {
                "sprints": sprints,
                "total_sprints": num_sprints,
                "sprint_duration_weeks": sprint_duration,
            },
        }

    async def _assess_risks(
        self,
        task: str,
        context: dict[str, Any],
    ) -> dict[str, Any]:
        risks = context.get("risks", [])

        default_risks = [
            {"id": "R-001", "description": "Resource availability", "probability": "Medium", "impact": "High"},
            {"id": "R-002", "description": "Scope creep", "probability": "High", "impact": "Medium"},
            {"id": "R-003", "description": "Technical complexity", "probability": "Medium", "impact": "Medium"},
            {"id": "R-004", "description": "Integration challenges", "probability": "Medium", "impact": "High"},
        ]

        risk_register = {
            "risks": risks or default_risks,
            "mitigation_strategies": {},
        }

        for risk in risk_register["risks"]:
            risk_register["mitigation_strategies"][risk["id"]] = "To be defined"

        return {
            "success": True,
            "artifact_type": "risk_register",
            "content": risk_register,
        }

    async def _create_timeline(
        self,
        task: str,
        context: dict[str, Any],
    ) -> dict[str, Any]:
        sprints = context.get("num_sprints", 6)
        sprint_duration = context.get("sprint_duration_weeks", 2)

        timeline = {
            "phases": [
                {"phase": "Sprint 1-2", "duration_weeks": sprint_duration * 2, "focus": "Foundation"},
                {"phase": "Sprint 3-4", "duration_weeks": sprint_duration * 2, "focus": "Core Features"},
                {"phase": "Sprint 5-6", "duration_weeks": sprint_duration * 2, "focus": "Polish & Testing"},
            ],
            "milestones": [
                {"name": "MVP Ready", "sprint": sprints // 2},
                {"name": "Feature Complete", "sprint": sprints - 1},
                {"name": "Release Ready", "sprint": sprints},
            ],
            "total_duration_weeks": sprints * sprint_duration,
        }

        return {
            "success": True,
            "artifact_type": "timeline",
            "content": timeline,
        }

    async def _general_planning_task(
        self,
        task: str,
        context: dict[str, Any],
    ) -> dict[str, Any]:
        return {
            "success": True,
            "task": task,
            "recommendations": [
                "Create Work Breakdown Structure",
                "Plan resource allocation",
                "Create sprint plan",
                "Assess project risks",
                "Create project timeline",
            ],
            "context_used": bool(context),
        }
