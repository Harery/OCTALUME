---
name: "lifecycle_tool_search"
description: "Tool search and discovery system for Unified Enterprise Lifecycle. Enables agents to find and load tools on-demand, preserving context window capacity."
type: "tool_search"
version: "1.0.0"
---

# LIFECYCLE TOOL SEARCH SYSTEM

**Dynamic Tool Discovery for Enterprise Development**

Based on Anthropic's "Advanced Tool Use" research, this system enables agents to discover and load tools on-demand, reducing context consumption by up to 85%.

---

## TOOL SEARCH ARCHITECTURE

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    TOOL SEARCH AND DISCOVERY SYSTEM                         │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  START                                                                     │
│    │                                                                        │
│    ▼                                                                        │
│  ┌──────────────────┐                                                      │
│  │ Agent Needs Tool │                                                      │
│  └────────┬─────────┘                                                      │
│           │                                                                │
│           ▼                                                                │
│  ┌────────────────────────────────────────────────────────────────────┐    │
│  │              Search Available Tools                                │    │
│  │  ┌──────────────────────────────────────────────────────────────┐ │    │
│  │  │ tool_search_tool_regex                                        │ │    │
│  │  │ - Search by name and description                             │ │    │
│  │  │ - Returns matching tool references                           │ │    │
│  │  └──────────────────────────────────────────────────────────────┘ │    │
│  │  ┌──────────────────────────────────────────────────────────────┐ │    │
│  │  │ tool_search_tool_bm25                                        │ │    │
│  │  │ - Semantic search                                           │ │    │
│  │  │ - Better for fuzzy matching                                 │ │    │
│  │  └──────────────────────────────────────────────────────────────┘ │    │
│  │  ┌──────────────────────────────────────────────────────────────┐ │    │
│  │  │ tool_search_custom                                           │ │    │
│  │  │ - Embedding-based search                                     │ │    │
│  │  │ - Custom ranking                                             │ │    │
│  │  └──────────────────────────────────────────────────────────────┘ │    │
│  └────────────────────────────────────────────────────────────────────┘    │
│           │                                                                │
│           ▼                                                                │
│  ┌────────────────────────────────────────────────────────────────────┐    │
│  │              Expand Tool Definitions                               │    │
│  │  - Load full tool definitions into context                         │    │
│  │  - Only load tools that were found in search                       │    │
│  └────────────────────────────────────────────────────────────────────┘    │
│           │                                                                │
│           ▼                                                                │
│  ┌──────────────────┐                                                      │
│  │ Agent Uses Tool  │                                                      │
│  └──────────────────┘                                                      │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## TOOL DEFINITION FORMAT

All lifecycle tools use this format with `defer_loading`:

```json
{
  "name": "lifecycle_phase_transition",
  "description": "Execute phase transition with quality gate validation. Checks exit criteria of current phase and entry criteria of next phase, updates project state, and archives artifacts.",
  "input_schema": {
    "type": "object",
    "properties": {
      "current_phase": {
        "type": "string",
        "description": "Current phase ID (e.g., phase_01_vision_strategy)"
      },
      "next_phase": {
        "type": "string",
        "description": "Next phase ID (e.g., phase_02_requirements_scope)"
      },
      "artifacts": {
        "type": "array",
        "items": {"type": "string"},
        "description": "List of artifact IDs created in current phase"
      }
    },
    "required": ["current_phase", "next_phase"]
  },
  "defer_loading": true,
  "examples": [
    {
      "current_phase": "phase_01_vision_strategy",
      "next_phase": "phase_02_requirements_scope",
      "artifacts": ["P1-VISION-001", "P1-BUSINESS-001"]
    }
  ]
}
```

---

## TOOL CATEGORIES

### 1. Phase Tools (8 tools)

```json
{
  "tools": [
    {
      "name": "phase_01_vision_strategy",
      "description": "Execute Phase 1: Vision & Strategy. Creates PRD, business case, and aligns stakeholders.",
      "defer_loading": true
    },
    {
      "name": "phase_02_requirements_scope",
      "description": "Execute Phase 2: Requirements & Scope. Defines functional and non-functional requirements.",
      "defer_loading": true
    },
    {
      "name": "phase_03_architecture_design",
      "description": "Execute Phase 3: Architecture & Design. Creates system architecture and technical specifications.",
      "defer_loading": true
    },
    {
      "name": "phase_04_development_planning",
      "description": "Execute Phase 4: Development Planning. Creates WBS, resource plan, and sprint plan.",
      "defer_loading": true
    },
    {
      "name": "phase_05_development_execution",
      "description": "Execute Phase 5: Development Execution. Implements features in agile sprints.",
      "defer_loading": true
    },
    {
      "name": "phase_06_quality_security",
      "description": "Execute Phase 6: Quality & Security Validation. Runs tests, security scans, and UAT.",
      "defer_loading": true
    },
    {
      "name": "phase_07_deployment_release",
      "description": "Execute Phase 7: Deployment & Release. Deploys to production and validates.",
      "defer_loading": true
    },
    {
      "name": "phase_08_operations_maintenance",
      "description": "Execute Phase 8: Operations & Maintenance. Monitors, maintains, and improves system.",
      "defer_loading": true
    }
  ]
}
```

