"""Tests for MCP server."""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from octalume.mcp.server import OctalumeMCPServer, TOOLS


class TestMCPServer:
    def test_tools_count(self):
        assert len(TOOLS) >= 30

    def test_tool_names_follow_convention(self):
        for tool in TOOLS:
            assert tool["name"].startswith("lifecycle_")

    def test_all_tools_have_required_properties(self):
        for tool in TOOLS:
            assert "name" in tool
            assert "description" in tool
            assert "input_schema" in tool

    def test_phase_tools_exist(self):
        tool_names = [t["name"] for t in TOOLS]
        assert "lifecycle_phase_start" in tool_names
        assert "lifecycle_phase_status" in tool_names
        assert "lifecycle_phase_validate" in tool_names
        assert "lifecycle_phase_transition" in tool_names

    def test_agent_tools_exist(self):
        tool_names = [t["name"] for t in TOOLS]
        assert "lifecycle_agent_spawn" in tool_names
        assert "lifecycle_agent_list" in tool_names
        assert "lifecycle_agent_status" in tool_names

    def test_artifact_tools_exist(self):
        tool_names = [t["name"] for t in TOOLS]
        assert "lifecycle_artifact_create" in tool_names
        assert "lifecycle_artifact_search" in tool_names

    def test_gate_tools_exist(self):
        tool_names = [t["name"] for t in TOOLS]
        assert "lifecycle_gate_check" in tool_names
        assert "lifecycle_go_no_go" in tool_names

    def test_compliance_tools_exist(self):
        tool_names = [t["name"] for t in TOOLS]
        assert "lifecycle_compliance_scan" in tool_names
        assert "lifecycle_compliance_report" in tool_names


class TestMCPServerIntegration:
    @pytest.fixture
    def server(self, tmp_path):
        return OctalumeMCPServer(state_dir=tmp_path)

    def test_server_initialization(self, server):
        assert server.state_manager is not None
        assert server.memory_bank is not None
        assert server.gate_validator is not None
        assert server.orchestrator is not None
        assert server.engine is not None
