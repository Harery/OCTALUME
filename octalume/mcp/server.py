"""OCTALUME MCP Server - 30+ tools for AI-native SDLC."""

import asyncio
import json
from pathlib import Path
from typing import Any

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

from octalume.core.engine import PhaseEngine
from octalume.core.gates import GateValidator
from octalume.core.orchestrator import AgentOrchestrator
from octalume.core.state import ProjectStateManager
from octalume.core.memory import MemoryBank
from octalume.core.models import (
    Artifact,
    ArtifactType,
    ComplianceStandard,
    ProjectState,
)
from octalume.compliance.scanner import ComplianceScanner
from octalume.utils.logging import get_logger

logger = get_logger(__name__)


TOOLS: list[dict[str, Any]] = [
    # Phase Orchestration Tools
    {
        "name": "lifecycle_phase_start",
        "description": "Start a specific phase in the SDLC lifecycle",
        "input_schema": {
            "type": "object",
            "properties": {
                "phase_number": {"type": "integer", "minimum": 1, "maximum": 8},
            },
            "required": ["phase_number"],
        },
    },
    {
        "name": "lifecycle_phase_status",
        "description": "Get detailed status of a specific phase",
        "input_schema": {
            "type": "object",
            "properties": {
                "phase_number": {"type": "integer", "minimum": 1, "maximum": 8},
            },
            "required": ["phase_number"],
        },
    },
    {
        "name": "lifecycle_phase_validate",
        "description": "Validate exit criteria for a phase",
        "input_schema": {
            "type": "object",
            "properties": {
                "phase_number": {"type": "integer", "minimum": 1, "maximum": 8},
            },
            "required": ["phase_number"],
        },
    },
    {
        "name": "lifecycle_phase_transition",
        "description": "Transition from current phase to the next",
        "input_schema": {
            "type": "object",
            "properties": {
                "artifacts": {"type": "array", "items": {"type": "object"}},
            },
        },
    },
    {
        "name": "lifecycle_phase_rollback",
        "description": "Rollback to a previous phase",
        "input_schema": {
            "type": "object",
            "properties": {
                "to_phase": {"type": "integer", "minimum": 1, "maximum": 7},
                "reason": {"type": "string"},
            },
            "required": ["to_phase", "reason"],
        },
    },

    # Agent Management Tools
    {
        "name": "lifecycle_agent_spawn",
        "description": "Spawn a new AI agent for a phase-specific task",
        "input_schema": {
            "type": "object",
            "properties": {
                "agent_type": {"type": "string", "enum": ["vision", "requirements", "architecture", "planning", "development", "quality", "deployment", "operations", "orchestrator"]},
                "task": {"type": "string"},
                "config": {"type": "object"},
            },
            "required": ["agent_type", "task"],
        },
    },
    {
        "name": "lifecycle_agent_delegate",
        "description": "Delegate a task to an existing agent",
        "input_schema": {
            "type": "object",
            "properties": {
                "agent_id": {"type": "string"},
                "task": {"type": "string"},
                "context": {"type": "object"},
            },
            "required": ["agent_id", "task"],
        },
    },
    {
        "name": "lifecycle_agent_status",
        "description": "Get status of a specific agent",
        "input_schema": {
            "type": "object",
            "properties": {
                "agent_id": {"type": "string"},
            },
            "required": ["agent_id"],
        },
    },
    {
        "name": "lifecycle_agent_list",
        "description": "List all agents, optionally filtered by phase or status",
        "input_schema": {
            "type": "object",
            "properties": {
                "phase": {"type": "integer", "minimum": 1, "maximum": 8},
                "status": {"type": "string", "enum": ["idle", "running", "completed", "failed", "timeout"]},
            },
        },
    },
    {
        "name": "lifecycle_agent_terminate",
        "description": "Terminate a running agent",
        "input_schema": {
            "type": "object",
            "properties": {
                "agent_id": {"type": "string"},
                "reason": {"type": "string"},
            },
            "required": ["agent_id"],
        },
    },

    # Artifact Tracking Tools
    {
        "name": "lifecycle_artifact_create",
        "description": "Create a new artifact with traceability ID",
        "input_schema": {
            "type": "object",
            "properties": {
                "phase": {"type": "integer", "minimum": 1, "maximum": 8},
                "artifact_type": {"type": "string", "enum": ["document", "code", "test", "configuration", "design", "report", "decision"]},
                "name": {"type": "string"},
                "content": {"type": ["string", "object"]},
                "file_path": {"type": "string"},
                "compliance_tags": {"type": "array", "items": {"type": "string"}},
            },
            "required": ["phase", "artifact_type", "name"],
        },
    },
    {
        "name": "lifecycle_artifact_get",
        "description": "Get an artifact by its ID",
        "input_schema": {
            "type": "object",
            "properties": {
                "artifact_id": {"type": "string"},
            },
            "required": ["artifact_id"],
        },
    },
    {
        "name": "lifecycle_artifact_search",
        "description": "Search artifacts by phase, type, or content",
        "input_schema": {
            "type": "object",
            "properties": {
                "phase": {"type": "integer", "minimum": 1, "maximum": 8},
                "artifact_type": {"type": "string"},
                "search_term": {"type": "string"},
                "limit": {"type": "integer", "default": 50},
            },
        },
    },
    {
        "name": "lifecycle_artifact_link",
        "description": "Link two artifacts together for traceability",
        "input_schema": {
            "type": "object",
            "properties": {
                "source_artifact_id": {"type": "string"},
                "target_artifact_id": {"type": "string"},
            },
            "required": ["source_artifact_id", "target_artifact_id"],
        },
    },

    # Quality Gate Tools
    {
        "name": "lifecycle_gate_check",
        "description": "Check if a quality gate passes",
        "input_schema": {
            "type": "object",
            "properties": {
                "phase_number": {"type": "integer", "minimum": 1, "maximum": 8},
                "gate_type": {"type": "string", "enum": ["entry", "exit"]},
            },
            "required": ["phase_number"],
        },
    },
    {
        "name": "lifecycle_gate_bypass",
        "description": "Bypass a quality gate (if allowed)",
        "input_schema": {
            "type": "object",
            "properties": {
                "phase_number": {"type": "integer", "minimum": 1, "maximum": 8},
                "reason": {"type": "string"},
                "approver": {"type": "string"},
            },
            "required": ["phase_number", "reason", "approver"],
        },
    },
    {
        "name": "lifecycle_gate_list",
        "description": "List all quality gate definitions",
        "input_schema": {
            "type": "object",
            "properties": {},
        },
    },
    {
        "name": "lifecycle_go_no_go",
        "description": "Execute a go/no-go decision for phase transition",
        "input_schema": {
            "type": "object",
            "properties": {
                "phase_number": {"type": "integer", "minimum": 1, "maximum": 8},
            },
            "required": ["phase_number"],
        },
    },

    # Compliance Tools
    {
        "name": "lifecycle_compliance_scan",
        "description": "Run a compliance scan against configured standards",
        "input_schema": {
            "type": "object",
            "properties": {
                "standards": {"type": "array", "items": {"type": "string", "enum": ["hipaa", "soc2", "pci_dss", "gdpr", "sox", "dod_itar"]}},
                "scope": {"type": "string", "enum": ["all", "artifacts", "processes", "documentation"]},
            },
        },
    },
    {
        "name": "lifecycle_compliance_report",
        "description": "Generate a compliance report",
        "input_schema": {
            "type": "object",
            "properties": {
                "standard": {"type": "string", "enum": ["hipaa", "soc2", "pci_dss", "gdpr", "sox", "dod_itar"]},
                "format": {"type": "string", "enum": ["json", "markdown", "html"]},
            },
            "required": ["standard"],
        },
    },
    {
        "name": "lifecycle_compliance_configure",
        "description": "Configure compliance standards for the project",
        "input_schema": {
            "type": "object",
            "properties": {
                "standards": {"type": "array", "items": {"type": "string", "enum": ["hipaa", "soc2", "pci_dss", "gdpr", "sox", "dod_itar"]}},
            },
            "required": ["standards"],
        },
    },

    # Project State Tools
    {
        "name": "lifecycle_project_init",
        "description": "Initialize a new OCTALUME project",
        "input_schema": {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "description": {"type": "string"},
                "compliance_standards": {"type": "array", "items": {"type": "string"}},
            },
            "required": ["name"],
        },
    },
    {
        "name": "lifecycle_project_status",
        "description": "Get complete project status summary",
        "input_schema": {
            "type": "object",
            "properties": {},
        },
    },
    {
        "name": "lifecycle_project_summary",
        "description": "Get a human-readable project summary",
        "input_schema": {
            "type": "object",
            "properties": {},
        },
    },

    # Memory & Context Tools
    {
        "name": "lifecycle_memory_save",
        "description": "Save a memory entry for long-term context",
        "input_schema": {
            "type": "object",
            "properties": {
                "category": {"type": "string", "enum": ["decisions", "progress", "blockers", "notes", "context"]},
                "key": {"type": "string"},
                "value": {"type": ["string", "object"]},
                "metadata": {"type": "object"},
            },
            "required": ["category", "key", "value"],
        },
    },
    {
        "name": "lifecycle_memory_load",
        "description": "Load a memory entry by category and key",
        "input_schema": {
            "type": "object",
            "properties": {
                "category": {"type": "string"},
                "key": {"type": "string"},
            },
            "required": ["category", "key"],
        },
    },
    {
        "name": "lifecycle_memory_query",
        "description": "Query memory entries",
        "input_schema": {
            "type": "object",
            "properties": {
                "category": {"type": "string"},
                "search_term": {"type": "string"},
                "limit": {"type": "integer", "default": 50},
            },
        },
    },

    # Observability Tools
    {
        "name": "lifecycle_trace_add",
        "description": "Add a trace entry for observability",
        "input_schema": {
            "type": "object",
            "properties": {
                "phase": {"type": "integer", "minimum": 1, "maximum": 8},
                "action": {"type": "string"},
                "artifact_id": {"type": "string"},
                "agent_id": {"type": "string"},
                "duration_ms": {"type": "number"},
                "metadata": {"type": "object"},
            },
            "required": ["phase", "action"],
        },
    },
    {
        "name": "lifecycle_trace_get",
        "description": "Get trace entries",
        "input_schema": {
            "type": "object",
            "properties": {
                "phase": {"type": "integer", "minimum": 1, "maximum": 8},
                "limit": {"type": "integer", "default": 100},
            },
        },
    },
    {
        "name": "lifecycle_health_check",
        "description": "Perform a health check on all agents",
        "input_schema": {
            "type": "object",
            "properties": {},
        },
    },

    # A2A Communication Tools
    {
        "name": "lifecycle_agent_message",
        "description": "Send a message from one agent to another",
        "input_schema": {
            "type": "object",
            "properties": {
                "from_agent": {"type": "string"},
                "to_agent": {"type": "string"},
                "message_type": {"type": "string"},
                "payload": {"type": "object"},
            },
            "required": ["from_agent", "to_agent", "message_type", "payload"],
        },
    },
    {
        "name": "lifecycle_agent_broadcast",
        "description": "Broadcast a message to multiple agents",
        "input_schema": {
            "type": "object",
            "properties": {
                "from_agent": {"type": "string"},
                "message_type": {"type": "string"},
                "payload": {"type": "object"},
                "phase_filter": {"type": "integer", "minimum": 1, "maximum": 8},
            },
            "required": ["from_agent", "message_type", "payload"],
        },
    },
]


