# CLAUDE.md - OCTALUME Enterprise Lifecycle Framework

**Auto-loaded context for Claude when working in this directory**

---

<!-- SEO Metadata -->
**Keywords:** OCTALUME, CLAUDE.md, Claude Code context, enterprise lifecycle, SDLC automation, AI-assisted development, 8-phase framework, quality gates, multi-agent orchestration
**Description:** Auto-loaded Claude Code context for OCTALUME framework - contains 8-phase enterprise lifecycle, quality gates, agent orchestration, and workflow automation
**Tags:** #OCTALUME #ClaudeCode #AIFramework #SDLC #EnterpriseLifecycle #MultiAgent
**Author:** Mohamed ElHarery
**Version:** 1.0.0
**LastUpdated:** 2026

---

**Copyright (c) 2026 Mohamed ElHarery**
**Email:** mohamed@harery.com
**Website:** https://www.harery.com/
**GitHub:** https://github.com/Harery
**License:** MIT License - See LICENSE file for details

---

## QUICK START

This is the **Unified Enterprise Lifecycle** framework - a complete enterprise-grade software development lifecycle from PRD/MVP to delivery.

### For New Projects

```bash
# Initialize a new project
claude --prompt "Initialize a new lifecycle project for [describe project]"

# The Initializer Agent will:
# - Create project structure
# - Generate feature list (200-500 features)
# - Set up git repository
# - Configure development environment
```

### For Existing Projects

```bash
# Continue working on existing project
claude

# The Coding Agent will:
# - Read project state
# - Continue from where you left off
# - Work on next feature incrementally
```

---

## FRAMEWORK STRUCTURE

```
OCTALUME/
├── CLAUDE.md                    # This file - auto-loaded by Claude
├── README.md                    # Main framework documentation
├── SETUP_GUIDE.md               # Setup and usage guide
├── FRAMEWORK_VISUALIZATION.md   # Mermaid diagrams
├── DIRECTORY_STRUCTURE.md       # Directory listing
├── .claude/                     # Agent configurations
│   ├── ORCHESTRATOR.md          # Multi-agent orchestrator
│   ├── CONTEXT_ENGINEERING.md   # Context management utilities
│   ├── agents/                  # Agent harnesses
│   │   ├── INITIALIZER.md       # First-run setup agent
│   │   └── CODING.md            # Incremental development agent
│   └── tools/                   # Tool definitions
│       └── TOOL_SEARCH.md       # Tool discovery system
└── skills/                      # Agent skills (modular)
    ├── phase_01_vision_strategy/SKILL.md
    ├── phase_02_requirements_scope/SKILL.md
    ├── phase_03_architecture_design/SKILL.md
    ├── phase_04_development_planning/SKILL.md
    ├── phase_05_development_execution/SKILL.md
    ├── phase_06_quality_security/SKILL.md
    ├── phase_07_deployment_release/SKILL.md
    ├── phase_08_operations_maintenance/SKILL.md
    └── shared/                  # Cross-cutting skills
        ├── roles/SKILL.md       # All 16 role definitions
        ├── security/SKILL.md    # Security framework
        ├── quality/SKILL.md     # Quality framework
        ├── compliance/SKILL.md  # Compliance framework
        └── governance/SKILL.md  # Decision-making framework
```

---

## 8 PHASES OF THE LIFECYCLE

| Phase | Name | Owner | Duration | Key Deliverables |
|-------|------|-------|----------|------------------|
| 1 | Vision & Strategy | Product Owner | 4-6 weeks | PRD, Business Case |
| 2 | Requirements & Scope | Product Owner | 4-8 weeks | Requirements, Traceability Matrix |
| 3 | Architecture & Design | CTA | 6-10 weeks | System Architecture, Threat Models |
| 4 | Development Planning | Project Manager | 2-4 weeks | WBS, Resource Plan, Sprint Plan |
| 5 | Development Execution | Tech Lead | Variable (sprints) | Working Software |
| 6 | Quality & Security Validation | QA Lead | 4-8 weeks | Test Results, Security Sign-off |
| 7 | Deployment & Release | DevOps | 1-2 weeks | Production Deployment |
| 8 | Operations & Maintenance | SRE | Ongoing | Monitoring, Incidents, Improvements |

---

## 16 ROLES

### Executive & Leadership (3)
1. **Executive Sponsor** - Executive authority, budget approval
2. **Product Owner** - Product vision, requirements, ROI
3. **Project Manager** - Project execution, timeline, budget

### Technical Leadership (2)
4. **CTA** - Technical vision, architecture decisions
5. **Tech Lead** - Delivery execution, team leadership

