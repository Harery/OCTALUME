# OCTALUME Setup Guide

**Your step-by-step journey to getting OCTALUME running on Linux**

---

## 🎯 What You'll Accomplish

In the next 10 minutes, you'll:

✅ Verify your system is ready
✅ Install OCTALUME
✅ Configure Claude Code
✅ Run your first OCTALUME project

**Sound good? Let's get started.**

---

## 👥 Who This Guide Is For

**This guide is perfect for you if:**

| Your Role | What You'll Get From This Guide |
|-----------|--------------------------------|
| **Developer** | Setup OCTALUME on your local machine |
| **DevOps Engineer** | Install in production environments |
| **Technical Lead** | Evaluate for team adoption |
| **System Administrator** | Configure on Linux systems |

**Prerequisite:** Basic comfort with command-line interfaces and package managers.

---

## 📋 Table of Contents

1. [Prerequisites](#prerequisites) — What you need before starting
2. [Installation](#installation) — Step-by-step setup
3. [Quick Start](#quick-start) — Your first project
4. [How OCTALUME Works](#how-octalume-works) — Understanding the framework
5. [Common Issues](#common-issues) — When things don't go as planned

---

## ✅ Prerequisites

### Let's Verify Your System

**Before we begin, let's make sure your system is ready:**

```bash
# Check Node.js version (need 18+)
node --version
```

**Expected output:** `v18.x.x` or higher

**If you see an older version:** Upgrade at [nodejs.org](https://nodejs.org)

```bash
# Check npm version (need 9+)
npm --version
```

**Expected output:** `9.x.x` or higher

**If you see an older version:** Update Node.js and npm will update too

```bash
# Check git version (need 2.0+)
git --version
```

**Expected output:** `git version 2.x.x` or higher

**If not installed:** Get it at [git-scm.com](https://git-scm.com)

### Minimum Requirements

| Component | Minimum Version |
|-----------|-----------------|
| Node.js | 18.0.0+ |
| npm | 9.0.0+ |
| git | 2.0+ |
| Linux | Ubuntu 20.04+, Debian 11+, CentOS 8+, or compatible |

### Platform Support

**Fully Supported:**
- ✅ **Linux** (Ubuntu, Debian, CentOS, RHEL, Arch, and compatible)

**Community Support:**
- ⚠️ **macOS** (Intel and Apple Silicon) — May work with minor adjustments
- ⚠️ **Windows 10/11** with WSL2 — Requires Windows Subsystem for Linux 2

> **Note:** This guide focuses on Linux. For macOS or Windows, adapt these instructions or check community resources.

---

## 🚀 Installation

### Step 1: Copy OCTALUME (1 minute)

**Let's put OCTALUME somewhere convenient:**

```bash
# Navigate to your preferred location
cd ~/projects/

# Copy OCTALUME folder
cp -r /path/to/OCTALUME ./

# Navigate into OCTALUME
cd OCTALUME
```

**What just happened:** You now have OCTALUME in your projects directory, ready to use.

### Step 2: Install MCP Server Dependencies (2 minutes)

**OCTALUME includes an MCP server for enhanced functionality:**

```bash
# Navigate to MCP server directory
cd .claude/mcp-server

# Install dependencies
npm install
```

**Expected output:** Lots of package installation text, ending with `added XXX packages`

**If you see errors:**
- `EACCES` permission error → Try with `sudo npm install`
- `network timeout` → Check your internet connection and try again
- `version mismatch` → Ensure Node.js 18+ is installed

```bash
# Return to root directory
cd ../..
```

### Step 3: Install Claude Code (2 minutes)

**Claude Code is the AI assistant that powers OCTALUME:**

```bash
# Install Claude Code globally
npm install -g @anthropic-ai/claude-code
```

**Expected output:** `+ @anthropic-ai/claude-code@X.X.X`

```bash
# Verify installation
claude --version
```

**Expected output:** Claude Code version information

```bash
# Login to your Anthropic account
claude login
```

**What happens:** Your browser opens — follow the prompts to authenticate

**If login fails:**
- Check your network connection
- Verify your Anthropic account is active
- Try `claude auth status` to check if already logged in

### Step 4: Verify Installation (1 minute)

**Let's make sure everything is ready:**

```bash
# Verify OCTALUME structure
ls -la
```

**You should see:**
```
✓ SETUP_GUIDE.md
✓ README.md
✓ FRAMEWORK_VISUALIZATION.md
✓ DIRECTORY_STRUCTURE.md
✓ CLAUDE.md
✓ LICENSE
✓ .gitignore
✓ .claude/          <-- HIDDEN but REQUIRED
✓ skills/
```

```bash
# Verify .claude directory exists
ls -la .claude/
```

**You should see:**
```
✓ ORCHESTRATOR.md
✓ CONTEXT_ENGINEERING.md
✓ agents/
✓ mcp-server/
✓ tools/
```

```bash
# Verify MCP server is ready
ls .claude/mcp-server/node_modules/
```

**You should see:** A long list of installed packages

**If any of these checks fail:**
- Missing `.claude/` directory → Re-copy OCTALUME including hidden files
- Empty `node_modules/` → Run `npm install` again in `.claude/mcp-server`
- Missing files → Re-copy OCTALUME from source

---

## 🎯 Quick Start

### Your First OCTALUME Project

**You're ready! Let's create your first project:**

```bash
# Navigate to OCTALUME directory
cd ~/projects/OCTALUME

# Start Claude Code
claude

# Your first prompt:
Initialize a new OCTALUME project for [your project idea]
```

**Example prompt:**
```
Initialize a new OCTALUME project for a task management app with:
- User registration and authentication
- Task creation, editing, and deletion
- Task categorization with tags
- Due dates and reminders
- Team collaboration features

Target market: Small teams and freelancers
Budget: Project resources - $50,000
Timeline: 4 months
Team: 3 developers, 1 QA
```

**What happens next:**
1. Claude asks clarifying questions
2. Creates your project structure
3. Generates a comprehensive feature list
4. Sets up git repository
5. Configures development environment
6. Starts Phase 1: Vision & Strategy

---

## 📖 How OCTALUME Works

### The Big Picture

**OCTALUME guides you through 8 phases:**

```
1. START → Claude Code session in OCTALUME directory
2. INITIALIZE → Create new project with /lifecycle-init
3. PHASE 1 → Vision & Strategy (Business Case + PRD)
4. PHASE 2 → Requirements (Requirements List)
5. PHASE 3-4 → Architecture & Planning (System Design + Sprint Plan)
6. PHASE 5 → Development (Build MVP with Agile sprints)
7. PHASE 6-8 → Quality, Deploy, Operations (Production)
```

### Creating a Business Case

**What is it?** A document that justifies why this project is worth investing in.

**What it includes:**
- Executive summary
- Business problem statement
- Proposed solution
- Market analysis
- Financial projections (ROI, cost estimates)
- Risk assessment
- Implementation timeline

**How OCTALUME creates it:**

```bash
# Start Claude Code
claude

# Use this prompt:
Initialize a new OCTALUME project for a task management app with:
- User registration and authentication
- Task creation, editing, and deletion
- Task categorization with tags
- Due dates and reminders
- Team collaboration features

Target market: Small teams and freelancers
Budget: Project resources - $50,000
Timeline: 4 months
Team: 3 developers, 1 QA
```

**What OCTALUME does:**
1. Analyzes your project description
2. Generates comprehensive Business Case
3. Creates financial projections with ROI
4. Identifies risks and mitigation strategies
5. Saves to: `artifacts/P1/P1-VISION-001-business-case.md`

**Example output:**

<details>
<summary><strong>See what a Business Case looks like</strong></summary>

```markdown
# Business Case: TeamSync Task Management

## Executive Summary
TeamSync is a task management application designed for small teams and freelancers
who need simple, powerful collaboration tools without enterprise complexity.

## Business Problem
Current solutions are either:
- Too simple (lack team features)
- Too complex (enterprise overload, expensive)
- Poor user experience (steep learning curve)

## Proposed Solution
TeamSync provides:
- Simple, intuitive task management
- Powerful collaboration features
- Affordable pricing per user
- Quick onboarding (5 minutes)

## Market Analysis
- Total addressable market: 50M freelancers worldwide
- Serviceable market: 5M using task management tools
- Target market: 500K small teams (2-10 people)

## Financial Projections
- Development cost: Project investment,000
- Monthly operating cost: Operational expenses,000
- Break-even: Estimated timeline based on user adoption
- Year 1 revenue projection: $180,000 (3,000 users avg)

## Risk Assessment
| Risk | Impact | Mitigation |
|------|--------|------------|
| Competition | High | Focus on simplicity and UX |
| Technical complexity | Medium | Use proven technologies |
| Time to market | Medium | MVP-first approach |

## Implementation Timeline
- Phase 1-2: 8 weeks (Vision & Requirements)
- Phase 3-4: 6 weeks (Architecture & Planning)
- Phase 5: 12 weeks (Development - 6 sprints)
- Phase 6: 4 weeks (Quality & Security)
- Phase 7: 2 weeks (Deployment)
- Total: 32 weeks (under 4-month target with buffer)
```

</details>

### Creating a PRD (Product Requirements Document)

**What is it?** A detailed document describing what you're building.

**What it includes:**
- Product vision and goals
- User personas
- User stories
- Functional requirements
- Non-functional requirements
- Success metrics
- Acceptance criteria

**How to create it (after Business Case):**

```bash
# In the same Claude Code session:
Now create the PRD for this task management app

Include:
- 3-5 user personas with demographics and goals
- 10-15 key user stories
- Functional requirements for each major feature
- Non-functional requirements (performance, security, scalability)
- Success metrics and KPIs
```

**What OCTALUME does:**
1. Reads the Business Case as context
2. Generates detailed PRD with user stories
3. Defines functional and non-functional requirements
4. Sets measurable success criteria
5. Saves to: `artifacts/P1/P1-VISION-002-prd.md`

### Building an MVP

**What is it?** The simplest version of your product that:
- Solves the core user problem
- Demonstrates key functionality
- Can be released to early users
- Provides feedback for future development

**When to build it:** Phase 5 (after completing Phases 1-4)

```bash
# In Claude Code, after completing planning:
We've completed the architecture and planning phases.
Now let's start Phase 5 and build the MVP.

Focus on these core features first:
1. User registration and login
2. Task creation and editing
3. Task lists and organization
4. Basic collaboration (assign tasks)

Use Python with Django framework, PostgreSQL database,
and Bootstrap for frontend.
```

**MVP Development Process:**

| Sprint | Duration | Features |
|--------|----------|----------|
| Sprint 1 | 2 weeks | User authentication, Database setup, Basic project structure |
| Sprint 2 | 2 weeks | Task CRUD operations, Task lists |
| Sprint 3 | 2 weeks | Task assignment, Comments, Basic notifications |

**Result:** MVP ready for user testing!

---

## 🔧 Common Issues: When Things Don't Go as Planned

<details>
<summary><strong>Claude Code not loading CLAUDE.md?</strong></summary>

**Symptom:** CLAUDE.md content not available when you start Claude Code

**Most likely cause:** You're not in the OCTALUME directory

**Quick fix:**
```bash
# Check where you are
pwd
# Should show: ~/projects/OCTALUME

# If not, navigate there
cd ~/projects/OCTALUME

# Try again
claude
```

**Still not working?** Make sure the `.claude` directory exists:
```bash
ls -la | grep .claude
# You should see: .claude/

# If not present, re-copy including hidden files
cp -r /source/OCTALUME/ ~/projects/OCTALUME/
```

</details>

<details>
<summary><strong>Hidden .claude folder not visible?</strong></summary>

**Symptom:** Can't see the `.claude` directory

**Why this happens:** Files starting with `.` are hidden by default

**Quick fix:**
```bash
# Show hidden files
ls -la | grep .claude

# If you see .claude/, everything is fine!
# It's there, just hidden from normal ls
```

**To verify it exists:**
```bash
# Try to access it
cd .claude
pwd
# Should show: ~/projects/OCTALUME/.claude
```

</details>

<details>
<summary><strong>npm install fails?</strong></summary>

**Symptom:** `npm install` command fails

**Most likely cause:** Node.js version is too old

**Quick fix:**
```bash
# Check Node.js version
node --version
# Must be 18+

# If too old, install Node.js 18+
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs

# Verify
node --version
# Should now show v18.x.x or higher
```

**Other reasons npm install might fail:**
- **Network timeout** → Check internet connection
- **Permission denied** → Try with `sudo npm install`
- **Disk space** → Check available disk space with `df -h`

</details>

<details>
<summary><strong>claude login fails?</strong></summary>

**Symptom:** Can't authenticate with Anthropic

**Quick checks:**
```bash
# Check network
ping api.anthropic.com
# Should get responses

# Check if already logged in
claude auth status
# Might show you're already authenticated
```

**If you need to re-login:**
```bash
claude login
# Browser opens → follow prompts
```

**Common issues:**
- **Wrong credentials** → Verify your Anthropic account email/password
- **Network blocked** → Check firewall/proxy settings
- **Browser issues** → Try a different browser

</details>

<details>
<summary><strong>MCP tools not available?</strong></summary>

**Symptom:** MCP tools don't appear in Claude Code

**Quick fix:**
```bash
cd .claude/mcp-server
rm -rf node_modules package-lock.json
npm install
cd ../..
```

**Verify installation:**
```bash
ls .claude/mcp-server/node_modules/
# Should see lots of packages
```

**Still failing?** Check Node.js version:
```bash
node --version
# Must be 18+ for MCP server compatibility
```

</details>

---

## 📚 Quick Reference

### Essential Commands

```bash
# Navigate to OCTALUME
cd ~/projects/OCTALUME

# Start Claude Code
claude

# Initialize new project
"Initialize a new OCTALUME project for [describe your project]"

# Continue existing project
"Continue working on Phase [X]"

# Check project status
"What is the current project status?"

# Move to next phase
"We've completed Phase [X]. Run go/no-go decision."

# Work on next feature
"Continue with the next feature"
```

### File Locations

| What | Where |
|------|-------|
| Main docs | `~/projects/OCTALUME/*.md` |
| Framework internals | `~/projects/OCTALUME/.claude/` |
| Phase skills | `~/projects/OCTALUME/skills/phase_*/` |
| Shared skills | `~/projects/OCTALUME/skills/shared/` |
| Artifacts | `~/projects/OCTALUME/artifacts/P*/` |

---

## 🎓 Next Steps

**After completing setup:**

1. ✅ Read [README.md](README.md) — Understand the full framework
2. ✅ Review [FRAMEWORK_VISUALIZATION.md](FRAMEWORK_VISUALIZATION.md) — See the 8-phase flow
3. ✅ Test the installation — Follow [TESTING_GUIDE.md](TESTING_GUIDE.md)
4. ✅ Start your first project — Use Claude Code to initialize
5. ✅ Create Business Case — Phase 1 deliverable
6. ✅ Create PRD — Phase 1 deliverable
7. ✅ Build MVP — Phase 5 deliverable

---

## 🏆 What You'll Create

**With OCTALUME, you'll create:**

| Deliverable | Why It Matters |
|-------------|----------------|
| **Business Case** | Justifies your project investment |
| **PRD** | Defines what you're building |
| **MVP** | Proves your concept works |
| **Full Product** | Scales through all 8 phases |

**All with AI assistance via Claude Code!**

---

## 💡 Pro Tips

### Tip #1: Always Start in the Right Directory

```bash
# Make this your first command
cd ~/projects/OCTALUME

# Then start Claude Code
claude
```

**Why:** Claude Code only loads CLAUDE.md if you're in the OCTALUME directory.

### Tip #2: Keep .claude Directory Intact

**Never delete or rename the `.claude` directory.** It contains:
- Auto-loaded context
- Agent configurations
- MCP server
- Tool definitions

### Tip #3: Verify Before You Begin

```bash
# Quick pre-flight check
pwd                    # Should show ~/projects/OCTALUME
node --version         # Should be v18+
claude --version       # Should show version info
```

**Pass all checks?** You're ready to go!

### Tip #4: Use Specific Prompts

**Vague:** "Help me with OCTALUME"

**Specific:** "Initialize a new OCTALUME project for a CRM system with lead tracking, contact management, and sales pipeline features."

**Why:** Specific prompts get specific results.

---

## 🎉 You're Ready!

**Congratulations!** You've completed the OCTALUME setup. You're now ready to:

- ✅ Create your first project
- ✅ Build software with confidence
- ✅ Deliver on time and on budget
- ✅ Maintain quality and security throughout

**Welcome to the OCTALUME community. Let's build something great together!**

---

**Platform:** Linux
**Version:** 1.0.0
**Last Updated:** 2026-01-20

---

> **One more thing:** Setup is just the beginning. As you use OCTALUME, you'll discover patterns, shortcuts, and best practices that work for your team. Don't be afraid to experiment — the framework is here to guide you, not constrain you.
