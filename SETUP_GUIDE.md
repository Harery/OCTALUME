# OCTALUME Setup Guide

Complete installation and setup instructions for the OCTALUME Enterprise Lifecycle Framework.

---

## Quick Start (2 Minutes)

```bash
# Clone the repository
git clone https://github.com/Harery/OCTALUME.git
cd OCTALUME

# Start Claude Code
claude
```

OCTALUME loads automatically. No additional installation required.

---

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Installation](#installation)
3. [First Project](#first-project)
4. [Daily Workflow](#daily-workflow)
5. [Common Issues](#common-issues)
6. [Reference](#reference)

---

## Prerequisites

### Required Software

| Software | Version | Check Command |
|----------|---------|---------------|
| Node.js | 18.0+ | `node --version` |
| npm | 9.0+ | `npm --version` |
| git | 2.0+ | `git --version` |
| jq | 1.6+ | `jq --version` |

### Install Missing Dependencies

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install nodejs npm git jq
```

**CentOS/RHEL:**
```bash
sudo yum install nodejs npm git jq
```

**macOS:**
```bash
brew install node git jq
```

### Platform Support

| Platform | Status |
|----------|--------|
| Linux (Ubuntu, Debian, CentOS) | Fully Supported |
| macOS (Intel and Apple Silicon) | Supported |
| Windows with WSL2 | Supported |

---

## Installation

### Step 1: Clone the Repository

```bash
cd ~/projects
git clone https://github.com/Harery/OCTALUME.git
cd OCTALUME
```

### Step 2: Install MCP Server (Optional)

The MCP server provides enhanced functionality:

```bash
cd .claude/mcp-server
npm install
cd ../..
```

### Step 3: Install Claude Code

```bash
npm install -g @anthropic-ai/claude-code
```

### Step 4: Login to Claude

```bash
claude login
```

Follow the browser prompts to authenticate.

### Step 5: Verify Installation

```bash
ls -la
```

You should see:
- CLAUDE.md
- README.md
- SETUP_GUIDE.md
- skills/
- .claude/

---

## First Project

### Start Claude Code

```bash
cd ~/projects/OCTALUME
claude
```

### Initialize Your Project

Type this prompt:

```
Initialize a new lifecycle project for [describe your project]
```

**Example:**
```
Initialize a new lifecycle project for a task management app with:
- User authentication
- Task creation and editing
- Due dates and reminders
- Team collaboration
Timeline: 4 months
Team: 3 developers
```

### What Happens Next

1. Claude asks clarifying questions
2. Creates project structure
3. Generates 200-500 features
4. Sets up git repository
5. Starts Phase 1: Vision and Strategy

---

## Daily Workflow

### Starting Your Day

```bash
cd ~/projects/OCTALUME
claude
```

Claude reads your project state and continues where you left off.

### Check Status

```
What is the current project status?
```

### Move to Next Phase

```
We have completed Phase 2. Run go/no-go and move to Phase 3.
```

### Handle Blockers

```
We are blocked on [describe the issue]
```

### Continue Development

```
Continue with the next feature
```

---

## Common Issues

### Claude Code Not Loading Context

**Problem:** Claude does not recognize OCTALUME commands.

**Solution:** Ensure you are in the OCTALUME directory:
```bash
pwd  # Should show path to OCTALUME
```

### MCP Server Issues

**Problem:** npm install fails in .claude/mcp-server

**Solution:**
```bash
rm -rf node_modules package-lock.json
npm install
```

### Permission Errors

**Problem:** Permission denied when running scripts

**Solution:**
```bash
chmod +x scripts/*.sh
chmod +x .claude/hooks/*.sh
chmod +x .claude/memory/*.sh
```

### Node Version Too Old

**Problem:** Requires Node.js 18+

**Solution:**
```bash
# Using nvm
nvm install 18
nvm use 18
```

---

## Reference

### Essential Commands

| Action | Command |
|--------|---------|
| Start Claude Code | `claude` |
| Initialize project | `Initialize a new lifecycle project for...` |
| Check status | `What is the current project status?` |
| Move to next phase | `We have completed Phase X. Run go/no-go.` |
| Continue work | `Continue with the next feature` |

### File Locations

| What | Where |
|------|-------|
| Framework context | CLAUDE.md |
| Phase skills | skills/phase_XX/ |
| Shared skills | skills/shared/ |
| Memory bank | .claude/memory/ |
| Project state | .claude/project-state.json |

### The 8 Phases

| Phase | Name | Owner |
|:-----:|------|-------|
| 1 | Vision and Strategy | Product Owner |
| 2 | Requirements and Scope | Product Owner |
| 3 | Architecture and Design | CTA |
| 4 | Development Planning | Project Manager |
| 5 | Development Execution | Tech Lead |
| 6 | Quality and Security | QA Lead |
| 7 | Deployment and Release | DevOps |
| 8 | Operations and Maintenance | SRE |

---

## Next Steps

After setup:

1. Read [README.md](README.md) for framework overview
2. Review [FRAMEWORK_VISUALIZATION.md](FRAMEWORK_VISUALIZATION.md) for visual workflows
3. Run [TESTING_GUIDE.md](TESTING_GUIDE.md) to verify installation
4. Start your first project with Claude Code

---

## Support

| Channel | Details |
|---------|---------|
| Repository | https://github.com/Harery/OCTALUME |
| Email | octalume@harery.com |
| Website | https://harery.com |

---

Version 1.0.0 | OCTALUME Enterprise Lifecycle Framework
