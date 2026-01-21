# CLAUDE.md — Your OCTALUME Context

**Auto-loaded when you start Claude Code in this directory**

---

## 🎯 What This File Does

When you start Claude Code from an OCTALUME directory, this file loads automatically. It gives Claude everything needed to understand your project and guide you through the software development lifecycle.

**Think of this as Claude's "operating manual" for working with your project.**

---

## 🚀 Quick Start: What Can You Do?

<details>
<summary><strong>Starting a new project?</strong></summary>

```bash
claude --prompt "Initialize a new lifecycle project for [describe your project]"
```

**What happens:** Claude creates your project structure, generates a comprehensive feature list (200-500 features), sets up git, and configures your development environment.

**Example prompt:**
```
"Initialize a new lifecycle project for an e-commerce platform with:
- User authentication and authorization
- Product catalog with search and filtering
- Shopping cart and checkout process
- Payment integration (Stripe/PayPal)
- Order management and tracking
- Admin dashboard for inventory management

Target market: Small to medium businesses
Budget: Project resources allocated
Timeline: 6 months
Team: 5 developers, 1 QA, 1 DevOps
Compliance: PCI DSS required"
```

</details>

<details>
<summary><strong>Continuing an existing project?</strong></summary>

```bash
claude
```

**What happens:** Claude detects your existing project, reads its state, and continues from where you left off. It knows your current phase, progress, and what to work on next.

**Example interaction:**
```
You: "What's the current project status?"

Claude: "You're in Phase 3 (Architecture & Design). You've completed:
✓ System architecture document
✓ Technology stack decisions
✓ Database design

Still to do:
○ Threat modeling
○ Security architecture
○ Deployment architecture

Shall we continue with threat modeling?"
```

</details>

<details>
<summary><strong>Moving to the next phase?</strong></summary>

```bash
# In Claude Code:
"We've completed Phase [X]. Run go/no-go and move to Phase [X+1]."
```

**What happens:** Claude validates exit criteria for your current phase, validates entry criteria for the next phase, gets approvals, updates project state, and spawns the phase-specific agent.

**Example:**
```
You: "We've completed Phase 2. Run go/no-go and move to Phase 3."

Claude: "Let me validate Phase 2 exit criteria...

✓ All requirements approved
✓ Traceability matrix created
✓ Stakeholders signed off

Now validating Phase 3 entry criteria...

✓ Approved requirements available
✓ CTA assigned
✓ Architecture team ready

Go/No-Go Decision: GO ✓

Updating project state... Spawning Phase 3 agent...
You're now in Phase 3: Architecture & Design."
```

</details>

<details>
<summary><strong>Hit a blocker?</strong></summary>

```bash
# In Claude Code:
"We're blocked on [describe the blocker]."
```

**What happens:** Claude diagnoses the issue, spawns an escalation agent if needed, facilitates decision-making, and helps you resolve the blocker.

**Example:**
```
You: "We're blocked. The team can't agree on microservices vs monolith."

Claude: "I understand — this is a common architecture debate. Let me help you work through it.

**Considerations for microservices:**
- Pros: Scalability, team autonomy, technology flexibility
- Cons: Complexity, distributed transactions, operational overhead

**Considerations for monolith:**
- Pros: Simplicity, easier debugging, faster development
- Cons: Scalability limits, tight coupling, difficult to parallelize

**Questions to guide your decision:**
1. What's your expected scale? (users, data volume, transaction rate)
2. How big is your team? (microservices need more DevOps capacity)
3. What's your timeline? (monoliths are faster to build initially)
4. What are your scaling requirements? (vertical vs horizontal)

Based on your project (e-commerce, 6-month timeline, 6-person team), I'd recommend: **start with monolith, design for future microservices extraction.**

Want me to explain this approach in more detail?"
```

</details>

---

## 📁 Framework Structure