### Security & Compliance (3)
6. **CISO** - Overall security strategy
7. **Security Architect** - Security design, implementation
8. **Compliance Officer** - Regulatory compliance, audits

### Quality & Testing (3)
9. **QA Lead** - Quality strategy, testing governance
10. **QA Engineers** - Test design, execution
11. **Performance Engineer** - Performance testing

### Development & Infrastructure (3)
12. **Developers** - Code development, testing
13. **DevOps** - CI/CD, infrastructure automation
14. **SRE** - Production reliability, monitoring

### Data & Infrastructure (2)
15. **Data Architect** - Data modeling, integration
16. **Cloud Architect** - Cloud infrastructure design

> See `skills/shared/roles/SKILL.md` for complete role definitions

---

## COMMON WORKFLOWS

### 1. Start a New Project

```bash
# Ask Claude to initialize a new project
"Initialize a new lifecycle project for an e-commerce platform with:
- User registration and authentication
- Product catalog and search
- Shopping cart and checkout
- Payment integration (Stripe)
- Order management
- Admin dashboard

Compliance: PCI DSS required
Team: 5 developers, 1 QA, 1 DevOps
"
```

### 2. Continue an Existing Project

```bash
# Claude automatically detects existing project
# It will:
# 1. Read .claude/project-state.json
# 2. Read claude-progress.txt
# 3. Continue from where you left off
# 4. Work on next feature
```

### 3. Move to Next Phase

```bash
# After completing a phase
"We've completed Phase 1. Run go/no-go decision and move to Phase 2."

# Claude will:
# 1. Validate exit criteria for Phase 1
# 2. Validate entry criteria for Phase 2
# 3. Get approvals
# 4. Update project state
# 5. Spawn Phase 2 agent
```

### 4. Handle Blockers

```bash
# When blocked
"We're blocked on Phase 3. The security architecture can't be decided."

# Claude will:
# 1. Diagnose the blocker
# 2. Spawn escalation agent if needed
# 3. Facilitate decision-making
# 4. Resolve blocker
```

---

## TRACEABILITY SYSTEM

All artifacts follow the format: `P{N}-{SECTION}-###`

**Examples**:
- `P1-VISION-001`: Phase 1, Vision document, item 1
- `P3-ARCH-015`: Phase 3, Architecture, item 15
- `P5-CODE-427`: Phase 5, Code commit/story, item 427

**Traceability Chain**:
```
Epic → Feature → Story → Commit → Build → Artifact → Release → Test → Result
```

---

## QUALITY GATES

Each phase has entry and exit criteria. A phase cannot proceed without meeting quality gates.

| Phase | Entry Criteria | Exit Criteria |
|-------|---------------|---------------|
| 1 | Business idea identified | Business case approved, PRD completed |
| 2 | Approved PRD | Requirements approved, traceability matrix created |
| 3 | Approved requirements | Architecture approved, threat models completed |
| 4 | Approved architecture | WBS approved, resources allocated, sprints planned |
| 5 | Approved plan | All features complete, unit tests passing |
| 6 | Complete development | All tests passing, security validated, UAT signed off |
| 7 | Validated build | Deployed to production, smoke tests passing |
| 8 | Released to production | Monitoring active, SLAs met |

---

## BASH COMMANDS

### Project Initialization

```bash
# Initialize git repository
git init

# Set up project structure
mkdir -p docs/{vision,requirements,architecture,design,testing,operations}
mkdir -p src tests scripts
mkdir -p artifacts/{P1,P2,P3,P4,P5,P6,P7,P8}

# Create feature list
touch feature_list.json

# Create progress tracking
touch claude-progress.txt
touch .claude/project-state.json

# Create initialization script
cat > scripts/init.sh <<'EOF'
#!/bin/bash
# Development environment setup
set -e
echo "🚀 Setting up development environment..."
# Add your setup commands here
EOF
chmod +x scripts/init.sh
```

### Git Workflow

```bash
# Commit with artifact traceability
git add .
git commit -m "feat: [description]

Artifacts: P{N}-{SECTION}-{###}
Feature: F-{XXX}
Status: passing
"

# View recent work
git log --oneline -20

# View current status
git status
```

### Testing

```bash
# Run unit tests
npm test  # or pytest, jest, etc.

# Run integration tests
npm run test:integration

# Run E2E tests
npm run test:e2e

# Run all tests
npm run test:all
```

---

## METHODOLOGY

**NOT 100% Agile** - This framework uses a **hybrid approach**:

