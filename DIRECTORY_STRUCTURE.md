# OCTALUME Directory Structure: Your File-by-File Guide

**Hello, curious explorer!** You're probably wondering, "What's actually in this framework, and where do I find things?" Great question! Think of this as your map to the OCTALUME treasure chest. We'll explore every drawer and shelf together.

---

## What You'll Find Here

This document is your complete guide to:
- Where files live (the directory map)
- What each file does (the descriptions)
- How files connect (the relationships)
- Naming conventions (so you know what's what)

**Who this is for:**
- **Developers** wanting to understand the framework's structure
- **DevOps Engineers** setting up OCTALUME in environments
- **Technical Leads** evaluating framework organization
- **System Administrators** managing OCTALUME deployments
- **Curious minds** who just want to know what makes OCTALUME tick

---

## Quick Overview: The Big Picture

Before we dive into details, here's how OCTALUME is organized:

```
OCTALUME/
├── 📄 Root files (guides, documentation)
├── 📁 .claude/ (framework brain & configuration)
└── 📁 skills/ (8 phase skills + 5 shared skills)
```

**Three main areas:**
1. **Root** — Documentation you'll reference often
2. **.claude/** — The framework's engine (agents, tools, settings)
3. **skills/** — Modular instructions for each phase and shared capabilities

---

## Table of Contents

Jump to what interests you:

1. **[Root Directory](#root-directory)** — Documentation files you'll use often
2. **[.claude/ Directory](#claude-directory)** — The framework's engine
3. **[skills/ Directory](#skills-directory)** — Phase and shared skills
4. **[File Descriptions](#file-descriptions)** — What each file does
5. **[Traceability Naming Convention](#traceability-naming-convention)** — How files are named
6. **[Statistics](#statistics)** — Numbers that matter

---

## Root Directory

**What's here:** The documentation you'll reference most often.

```
OCTALUME/
├── SETUP_GUIDE.md                 # How to get started with Claude Code
├── TESTING_GUIDE.md               # How to test on a fresh Linux system
├── FRAMEWORK_VISUALIZATION.md     # Visual diagrams of how everything works
├── DIRECTORY_STRUCTURE.md         # This file - your directory map
├── CLAUDE.md                      # Auto-loaded brain when you use Claude
├── .gitignore                     # What to ignore in git
├── .claude/                       # Framework engine (hidden directory)
└── skills/                        # All the skills (phase + shared)
```

### What These Files Do

| File | What It's For | When You'll Use It |
|------|---------------|-------------------|
| `SETUP_GUIDE.md` | Getting started guide | First time setting up |
| `TESTING_GUIDE.md` | Testing procedures | Verifying installation |
| `FRAMEWORK_VISUALIZATION.md` | Visual diagrams | Understanding workflows |
| `DIRECTORY_STRUCTURE.md` | This file! | Finding things |
| `CLAUDE.md` | Framework context | Auto-loads when you use Claude |
| `.gitignore` | Git exclusions | When committing to git |

<details>
<summary>💡 Why are these files at the root?</summary>

**Accessibility:** Put frequently-used files where they're easy to find.

**Convention:** Markdown files at root is a standard pattern—developers know to look there.

**Clonability:** When you clone OCTALUME, you immediately see the documentation without digging through folders.

**Auto-loading:** `CLAUDE.md` at root means Claude Code finds and loads it automatically.

</details>

---

## .claude/ Directory

**What's here:** The framework's engine—agents, tools, configuration, and enforcement systems.

```
.claude/
├── 📚 Documentation (4 files)
│   ├── ORCHESTRATOR.md            # How agents work together
│   ├── CONTEXT_ENGINEERING.md     # Managing information efficiently
│   ├── MEMORY_BANK.md             # Memory system docs
│   └── HOOKS.md                   # Event-driven automation
│
├── ⚙️ Configuration (1 file)
│   └── settings.json              # Claude Code settings
│
├── 🤖 Agents (3 files)
│   ├── INITIALIZER.md             # First-run setup agent
│   ├── CODING.md                  # Incremental development agent
│   └── agent-spawner.js           # Agent spawning mechanism
│
├── 🚦 Enforcement Systems (4 files)
│   ├── validators/
│   │   └── phase-gate-validator.js # Quality gate enforcement
│   ├── escalation/
│   │   └── escalation-manager.js   # Go/no-go decisions
│   ├── bindings/
│   │   └── task-skill-binder.js    # Connecting tasks to skills
│   └── handoff/
│       └── handoff-verify.js       # Phase transition verification
│
├── 💾 Memory Management (8 files)
│   ├── memory/
│   │   ├── memory-lock.js          # Prevents concurrent access issues
│   │   ├── state-sync.js           # Keeps files in sync
│   │   ├── memory.json             # Active memory storage
│   │   ├── load.sh                 # Load memory
│   │   ├── save.sh                 # Save memory
│   │   ├── search.sh               # Search memory
│   │   ├── list.sh                 # List memory contents
│   │   └── delete.sh               # Delete memory entries
│
├── ⌨️ Commands (4 files)
│   ├── commands/
│   │   ├── lifecycle-init.md       # Initialize new project
│   │   ├── lifecycle-phase.md      # Work on specific phase
│   │   ├── lifecycle-feature.md    # Work on specific feature
│   │   └── lifecycle-scan.md       # Security/compliance scan
│
├── 🪝 Hooks (3 files)
│   ├── hooks/
│   │   ├── user-prompt-submit.sh   # Before prompt submission
│   │   ├── pre-tool-use.sh         # Before tool use
│   │   └── post-tool-response.sh   # After tool response
│
├── 🔧 Tools (1 file)
│   └── tools/
│       └── TOOL_SEARCH.md          # Tool discovery system
│
├── 📋 Templates (2 files)
│   └── templates/
│       ├── example-project-state.json # Example project state
│       └── example-feature-list.json  # Example 50-feature list
│
├── 🌐 MCP Server (4 files)
│   └── mcp-server/
│       ├── index.js                # Server entry point
│       ├── package.json            # NPM configuration
│       ├── package-lock.json       # Dependency lock file
│       └── README.md               # MCP server docs
│
└── 🔐 Local Settings (1 file)
    └── local/
        └── settings.json           # Local Claude settings
```

### What These Components Do

<details>
<summary>📚 Documentation Files (ORCHESTRATOR, CONTEXT_ENGINEERING, etc.)</summary>

**ORCHESTRATOR.md**
- **What:** How multiple agents work together
- **Why:** Coordinated effort > chaos
- **Example:** Initializer creates project → Phase agent takes over → Coding agent writes code

**CONTEXT_ENGINEERING.md**
- **What:** Strategies for managing information efficiently
- **Why:** Claude has token limits—we need to be smart
- **Example:** 3-level loading (metadata → full skill → referenced files)

**MEMORY_BANK.md**
- **What:** How the memory system works
- **Why:** Remember things across sessions
- **Example:** Project decisions, block resolution, lessons learned

**HOOKS.md**
- **What:** Event-driven automation
- **Why:** Automate repetitive tasks
- **Example:** Before running a tool, validate permissions

</details>

<details>
<summary>🤖 Agent System (INITIALIZER, CODING, agent-spawner)</summary>

**INITIALIZER.md**
- **Job:** Set up new projects
- **Does:** Creates folders, generates features, initializes git
- **When:** First time you start a project
- **Example:** You say "Initialize a project" → Initializer creates everything

**CODING.md**
- **Job:** Write code one feature at a time
- **Does:** Writes, tests, commits code
- **When:** Working on features in Phase 5
- **Example:** You say "Work on feature F-001" → Coding agent implements it

**agent-spawner.js**
- **Job:** Spawn the right agent at the right time
- **Does:** Detects what you need, spawns appropriate agent
- **When:** Automatically (you don't manage this)
- **Example:** Phase changes → Spawns new phase agent

</details>

<details>
<summary>🚦 Enforcement Systems (validators, escalation, bindings, handoff)</summary>

**phase-gate-validator.js**
- **Job:** Enforce quality gates
- **Does:** Checks entry/exit criteria before phase transitions
- **Why:** Prevents skipping quality checks
- **Example:** Can't move to Phase 3 until Phase 2 requirements approved

**escalation-manager.js**
- **Job:** Handle go/no-go decisions
- **Does:** Gets approvals, escalates if needed
- **Why:** Important decisions need proper authority
- **Example:** No-Go at gate → Escalates to executive sponsor

**task-skill-binder.js**
- **Job:** Connect tasks to skills
- **Does:** Determines which skill handles which task
- **Why:** Right tool for the job
- **Example:** "Create PRD" → Binds to Phase 1 skill

**handoff-verify.js**
- **Job:** Verify phase transitions
- **Does:** Checks that everything is complete before moving on
- **Why:** Nothing left behind
- **Example:** All artifacts committed → All tests passing → Then move to next phase

</details>

<details>
<summary>💾 Memory System (memory-lock, state-sync, scripts)</summary>

**Why memory matters:**
- Projects span days/weeks
- You'll have multiple Claude sessions
- Memory ensures continuity

**memory-lock.js**
- **Problem:** Two sessions writing at once = corruption
- **Solution:** File-based locking
- **Result:** Safe concurrent access

**state-sync.js**
- **Problem:** Multiple files need to stay in sync
- **Solution:** Bidirectional synchronization
- **Result:** project-state.json ↔ feature_list.json ↔ claude-progress.txt

**Shell scripts (load, save, search, list, delete)**
- **Purpose:** Manual memory operations
- **When:** You need to inspect or manage memory directly
- **Example:** Search memory for past decisions

</details>

<details>
<summary>⌨️ Commands (lifecycle-init, lifecycle-phase, lifecycle-feature, lifecycle-scan)</summary>

**These are shortcuts—like CLI commands for OCTALUME.**

**lifecycle-init.md**
- **What:** Initialize a new project
- **When:** Starting fresh
- **Does:** Sets up structure, generates features, creates git repo
- **Example:** `/lifecycle-init` or ask Claude to initialize

**lifecycle-phase.md**
- **What:** Work on a specific phase
- **When:** You want to jump to a phase
- **Does:** Spawns phase agent, loads phase context
- **Example:** "Work on Phase 3"

**lifecycle-feature.md**
- **What:** Work on a specific feature
- **When:** Developing in Phase 5
- **Does:** Loads feature context, implements it
- **Example:** "Work on feature F-042"

**lifecycle-scan.md**
- **What:** Security/compliance scan
- **When:** Checking for issues
- **Does:** Analyzes code, docs, config for problems
- **Example:** "Run a security scan"

</details>

<details>
<summary>🪝 Hooks (user-prompt-submit, pre-tool-use, post-tool-response)</summary>

**Hooks are automation triggers—they run at specific events.**

**user-prompt-submit.sh**
- **When:** Before your prompt goes to Claude
- **Purpose:** Validate, enhance, or block prompts
- **Example:** Check for sensitive data in prompt

**pre-tool-use.sh**
- **When:** Before any tool runs
- **Purpose:** Validate permissions, prevent mistakes
- **Example:** Confirm before deleting files

**post-tool-response.sh**
- **When:** After tool completes
- **Purpose:** Process results, trigger actions
- **Example:** Log tool usage for audit

</details>

<details>
<summary>🌐 MCP Server (index.js, package.json, etc.)</summary>

**MCP = Model Context Protocol — A standardized way for Claude to talk to external tools.**

**index.js**
- **What:** Server entry point
- **Does:** Starts server, registers tools, handles requests
- **Why:** Enables Claude to query project state

**package.json**
- **What:** NPM configuration
- **Does:** Defines dependencies, scripts, metadata
- **Why:** Node.js knows how to run the server

**package-lock.json**
- **What:** Dependency lock file
- **Does:** Exact versions of all dependencies
- **Why:** Reproducible installs

**README.md**
- **What:** MCP server documentation
- **Does:** Explains server, tools, usage
- **Why:** Developers need to know how to use it

**What the server provides:**
- 9 lifecycle management tools
- Project state queries
- Traceability lookups
- Feature list management

</details>

---

## skills/ Directory

**What's here:** Modular instructions for each phase + shared capabilities that cut across all phases.

```
skills/
├── 📊 Phase Skills (8 phases)
│   ├── phase_01_vision_strategy/
│   │   ├── SKILL.md                   # Phase 1 instructions
│   │   ├── templates/
│   │   │   ├── business-case-template.md
│   │   │   └── prd-template.md
│   │   └── examples/
│   │       └── sample-business-case.md
│   │
│   ├── phase_02_requirements_scope/
│   │   └── SKILL.md                   # Phase 2 instructions
│   │
│   ├── phase_03_architecture_design/
│   │   └── SKILL.md                   # Phase 3 instructions
│   │
│   ├── phase_04_development_planning/
│   │   └── SKILL.md                   # Phase 4 instructions
│   │
│   ├── phase_05_development_execution/
│   │   └── SKILL.md                   # Phase 5 instructions
│   │
│   ├── phase_06_quality_security/
│   │   └── SKILL.md                   # Phase 6 instructions
│   │
│   ├── phase_07_deployment_release/
│   │   └── SKILL.md                   # Phase 7 instructions
│   │
│   └── phase_08_operations_maintenance/
│       └── SKILL.md                   # Phase 8 instructions
│
└── 🌐 Shared Skills (5 cross-cutting skills)
    ├── roles/
    │   └── SKILL.md                   # All 16 role definitions
    ├── security/
    │   └── SKILL.md                   # Security framework
    ├── quality/
    │   └── SKILL.md                   # Quality framework
    ├── compliance/
    │   └── SKILL.md                   # Compliance framework
    └── governance/
        └── SKILL.md                   # Decision-making framework
```

### Phase Skills: What Each Does

| Phase | Skill File | Owner | Key Deliverables |
|:-----:|------------|-------|------------------|
| 1 | `phase_01_vision_strategy/SKILL.md` | Product Owner | PRD, Business Case, Market Analysis |
| 2 | `phase_02_requirements_scope/SKILL.md` | Product Owner | Requirements, NFRs, Traceability Matrix |
| 3 | `phase_03_architecture_design/SKILL.md` | CTA | System Architecture, Security Design |
| 4 | `phase_04_development_planning/SKILL.md` | Project Manager | WBS, Resource Plan, Sprint Plan |
| 5 | `phase_05_development_execution/SKILL.md` | Tech Lead | Code, Reviews, Unit Tests |
| 6 | `phase_06_quality_security/SKILL.md` | QA Lead | QA Testing, Security, UAT |
| 7 | `phase_07_deployment_release/SKILL.md` | DevOps | Deployment, Release, Rollback |
| 8 | `phase_08_operations_maintenance/SKILL.md` | SRE | Monitoring, Incidents, Maintenance |

### Shared Skills: Cross-Cutting Capabilities

| Skill | What It Provides |
|-------|------------------|
| `shared/roles/SKILL.md` | All 16 role definitions (who does what) |
| `shared/security/SKILL.md` | Security framework (threats, controls, best practices) |
| `shared/quality/SKILL.md` | Quality framework (testing, metrics, standards) |
| `shared/compliance/SKILL.md` | Compliance framework (regulations, audits, controls) |
| `shared/governance/SKILL.md` | Governance framework (decisions, RACI, authority) |

<details>
<summary>🔗 Why are some skills "shared"?</summary>

**Shared skills = Cross-cutting concerns**

These aren't tied to a specific phase—they're used everywhere:

**Security Example:**
- Phase 1: Security considerations in vision
- Phase 2: Security requirements
- Phase 3: Security architecture
- Phase 4: Security planning
- Phase 5: Secure coding
- Phase 6: Security testing
- Phase 7: Secure deployment
- Phase 8: Security operations

**Without shared skills:** Repeat security guidance 8 times (and keep it in sync)
**With shared skills:** Define once, reference everywhere

**Same logic applies to:**
- Quality (testing, metrics, standards)
- Compliance (regulations, audits)
- Governance (decisions, authority)
- Roles (who does what)

</details>

---

## File Descriptions

### Root-Level Files

| File | Purpose | When You'll Use It |
|------|---------|-------------------|
| `SETUP_GUIDE.md` | Getting started with Claude Code | First-time setup |
| `TESTING_GUIDE.md` | Testing on fresh Linux | Verifying installation |
| `FRAMEWORK_VISUALIZATION.md` | Visual diagrams | Understanding workflows |
| `DIRECTORY_STRUCTURE.md` | This file | Finding things |
| `CLAUDE.md` | Framework context | Auto-loads (you'll see the effects) |
| `.gitignore` | Git exclusions | When committing to git |

### Core Documentation

| File | What It Covers | Key Insights |
|------|----------------|--------------|
| `ORCHESTRATOR.md` | Multi-agent system | How agents coordinate |
| `CONTEXT_ENGINEERING.md` | Context management | How information is organized |
| `MEMORY_BANK.md` | Memory system | How OCTALUME remembers |
| `HOOKS.md` | Event automation | How triggers work |

### Agent System

| File | Role | What It Does |
|------|------|--------------|
| `INITIALIZER.md` | First-run agent | Creates new projects |
| `CODING.md` | Development agent | Writes code incrementally |
| `agent-spawner.js` | Agent manager | Spawns right agent at right time |

### Enforcement & Quality

| File | Purpose | What It Prevents |
|------|---------|------------------|
| `phase-gate-validator.js` | Quality gate enforcement | Skipping quality checks |
| `escalation-manager.js` | Go/no-go decisions | Unapproved phase transitions |
| `task-skill-binder.js` | Task-skill mapping | Using wrong tools |
| `handoff-verify.js` | Handoff verification | Incomplete phase transitions |

### Memory Management

| File | Purpose | When Used |
|------|---------|----------|
| `memory-lock.js` | Concurrent access safety | Multiple sessions |
| `state-sync.js` | File synchronization | Keeping state consistent |
| `memory.json` | Active memory store | Storing project memory |
| `load.sh` | Load memory | Manual memory load |
| `save.sh` | Save memory | Manual memory save |
| `search.sh` | Search memory | Find past decisions |
| `list.sh` | List memory | See what's stored |
| `delete.sh` | Delete memory | Remove old entries |

### Commands

| Command | Purpose | Example Usage |
|---------|---------|---------------|
| `lifecycle-init.md` | Initialize project | "Initialize a new project" |
| `lifecycle-phase.md` | Work on phase | "Work on Phase 3" |
| `lifecycle-feature.md` | Work on feature | "Implement feature F-001" |
| `lifecycle-scan.md` | Security scan | "Run security scan" |

### Hooks

| Hook | When It Runs | Purpose |
|------|-------------|---------|
| `user-prompt-submit.sh` | Before prompt | Validate/enhance prompts |
| `pre-tool-use.sh` | Before tool | Prevent mistakes |
| `post-tool-response.sh` | After tool | Process results |

### MCP Server

| File | Purpose |
|------|---------|
| `index.js` | Server entry point |
| `package.json` | NPM configuration |
| `package-lock.json` | Dependency lock |
| `README.md` | Server documentation |

---

## Traceability Naming Convention

**Every artifact follows: `P{N}-{SECTION}-###`**

This naming convention isn't arbitrary—it's how OCTALUME tracks everything from idea to production.

### The Pattern

```
P{N}-{SECTION}-{###}
 │   │        │
 │   │        └─ Sequential number (001, 002, 003...)
 │   └────────── Section type (VISION, REQ, ARCH, etc.)
 └────────────── Phase number (1-8)
```

### Examples by Phase

| Phase | Prefix | Example | What It Means |
|:-----:|--------|---------|---------------|
| 1 | `P1-VISION-###` | `P1-VISION-001` | Phase 1, Vision document, item 1 |
| 2 | `P2-REQ-###` | `P2-REQ-015` | Phase 2, Requirements, item 15 |
| 3 | `P3-ARCH-###` | `P3-ARCH-042` | Phase 3, Architecture, item 42 |
| 4 | `P4-PLAN-###` | `P4-PLAN-008` | Phase 4, Planning, item 8 |
| 5 | `P5-CODE-###` | `P5-CODE-789` | Phase 5, Code commit, item 789 |
| 6 | `P6-TEST-###` | `P6-TEST-123` | Phase 6, Test artifact, item 123 |
| 7 | `P7-DEPLOY-###` | `P7-DEPLOY-001` | Phase 7, Deployment, item 1 |
| 8 | `P8-OPS-###` | `P8-OPS-056` | Phase 8, Operations, item 56 |

### Why This Matters

**Traceability in action:**

```
Feature: "User login"
  → P2-REQ-042 (Login requirement)
    → P5-CODE-789 (Implementation)
      → P6-TEST-123 (Test)
        → P7-DEPLOY-045 (Deployment)
```

**Benefits:**
- **Debugging:** "When did we add this?" → Check the artifact ID
- **Compliance:** "Show me the requirement" → Follow the ID back
- **Impact analysis:** "What depends on this?" → Trace the ID forward

<details>
<summary>🔍 Real-world traceability example</summary>

**Scenario:** A security vulnerability is found in the password reset feature.

**Without traceability:**
- "I think Bob worked on password reset... maybe last year?"
- "Not sure which requirement this is for"
- "Good luck finding the test"

**With traceability:**
1. Start with: `P6-TEST-456` (Failed security test)
2. Trace back:
   - `P6-TEST-456` → `P5-CODE-789` (Code commit)
   - `P5-CODE-789` → `P2-REQ-123` (Requirement)
   - `P2-REQ-123` → `P1-VISION-012` (Business case)
3. Now you know:
   - **Who:** Commit author (from git)
   - **What:** Requirement details (from P2-REQ-123)
   - **Why:** Business justification (from P1-VISION-012)
   - **When:** All dates and versions

**Traceability = Complete audit trail**

</details>

---

## Statistics: The Numbers

**Ever wonder just how much stuff is in OCTALUME? Here are the numbers.**

### File Counts by Category

| Category | File Count | What It Means |
|----------|------------|---------------|
| Root Documentation Files | 5 | Guides you'll reference often |
| .claude/ Documentation | 4 | Framework internals explained |
| Agent Harnesses | 3 | Agents that do the work |
| Enforcement Systems | 4 | Quality gates & validation |
| Memory Scripts | 8 | Memory management tools |
| Commands | 4 | Shortcut commands |
| Hooks | 3 | Event automation triggers |
| Phase Skills | 8 | One per phase (1-8) |
| Shared Skills | 5 | Security, quality, compliance, etc. |
| Phase 1 Templates | 2 | Business case & PRD templates |
| Phase 1 Examples | 1 | Sample business case |
| MCP Server Files | 4 | Server + config + docs |

**Total: ~51 operational files**

### What This Tells You

**Complexity:** 51 files might seem like a lot, but consider:
- Each file has a specific purpose
- Files are organized logically
- You don't need to understand everything at once
- Start with what you need, learn the rest over time

**Modularity:**
- 8 phase skills (one per phase)
- 5 shared skills (cross-cutting concerns)
- 3 agents (specialized workers)
- 4 enforcement systems (quality control)

**Extensibility:**
- Easy to add new phases (just add a skill)
- Easy to add new shared skills (drop in skills/shared/)
- Easy to customize (change templates, examples)

---

## Navigating the Structure

**Here's how to find what you need:**

### "I want to..."

<details>
<summary>...understand a phase</summary>

**Go to:** `skills/phase_XX_*/SKILL.md`

**Example:**
```
skills/phase_01_vision_strategy/SKILL.md
```

**What you'll find:**
- Phase objectives
- Entry/exit criteria
- Deliverables
- Process steps

</details>

<details>
<summary>...understand a role</summary>

**Go to:** `skills/shared/roles/SKILL.md`

**What you'll find:**
- All 16 role definitions
- Responsibilities
- Decision authority
- Example scenarios

</details>

<details>
<summary>...set up a new project</summary>

**Go to:** `SETUP_GUIDE.md` or use `/lifecycle-init`

**What happens:**
- Initializer agent creates structure
- Generates 200-500 features
- Initializes git
- Creates configuration files

</details>

<details>
<summary>...troubleshoot an issue</summary>

**Check these files:**
1. `TESTING_GUIDE.md` — Is it a setup issue?
2. `FRAMEWORK_VISUALIZATION.md` — Is it a workflow issue?
3. `ORCHESTRATOR.md` — Is it an agent issue?
4. `CONTEXT_ENGINEERING.md` — Is it a context issue?

</details>

<details>
<summary>...understand how agents work</summary>

**Go to:** `.claude/ORCHESTRATOR.md`

**What you'll learn:**
- How agents are spawned
- How agents coordinate
- How agents hand off work
- Quality gate enforcement

</details>

---

## Common Patterns

**Once you understand these patterns, the structure makes sense:**

### Pattern 1: SKILL.md

**Every phase has a SKILL.md:**
```
skills/phase_XX_*/SKILL.md
```

**What's inside:**
- YAML frontmatter (metadata)
- Phase description
- Entry/exit criteria
- Process steps
- Deliverables

### Pattern 2: Templates and Examples

**Phase 1 has templates (others may too):**
```
skills/phase_01_vision_strategy/
├── templates/     # Start here
└── examples/      # See what good looks like
```

**Why:** Templates accelerate, examples inspire

### Pattern 3: Scripts in .claude/

**Shell scripts for automation:**
```
.claude/memory/*.sh      # Memory operations
.claude/hooks/*.sh       # Event triggers
```

**Why:** Some things are easier in shell scripts

### Pattern 4: Configuration Files

**JSON for configuration:**
```
.claude/settings.json                    # Claude Code settings
.claude/local/settings.json              # Local overrides
.claude/templates/example-*.json        # Examples
```

**Why:** JSON is machine-readable, easy to parse

---

## Additional Resources

**Want to go deeper?**

| Resource | What It Covers | When to Use |
|----------|----------------|-------------|
| `README.md` | Framework overview | Getting started |
| `SETUP_GUIDE.md` | Installation & setup | First time |
| `FRAMEWORK_VISUALIZATION.md` | Visual diagrams | Understanding workflows |
| `CLAUDE.md` | Framework context | Auto-loads (reference as needed) |
| `TESTING_GUIDE.md` | Testing procedures | Verifying installation |
| `ORCHESTRATOR.md` | Agent system | Understanding agents |
| `CONTEXT_ENGINEERING.md` | Context management | Optimizing performance |

---

## Quick Reference Card

**Print this out or keep it handy:**

```
OCTALUME/
├── Root files (guides, docs, CLAUDE.md)
├── .claude/
│   ├── Documentation (ORCHESTRATOR, etc.)
│   ├── agents/ (INITIALIZER, CODING)
│   ├── validators/ (quality gates)
│   ├── escalation/ (go/no-go)
│   ├── memory/ (project memory)
│   ├── commands/ (lifecycle-*)
│   ├── hooks/ (event triggers)
│   ├── tools/ (tool search)
│   ├── mcp-server/ (9 lifecycle tools)
│   └── templates/ (examples)
└── skills/
    ├── phase_01_vision_strategy/
    ├── phase_02_requirements_scope/
    ├── phase_03_architecture_design/
    ├── phase_04_development_planning/
    ├── phase_05_development_execution/
    ├── phase_06_quality_security/
    ├── phase_07_deployment_release/
    ├── phase_08_operations_maintenance/
    └── shared/
        ├── roles/
        ├── security/
        ├── quality/
        ├── compliance/
        └── governance/
```

---

## Final Thoughts

You've just toured the entire OCTALUME structure:

✅ **Root files** — Documentation at your fingertips
✅ **.claude/** — The framework's engine
✅ **skills/** — Modular instructions
✅ **Naming conventions** — Traceability in action
✅ **Patterns** — Once you see them, they make sense

**Remember:**
- You don't need to understand everything at once
- Start with what you need, learn the rest over time
- The structure is logical—each file has a purpose
- Reference this guide whenever you need to find something

---

**Version:** 1.0.0
**Last Updated:** 2026-01-20
**Expert Mentor Style**: Navigable, annotated, confidence-building documentation

---

> **You're not alone in this.** The OCTALUME structure might seem complex at first, but there's method to the madness. Every file has a purpose, every directory a reason. Take your time, explore at your own pace, and don't hesitate to reference this guide whenever you need to find something.