### 2. Governance Tools

```json
{
  "tools": [
    {
      "name": "governance_approve_go_no_go",
      "description": "Execute go/no-go decision for phase transition. Requires executive sponsor approval.",
      "defer_loading": true
    },
    {
      "name": "governance_create_change_request",
      "description": "Create change request for scope, timeline, or budget changes.",
      "defer_loading": true
    },
    {
      "name": "governance_escalate_issue",
      "description": "Escalate issue to next level (L1→L2→L3→L4).",
      "defer_loading": true
    },
    {
      "name": "governance_update_raci",
      "description": "Update RACI matrix for specific activity.",
      "defer_loading": true
    }
  ]
}
```

### 3. Security Tools

```json
{
  "tools": [
    {
      "name": "security_threat_model",
      "description": "Perform threat modeling using STRIDE, PASTA, or LINDDUN methodology.",
      "defer_loading": true
    },
    {
      "name": "security_sast_scan",
      "description": "Run Static Application Security Testing (SAST) scan on codebase.",
      "defer_loading": true
    },
    {
      "name": "security_dast_scan",
      "description": "Run Dynamic Application Security Testing (DAST) scan on running application.",
      "defer_loading": true
    },
    {
      "name": "security_sca_scan",
      "description": "Run Software Composition Analysis (SCA) scan for dependency vulnerabilities.",
      "defer_loading": true
    },
    {
      "name": "security_pen_test",
      "description": "Execute penetration testing (internal or external).",
      "defer_loading": true
    }
  ]
}
```

### 4. Quality Tools

```json
{
  "tools": [
    {
      "name": "quality_create_test_plan",
      "description": "Create comprehensive test plan for phase or feature.",
      "defer_loading": true
    },
    {
      "name": "quality_run_unit_tests",
      "description": "Run unit tests and generate coverage report.",
      "defer_loading": true
    },
    {
      "name": "quality_run_integration_tests",
      "description": "Run integration tests across components.",
      "defer_loading": true
    },
    {
      "name": "quality_run_e2e_tests",
      "description": "Run end-to-end tests with browser automation.",
      "defer_loading": true
    },
    {
      "name": "quality_performance_test",
      "description": "Run performance and load testing.",
      "defer_loading": true
    },
    {
      "name": "quality_defect_report",
      "description": "Create or update defect report with severity and priority.",
      "defer_loading": true
    }
  ]
}
```

### 5. Compliance Tools

```json
{
  "tools": [
    {
      "name": "compliance_identify_regulations",
      "description": "Identify applicable regulations (HIPAA, SOC 2, PCI DSS, GDPR, SOX, etc.).",
      "defer_loading": true
    },
    {
      "name": "compliance_create_matrix",
      "description": "Create compliance matrix mapping regulations to controls.",
      "defer_loading": true
    },
    {
      "name": "compliance_run_audit",
      "description": "Execute internal compliance audit.",
      "defer_loading": true
    },
    {
      "name": "compliance_evidence_collect",
      "description": "Collect evidence for compliance requirements.",
      "defer_loading": true
    }
  ]
}
```

### 6. Artifact Tools

```json
{
  "tools": [
    {
      "name": "artifact_create",
      "description": "Create artifact with traceability ID (P{N}-{SECTION}-###).",
      "defer_loading": true
    },
    {
      "name": "artifact_update",
      "description": "Update existing artifact with version history.",
      "defer_loading": true
    },
    {
      "name": "artifact_link",
      "description": "Link artifacts together (e.g., requirement → design → code → test).",
      "defer_loading": true
    },
    {
      "name": "artifact_search",
      "description": "Search artifacts by ID, phase, type, or content.",
      "defer_loading": true
    }
  ]
}
```

### 7. Documentation Tools

```json
{
  "tools": [
    {
      "name": "docs_create_prd",
      "description": "Create Product Requirements Document (PRD) template.",
      "defer_loading": true
    },
    {
      "name": "docs_create_architecture",
      "description": "Create architecture document with diagrams.",
      "defer_loading": true
    },
    {
      "name": "docs_create_test_plan",
      "description": "Create test plan document.",
      "defer_loading": true
    },
    {
      "name": "docs_create_user_story",
      "description": "Create user story with acceptance criteria.",
      "defer_loading": true
    }
  ]
}
```

---

## TOOL SEARCH USAGE

### Example 1: Agent Needs Security Tool

```python
# Agent searches for security tools
search_results = tool_search_regex("security threat model")

# Returns:
{
  "tools": [
    {
      "name": "security_threat_model",
      "description": "Perform threat modeling using STRIDE, PASTA, or LINDDUN methodology."
    }
  ]
}

# Agent now loads full definition of security_threat_model
tool_definition = load_tool("security_threat_model")

# Agent uses the tool
result = use_tool("security_threat_model", {
  "methodology": "STRIDE",
  "scope": "authentication_system"
})
```