```
┌─────────────────────────────────────────────────────────────┐
│                    HYBRID METHODOLOGY                       │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  FORMAL PHASES (1-4, 6-8)                                  │
│  ├── Structured deliverables                               │
│  ├── Go/No-Go decisions                                    │
│  ├── Documentation requirements                            │
│  └── Quality gates                                         │
│                                                             │
│  AGILE EXECUTION (Phase 5 only)                            │
│  ├── Sprint planning (2-week sprints)                      │
│  ├── Daily standups                                        │
│  ├── Sprint reviews                                        │
│  └── Retrospectives                                        │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

## SECURITY, QUALITY, COMPLIANCE

All three are **built-in from Phase 1**, not added later.

### Security First
- Security requirements identified in Phase 2
- Security architecture designed in Phase 3
- Threat modeling conducted in Phase 3
- Security testing in Phase 6
- Security operations in Phase 8

### Quality First
- Quality metrics defined in Phase 1
- Testable requirements in Phase 2
- Testability designed in Phase 3
- Test strategy in Phase 4
- Continuous testing throughout

### Compliance First
- Regulations identified in Phase 1
- Compliance requirements in Phase 2
- Compliance controls designed in Phase 3
- Compliance testing in Phase 6
- Audit readiness in Phase 8

---

## REGULATORY FRAMEWORKS SUPPORTED

| Regulation | Industry | Key Requirements |
|------------|----------|------------------|
| **HIPAA** | Healthcare | PHI protection, breach notification |
| **SOC 2** | Services | Security, availability, privacy controls |
| **PCI DSS** | Payments | Card data security, vulnerability scanning |
| **SOX** | Public companies | Financial reporting controls, audit trail |
| **GDPR** | EU data | Data subject rights, breach notification |
| **DoD/ITAR** | Defense | CMMC, controlled technical data |

---

## DOCUMENTATION STYLE

### Code Comments

```typescript
/**
 * Validates email format
 * @param email - Email address to validate
 * @returns true if valid, false otherwise
 */
export function isValidEmail(email: string): boolean {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailRegex.test(email);
}
```

### Commit Messages

```
feat: add user authentication (P5-CODE-001)

- Implement email/password authentication
- Add JWT token management
- Add password hashing with bcrypt
- Add unit tests for auth module
- Add integration tests for login flow

Artifacts: P5-CODE-001, P5-TEST-001
Feature: F-001
Status: passing
```

### Artifact Naming

```
Format: P{N}-{SECTION}-{###}

Examples:
P1-VISION-001  (Phase 1, Vision, item 1)
P2-REQ-015     (Phase 2, Requirements, item 15)
P3-ARCH-042    (Phase 3, Architecture, item 42)
P5-CODE-789    (Phase 5, Code, item 789)
P6-TEST-123    (Phase 6, Test, item 123)
```

---

## WORKING WITH CLAUDE IN THIS FRAMEWORK

### DO:

- **Start with context**: Let Claude read the framework structure first
- **Use specific prompts**: Be explicit about what you want
- **Follow the phases**: Work through phases sequentially
- **Test everything**: Never mark features as complete without testing
- **Commit often**: Make small, incremental commits
- **Update progress**: Keep claude-progress.txt current

### DON'T:

- **Skip phases**: Each phase has important deliverables
- **Ignore quality gates**: Entry/exit criteria exist for a reason
- **Work on multiple features**: Do one feature at a time
- **Declare victory early**: Only mark complete after testing
- **Leave broken code**: Always leave clean state

---

## IMPORTANT NOTES

1. **One Framework**: This is a single unified framework, not multiple tiers
2. **Clear Authority**: Every task has a designated owner
3. **Complete Lifecycle**: Covers PRD/MVP through delivery to operations
4. **Enterprise Grade**: Security, audit, governance built-in
5. **Full Traceability**: Every decision and deliverable tracked
6. **Quality First**: Testing, security, compliance integrated throughout

---

## GETTING HELP

- **Framework Overview**: See `UNIFIED_ENTERPRISE_LIFECYCLE.md`
- **Skill Index**: See `SKILLS.md`
- **Phase Details**: See `skills/phase_*/SKILL.md`
- **Role Definitions**: See `skills/shared/roles/SKILL.md`
- **Security Guidance**: See `skills/shared/security/SKILL.md`
- **Quality Guidance**: See `skills/shared/quality/SKILL.md`
- **Compliance Guidance**: See `skills/shared/compliance/SKILL.md`
- **Governance Guidance**: See `skills/shared/governance/SKILL.md`

---

## FRAMEWORK VERSION

Version: 1.0.0
Last Updated: 2026
Based on: Industry Best Practices for Multi-Agent Systems, Agent Skills, Context Engineering, and Long-Running Agents
