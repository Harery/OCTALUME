"""Phase orchestration MCP tools."""

from typing import Any

from mcp.types import Tool

PHASE_TOOLS: list[Tool] = [
    Tool(
        name="lifecycle_phase_start",
        description="Start a specific phase in the SDLC lifecycle",
        inputSchema={
            "type": "object",
            "properties": {
                "phase_number": {"type": "integer", "minimum": 1, "maximum": 8},
            },
            "required": ["phase_number"],
        },
    ),
    Tool(
        name="lifecycle_phase_status",
        description="Get detailed status of a specific phase",
        inputSchema={
            "type": "object",
            "properties": {
                "phase_number": {"type": "integer", "minimum": 1, "maximum": 8},
            },
            "required": ["phase_number"],
        },
    ),
    Tool(
        name="lifecycle_phase_validate",
        description="Validate exit criteria for a phase",
        inputSchema={
            "type": "object",
            "properties": {
                "phase_number": {"type": "integer", "minimum": 1, "maximum": 8},
            },
            "required": ["phase_number"],
        },
    ),
    Tool(
        name="lifecycle_phase_transition",
        description="Transition from current phase to the next",
        inputSchema={
            "type": "object",
            "properties": {
                "artifacts": {"type": "array", "items": {"type": "object"}},
            },
        },
    ),
    Tool(
        name="lifecycle_phase_rollback",
        description="Rollback to a previous phase",
        inputSchema={
            "type": "object",
            "properties": {
                "to_phase": {"type": "integer", "minimum": 1, "maximum": 7},
                "reason": {"type": "string"},
            },
            "required": ["to_phase", "reason"],
        },
    ),
]


def register_phase_tools(server: Any) -> None:
    for tool in PHASE_TOOLS:
        server.add_tool(tool)
