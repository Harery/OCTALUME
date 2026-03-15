"""Agent management MCP tools."""

from typing import Any

from mcp.types import Tool

AGENT_TOOLS: list[Tool] = [
    Tool(
        name="lifecycle_agent_spawn",
        description="Spawn a new AI agent for a phase-specific task",
        inputSchema={
            "type": "object",
            "properties": {
                "agent_type": {
                    "type": "string",
                    "enum": [
                        "vision",
                        "requirements",
                        "architecture",
                        "planning",
                        "development",
                        "quality",
                        "deployment",
                        "operations",
                        "orchestrator",
                    ],
                },
                "task": {"type": "string"},
                "config": {"type": "object"},
            },
            "required": ["agent_type", "task"],
        },
    ),
    Tool(
        name="lifecycle_agent_delegate",
        description="Delegate a task to an existing agent",
        inputSchema={
            "type": "object",
            "properties": {
                "agent_id": {"type": "string"},
                "task": {"type": "string"},
                "context": {"type": "object"},
            },
            "required": ["agent_id", "task"],
        },
    ),
    Tool(
        name="lifecycle_agent_status",
        description="Get status of a specific agent",
        inputSchema={
            "type": "object",
            "properties": {
                "agent_id": {"type": "string"},
            },
            "required": ["agent_id"],
        },
    ),
    Tool(
        name="lifecycle_agent_list",
        description="List all agents, optionally filtered by phase or status",
        inputSchema={
            "type": "object",
            "properties": {
                "phase": {"type": "integer", "minimum": 1, "maximum": 8},
                "status": {
                    "type": "string",
                    "enum": ["idle", "running", "completed", "failed", "timeout"],
                },
            },
        },
    ),
    Tool(
        name="lifecycle_agent_terminate",
        description="Terminate a running agent",
        inputSchema={
            "type": "object",
            "properties": {
                "agent_id": {"type": "string"},
                "reason": {"type": "string"},
            },
            "required": ["agent_id"],
        },
    ),
]


def register_agent_tools(server: Any) -> None:
    for tool in AGENT_TOOLS:
        server.add_tool(tool)
