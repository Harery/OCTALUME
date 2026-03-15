"""Observability MCP tools."""

from typing import Any

from mcp.types import Tool

OBSERVABILITY_TOOLS: list[Tool] = [
    Tool(
        name="lifecycle_trace_add",
        description="Add a trace entry for observability",
        inputSchema={
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
    ),
    Tool(
        name="lifecycle_trace_get",
        description="Get trace entries",
        inputSchema={
            "type": "object",
            "properties": {
                "phase": {"type": "integer", "minimum": 1, "maximum": 8},
                "limit": {"type": "integer", "default": 100},
            },
        },
    ),
    Tool(
        name="lifecycle_health_check",
        description="Perform a health check on all agents",
        inputSchema={
            "type": "object",
            "properties": {},
        },
    ),
    Tool(
        name="lifecycle_agent_message",
        description="Send a message from one agent to another",
        inputSchema={
            "type": "object",
            "properties": {
                "from_agent": {"type": "string"},
                "to_agent": {"type": "string"},
                "message_type": {"type": "string"},
                "payload": {"type": "object"},
            },
            "required": ["from_agent", "to_agent", "message_type", "payload"],
        },
    ),
    Tool(
        name="lifecycle_agent_broadcast",
        description="Broadcast a message to multiple agents",
        inputSchema={
            "type": "object",
            "properties": {
                "from_agent": {"type": "string"},
                "message_type": {"type": "string"},
                "payload": {"type": "object"},
                "phase_filter": {"type": "integer", "minimum": 1, "maximum": 8},
            },
            "required": ["from_agent", "message_type", "payload"],
        },
    ),
]


def register_observability_tools(server: Any) -> None:
    for tool in OBSERVABILITY_TOOLS:
        server.add_tool(tool)
