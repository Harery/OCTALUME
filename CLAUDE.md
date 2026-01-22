# CLAUDE.md - OCTALUME Framework Context v2.0

This file is auto-loaded when Claude Code starts in this directory. It provides the complete context for understanding and working with the OCTALUME Enterprise Lifecycle Framework.

---

## 🚀 What's New in v2.0

OCTALUME v2.0 introduces powerful automation features while maintaining enterprise governance:

| Feature | Description | Command |
|---------|-------------|---------|
| **Cross-Session Memory** | Persists decisions, patterns, lessons across sessions | `/memory-search`, `/memory-save` |
| **Git Worktrees** | Parallel feature development without stashing | `/worktree-init`, `/worktree-merge` |
| **Automated QA** | Phase-specific quality checks with auto-fix | `/qa-run`, `/qa-fix` |
| **GitHub Integration** | Create issues/PRs directly from Claude | `/github-issue`, `/github-pr` |
| **Stack Detection** | Auto-detect project technologies | `/stack-detect` |
| **Changelog Generation** | Auto-generate CHANGELOG from commits | `/changelog` |

---

## Framework Overview

OCTALUME (Octa = 8 phases, Lume = light/guidance) is an enterprise software development lifecycle framework that guides projects from initial vision through production operations.

### Core Principles

1. Sequential phase progression with quality gates
2. Complete traceability from requirements to deployment
3. Security and compliance integrated from the start
4. Clear role ownership at every stage
5. Hybrid methodology: formal phases with agile execution

---

## Directory Structure

```
OCTALUME/
├── CLAUDE.md                         # This file (auto-loaded)
├── README.md                         # Framework overview
├── SETUP_GUIDE.md                    # Installation and setup
├── FRAMEWORK_VISUALIZATION.md        # Visual workflow diagrams
├── DIRECTORY_STRUCTURE.md            # File organization reference
├── .claude/
│   ├── ORCHESTRATOR.md               # Multi-agent coordinator
│   ├── CONTEXT_ENGINEERING.md        # Context management
│   ├── agents/                       # Agent harnesses
│   ├── commands/                     # 🆕 v2.0 slash commands
│   │   ├── memory-search.md
│   │   ├── memory-save.md
│   │   ├── worktree-init.md
│   │   ├── worktree-merge.md
│   │   ├── qa-run.md
│   │   ├── qa-fix.md
│   │   ├── github-issue.md
│   │   ├── github-pr.md
│   │   ├── stack-detect.md
│   │   └── changelog.md
│   ├── memory/                       # 🆕 v2.0 persistent memory
│   │   ├── memory.json
│   │   ├── memory-manager.js
│   │   ├── sessions/
│   │   └── insights/
│   ├── worktrees/                    # 🆕 v2.0 worktree tracking
│   │   └── active.json
│   ├── qa/                           # 🆕 v2.0 automated QA
│   │   ├── config.json
│   │   ├── criteria/
│   │   └── reports/
│   ├── integrations/                 # 🆕 v2.0 external integrations
│   │   └── github.json
│   ├── specs/                        # 🆕 v2.0 detected stack
│   │   └── detected-stack.json
│   ├── hooks/                        # Event triggers
│   └── tools/                        # Tool definitions
├── scripts/                          # 🆕 v2.0 automation scripts
│   ├── worktree-manager.sh
│   ├── qa-runner.sh
│   ├── github-integration.sh
│   ├── stack-detector.sh
│   └── changelog-generator.sh
└── skills/                           # Phase-specific skills
    ├── phase_01_vision_strategy/
    ├── phase_02_requirements_scope/
    ├── phase_03_architecture_design/
    ├── phase_04_development_planning/
    ├── phase_05_development_execution/
    ├── phase_06_quality_security/
    ├── phase_07_deployment_release/
    ├── phase_08_operations_maintenance/
    └── shared/
```

---

## 🆕 v2.0 Commands Reference

### Memory Commands

| Command | Description | Example |
|---------|-------------|---------|
| `/memory-search <query>` | Search project memory for relevant context | `/memory-search authentication` |
| `/memory-save <type> <data>` | Save insight to persistent memory | `/memory-save decision {"decision": "Use JWT"}` |
| `/memory-context <field> <value>` | Set current working context | `/memory-context phase P3` |
| `/memory-stats` | View memory statistics | `/memory-stats` |

### Worktree Commands

| Command | Description | Example |
|---------|-------------|---------|
| `/worktree-init <name> [base]` | Create isolated feature worktree | `/worktree-init user-auth` |
| `/worktree-list` | List all active worktrees | `/worktree-list` |
| `/worktree-merge <name> [-d]` | Merge worktree back to base | `/worktree-merge user-auth --delete` |
| `/worktree-discard <name>` | Discard worktree without merging | `/worktree-discard failed-experiment` |

### QA Commands

| Command | Description | Example |
|---------|-------------|---------|
| `/qa-run [phase]` | Run quality checks | `/qa-run P3` |
| `/qa-fix` | Auto-fix common issues | `/qa-fix` |
| `/qa-status` | View last QA report | `/qa-status` |

### GitHub Commands

| Command | Description | Example |
|---------|-------------|---------|
| `/github-issue <title> [body]` | Create GitHub issue | `/github-issue "Add login feature"` |
| `/github-pr [title] [body]` | Create pull request | `/github-pr` |

### Utility Commands

| Command | Description | Example |
|---------|-------------|---------|
| `/stack-detect` | Detect project technology stack | `/stack-detect` |
| `/changelog [action]` | Generate or preview changelog | `/changelog preview` |

---

## The 8 Phases

