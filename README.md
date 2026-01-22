# OCTALUME v2.0

Enterprise Software Development Lifecycle Framework with AI-Powered Automation

[![Version](https://img.shields.io/badge/version-2.0.0-blue.svg)](CHANGELOG.md)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Compatible-purple.svg)](https://docs.anthropic.com/claude-code)

---

## 🚀 What's New in v2.0

OCTALUME v2.0 brings enterprise governance together with modern AI automation:

| Feature | Description |
|---------|-------------|
| 🧠 **Cross-Session Memory** | Claude remembers decisions, patterns, and lessons across sessions |
| 🌳 **Git Worktrees** | Parallel feature development without stashing |
| ✅ **Automated QA** | Phase-specific quality checks with auto-fix |
| 🐙 **GitHub Integration** | Create issues and PRs directly from Claude |
| 🔍 **Stack Detection** | Auto-detect project technologies and configure accordingly |
| 📝 **Changelog Generation** | Auto-generate CHANGELOG from conventional commits |

---

## What is OCTALUME?

**Octa** = 8 phases | **Lume** = light/guidance

OCTALUME guides you through the entire software lifecycle, from initial vision to production operations, ensuring nothing falls through the cracks.

---

## The Problem

Building enterprise software is complex:

- Requirements shift constantly
- Stakeholders pull in different directions
- Security becomes an afterthought
- Compliance gets tacked on at the end
- Documentation lags behind reality
- **AI assistants forget context between sessions**

---

## The Solution

OCTALUME provides:

| Feature | Benefit |
|---------|---------|
| 8 Sequential Phases | Clear progression from idea to production |
| Quality Gates | Go/no-go decisions prevent problems from advancing |
| 16 Defined Roles | Clear ownership at every stage |
| Full Traceability | Every decision and artifact tracked |
| Security First | Built-in from Phase 1, not bolted on later |
| Compliance Ready | HIPAA, SOC 2, PCI DSS, GDPR, SOX support |
| **AI Memory** | Context persists across Claude sessions |
| **Automation** | QA, Git workflows, and releases automated |

---

## The 8 Phases

| Phase | Name | Owner | What You Get |
|:-----:|------|-------|--------------|
| P1 | Vision and Strategy | Product Owner | PRD, Business Case |
| P2 | Requirements and Scope | Product Owner | Requirements, Traceability Matrix |
| P3 | Architecture and Design | CTA | System Architecture, Threat Models |
| P4 | Development Planning | Project Manager | WBS, Sprint Plan |
| P5 | Development Execution | Tech Lead | Working Software |
| P6 | Quality and Security | QA Lead | Test Results, Security Sign-off |
| P7 | Deployment and Release | DevOps | Production Deployment |
| P8 | Operations and Maintenance | SRE | Monitoring, Continuous Improvement |

---

## Quick Start

### Prerequisites
- Git
- Node.js 18+ (for memory system)
- GitHub CLI (`gh`) - optional, for GitHub integration
- Claude Code CLI - recommended

### Installation

```bash
# Clone the framework
git clone https://github.com/your-org/octalume.git my-project
cd my-project

# Initialize for your project
./scripts/init-project.sh

# Detect your technology stack
./scripts/stack-detector.sh detect

# Start Claude Code
claude
```

### First Commands

```bash
# Inside Claude Code session:

# See what stack was detected
/stack-detect

# Set your current phase
/memory-context phase P3

# Run quality checks
/qa-run

# Search memory for past decisions
/memory-search authentication
```

---

## v2.0 Commands Reference

### Memory System
| Command | Description |
|---------|-------------|
| `/memory-search <query>` | Search project memory |
| `/memory-save <type> <data>` | Save insight to memory |
| `/memory-context <field> <value>` | Set working context |
| `/memory-stats` | View memory statistics |

### Git Worktrees
| Command | Description |
|---------|-------------|
| `/worktree-init <name>` | Create feature worktree |
| `/worktree-list` | List active worktrees |
| `/worktree-merge <name>` | Merge worktree back |
| `/worktree-discard <name>` | Discard worktree |

### Quality Assurance
| Command | Description |
|---------|-------------|
| `/qa-run [phase]` | Run QA checks |
| `/qa-fix` | Auto-fix issues |
| `/qa-status` | View last QA report |

### GitHub Integration
| Command | Description |
|---------|-------------|
| `/github-issue <title>` | Create GitHub issue |
| `/github-pr` | Create pull request |

### Utilities
| Command | Description |
|---------|-------------|
| `/stack-detect` | Detect tech stack |
| `/changelog [action]` | Generate changelog |

---

## Typical Workflow

### Feature Development

```bash
# 1. Start feature in isolated worktree
/worktree-init user-authentication

# 2. Claude has context - develop your feature
# ... Claude assists with code ...

# 3. Save important decisions
/memory-save decision {"decision": "Use JWT tokens", "rationale": "Stateless, scalable"}

# 4. Run QA before merge
/qa-run P5

# 5. Merge and cleanup
/worktree-merge user-authentication --delete

# 6. Create PR with auto-generated description
/github-pr
```

### Release

```bash
# 1. Full QA check
/qa-run

# 2. Preview changelog
/changelog preview

# 3. Release (bumps version, generates changelog)
/changelog release minor
```

---

## Who Is This For?

| Your Situation | How OCTALUME Helps |
|----------------|-------------------|
| Building enterprise apps | Phase gates ensure quality |
| Working with Claude Code | Memory persists across sessions |
| Need compliance (HIPAA, SOC 2) | Built-in compliance checklists |
| Leading a development team | Clear roles and responsibilities |
| Managing complex projects | Full traceability from idea to production |

---

## Directory Structure

```
OCTALUME/
├── CLAUDE.md           # Auto-loaded by Claude Code
├── README.md           # This file
├── SETUP_GUIDE.md      # Detailed setup instructions
├── .claude/
│   ├── commands/       # Slash commands
│   ├── memory/         # Cross-session memory
│   ├── worktrees/      # Worktree tracking
│   ├── qa/             # QA criteria and reports
│   ├── integrations/   # GitHub, etc.
│   └── specs/          # Detected stack
├── scripts/            # Automation scripts
└── skills/             # Phase-specific knowledge
```

---

## Comparison with Auto-Claude

| Feature | OCTALUME v2.0 | Auto-Claude |
|---------|--------------|-------------|
| Enterprise Governance | ✅ 8-phase lifecycle | ❌ |
| Compliance Built-in | ✅ HIPAA, SOC 2, etc. | ❌ |
| Cross-Session Memory | ✅ | ✅ |
| Git Worktrees | ✅ | ✅ |
| QA Automation | ✅ Phase-specific | ✅ Generic |
| GitHub Integration | ✅ | ✅ |
| Claude Code Compatible | ✅ | ❌ Desktop only |
| Multi-Agent | ✅ Orchestrator | ✅ |
| Open Source | ✅ | ✅ |

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## Security

See [SECURITY.md](SECURITY.md) for reporting vulnerabilities.

## License

MIT License - see [LICENSE](LICENSE)

---

**OCTALUME v2.0.0** | Enterprise Lifecycle Framework
*Combining governance with automation for modern software delivery*