```
OCTALUME/
├── CLAUDE.md                    # ← This file (auto-loaded by Claude)
├── README.md                    # Main framework documentation
├── SETUP_GUIDE.md               # Installation and setup
├── FRAMEWORK_VISUALIZATION.md   # Visual workflow diagrams
├── DIRECTORY_STRUCTURE.md       # What's where
│
├── .claude/                     # Agent configurations
│   ├── ORCHESTRATOR.md          # Multi-agent coordinator
│   ├── CONTEXT_ENGINEERING.md   # Context management
│   ├── agents/                  # Agent harnesses
│   │   ├── INITIALIZER.md       # First-run setup
│   │   └── CODING.md            # Incremental development
│   └── tools/                   # Tool definitions
│       └── TOOL_SEARCH.md       # Tool discovery
│
└── skills/                      # Agent skills (modular)
    ├── phase_01_vision_strategy/     # Phase 1: Vision & Strategy
    ├── phase_02_requirements_scope/  # Phase 2: Requirements & Scope
    ├── phase_03_architecture_design/ # Phase 3: Architecture & Design
    ├── phase_04_development_planning/# Phase 4: Development Planning
    ├── phase_05_development_execution/# Phase 5: Development Execution
    ├── phase_06_quality_security/     # Phase 6: Quality & Security
    ├── phase_07_deployment_release/  # Phase 7: Deployment & Release
    ├── phase_08_operations_maintenance/# Phase 8: Operations & Maintenance
    │
    └── shared/                      # Cross-cutting skills
        ├── roles/SKILL.md            # All 16 role definitions
        ├── security/SKILL.md         # Security framework
        ├── quality/SKILL.md          # Quality framework
        ├── compliance/SKILL.md      # Compliance framework
        └── governance/SKILL.md       # Decision-making framework
```

---

## 🔄 The 8 Phases: Your Complete Journey

| Phase | What | Who | Duration | Key Deliverables |
|:-----:|------|-----|:--------:|------------------|
| 1 | Vision & Strategy | Product Owner | 4-6 weeks | PRD, Business Case |
| 2 | Requirements & Scope | Product Owner | 4-8 weeks | Requirements, Traceability Matrix |
| 3 | Architecture & Design | CTA | 6-10 weeks | System Architecture, Threat Models |
| 4 | Development Planning | Project Manager | 2-4 weeks | WBS, Resource Plan, Sprint Plan |
| 5 | Development Execution | Tech Lead | Variable (sprints) | Working Software |
| 6 | Quality & Security Validation | QA Lead | 4-8 weeks | Test Results, Security Sign-off |
| 7 | Deployment & Release | DevOps | 1-2 weeks | Production Deployment |
| 8 | Operations & Maintenance | SRE | Ongoing | Monitoring, Incidents, Improvements |

---

## 👥 The 16 Roles: Who Does What

<details>
<summary><strong>See all roles and responsibilities</strong></summary>

### Executive & Leadership (3)

1. **Executive Sponsor** — Executive authority and budget approval
2. **Product Owner** — Product vision, requirements, ROI
3. **Project Manager** — Project execution, timeline, budget

### Technical Leadership (2)

4. **CTA** — Technical vision and architecture decisions
5. **Tech Lead** — Delivery execution and team leadership

### Security & Compliance (3)

6. **CISO** — Overall security strategy
7. **Security Architect** — Security design and implementation
8. **Compliance Officer** — Regulatory compliance and audits

### Quality & Testing (3)

9. **QA Lead** — Quality strategy and testing governance
10. **QA Engineers** — Test design and execution
11. **Performance Engineer** — Performance testing

### Development & Infrastructure (3)

12. **Developers** — Code development and testing
13. **DevOps** — CI/CD and infrastructure automation
14. **SRE** — Production reliability and monitoring

### Data & Infrastructure (2)

15. **Data Architect** — Data modeling and integration
16. **Cloud Architect** — Cloud infrastructure design

</details>

> **See `skills/shared/roles/SKILL.md` for complete role definitions.**

---

## 🔗 Traceability: Tracking Everything

**Every artifact follows: `P{N}-{SECTION}-###`**

**Examples:**
- `P1-VISION-001` — Phase 1, Vision document, item 1
- `P3-ARCH-042` — Phase 3, Architecture, item 42
- `P5-CODE-789` — Phase 5, Code commit, item 789

**The traceability chain:**

```
Epic → Feature → Story → Commit → Build → Artifact → Release → Test → Result
```

**Why this matters:** When issues arise (or when something goes brilliantly), you can trace back to understand:
- What requirement prompted this?
- Who approved this decision?
- What test covers this?
- What release includes this?

---

## 🚦 Quality Gates: Don't Proceed Until Ready

Each phase has entry and exit criteria. **You cannot proceed without meeting quality gates.**

<details>
<summary><strong>See all quality gates</strong></summary>

| Phase | Enter When | Exit When |
|:-----:|------------|-----------|
| 1 | Business idea identified | Business case approved, PRD completed |
| 2 | Approved PRD | Requirements approved, traceability matrix created |
| 3 | Approved requirements | Architecture approved, threat models completed |
| 4 | Approved architecture | WBS approved, resources allocated, sprints planned |
| 5 | Approved plan | All features complete, unit tests passing |
| 6 | Complete development | All tests passing, security validated, UAT signed off |
| 7 | Validated build | Deployed to production, smoke tests passing |
| 8 | Released to production | Monitoring active, SLAs met |

