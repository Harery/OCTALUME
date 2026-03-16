"""Requirements agent for Phase 2 - Requirements and Scope."""

from typing import Any

from octalume.agents.base import BaseAgent
from octalume.core.memory import MemoryBank
from octalume.core.state import ProjectStateManager


class RequirementsAgent(BaseAgent):
    """Agent for Phase 2: Requirements and Scope.

    Responsibilities:
    - Requirements elicitation
    - User story creation
    - Acceptance criteria definition
    - Traceability matrix maintenance
    - MVP scope definition
    """

    def __init__(
        self,
        state_manager: ProjectStateManager,
        memory: MemoryBank,
        agent_id: str = "requirements-agent",
    ):
        super().__init__(
            agent_id=agent_id,
            name="Requirements Agent",
            phase=2,
            capabilities=[
                "requirements_elicitation",
                "user_story_creation",
                "acceptance_criteria",
                "traceability_matrix",
                "moscow_prioritization",
                "mvp_definition",
            ],
            state_manager=state_manager,
            memory=memory,
        )

    async def _execute_task(
        self,
        task: str,
        context: dict[str, Any],
    ) -> dict[str, Any]:
        """Execute requirements tasks."""
        task_lower = task.lower()

        if "functional" in task_lower and "requirement" in task_lower:
            return await self._create_functional_requirements(task, context)
        elif "non-functional" in task_lower or "nfr" in task_lower:
            return await self._create_non_functional_requirements(task, context)
        elif "user stor" in task_lower:
            return await self._create_user_stories(task, context)
        elif "security" in task_lower and "requirement" in task_lower:
            return await self._create_security_requirements(task, context)
        elif "traceability" in task_lower:
            return await self._create_traceability_matrix(task, context)
        elif "mvp" in task_lower or "scope" in task_lower:
            return await self._define_mvp_scope(task, context)
        else:
            return await self._general_requirements_task(task, context)

    async def _create_functional_requirements(
        self,
        task: str,
        context: dict[str, Any],
    ) -> dict[str, Any]:
        """Create functional requirements document."""
        features = context.get("features", [])

        requirements = []
        for i, feature in enumerate(features, 1):
            requirements.append(
                {
                    "id": f"FR-{i:03d}",
                    "description": feature.get("description", ""),
                    "priority": feature.get("priority", "medium"),
                    "source": feature.get("source", "stakeholder"),
                    "status": "draft",
                }
            )

        return {
            "success": True,
            "artifact_type": "functional_requirements",
            "content": {
                "total_requirements": len(requirements),
                "requirements": requirements,
                "categories": context.get("categories", []),
            },
        }

    async def _create_non_functional_requirements(
        self,
        task: str,
        context: dict[str, Any],
    ) -> dict[str, Any]:
        """Create non-functional requirements."""
        nfrs = {
            "performance": {
                "response_time": context.get("response_time", "< 200ms"),
                "throughput": context.get("throughput", "> 1000 req/s"),
                "concurrent_users": context.get("concurrent_users", "> 10000"),
            },
            "availability": {
                "uptime": context.get("uptime", "99.9%"),
                "mttr": context.get("mttr", "< 30 minutes"),
            },
            "security": {
                "authentication": "Required",
                "encryption": "TLS 1.3+",
                "compliance": context.get("compliance_standards", []),
            },
            "scalability": {
                "horizontal_scaling": "Supported",
                "auto_scaling": "Recommended",
            },
        }

        return {
            "success": True,
            "artifact_type": "non_functional_requirements",
            "content": nfrs,
        }

    async def _create_user_stories(
        self,
        task: str,
        context: dict[str, Any],
    ) -> dict[str, Any]:
        """Create user stories with acceptance criteria."""
        features = context.get("features", [])

        stories = []
        for i, feature in enumerate(features, 1):
            stories.append(
                {
                    "id": f"US-{i:03d}",
                    "as_a": feature.get("as_a", "user"),
                    "i_want": feature.get("i_want", feature.get("description", "")),
                    "so_that": feature.get("so_that", ""),
                    "acceptance_criteria": feature.get("acceptance_criteria", []),
                    "story_points": feature.get("story_points", "TBD"),
                    "priority": feature.get("priority", "medium"),
                }
            )

        return {
            "success": True,
            "artifact_type": "user_stories",
            "content": {
                "total_stories": len(stories),
                "stories": stories,
            },
        }

    async def _create_security_requirements(
        self,
        task: str,
        context: dict[str, Any],
    ) -> dict[str, Any]:
        """Create security requirements based on compliance standards."""
        standards = context.get("compliance_standards", [])

        security_reqs = {
            "authentication": [
                "Multi-factor authentication for admin access",
                "Password complexity requirements",
                "Session timeout configuration",
            ],
            "authorization": [
                "Role-based access control (RBAC)",
                "Least privilege principle",
                "Audit logging for access changes",
            ],
            "data_protection": [
                "Encryption at rest (AES-256)",
                "Encryption in transit (TLS 1.3)",
                "Data classification and handling",
            ],
            "audit_logging": [
                "All authentication events logged",
                "Data access logged",
                "System changes logged",
            ],
            "compliance_specific": {},
        }

        for standard in standards:
            if standard.lower() == "hipaa":
                security_reqs["compliance_specific"]["hipaa"] = [
                    "PHI access controls",
                    "Business associate agreements",
                    "Breach notification procedures",
                ]
            elif standard.lower() == "pci":
                security_reqs["compliance_specific"]["pci_dss"] = [
                    "Cardholder data protection",
                    "Vulnerability scanning",
                    "Penetration testing",
                ]
            elif standard.lower() == "gdpr":
                security_reqs["compliance_specific"]["gdpr"] = [
                    "Data subject rights implementation",
                    "Privacy by design",
                    "Data processing records",
                ]

        return {
            "success": True,
            "artifact_type": "security_requirements",
            "content": security_reqs,
            "standards_addressed": standards,
        }

    async def _create_traceability_matrix(
        self,
        task: str,
        context: dict[str, Any],
    ) -> dict[str, Any]:
        """Create requirements traceability matrix."""
        requirements = context.get("requirements", [])

        matrix = {
            "requirements": [],
            "trace_links": [],
        }

        for req in requirements:
            req_id = req.get("id", "")
            links = {
                "requirement_id": req_id,
                "linked_features": [],
                "linked_tests": [],
                "linked_code": [],
            }
            matrix["trace_links"].append(links)
            matrix["requirements"].append(req_id)

        return {
            "success": True,
            "artifact_type": "traceability_matrix",
            "content": matrix,
        }

    async def _define_mvp_scope(
        self,
        task: str,
        context: dict[str, Any],
    ) -> dict[str, Any]:
        """Define MVP scope using MoSCoW prioritization."""
        features = context.get("features", [])

        mvp = {
            "must_have": [],
            "should_have": [],
            "could_have": [],
            "wont_have": [],
        }

        for feature in features:
            priority = feature.get("priority", "could").lower()
            if priority == "must" or priority == "critical":
                mvp["must_have"].append(feature)
            elif priority == "should" or priority == "high":
                mvp["should_have"].append(feature)
            elif priority == "could" or priority == "medium":
                mvp["could_have"].append(feature)
            else:
                mvp["wont_have"].append(feature)

        return {
            "success": True,
            "artifact_type": "mvp_scope",
            "content": {
                "moscow": mvp,
                "mvp_features": mvp["must_have"],
                "timeline_estimate": "Based on must-have features",
            },
        }

    async def _general_requirements_task(
        self,
        task: str,
        context: dict[str, Any],
    ) -> dict[str, Any]:
        """Handle general requirements tasks."""
        return {
            "success": True,
            "task": task,
            "available_actions": [
                "create_functional_requirements",
                "create_non_functional_requirements",
                "create_user_stories",
                "create_security_requirements",
                "create_traceability_matrix",
                "define_mvp_scope",
            ],
        }
