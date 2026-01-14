# Unified Enterprise Lifecycle MCP Server

MCP (Model Context Protocol) server that provides lifecycle-specific tools to Claude Code.

## Installation

```bash
cd .claude/mcp-server
npm install
```

## Available Tools

| Tool | Description |
|------|-------------|
| `lifecycle_initialize_project` | Initialize a new lifecycle project |
| `lifecycle_execute_phase` | Execute a specific phase |
| `lifecycle_create_artifact` | Create artifact with traceability ID |
| `lifecycle_update_feature` | Update feature status |
| `lifecycle_validate_quality_gate` | Validate quality gates |
| `lifecycle_run_security_scan` | Run security scans |
| `lifecycle_get_project_state` | Get project state |
| `lifecycle_search_artifacts` | Search artifacts |
| `lifecycle_go_no_go` | Execute go/no-go decision |

## Usage

The MCP server is automatically configured in `.claude/settings.json`:

```json
{
  "mcpServers": {
    "lifecycle-tools": {
      "command": "node",
      "args": [".claude/mcp-server/index.js"]
    }
  }
}
```

## Development

```bash
# Watch mode for development
npm run dev

# Test
npm test
```

## Architecture

```
.claude/mcp-server/
├── package.json       # Dependencies and scripts
├── index.js           # Main MCP server implementation
├── README.md          # This file
└── node_modules/      # Installed dependencies
```
