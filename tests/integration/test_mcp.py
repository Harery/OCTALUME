"""Integration tests for MCP Server."""

import pytest
import json
from unittest.mock import Mock, AsyncMock, patch

from octalume.mcp.server import OctalumeMCPServer, TOOLS


class TestMCPServerInitialization:
    def test_server_creates_successfully(self):
        server = OctalumeMCPServer()
        assert server is not None

    def test_server_has_all_tools_registered(self):
        expected_count = 30
        assert len(TOOLS) >= expected_count, f"Expected at least {expected_count} tools, got {len(TOOLS)}"

    def test_all_tools_have_required_fields(self):
        for tool in TOOLS:
            assert "name" in tool, "Tool missing 'name'"
            assert "description" in tool, f"Tool {tool.get('name')} missing 'description'"
            assert "input_schema" in tool, f"Tool {tool.get('name')} missing 'input_schema'"


class TestPhaseTools:
    @pytest.mark.asyncio
    async def test_phase_start_tool_exists(self):
        tool_names = [t["name"] for t in TOOLS]
        assert "lifecycle_phase_start" in tool_names

    @pytest.mark.asyncio
    async def test_phase_status_tool_exists(self):
        tool_names = [t["name"] for t in TOOLS]
        assert "lifecycle_phase_status" in tool_names

    @pytest.mark.asyncio
    async def test_phase_validate_tool_exists(self):
        tool_names = [t["name"] for t in TOOLS]
        assert "lifecycle_phase_validate" in tool_names


class TestAgentTools:
    def test_agent_spawn_tool_schema(self):
        spawn_tool = next((t for t in TOOLS if t["name"] == "lifecycle_agent_spawn"), None)
        assert spawn_tool is not None
        assert "agent_type" in spawn_tool["input_schema"]["properties"]
        assert "task" in spawn_tool["input_schema"]["properties"]

    def test_agent_types_are_enum(self):
        spawn_tool = next((t for t in TOOLS if t["name"] == "lifecycle_agent_spawn"), None)
        agent_type_prop = spawn_tool["input_schema"]["properties"]["agent_type"]
        assert "enum" in agent_type_prop
        expected_types = [
            "vision", "requirements", "architecture", "planning",
            "development", "quality", "deployment", "operations", "orchestrator"
        ]
        for t in expected_types:
            assert t in agent_type_prop["enum"]


class TestArtifactTools:
    def test_artifact_create_tool_schema(self):
        create_tool = next((t for t in TOOLS if t["name"] == "lifecycle_artifact_create"), None)
        assert create_tool is not None
        required = create_tool["input_schema"].get("required", [])
        assert "phase" in required
        assert "artifact_type" in required
        assert "name" in required


class TestComplianceTools:
    def test_compliance_scan_tool_schema(self):
        scan_tool = next((t for t in TOOLS if t["name"] == "lifecycle_compliance_scan"), None)
        assert scan_tool is not None
        standards_prop = scan_tool["input_schema"]["properties"]["standards"]
        assert "enum" in standards_prop["items"]
        expected_standards = ["hipaa", "soc2", "pci_dss", "gdpr", "sox", "dod_itar"]
        for s in expected_standards:
            assert s in standards_prop["items"]["enum"]


class TestMemoryTools:
    def test_memory_save_tool_exists(self):
        tool_names = [t["name"] for t in TOOLS]
        assert "lifecycle_memory_save" in tool_names

    def test_memory_load_tool_exists(self):
        tool_names = [t["name"] for t in TOOLS]
        assert "lifecycle_memory_load" in tool_names

    def test_memory_query_tool_exists(self):
        tool_names = [t["name"] for t in TOOLS]
        assert "lifecycle_memory_query" in tool_names


class TestGateTools:
    def test_gate_check_tool_schema(self):
        gate_tool = next((t for t in TOOLS if t["name"] == "lifecycle_gate_check"), None)
        assert gate_tool is not None
        props = gate_tool["input_schema"]["properties"]
        assert "phase_number" in props
        assert "gate_type" in props


class TestToolHandler:
    @pytest.mark.asyncio
    async def test_handle_tool_call_returns_text_content(self):
        server = OctalumeMCPServer()

        with patch.object(server, '_get_state') as mock_state:
            mock_state.return_value = Mock()

            result = await server._handle_tool_call("lifecycle_gate_list", {})

            assert len(result) == 1
            assert hasattr(result[0], "type")
            assert result[0].type == "text"

    @pytest.mark.asyncio
    async def test_unknown_tool_returns_error(self):
        server = OctalumeMCPServer()

        result = await server._handle_tool_call("unknown_tool", {})

        assert len(result) == 1
        data = json.loads(result[0].text)
        assert "error" in data