class OctalumeMCPServer:
    """OCTALUME MCP Server with 30+ tools for AI-native SDLC."""

    def __init__(self, state_dir: Path | None = None):
        self.server = Server("octalume")
        self.state_manager = ProjectStateManager(state_dir)
        self.memory_bank = MemoryBank(state_dir / "memory" if state_dir else None)
        self.gate_validator = GateValidator(self.state_manager)
        self.orchestrator = AgentOrchestrator(self.state_manager)
        self.engine = PhaseEngine(
            self.state_manager,
            self.gate_validator,
            self.orchestrator,
        )
        self.compliance_scanner = ComplianceScanner()
        self._state: ProjectState | None = None

        self._register_tools()

    def _register_tools(self) -> None:
        """Register all MCP tools."""
        for tool_def in TOOLS:
            self.server.add_tool(Tool(**tool_def))

        self.server.set_tool_handler(self._handle_tool_call)
        logger.info("mcp_tools_registered", count=len(TOOLS))

    async def _get_state(self) -> ProjectState:
        """Get or load project state."""
        if self._state is None:
            self._state = await self.state_manager.get_or_create()
        return self._state

    async def _handle_tool_call(
        self,
        name: str,
        arguments: dict[str, Any],
    ) -> list[TextContent]:
        """Handle tool calls from Claude Code."""
        try:
            result = await self._dispatch_tool(name, arguments)
            return [TextContent(type="text", text=json.dumps(result, indent=2, default=str))]
        except Exception as e:
            logger.error("tool_call_error", tool=name, error=str(e))
            return [TextContent(type="text", text=json.dumps({"error": str(e)}, indent=2))]

    async def _dispatch_tool(self, name: str, args: dict[str, Any]) -> dict[str, Any]:
        """Dispatch tool call to appropriate handler."""
        state = await self._get_state()

        handlers = {
            "lifecycle_phase_start": self._phase_start,
            "lifecycle_phase_status": self._phase_status,
            "lifecycle_phase_validate": self._phase_validate,
            "lifecycle_phase_transition": self._phase_transition,
            "lifecycle_phase_rollback": self._phase_rollback,
            "lifecycle_agent_spawn": self._agent_spawn,
            "lifecycle_agent_delegate": self._agent_delegate,
            "lifecycle_agent_status": self._agent_status,
            "lifecycle_agent_list": self._agent_list,
            "lifecycle_agent_terminate": self._agent_terminate,
            "lifecycle_artifact_create": self._artifact_create,
            "lifecycle_artifact_get": self._artifact_get,
            "lifecycle_artifact_search": self._artifact_search,
            "lifecycle_artifact_link": self._artifact_link,
            "lifecycle_gate_check": self._gate_check,
            "lifecycle_gate_bypass": self._gate_bypass,
            "lifecycle_gate_list": self._gate_list,
            "lifecycle_go_no_go": self._go_no_go,
            "lifecycle_compliance_scan": self._compliance_scan,
            "lifecycle_compliance_report": self._compliance_report,
            "lifecycle_compliance_configure": self._compliance_configure,
            "lifecycle_project_init": self._project_init,
            "lifecycle_project_status": self._project_status,
            "lifecycle_project_summary": self._project_summary,
            "lifecycle_memory_save": self._memory_save,
            "lifecycle_memory_load": self._memory_load,
            "lifecycle_memory_query": self._memory_query,
            "lifecycle_trace_add": self._trace_add,
            "lifecycle_trace_get": self._trace_get,
            "lifecycle_health_check": self._health_check,
            "lifecycle_agent_message": self._agent_message,
            "lifecycle_agent_broadcast": self._agent_broadcast,
        }

        handler = handlers.get(name)
        if not handler:
            raise ValueError(f"Unknown tool: {name}")

        return await handler(state, args)

    async def _phase_start(self, state: ProjectState, args: dict[str, Any]) -> dict[str, Any]:
        phase_num = args["phase_number"]
        state = await self.engine.start_phase(state, phase_num)
        self._state = state
        phase = state.phases[phase_num]
        return {"success": True, "phase": phase.model_dump()}

    async def _phase_status(self, state: ProjectState, args: dict[str, Any]) -> dict[str, Any]:
        phase_num = args["phase_number"]
        return await self.engine.get_phase_status(state, phase_num)

    async def _phase_validate(self, state: ProjectState, args: dict[str, Any]) -> dict[str, Any]:
        phase_num = args["phase_number"]
        result = await self.gate_validator.validate_exit(state, phase_num)
        return result.model_dump()

    async def _phase_transition(self, state: ProjectState, args: dict[str, Any]) -> dict[str, Any]:
        artifacts_data = args.get("artifacts", [])
        artifacts = []
        for a in artifacts_data:
            artifacts.append(Artifact(
                id=a.get("id", f"P{state.current_phase}-ART-{len(state.artifacts)+1:03d}"),
                phase=state.current_phase,
                name=a["name"],
                artifact_type=ArtifactType(a.get("artifact_type", "document")),
                content=a.get("content"),
                file_path=a.get("file_path"),
            ))

        current = state.current_phase
        state, gate_result = await self.engine.transition_phase(state, current, current + 1)
        self._state = state
        return {"success": gate_result.passed, "gate_result": gate_result.model_dump()}

    async def _phase_rollback(self, state: ProjectState, args: dict[str, Any]) -> dict[str, Any]:
        to_phase = args["to_phase"]
        reason = args["reason"]
        state = await self.engine.rollback_phase(state, to_phase, reason)
        self._state = state
        return {"success": True, "current_phase": state.current_phase}

    async def _agent_spawn(self, state: ProjectState, args: dict[str, Any]) -> dict[str, Any]:
        agent_id = await self.orchestrator.spawn_agent(
            state=state,
            agent_type=args["agent_type"],
            task=args["task"],
            config=args.get("config"),
        )
        self._state = state
        return {"success": True, "agent_id": agent_id}

    async def _agent_delegate(self, state: ProjectState, args: dict[str, Any]) -> dict[str, Any]:
        task_id = await self.orchestrator.delegate_task(
            state=state,
            agent_id=args["agent_id"],
            task=args["task"],
            context=args.get("context"),
        )
        self._state = state
        return {"success": True, "task_id": task_id}

    async def _agent_status(self, state: ProjectState, args: dict[str, Any]) -> dict[str, Any]:
        return await self.orchestrator.get_agent_status(state, args["agent_id"])

    async def _agent_list(self, state: ProjectState, args: dict[str, Any]) -> dict[str, Any]:
        agents = await self.orchestrator.list_agents(
            state=state,
            phase=args.get("phase"),
            status=args.get("status"),
        )
        return {"agents": agents}

    async def _agent_terminate(self, state: ProjectState, args: dict[str, Any]) -> dict[str, Any]:
        result = await self.orchestrator.terminate_agent(
            state=state,
            agent_id=args["agent_id"],
            reason=args.get("reason", "manual_termination"),
        )
        self._state = state
        return {"success": result}

    async def _artifact_create(self, state: ProjectState, args: dict[str, Any]) -> dict[str, Any]:
        phase = args["phase"]
        artifact_type = ArtifactType(args["artifact_type"])

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
        counter = state.artifact_counter.get(section, 0) + 1

        artifact = Artifact(
            id=f"P{phase}-{section}-{counter:03d}",
            phase=phase,
            name=args["name"],
            artifact_type=artifact_type,
            content=args.get("content"),
            file_path=args.get("file_path"),
            compliance_tags=[ComplianceStandard(t) for t in args.get("compliance_tags", [])],
        )

        state.artifacts[artifact.id] = artifact
        state.phases[phase].artifacts.append(artifact.id)
        state.artifact_counter[section] = counter

        await self.state_manager.save(state)
        self._state = state

        return {"success": True, "artifact": artifact.model_dump()}

    async def _artifact_get(self, state: ProjectState, args: dict[str, Any]) -> dict[str, Any]:
        artifact_id = args["artifact_id"]
        if artifact_id not in state.artifacts:
            return {"error": f"Artifact not found: {artifact_id}"}
        return {"artifact": state.artifacts[artifact_id].model_dump()}

    async def _artifact_search(self, state: ProjectState, args: dict[str, Any]) -> dict[str, Any]:
        results = []
        for artifact in state.artifacts.values():
            if "phase" in args and artifact.phase != args["phase"]:
                continue
            if "artifact_type" in args and artifact.artifact_type.value != args["artifact_type"]:
                continue
            if "search_term" in args:
                term = args["search_term"].lower()
                if term not in artifact.name.lower():
                    if isinstance(artifact.content, str) and term not in artifact.content.lower():
                        continue
            results.append(artifact.model_dump())
            if len(results) >= args.get("limit", 50):
                break
        return {"artifacts": results, "count": len(results)}

    async def _artifact_link(self, state: ProjectState, args: dict[str, Any]) -> dict[str, Any]:
        source_id = args["source_artifact_id"]
        target_id = args["target_artifact_id"]

        if source_id not in state.artifacts:
            return {"error": f"Source artifact not found: {source_id}"}
        if target_id not in state.artifacts:
            return {"error": f"Target artifact not found: {target_id}"}

        if target_id not in state.artifacts[source_id].linked_artifacts:
            state.artifacts[source_id].linked_artifacts.append(target_id)
            await self.state_manager.save(state)
            self._state = state

        return {"success": True, "source": source_id, "target": target_id}

    async def _gate_check(self, state: ProjectState, args: dict[str, Any]) -> dict[str, Any]:
        phase_num = args["phase_number"]
        gate_type = args.get("gate_type", "exit")

        if gate_type == "entry":
            result = await self.gate_validator.validate_entry(state, phase_num)
        else:
            result = await self.gate_validator.validate_exit(state, phase_num)

        return result.model_dump()

    async def _gate_bypass(self, state: ProjectState, args: dict[str, Any]) -> dict[str, Any]:
        result = await self.gate_validator.bypass_gate(
            state=state,
            phase_num=args["phase_number"],
            reason=args["reason"],
            approver=args["approver"],
        )
        self._state = state
        return result.model_dump()

    async def _gate_list(self, state: ProjectState, args: dict[str, Any]) -> dict[str, Any]:
        return {"gates": self.gate_validator.list_all_gates()}

    async def _go_no_go(self, state: ProjectState, args: dict[str, Any]) -> dict[str, Any]:
        return await self.gate_validator.run_go_no_go(state, args["phase_number"])

    async def _compliance_scan(self, state: ProjectState, args: dict[str, Any]) -> dict[str, Any]:
        standards = [ComplianceStandard(s) for s in args.get("standards", [])]
        if not standards:
            standards = state.compliance_standards

        result = await self.compliance_scanner.scan(
            state=state,
            standards=standards,
            scope=args.get("scope", "all"),
        )
        return result

    async def _compliance_report(self, state: ProjectState, args: dict[str, Any]) -> dict[str, Any]:
        standard = ComplianceStandard(args["standard"])
        report = await self.compliance_scanner.generate_report(
            state=state,
            standard=standard,
            format=args.get("format", "json"),
        )
        return report

    async def _compliance_configure(self, state: ProjectState, args: dict[str, Any]) -> dict[str, Any]:
        state.compliance_standards = [ComplianceStandard(s) for s in args["standards"]]
        await self.state_manager.save(state)
        self._state = state
        return {"success": True, "standards": [s.value for s in state.compliance_standards]}

    async def _project_init(self, state: ProjectState, args: dict[str, Any]) -> dict[str, Any]:
        new_state = await self.state_manager.create(
            name=args["name"],
            description=args.get("description"),
            compliance_standards=args.get("compliance_standards"),
        )
        self._state = new_state
        return {"success": True, "project_id": str(new_state.id)}

    async def _project_status(self, state: ProjectState, args: dict[str, Any]) -> dict[str, Any]:
        return state.model_dump()

    async def _project_summary(self, state: ProjectState, args: dict[str, Any]) -> dict[str, Any]:
        return await self.state_manager.get_summary(state)

    async def _memory_save(self, state: ProjectState, args: dict[str, Any]) -> dict[str, Any]:
        entry_id = self.memory_bank.save(
            category=args["category"],
            key=args["key"],
            value=args["value"],
            metadata=args.get("metadata"),
        )
        return {"success": True, "entry_id": entry_id}

    async def _memory_load(self, state: ProjectState, args: dict[str, Any]) -> dict[str, Any]:
        value = self.memory_bank.load(args["category"], args["key"])
        return {"value": value}

    async def _memory_query(self, state: ProjectState, args: dict[str, Any]) -> dict[str, Any]:
        results = self.memory_bank.query(
            category=args.get("category"),
            search_term=args.get("search_term"),
            limit=args.get("limit", 50),
        )
        return {"results": results}

    async def _trace_add(self, state: ProjectState, args: dict[str, Any]) -> dict[str, Any]:
        trace_id = self.memory_bank.add_trace(
            phase=args["phase"],
            action=args["action"],
            artifact_id=args.get("artifact_id"),
            agent_id=args.get("agent_id"),
            duration_ms=args.get("duration_ms"),
            metadata=args.get("metadata"),
        )
        return {"success": True, "trace_id": trace_id}

    async def _trace_get(self, state: ProjectState, args: dict[str, Any]) -> dict[str, Any]:
        traces = self.memory_bank.get_traces(
            phase=args.get("phase"),
            limit=args.get("limit", 100),
        )
        return {"traces": traces}

    async def _health_check(self, state: ProjectState, args: dict[str, Any]) -> dict[str, Any]:
        return await self.orchestrator.health_check(state)

    async def _agent_message(self, state: ProjectState, args: dict[str, Any]) -> dict[str, Any]:
        message_id = await self.orchestrator.send_agent_message(
            state=state,
            from_agent=args["from_agent"],
            to_agent=args["to_agent"],
            message_type=args["message_type"],
            payload=args["payload"],
        )
        return {"success": True, "message_id": message_id}

    async def _agent_broadcast(self, state: ProjectState, args: dict[str, Any]) -> dict[str, Any]:
        message_ids = await self.orchestrator.broadcast_message(
            state=state,
            from_agent=args["from_agent"],
            message_type=args["message_type"],
            payload=args["payload"],
            phase_filter=args.get("phase_filter"),
        )
        return {"success": True, "message_ids": message_ids}


def create_server(state_dir: Path | None = None) -> OctalumeMCPServer:
    """Create an OCTALUME MCP server instance."""
    return OctalumeMCPServer(state_dir)


def run_server(state_dir: Path | None = None) -> None:
    """Run the OCTALUME MCP server."""
    server = create_server(state_dir)

    async def main() -> None:
        async with stdio_server() as (read_stream, write_stream):
            await server.server.run(
                read_stream,
                write_stream,
                server.server.create_initialization_options(),
            )

    asyncio.run(main())


if __name__ == "__main__":
    run_server()