| Phase | Name | Owner | Duration | Key Deliverables |
|:-----:|------|-------|:--------:|------------------|
| P1 | Vision and Strategy | Product Owner | 4-6 weeks | PRD, Business Case |
| P2 | Requirements and Scope | Product Owner | 4-8 weeks | Requirements, Traceability Matrix |
| P3 | Architecture and Design | CTA | 6-10 weeks | System Architecture, Threat Models |
| P4 | Development Planning | Project Manager | 2-4 weeks | WBS, Resource Plan, Sprint Plan |
| P5 | Development Execution | Tech Lead | Variable | Working Software |
| P6 | Quality and Security | QA Lead | 4-8 weeks | Test Results, Security Sign-off |
| P7 | Deployment and Release | DevOps | 1-2 weeks | Production Deployment |
| P8 | Operations and Maintenance | SRE | Ongoing | Monitoring, Incidents |

---

## Quality Gates

Each phase has entry and exit criteria. Run `/qa-run P{N}` to validate.

| Phase | Entry Criteria | Exit Criteria |
|:-----:|----------------|---------------|
| P1 | Business idea identified | Business case approved, PRD completed |
| P2 | Approved PRD | Requirements approved, traceability matrix created |
| P3 | Approved requirements | Architecture approved, threat models completed |
| P4 | Approved architecture | WBS approved, resources allocated, sprints planned |
| P5 | Approved plan | All features complete, unit tests passing |
| P6 | Complete development | All tests passing, security validated, UAT signed off |
| P7 | Validated build | Deployed to production, smoke tests passing |
| P8 | Released to production | Monitoring active, SLAs met |

---

## The 16 Roles

### Executive and Leadership
1. **Executive Sponsor** - Executive authority and budget approval
2. **Product Owner** - Product vision, requirements, ROI
3. **Project Manager** - Project execution, timeline, budget

### Technical Leadership
4. **CTA (Chief Technology Architect)** - Technical vision and architecture decisions
5. **Tech Lead** - Delivery execution and team leadership

### Security and Compliance
6. **CISO** - Overall security strategy
7. **Security Architect** - Security design and implementation
8. **Compliance Officer** - Regulatory compliance and audits

### Quality and Testing
9. **QA Lead** - Quality strategy and testing governance
10. **QA Engineers** - Test design and execution
11. **Performance Engineer** - Performance testing

### Development and Infrastructure
12. **Developers** - Code development and testing
13. **DevOps** - CI/CD and infrastructure automation
14. **SRE** - Production reliability and monitoring

### Data and Cloud
15. **Data Architect** - Data modeling and integration
16. **Cloud Architect** - Cloud infrastructure design

---

## 🆕 v2.0 Workflows

### Starting a New Session

```bash
# Claude automatically:
# 1. Loads memory from previous sessions
# 2. Detects current git branch → infers phase
# 3. Loads detected stack configuration
# 4. Provides relevant context

# Set explicit context if needed:
/memory-context phase P3
/memory-context feature user-authentication
```

### Feature Development Flow

```bash
# 1. Create isolated worktree
/worktree-init user-authentication

# 2. Work on feature (Claude has full context)
# ... develop code ...

# 3. Save important decisions
/memory-save decision {"decision": "Use bcrypt for hashing", "rationale": "Industry standard"}

# 4. Run QA before merge
/qa-run P5

# 5. Merge and cleanup
/worktree-merge user-authentication --delete

# 6. Create PR
/github-pr "Feature: User Authentication"
```

### Release Flow

```bash
# 1. Run full QA
/qa-run

# 2. Generate changelog
/changelog preview
/changelog release minor

# 3. Follow changelog output for git commands
git add -A && git commit -m "chore: release v1.2.0"
git tag -a v1.2.0 -m "Release v1.2.0"
git push && git push --tags
```

---

## Artifact Traceability

All artifacts follow the naming convention: P{N}-{SECTION}-{###}

Examples:
- P1-VISION-001: Phase 1, Vision document, item 1
- P2-REQ-015: Phase 2, Requirements, item 15
- P3-ARCH-042: Phase 3, Architecture, item 42
- P5-CODE-789: Phase 5, Code commit, item 789
- P6-TEST-123: Phase 6, Test case, item 123

Traceability chain:
```
Epic → Feature → Story → Commit → Build → Artifact → Release → Test → Result
```

---

## Project State Management

### State Files
- `.claude/project-state.json` - Current project state
- `.claude/memory/memory.json` - Cross-session memory
- `.claude/worktrees/active.json` - Active worktrees
- `.claude/specs/detected-stack.json` - Technology stack

### Memory Categories

| Category | Use For | Example |
|----------|---------|---------|
| `architecture_decisions` | Design choices with rationale | "Use microservices for scaling" |
| `code_patterns` | Patterns that worked well | "Repository pattern for data" |
| `gotchas` | Issues and solutions | "Race condition in token refresh" |
| `best_practices` | Discovered practices | "Validate at API boundary" |
| `lessons_learned` | Session insights | "Integration tests caught regression" |

---

## CLI Compatibility

All v2.0 features are designed for Claude Code CLI:

```bash
# Works with Claude Code
claude --dir /path/to/project

# Slash commands work in conversation
> /memory-search authentication
> /qa-run P3
> /worktree-init new-feature
```

Scripts also work standalone:
```bash
./scripts/qa-runner.sh run P3
./scripts/stack-detector.sh detect
./scripts/changelog-generator.sh release minor
```

---

## Getting Help

- **Framework Guide**: See `README.md`
- **Setup Instructions**: See `SETUP_GUIDE.md`
- **Phase Details**: See `skills/phase_XX/` directories
- **Command Help**: Each command has built-in documentation

---

**OCTALUME v2.0.0** | Enterprise Lifecycle Framework
*Combining governance with automation for modern software delivery*
