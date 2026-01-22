# CLAUDE.md - OCTALUME Framework Context

This file is auto-loaded when Claude Code starts in this directory. It provides the complete context for understanding and working with the OCTALUME Enterprise Lifecycle Framework.

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
├── .claude/                          # Agent configurations
│   ├── ORCHESTRATOR.md               # Multi-agent coordinator
│   ├── CONTEXT_ENGINEERING.md        # Context management
│   ├── agents/                       # Agent harnesses
│   ├── memory/                       # Persistent memory storage
│   ├── hooks/                        # Event triggers
│   └── tools/                        # Tool definitions
└── skills/                           # Phase-specific skills
    ├── phase_01_vision_strategy/
    ├── phase_02_requirements_scope/
    ├── phase_03_architecture_design/
    ├── phase_04_development_planning/
    ├── phase_05_development_execution/
    ├── phase_06_quality_security/
    ├── phase_07_deployment_release/
    ├── phase_08_operations_maintenance/
    └── shared/                       # Cross-cutting concerns
        ├── roles/
        ├── security/
        ├── quality/
        ├── compliance/
        └── governance/
```

---

## The 8 Phases

| Phase | Name | Owner | Duration | Key Deliverables |
|:-----:|------|-------|:--------:|------------------|
| 1 | Vision and Strategy | Product Owner | 4-6 weeks | PRD, Business Case |
| 2 | Requirements and Scope | Product Owner | 4-8 weeks | Requirements, Traceability Matrix |
| 3 | Architecture and Design | CTA | 6-10 weeks | System Architecture, Threat Models |
| 4 | Development Planning | Project Manager | 2-4 weeks | WBS, Resource Plan, Sprint Plan |
| 5 | Development Execution | Tech Lead | Variable | Working Software |
| 6 | Quality and Security | QA Lead | 4-8 weeks | Test Results, Security Sign-off |
| 7 | Deployment and Release | DevOps | 1-2 weeks | Production Deployment |
| 8 | Operations and Maintenance | SRE | Ongoing | Monitoring, Incidents |

---

## Quality Gates

Each phase has entry and exit criteria. Progression requires passing the quality gate.

| Phase | Entry Criteria | Exit Criteria |
|:-----:|----------------|---------------|
| 1 | Business idea identified | Business case approved, PRD completed |
| 2 | Approved PRD | Requirements approved, traceability matrix created |
| 3 | Approved requirements | Architecture approved, threat models completed |
| 4 | Approved architecture | WBS approved, resources allocated, sprints planned |
| 5 | Approved plan | All features complete, unit tests passing |
| 6 | Complete development | All tests passing, security validated, UAT signed off |
| 7 | Validated build | Deployed to production, smoke tests passing |
| 8 | Released to production | Monitoring active, SLAs met |

---

## The 16 Roles

### Executive and Leadership
1. Executive Sponsor - Executive authority and budget approval
2. Product Owner - Product vision, requirements, ROI
3. Project Manager - Project execution, timeline, budget

### Technical Leadership
4. CTA (Chief Technology Architect) - Technical vision and architecture decisions
5. Tech Lead - Delivery execution and team leadership

### Security and Compliance
6. CISO - Overall security strategy
7. Security Architect - Security design and implementation
8. Compliance Officer - Regulatory compliance and audits

### Quality and Testing
9. QA Lead - Quality strategy and testing governance
10. QA Engineers - Test design and execution
11. Performance Engineer - Performance testing

### Development and Infrastructure
12. Developers - Code development and testing
13. DevOps - CI/CD and infrastructure automation
14. SRE - Production reliability and monitoring

### Data and Cloud
15. Data Architect - Data modeling and integration
16. Cloud Architect - Cloud infrastructure design

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
Epic to Feature to Story to Commit to Build to Artifact to Release to Test to Result

---

## Commands and Workflows

### Initialize New Project

When a user requests project initialization:

1. Gather project details (description, timeline, team size, compliance requirements)
2. Create project structure in artifacts/ directory
3. Generate comprehensive feature list (200-500 features)
4. Initialize git repository
5. Create project-state.json
6. Begin Phase 1

Example user prompt:
```
Initialize a new lifecycle project for an e-commerce platform with user authentication, product catalog, shopping cart, and payment integration. Timeline: 6 months, Team: 5 developers.
```

### Continue Existing Project

When resuming work:

1. Read .claude/project-state.json for current state
2. Read claude-progress.txt for recent progress
3. Check git log for recent commits
4. Identify current phase and pending tasks
5. Continue from last checkpoint

### Phase Transition

When user requests phase transition:

1. Validate all exit criteria for current phase
2. Document completion in progress file
3. Validate entry criteria for next phase
4. Update project-state.json
5. Load next phase skill from skills/phase_XX/
6. Begin next phase activities

Example user prompt:
```
We have completed Phase 2. Run go/no-go and move to Phase 3.
```

### Handle Blockers

When user reports a blocker:

1. Identify the blocker type (technical, resource, decision, dependency)
2. Check relevant skill files for guidance
3. Propose resolution options
4. Document decision in memory bank
5. Update project state if needed

---

## Project State Management

### State File Location
.claude/project-state.json

### State Structure
```json
{
  "project_name": "string",
  "current_phase": 1-8,
  "phase_status": "not_started|in_progress|blocked|complete",
  "created_at": "ISO8601",
  "updated_at": "ISO8601",
  "phases": {
    "phase_1": { "status": "string", "started": "date", "completed": "date" }
  }
}
```

### Memory Bank Location
.claude/memory/memory.json

### Memory Categories
- decisions: Architecture and design decisions
- progress: Completed milestones
- blockers: Current impediments
- notes: General observations

---

## Git Workflow

### Commit Message Format
```
type: description (artifact-id)