### Example 2: Agent Needs Quality Tool

```python
# Agent searches for testing tools
search_results = tool_search_regex("test")

# Returns multiple matches:
{
  "tools": [
    {"name": "quality_run_unit_tests", "description": "Run unit tests..."},
    {"name": "quality_run_integration_tests", "description": "Run integration tests..."},
    {"name": "quality_run_e2e_tests", "description": "Run end-to-end tests..."},
    {"name": "quality_performance_test", "description": "Run performance testing..."}
  ]
}

# Agent selects the appropriate tool based on context
# For integration testing:
tool_definition = load_tool("quality_run_integration_tests")
```

### Example 3: Agent Needs Governance Tool

```python
# Agent searches for approval tools
search_results = tool_search_regex("approve go no go")

# Returns:
{
  "tools": [
    {
      "name": "governance_approve_go_no_go",
      "description": "Execute go/no-go decision for phase transition..."
    }
  ]
}

# Agent loads and uses the tool
tool_definition = load_tool("governance_approve_go_no_go")
result = use_tool("governance_approve_go_no_go", {
  "phase": "phase_01_vision_strategy",
  "approver": "Executive Sponsor"
})
```

---

## TOOL SEARCH STRATEGIES

### 1. Regex Search (tool_search_tool_regex)

**Best for**: Exact name matches, known tool names

```python
# Exact match
search_results = tool_search_regex("security_sast_scan")

# Partial match
search_results = tool_search_regex("sast")

# Multiple keywords
search_results = tool_search_regex("security.*scan")
```

### 2. BM25 Search (tool_search_tool_bm25)

**Best for**: Semantic similarity, fuzzy matching

```python
# Semantic search
search_results = tool_search_tool_bm25("check code for security issues")
# Returns: security_sast_scan, security_dast_scan, security_sca_scan

# Fuzzy match
search_results = tool_search_tool_bm25("testing")
# Returns: all quality testing tools
```

### 3. Custom Embedding Search

**Best for**: Complex queries, domain-specific matching

```python
# Complex query
search_results = tool_search_custom("how to verify compliance with HIPAA")
# Returns: compliance_identify_regulations, compliance_create_matrix, compliance_run_audit
```

---

## TOOL DISCOVERY PROMPT

When an agent needs to discover tools:

```
You need to find and use the appropriate tool for your task.

TOOL DISCOVERY PROCESS:
1. Search for tools using tool_search_tool_regex or tool_search_tool_bm25
2. Review search results
3. Select the most relevant tool
4. Load the full tool definition
5. Use the tool with appropriate parameters

EXAMPLE:
Task: "Perform threat modeling on authentication system"

Step 1: Search
> tool_search_tool_regex("threat model")
Result: security_threat_model

Step 2: Load
> load_tool("security_threat_model")

Step 3: Use
> security_threat_model(methodology="STRIDE", scope="authentication_system")

ALWAYS:
- Search for tools before using them
- Read the tool description carefully
- Use the tool with correct parameters
- Handle tool errors appropriately
```

---

## CONTEXT SAVINGS

### Without Tool Search

```
All 50+ tools loaded upfront: ~72,000 tokens
Conversation history: ~5,000 tokens
System prompt: ~3,000 tokens
----------------------------------------
Total context overhead: ~80,000 tokens
Available for task: ~120,000 tokens (200K context window)
```

### With Tool Search

```
Tool Search Tool only: ~500 tokens
Relevant tools (3-5): ~3,000 tokens
Conversation history: ~5,000 tokens
System prompt: ~3,000 tokens
----------------------------------------
Total context overhead: ~11,500 tokens
Available for task: ~188,500 tokens (200K context window)

SAVINGS: 85% reduction in tool overhead
```

---

## BEST PRACTICES

### 1. Use Descriptive Tool Names

```
 GOOD: "security_sast_scan"
 BAD: "scan_tool"
```

### 2. Write Clear Tool Descriptions

```
 GOOD: "Run Static Application Security Testing (SAST) scan on codebase to identify security vulnerabilities in source code."
 BAD: "Scan code"
```

### 3. Provide Tool Examples

```json
{
  "examples": [
    {
      "description": "Scan authentication module",
      "parameters": {
        "target": "src/auth/",
        "severity_threshold": "high"
      }
    }
  ]
}
```

### 4. Defer Non-Essential Tools

```json
{
  "defer_loading": true
}
```

### 5. Keep Core Tools Loaded

```json
{
  "name": "artifact_create",
  "defer_loading": false  // Always available
}
```

---

## SEE ALSO

- **Programmatic Tool Calling**: `PROGRAMMATIC_TOOLS.md` - Orchestrate tools via code
- **Tool Examples**: `TOOL_EXAMPLES.md` - Tool usage examples
- **Context Engineering**: `../CONTEXT_ENGINEERING.md` - Context optimization

---

**This tool search system implements Anthropic's advanced tool use research.**

---

---

**Version 1.0.0 | OCTALUME Enterprise Lifecycle Framework**
