"""Compliance MCP tools."""

from typing import Any

from mcp.types import Tool

COMPLIANCE_TOOLS: list[Tool] = [
    Tool(
        name="lifecycle_compliance_scan",
        description="Run a compliance scan against configured standards",
        inputSchema={
            "type": "object",
            "properties": {
                "standards": {
                    "type": "array",
                    "items": {
                        "type": "string",
                        "enum": ["hipaa", "soc2", "pci_dss", "gdpr", "sox", "dod_itar"],
                    },
                },
                "scope": {
                    "type": "string",
                    "enum": ["all", "artifacts", "processes", "documentation"],
                },
            },
        },
    ),
    Tool(
        name="lifecycle_compliance_report",
        description="Generate a compliance report",
        inputSchema={
            "type": "object",
            "properties": {
                "standard": {
                    "type": "string",
                    "enum": ["hipaa", "soc2", "pci_dss", "gdpr", "sox", "dod_itar"],
                },
                "format": {"type": "string", "enum": ["json", "markdown", "html"]},
            },
            "required": ["standard"],
        },
    ),
    Tool(
        name="lifecycle_compliance_configure",
        description="Configure compliance standards for the project",
        inputSchema={
            "type": "object",
            "properties": {
                "standards": {
                    "type": "array",
                    "items": {
                        "type": "string",
                        "enum": ["hipaa", "soc2", "pci_dss", "gdpr", "sox", "dod_itar"],
                    },
                },
            },
            "required": ["standards"],
        },
    ),
]


def register_compliance_tools(server: Any) -> None:
    for tool in COMPLIANCE_TOOLS:
        server.add_tool(tool)
