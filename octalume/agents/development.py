"""Development agent for Phase 5 - Development Execution."""

from typing import Any

from octalume.agents.base import BaseAgent
from octalume.core.state import ProjectStateManager
from octalume.core.memory import MemoryBank


class DevelopmentAgent(BaseAgent):
    """Agent for Phase 5: Development Execution.

    Responsibilities:
    - Code implementation
    - Unit testing
    - Code review preparation
    - Technical documentation
    - Bug fixes
    """

    def __init__(
        self,
        state_manager: ProjectStateManager,
        memory: MemoryBank,
        agent_id: str = "development-agent",
    ):
        super().__init__(
            agent_id=agent_id,
            name="Development Agent",
            phase=5,
            capabilities=[
                "code_implementation",
                "unit_testing",
                "code_review",
                "technical_documentation",
                "bug_fixing",
                "refactoring",
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

        if "implement" in task_lower or "code" in task_lower:
            return await self._implement_feature(task, context)
        elif "test" in task_lower or "unit" in task_lower:
            return await self._create_unit_tests(task, context)
        elif "review" in task_lower:
            return await self._prepare_code_review(task, context)
        elif "doc" in task_lower:
            return await self._create_technical_docs(task, context)
        elif "bug" in task_lower or "fix" in task_lower:
            return await self._fix_bug(task, context)
        elif "refactor" in task_lower:
            return await self._refactor_code(task, context)
        else:
            return await self._general_development_task(task, context)

    async def _implement_feature(
        self,
        task: str,
        context: dict[str, Any],
    ) -> dict[str, Any]:
        feature = context.get("feature", {})

        implementation = {
            "feature_name": feature.get("name", "Unknown"),
            "files_to_create": [],
            "files_to_modify": [],
            "dependencies": context.get("dependencies", []),
            "implementation_steps": [
                "1. Create module structure",
                "2. Implement core logic",
                "3. Add error handling",
                "4. Write unit tests",
                "5. Update documentation",
            ],
            "estimated_effort": context.get("effort", "TBD"),
        }

        return {
            "success": True,
            "artifact_type": "implementation_plan",
            "content": implementation,
        }

    async def _create_unit_tests(
        self,
        task: str,
        context: dict[str, Any],
    ) -> dict[str, Any]:
        module = context.get("module", "")

        test_plan = {
            "module": module,
            "test_file": f"tests/test_{module.replace('.', '_')}.py",
            "test_cases": [
                {"name": "test_happy_path", "description": "Test normal operation"},
                {"name": "test_edge_cases", "description": "Test boundary conditions"},
                {"name": "test_error_handling", "description": "Test error scenarios"},
            ],
            "coverage_target": context.get("coverage_target", 80),
        }

        return {
            "success": True,
            "artifact_type": "unit_test_plan",
            "content": test_plan,
        }

    async def _prepare_code_review(
        self,
        task: str,
        context: dict[str, Any],
    ) -> dict[str, Any]:
        files = context.get("files", [])

        review_checklist = {
            "files": files,
            "checks": [
                "Code follows style guide",
                "Functions have clear purpose",
                "Error handling is comprehensive",
                "Tests are included",
                "Documentation is updated",
                "No security vulnerabilities",
                "No performance issues",
            ],
            "reviewers_needed": context.get("reviewers", 1),
        }

        return {
            "success": True,
            "artifact_type": "code_review_checklist",
            "content": review_checklist,
        }

    async def _create_technical_docs(
        self,
        task: str,
        context: dict[str, Any],
    ) -> dict[str, Any]:
        component = context.get("component", "")

        docs = {
            "component": component,
            "sections": [
                "Overview",
                "Architecture",
                "API Reference",
                "Configuration",
                "Examples",
                "Troubleshooting",
            ],
            "format": context.get("format", "markdown"),
        }

        return {
            "success": True,
            "artifact_type": "technical_documentation",
            "content": docs,
        }

    async def _fix_bug(
        self,
        task: str,
        context: dict[str, Any],
    ) -> dict[str, Any]:
        bug = context.get("bug", {})

        fix_plan = {
            "bug_id": bug.get("id", ""),
            "description": bug.get("description", ""),
            "root_cause": "To be analyzed",
            "fix_steps": [
                "1. Reproduce the bug",
                "2. Identify root cause",
                "3. Implement fix",
                "4. Add regression test",
                "5. Verify fix",
            ],
            "affected_files": bug.get("affected_files", []),
        }

        return {
            "success": True,
            "artifact_type": "bug_fix_plan",
            "content": fix_plan,
        }

    async def _refactor_code(
        self,
        task: str,
        context: dict[str, Any],
    ) -> dict[str, Any]:
        refactor_plan = {
            "scope": context.get("scope", "module"),
            "reason": context.get("reason", ""),
            "steps": [
                "1. Ensure tests exist and pass",
                "2. Make small incremental changes",
                "3. Run tests after each change",
                "4. Update documentation",
            ],
            "risks": [
                "Breaking existing functionality",
                "Introducing new bugs",
            ],
        }

        return {
            "success": True,
            "artifact_type": "refactor_plan",
            "content": refactor_plan,
        }

    async def _general_development_task(
        self,
        task: str,
        context: dict[str, Any],
    ) -> dict[str, Any]:
        return {
            "success": True,
            "task": task,
            "recommendations": [
                "Implement feature",
                "Write unit tests",
                "Prepare for code review",
                "Update documentation",
                "Fix any bugs",
            ],
            "context_used": bool(context),
        }
