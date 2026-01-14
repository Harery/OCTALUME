# OCTALUME - Enterprise Software Development Lifecycle Framework

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://github.com/Harery/OCTALUME/blob/main/LICENSE)
[![Version](https://img.shields.io/badge/Version-1.0.0-blue.svg)](https://github.com/Harery/OCTALUME)
[![Framework](https://img.shields.io/badge/Framework-Enterprise-green.svg)](https://www.harery.com/)
[![AI](https://img.shields.io/badge/AI-Assisted-orange.svg)](https://github.com/Harery)

---

<!-- SEO Metadata -->
**Title:** OCTALUME - Enterprise 8-Phase Software Development Lifecycle Framework with Quality Gates & AI Orchestration
**Description:** OCTALUME is an enterprise-grade 8-phase SDLC framework with quality gates, multi-agent orchestration, security, compliance, and AI-assisted development using Claude Code. Perfect for regulated industries (HIPAA, SOC 2, PCI DSS, SOX, GDPR).
**Keywords:** OCTALUME, enterprise SDLC, software development lifecycle, 8-phase framework, stage-gate process, quality gates, go-no-go decisions, project management, Claude Code, AI-assisted development, enterprise methodology, phase transitions, multi-agent orchestration, SDLC automation, DevOps, Agile, waterfall hybrid, security by design, compliance framework, traceability system, artifact management
**Author:** Mohamed ElHarery
**Email:** mohamed@harery.com
**Website:** https://www.harery.com/
**GitHub:** https://github.com/Harery
**Tags:** #OCTALUME #SDLC #EnterpriseFramework #ProjectManagement #QualityGates #StageGate #DevOps #Agile #SoftwareDevelopment #ClaudeCode #AIFramework #LifecycleManagement #Compliance #Security #Governance
**Category:** Software Development, Project Management, Enterprise Framework
**Version:** 1.0.0
**LastUpdated:** 2026

---

## 🚀 Quick Start

```bash
# Install OCTALUME
git clone https://github.com/Harery/OCTALUME.git
cd OCTALUME

# Install dependencies
cd .claude/mcp-server && npm install && cd ../..

# Start with Claude Code
claude
```

**OCTALUME automatically loads in Claude Code - no additional setup required!**

---

## 📋 What is OCTALUME?

**OCTALUME** (Octa = 8 phases + Lume = light/guidance) is an enterprise-grade software development lifecycle framework that provides:

### Core Features
- ✅ **8 Phases** - Complete lifecycle from Vision to Operations
- ✅ **Quality Gates** - Go/No-Go decisions at each phase transition
- ✅ **Multi-Agent Orchestration** - AI-assisted development with Claude Code
- ✅ **Security First** - Security and compliance built-in from Phase 1
- ✅ **Full Traceability** - Every decision and deliverable tracked
- ✅ **16 Defined Roles** - Clear ownership and accountability
- ✅ **Hybrid Methodology** - Formal phases + Agile execution

### Perfect For
- 🏢 **Enterprise Teams** building scalable software
- 🏗️ **Software Development Companies** managing multiple projects
- 🚀 **Startups** building enterprise-grade products
- 🏛️ **Government Projects** requiring audit trails
- 🏥 **Regulated Industries** (HIPAA, SOC 2, PCI DSS, SOX, GDPR)

---

## 🎯 The 8 Phases

```
┌────────────────────────────────────────────────────────────────┐
│                  OCTALUME 8-PHASE LIFECYCLE                   │
├────────────────────────────────────────────────────────────────┤
│                                                                │
│  Phase 1: Vision & Strategy      ──►  PRD, Business Case       │
│  Phase 2: Requirements & Scope   ──►  Requirements List         │
│  Phase 3: Architecture & Design   ──►  System Architecture     │
│  Phase 4: Development Planning    ──►  WBS, Sprint Plan         │
│  Phase 5: Development Execution   ──►  Working Software         │
│  Phase 6: Quality & Security      ──►  Test Results             │
│  Phase 7: Deployment & Release    ──►  Production Deploy        │
│  Phase 8: Operations & Maintenance ──►  Monitoring, Incidents    │
│                                                                │
└────────────────────────────────────────────────────────────────┘
```

---

## 📚 Documentation

| Document | Description |
|----------|-------------|
| [SETUP_GUIDE.md](SETUP_GUIDE.md) | How to set up and use OCTALUME with Claude Code |
| [FRAMEWORK_VISUALIZATION.md](FRAMEWORK_VISUALIZATION.md) | Mermaid diagrams showing workflows and flows |
| [DIRECTORY_STRUCTURE.md](DIRECTORY_STRUCTURE.md) | Complete directory and file listing |
| [CLAUDE.md](CLAUDE.md) | Auto-loaded framework context for Claude Code |
| [LICENSE](LICENSE) | MIT License |

---

## 🛠️ Key Components

### Enforcement Systems
- **Phase Gate Validator** - Entry/exit criteria validation
- **Escalation Manager** - Go/No-Go decision enforcement
- **Agent Spawner** - Multi-agent lifecycle management
- **Task-Skill Binder** - Automatic skill selection
- **Memory System** - State persistence and synchronization
- **Handoff Verification** - Phase transition validation

### Skills (13 Total)
- **8 Phase Skills** - One for each lifecycle phase
- **5 Shared Skills** - Roles, Security, Quality, Compliance, Governance

### MCP Server
- 9 lifecycle tools for Claude Code integration
- Seamless workflow automation
- Quality gate enforcement

---

## 🎖️ 16 Defined Roles

### Executive & Leadership
1. Executive Sponsor
2. Product Owner
3. Project Manager

### Technical Leadership
4. CTA (Chief Technology Architect)
5. Tech Lead

### Security & Compliance
6. CISO
7. Security Architect
8. Compliance Officer

### Quality & Testing
9. QA Lead
10. QA Engineers
11. Performance Engineer

### Development & Infrastructure
12. Developers
13. DevOps Engineer
14. SRE (Site Reliability Engineer)

### Data & Infrastructure
15. Data Architect
16. Cloud Architect

---

## 🔒 Built-In Compliance

OCTALUME supports regulatory frameworks for:
- **HIPAA** - Healthcare (PHI protection, breach notification)
- **SOC 2** - Services (Security, availability, privacy controls)
- **PCI DSS** - Payments (Card data security, vulnerability scanning)
- **SOX** - Public companies (Financial reporting controls, audit trail)
- **GDPR** - EU data (Data subject rights, breach notification)
- **DoD/ITAR** - Defense (CMMC, controlled technical data)

---

## 📊 Traceability System

All artifacts follow the format: `P{N}-{SECTION}-###`

**Examples:**
- `P1-VISION-001` - Phase 1, Vision document, item 1
- `P3-ARCH-015` - Phase 3, Architecture, item 15
- `P5-CODE-427` - Phase 5, Code commit, item 427

**Traceability Chain:**
```
Epic → Feature → Story → Commit → Build → Artifact → Release → Test → Result
```

---

## 🤖 AI-Assisted Development

OCTALUME integrates seamlessly with **Claude Code** for:
- ✅ Automatic phase detection
- ✅ Skill-based task routing
- ✅ Quality gate validation
- ✅ Memory persistence across sessions
- ✅ Multi-agent orchestration
- ✅ Context-aware assistance

---

## 📦 Installation

### Prerequisites
- Node.js 18+
- npm 9+
- Claude Code installed
- Git 2+

### Setup (4 Steps)

```bash
# 1. Copy OCTALUME folder (including hidden .claude/ directory)
cp -r OCTALUME/ ~/your-location/

# 2. Install MCP server dependencies
cd OCTALUME/.claude/mcp-server
npm install

# 3. Install Claude Code globally
npm install -g @anthropic-ai/claude-code

# 4. Start using
cd ~/your-location/OCTALUME
claude
```

---

## 💡 Usage Examples

### Start a New Project
```
Initialize a new OCTALUME project for an e-commerce platform with:
- User authentication
- Product catalog
- Shopping cart
- Payment integration
- Order management

Compliance: PCI DSS required
Team: 5 developers, 1 QA, 1 DevOps
```

### Continue Existing Project
```
Continue working on Phase 3: Architecture & Design
```

### Phase Transition
```
Complete Phase 2 and run go/no-go decision to move to Phase 3
```

---

## 📈 Methodology

**Hybrid Approach:** Formal Phases + Agile Execution

```
┌─────────────────────────────────────────┐
│         HYBRID METHODOLOGY              │
├─────────────────────────────────────────┤
│                                         │
│  FORMAL PHASES (1-4, 6-8)             │
│  ├── Structured deliverables            │
│  ├── Go/No-Go decisions                 │
│  ├── Documentation requirements         │
│  └── Quality gates                      │
│                                         │
│  AGILE EXECUTION (Phase 5 only)        │
│  ├── Sprint planning (2-week sprints)   │
│  ├── Daily standups                     │
│  ├── Sprint reviews                     │
│  └── Retrospectives                     │
│                                         │
└─────────────────────────────────────────┘
```

---

## 🌟 Key Benefits

| Benefit | Description |
|---------|-------------|
| **Complete Lifecycle** | From PRD/MVP to Operations |
| **Quality Built-In** | Testing, security, compliance from Phase 1 |
| **Clear Authority** | Every task has designated owner |
| **Full Traceability** | Every decision tracked |
| **AI-Assisted** | Claude Code integration for automation |
| **Enterprise Ready** | Meets regulatory requirements |
| **Team Scalable** | Works for teams of any size |

---

## 📄 License

MIT License - Copyright (c) 2026 Mohamed ElHarery

See [LICENSE](LICENSE) file for details.

---

## 👤 Author

**Mohamed ElHarery**
- 📧 Email: mohamed@harery.com
- 🌐 Website: https://www.harery.com/
- 💻 GitHub: https://github.com/Harery

---

## 🔗 Links

- **Website:** https://www.harery.com/
- **GitHub:** https://github.com/Harery/OCTALUME
- **Documentation:** https://github.com/Harery/OCTALUME/wiki
- **Issues:** https://github.com/Harery/OCTALUME/issues

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

---

## ⭐ Star History

If you find OCTALUME useful, please consider giving it a star!

---

**Keywords:** OCTALUME, enterprise SDLC, software development lifecycle, 8-phase framework, stage-gate process, quality gates, project management, Claude Code, AI-assisted development, enterprise methodology, go-no-go decisions, phase transitions, multi-agent orchestration, SDLC automation, DevOps, Agile, waterfall hybrid, security by design, compliance framework, traceability system

---

**Version:** 1.0.0
**Last Updated:** 2026