**What this prevents:**
- Building the wrong thing (Phase 1 gate)
- Scope creep (Phase 2 gate)
- Wrong architecture (Phase 3 gate)
- Unrealistic plans (Phase 4 gate)
- Incomplete features (Phase 5 gate)
- Bugs in production (Phase 6 gate)
- Failed deployments (Phase 7 gate)
- Unstable operations (Phase 8 gate)

</details>

---

## 💻 Working with Claude: Best Practices

### ✅ DO:

| Practice | Why It Matters |
|----------|----------------|
| **Start with context** | Let Claude read the framework first |
| **Be specific** | Clear prompts get clear results |
| **Follow the phases** | Work through sequentially (there's a reason for the order) |
| **Test everything** | Never mark features complete without testing |
| **Commit often** | Small, incremental commits are easier to review and revert |
| **Update progress** | Keep progress files current for continuity |

### ❌ DON'T:

| Pitfall | Why It's Problematic |
|---------|---------------------|
| **Skip phases** | Each phase has important deliverables that feed into later phases |
| **Ignore quality gates** | Entry/exit criteria exist for good reasons |
| **Work on multiple features** | One thing at a time reduces cognitive load and errors |
| **Declare victory early** | Only mark complete after testing and validation |
| **Leave broken code** | Always leave clean, working state for the next session |

---

## 🛠️ Bash Commands: Your Quick Reference

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
echo "Setting up development environment..."
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

# Check status
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

## 📋 Methodology: Hybrid Approach

**Not 100% Agile — not fully Waterfall. You get the best of both.**

### Formal Phases (1-4, 6-8)
- Structured deliverables
- Go/No-Go decisions
- Documentation requirements
- Quality gates

### Agile Execution (Phase 5 only)
- Sprint planning (2-week sprints)
- Daily standups
- Sprint reviews
- Retrospectives

**Why this works:**
- **Upfront planning** prevents expensive mistakes
- **Architecture decisions** made before coding begins
- **Agile execution** gives flexibility and rapid feedback
- **Quality gates** ensure nothing slips through

---

## 🔒 Security, Quality, Compliance: Built From Day One

**These aren't add-ons — they're foundational.**

### Security First
- Requirements identified in Phase 2
- Architecture designed in Phase 3
- Threat modeling in Phase 3
- Testing in Phase 6
- Operations in Phase 8

### Quality First
- Metrics defined in Phase 1
- Testable requirements in Phase 2
- Testability designed in Phase 3
- Test strategy in Phase 4
- Continuous testing throughout

### Compliance First
- Regulations identified in Phase 1
- Requirements in Phase 2
- Controls designed in Phase 3
- Testing in Phase 6
- Audit readiness in Phase 8

---

## 📜 Regulatory Frameworks Supported

| Regulation | Industry | What's Covered |
|------------|----------|----------------|
| **HIPAA** | Healthcare | PHI protection, breach notification |
| **SOC 2** | Services | Security, availability, privacy controls |
| **PCI DSS** | Payments | Card data security, vulnerability scanning |
| **SOX** | Public companies | Financial controls, audit trail |
| **GDPR** | EU data | Data subject rights, breach notification |
| **DoD/ITAR** | Defense | CMMC, controlled technical data |

---

## 📝 Documentation Style Guide

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

## ⚠️ Important Notes

1. **One Framework** — This is a single unified framework, not multiple tiers
2. **Clear Authority** — Every task has a designated owner
3. **Complete Lifecycle** — Covers PRD/MVP through delivery to operations
4. **Enterprise Grade** — Security, audit, governance built-in
5. **Full Traceability** — Every decision and deliverable tracked
6. **Quality First** — Testing, security, compliance integrated throughout

---

## 📚 Getting Help

| Topic | Where to Look |
|-------|---------------|
| **Framework Overview** | `README.md` |
| **Phase Details** | `skills/phase_*/SKILL.md` |
| **Role Definitions** | `skills/shared/roles/SKILL.md` |
| **Security Guidance** | `skills/shared/security/SKILL.md` |
| **Quality Guidance** | `skills/shared/quality/SKILL.md` |
| **Compliance Guidance** | `skills/shared/compliance/SKILL.md` |
| **Governance Guidance** | `skills/shared/governance/SKILL.md` |

---

**Version:** 1.0.0 | **Last Updated:** 2026-01-20

---

> **You've got this.** Building software is complex, but you don't have to figure it out alone. OCTALUME + Claude Code = your expert guide through every step of the journey. Let's build something great together.
