"""Quality gate MCP tools."""

from typing import Any

from mcp.types import Tool

GATE_TOOLS: list[Tool] = [
    Tool(
        name="lifecycle_gate_check",
        description="Check if a quality gate passes",
        inputSchema={
            "type": "object",
            "properties": {
                "phase_number": {"type": "integer", "minimum": 1, "maximum": 8},
                "gate_type": {"type": "string", "enum": ["entry", "exit"]},
            },
            "required": ["phase_number"],
        },
    ),
    Tool(
        name="lifecycle_gate_bypass",
        description="Bypass a quality gate (if allowed)",
        inputSchema={
            "type": "object",
            "properties": {
                "phase_number": {"type": "integer", "minimum": 1, "maximum": 8},
                "reason": {"type": "string"},
                "approver": {"type": "string"},
            },
            "required": ["phase_number", "reason", "approver"],
        },
    ),
    Tool(
        name="lifecycle_gate_list",
        description="List all quality gate definitions",
        inputSchema={
            "type": "object",
            "properties": {},
        },
    ),
    Tool(
        name="lifecycle_go_no_go",
        description="Execute a go/no-go decision for phase transition",
        inputSchema={
            "type": "object",
            "properties": {
                "phase_number": {"type": "integer", "minimum": 1, "maximum": 8},
            },
            "required": ["phase_number"],
        },
    ),
]


def register_gate_tools(server: Any) -> None:
    for tool in GATE_TOOLS:
        server.add_tool(tool)
