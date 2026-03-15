"""Artifact tracking MCP tools."""

from typing import Any

from mcp.types import Tool

ARTIFACT_TOOLS: list[Tool] = [
    Tool(
        name="lifecycle_artifact_create",
        description="Create a new artifact with traceability ID",
        inputSchema={
            "type": "object",
            "properties": {
                "phase": {"type": "integer", "minimum": 1, "maximum": 8},
                "artifact_type": {
                    "type": "string",
                    "enum": [
                        "document",
                        "code",
                        "test",
                        "configuration",
                        "design",
                        "report",
                        "decision",
                    ],
                },
                "name": {"type": "string"},
                "content": {"type": ["string", "object"]},
                "file_path": {"type": "string"},
                "compliance_tags": {"type": "array", "items": {"type": "string"}},
            },
            "required": ["phase", "artifact_type", "name"],
        },
    ),
    Tool(
        name="lifecycle_artifact_get",
        description="Get an artifact by its ID",
        inputSchema={
            "type": "object",
            "properties": {
                "artifact_id": {"type": "string"},
            },
            "required": ["artifact_id"],
        },
    ),
    Tool(
        name="lifecycle_artifact_search",
        description="Search artifacts by phase, type, or content",
        inputSchema={
            "type": "object",
            "properties": {
                "phase": {"type": "integer", "minimum": 1, "maximum": 8},
                "artifact_type": {"type": "string"},
                "search_term": {"type": "string"},
                "limit": {"type": "integer", "default": 50},
            },
        },
    ),
    Tool(
        name="lifecycle_artifact_link",
        description="Link two artifacts together for traceability",
        inputSchema={
            "type": "object",
            "properties": {
                "source_artifact_id": {"type": "string"},
                "target_artifact_id": {"type": "string"},
            },
            "required": ["source_artifact_id", "target_artifact_id"],
        },
    ),
]


def register_artifact_tools(server: Any) -> None:
    for tool in ARTIFACT_TOOLS:
        server.add_tool(tool)