- Detail 1
- Detail 2

Artifacts: P{N}-{SECTION}-{###}
Feature: F-{XXX}
Status: passing
```

### Types
- feat: New feature
- fix: Bug fix
- docs: Documentation
- refactor: Code refactoring
- test: Adding tests
- chore: Maintenance

---

## Methodology

OCTALUME uses a hybrid approach:

### Formal Phases (1-4, 6-8)
- Structured deliverables with templates
- Go/No-Go decisions at transitions
- Documentation requirements
- Quality gates with approval

### Agile Execution (Phase 5)
- 2-week sprints
- Sprint planning at start
- Daily standups (15 minutes)
- Sprint reviews with stakeholders
- Retrospectives for improvement

---

## Security, Quality, Compliance

These are integrated throughout, not added later.

### Security Integration
- Phase 2: Security requirements identified
- Phase 3: Security architecture designed, threat modeling
- Phase 6: Security testing, penetration testing
- Phase 8: Security operations, monitoring

### Quality Integration
- Phase 1: Quality metrics defined
- Phase 2: Testable requirements written
- Phase 3: Testability designed in
- Phase 4: Test strategy planned
- Phase 5: Continuous testing
- Phase 6: Comprehensive validation

### Compliance Integration
- Phase 1: Regulations identified
- Phase 2: Compliance requirements documented
- Phase 3: Controls designed
- Phase 6: Compliance testing
- Phase 8: Audit readiness

### Supported Regulations
- HIPAA: Healthcare data protection
- SOC 2: Service organization controls
- PCI DSS: Payment card security
- SOX: Financial controls
- GDPR: EU data protection
- DoD/ITAR: Defense requirements

---

## Skill Loading

Each phase has a dedicated skill file at skills/phase_XX_name/SKILL.md

Skill files contain:
- Phase metadata (owner, participants, duration)
- Entry criteria
- Exit criteria
- Step-by-step activities
- Templates and examples
- Best practices

Load the appropriate skill when:
- Starting a new phase
- User asks about phase-specific activities
- Generating phase deliverables

---

## Best Practices

### Do
- Start with context: Read project state before acting
- Be specific: Generate detailed, actionable deliverables
- Follow phases: Work sequentially through the lifecycle
- Test everything: Never mark complete without validation
- Commit often: Small, incremental commits with traceability
- Update progress: Keep state files current

### Do Not
- Skip phases: Each phase feeds into the next
- Ignore quality gates: Entry/exit criteria exist for good reasons
- Work on multiple features: One task at a time
- Declare victory early: Only mark complete after testing
- Leave broken code: Always maintain working state

---

## Reference Files

| Topic | Location |
|-------|----------|
| Framework Overview | README.md |
| Installation | SETUP_GUIDE.md |
| Phase 1-8 Details | skills/phase_XX/SKILL.md |
| Role Definitions | skills/shared/roles/SKILL.md |
| Security Guidance | skills/shared/security/SKILL.md |
| Quality Guidance | skills/shared/quality/SKILL.md |
| Compliance Guidance | skills/shared/compliance/SKILL.md |
| Governance | skills/shared/governance/SKILL.md |

---

## Contact

- Repository: https://github.com/Harery/OCTALUME
- Email: octalume@harery.com
- Website: https://harery.com

---

Version 1.0.0 | OCTALUME Enterprise Lifecycle Framework
