# OCTALUME Framework - Setup Guide (Linux)

**Complete step-by-step guide to set up and use OCTALUME on Linux**

---

<!-- SEO Metadata -->
**Keywords:** OCTALUME, Linux setup, enterprise SDLC, software development lifecycle, 8-phase framework, stage-gate process, quality gates, project management, Claude Code, AI-assisted development, Business Case, PRD, MVP creation
**Description:** Complete Linux setup guide for OCTALUME - create Business Case, PRD, and MVP using enterprise-grade 8-phase SDLC framework with AI-assisted development
**Tags:** #OCTALUME #Linux #SDLC #BusinessCase #PRD #MVP #ProjectManagement #ClaudeCode #AIFramework
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

## TABLE OF CONTENTS

1. [Prerequisites](#prerequisites)
2. [Installation](#installation)
3. [Quick Start](#quick-start)
4. [How to Use OCTALUME](#how-to-use-octalume)
   - [Creating a Business Case](#creating-a-business-case)
   - [Creating a PRD](#creating-a-prd)
   - [Creating an MVP](#creating-an-mvp)
5. [Where to Start](#where-to-start)
6. [Troubleshooting](#troubleshooting)

---

## PREREQUISITES

Before installing OCTALUME, ensure you have:

```bash
# Check Node.js version (must be 18+)
node --version

# Check npm version
npm --version

# Check git version
git --version
```

**Minimum Requirements:**
- Node.js: 18.0.0 or higher
- npm: 9.0.0 or higher
- git: 2.0 or higher
- Linux: Ubuntu 20.04+, Debian 11+, CentOS 8+, or compatible

---

## INSTALLATION

### Step 1: Copy OCTALUME Framework

```bash
# Navigate to your preferred directory
cd ~/projects/

# Copy OCTALUME folder
cp -r /path/to/OCTALUME ./

# Navigate into OCTALUME
cd OCTALUME
```

### Step 2: Install MCP Server Dependencies

```bash
# Navigate to MCP server directory
cd .claude/mcp-server

# Install dependencies
npm install

# Return to root
cd ../..
```

### Step 3: Install Claude Code

```bash
# Install Claude Code globally
npm install -g @anthropic-ai/claude-code

# Verify installation
claude --version

# Login to your Anthropic account
claude login
```

Follow the browser prompts to authenticate.

### Step 4: Verify Installation

```bash
# Verify OCTALUME structure
ls -la

# You should see:
# - SETUP_GUIDE.md
# - README.md
# - FRAMEWORK_VISUALIZATION.md
# - DIRECTORY_STRUCTURE.md
# - CLAUDE.md
# - LICENSE
# - .gitignore
# - .claude/          <-- HIDDEN but REQUIRED
# - skills/

# Verify .claude directory exists
ls -la .claude/

# Verify MCP server is ready
ls .claude/mcp-server/node_modules/
```

---

## QUICK START

```bash
# Navigate to OCTALUME directory
cd ~/projects/OCTALUME

# Start Claude Code
claude

# Your first prompt:
Initialize a new OCTALUME project for [your project idea]
```

---

## HOW TO USE OCTALUME

### Complete Workflow Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                  OCTALUME PROJECT CREATION FLOW               │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. START with Claude Code                                     │
│     └─> claude (in OCTALUME directory)                         │
│                                                                 │
│  2. INITIALIZE Project                                         │
│     └─> "Initialize a new OCTALUME project for..."            │
│                                                                 │
│  3. PHASE 1: Vision & Strategy                                  │
│     ├─> Business Case Created                                  │
│     ├─> PRD Created                                           │
│     └─> Go/No-Go Decision                                     │
│                                                                 │
│  4. PHASE 2: Requirements                                      │
│     └─> Requirements List Created                               │
│                                                                 │
│  5. PHASE 3-4: Architecture & Planning                         │
│     └─> System Design & Sprint Plan                            │
│                                                                 │
│  6. PHASE 5: Development (Build MVP)                            │
│     └─> Working MVP Created                                    │
│                                                                 │
│  7. PHASE 6-8: Quality, Deploy, Operations                    │
│     └─> Production Deployment                                   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

### Creating a Business Case

**What is a Business Case?**
A document that justifies the investment in a project. It includes:
- Executive summary
- Business problem statement
- Proposed solution
- Market analysis
- Financial projections (ROI, cost estimates)
- Risk assessment
- Implementation timeline

**How OCTALUME Creates It:**

```bash
# Start Claude Code
claude

# Use this prompt:
Initialize a new OCTALUME project for an e-commerce platform with:
- User authentication and authorization
- Product catalog with search and filtering
- Shopping cart and checkout process
- Payment integration (Stripe/PayPal)
- Order management and tracking
- Admin dashboard for inventory management

Target market: Small to medium businesses
Budget: $50,000 - $100,000
Timeline: 6 months
Team: 5 developers, 1 QA, 1 DevOps
Compliance: PCI DSS required for payment processing
```

**What OCTALUME Does:**
1. ✅ Analyzes your project description
2. ✅ Generates comprehensive Business Case
3. ✅ Creates financial projections with ROI
4. ✅ Identifies risks and mitigation strategies
5. ✅ Saves to: `artifacts/P1/P1-VISION-001-business-case.md`

**Business Case Template Location:**
```
skills/phase_01_vision_strategy/templates/business-case-template.md
```

---

### Creating a PRD (Product Requirements Document)

**What is a PRD?**
A detailed document that describes what you're building, including:
- Product vision and goals
- User personas
- User stories
- Functional requirements
- Non-functional requirements
- Success metrics
- Acceptance criteria

**How OCTALUME Creates It:**

After creating the Business Case, continue with:

```bash
# In the same Claude Code session:
Now create the PRD for this e-commerce platform

Include:
- 3-5 user personas with demographics and goals
- 10-15 key user stories
- Functional requirements for each major feature
- Non-functional requirements (performance, security, scalability)
- Success metrics and KPIs
```

**What OCTALUME Does:**
1. ✅ Reads the Business Case as context
2. ✅ Generates detailed PRD with user stories
3. ✅ Defines functional and non-functional requirements
4. ✅ Sets measurable success criteria
5. ✅ Saves to: `artifacts/P1/P1-VISION-002-prd.md`

**PRD Template Location:**
```
skills/phase_01_vision_strategy/templates/prd-template.md
```

---

### Creating an MVP (Minimum Viable Product)

**What is an MVP?**
The simplest version of your product that:
- Solves the core user problem
- Demonstrates key functionality
- Can be released to early users
- Provides feedback for future development

**How OCTALUME Creates It:**

**Phase 5 is where the MVP is built.** After completing Phases 1-4:

```bash
# In Claude Code, after completing planning:
We've completed the architecture and planning phases.
Now let's start Phase 5 and build the MVP.

Focus on these core features first:
1. User registration and login
2. Product listing page
3. Basic shopping cart
4. Simple checkout with one payment option
5. Order confirmation

Use Python with Django framework, PostgreSQL database,
and Bootstrap for frontend.
```

**What OCTALUME Does:**
1. ✅ Identifies MVP features from the full feature list
2. ✅ Generates code iteratively (one feature at a time)
3. ✅ Creates unit tests for each feature
4. ✅ Performs code reviews
5. ✅ Commits with traceability (P5-CODE-###)
6. ✅ Delivers working MVP after first sprint

**MVP Development Process:**
```
┌─────────────────────────────────────────┐
│         MVP DEVELOPMENT CYCLE          │
├─────────────────────────────────────────┤
│                                         │
│  Sprint 1 (2 weeks)                     │
│  ├─> User authentication                │
│  ├─> Database setup                     │
│  ├─> Basic project structure           │
│  └─> Working login system              │
│                                         │
│  Sprint 2 (2 weeks)                     │
│  ├─> Product catalog                   │
│  ├─> Product detail page               │
│  └─> Search functionality              │
│                                         │
│  Sprint 3 (2 weeks)                     │
│  ├─> Shopping cart                     │
│  ├─> Checkout process                  │
│  └─> Payment integration               │
│                                         │
│  MVP READY for user testing!           │
│                                         │
└─────────────────────────────────────────┘
```

---

## WHERE TO START

### Step-by-Step Starting Point

```
┌─────────────────────────────────────────────────────────────┐
│                    WHERE TO START                            │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  STEP 1: Open Terminal                                       │
│  ─────────────────                                        │
│  cd ~/projects/OCTALUME                                     │
│                                                             │
│  STEP 2: Start Claude Code                                  │
│  ─────────────────────────                                │
│  claude                                                     │
│                                                             │
│  STEP 3: Initialize Your Project                           │
│  ─────────────────────────                                │
│  "Initialize a new OCTALUME project for [your idea]"      │
│                                                             │
│  STEP 4: Review Business Case                              │
│  ─────────────────────────                                │
│  OCTALUME generates it automatically                       │
│  Review and approve                                       │
│                                                             │
│  STEP 5: Create PRD                                        │
│  ─────────────────────────                                │
│  "Now create the PRD for this project"                    │
│  Review and refine                                        │
│                                                             │
│  STEP 6: Proceed Through Phases                           │
│  ─────────────────────────                                │
│  Follow OCTALUME's guidance through all 8 phases          │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### First-Time User Example

```bash
# 1. Navigate to OCTALUME
cd ~/projects/OCTALUME

# 2. Start Claude Code
claude

# 3. Your complete first prompt:
Initialize a new OCTALUME project for a task management application with:
- User authentication (email/password, OAuth)
- Project creation and management
- Task creation with due dates and priorities
- Team member collaboration
- Progress tracking and reporting
- Email notifications

Target: Startups and small teams
Budget: $30,000
Timeline: 4 months
Compliance: SOC 2 required

After initialization, create the Business Case and PRD.
```

---

## DELIVERABLES TIMELINE

```
┌────────────────────────────────────────────────────────────────┐
│              WHAT YOU GET AND WHEN                          │
├────────────────────────────────────────────────────────────────┤
│                                                                │
│  Week 1-4                                                       │
│  ├─ Business Case (P1-VISION-001)                            │
│  ├─ PRD (P1-VISION-002)                                       │
│  ├─ Market Analysis                                           │
│  └─ Stakeholder Sign-off                                     │
│                                                                │
│  Week 5-8                                                       │
│  ├─ Requirements List (P2-REQ-###)                           │
│  ├─ Traceability Matrix                                        │
│  └─ Approval                                                 │
│                                                                │
│  Week 9-14                                                      │
│  ├─ System Architecture (P3-ARCH-###)                         │
│  ├─ Security Architecture                                     │
│  └─ Data Architecture                                         │
│                                                                │
│  Week 15-16                                                    │
│  ├─ Development Plan (P4-PLAN-###)                           │
│  ├─ Sprint 0 Setup                                           │
│  └─ Resource Allocation                                       │
│                                                                │
│  Week 17+                                                       │
│  ├─ MVP Development (P5-CODE-###)                            │
│  │   ├─ Sprint 1: Core features                              │
│  │   ├─ Sprint 2: Enhanced features                          │
│  │   └─ Sprint 3: Polish and test                            │
│  ├─ MVP Ready                                                │
│  └─ User Testing Begins                                      │
│                                                                │
└────────────────────────────────────────────────────────────────┘
```

---

## TROUBLESHOOTING

### Problem: Claude Code doesn't load CLAUDE.md

```bash
# SOLUTION: Make sure you're in the OCTALUME directory
pwd  # Should show: ~/projects/OCTALUME

cd ~/projects/OCTALUME
claude
```

### Problem: Hidden .claude folder not visible

```bash
# SOLUTION: Show hidden files
ls -la | grep .claude

# If not present, re-copy including hidden files
cp -r /source/OCTALUME/ ~/projects/OCTALUME/
```

### Problem: npm install fails

```bash
# SOLUTION: Check Node.js version
node --version  # Must be 18+

# If too old, install Node.js 18+
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs

# Verify
node --version
```

### Problem: claude login fails

```bash
# SOLUTION: Check network connection
ping api.anthropic.com

# Check if already logged in
claude auth status

# Re-login if needed
claude login
```

### Problem: MCP server tools not available

```bash
# SOLUTION: Reinstall dependencies
cd .claude/mcp-server
rm -rf node_modules package-lock.json
npm install
cd ../..
```

---

## QUICK REFERENCE COMMANDS

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

# Work on feature
"Continue with the next feature"
```

---

## FILE STRUCTURE

```
OCTALUME/
├── SETUP_GUIDE.md               ← You are here
├── README.md                    ← Project overview
├── FRAMEWORK_VISUALIZATION.md   ← Visual diagrams
├── DIRECTORY_STRUCTURE.md       ← Complete file listing
├── CLAUDE.md                    ← Auto-loaded by Claude Code
├── LICENSE
├── .gitignore
│
├── .claude/                     ← HIDDEN but REQUIRED!
│   ├── mcp-server/              ← AI tools (npm install required)
│   ├── agents/                  ← Agent configurations
│   ├── skills/                  ← Phase skills
│   ├── memory/                  ← Project state
│   └── ...                     ← Other systems
│
└── skills/                      ← All phase and shared skills
    ├── phase_01_vision_strategy/    ← Business Case & PRD
    ├── phase_02_requirements_scope/
    ├── phase_03_architecture_design/
    ├── phase_04_development_planning/
    ├── phase_05_development_execution/    ← MVP built here
    ├── phase_06_quality_security/
    ├── phase_07_deployment_release/
    ├── phase_08_operations_maintenance/
    └── shared/                   ← Cross-cutting skills
```

---

## NEXT STEPS

After completing setup:

1. ✅ **Read README.md** - Understand the full framework
2. ✅ **Review FRAMEWORK_VISUALIZATION.md** - See the 8-phase flow
3. ✅ **Start your first project** - Use Claude Code to initialize
4. ✅ **Create Business Case** - Phase 1 deliverable
5. ✅ **Create PRD** - Phase 1 deliverable
6. ✅ **Build MVP** - Phase 5 deliverable

---

## GETTING HELP

```
┌─────────────────────────────────────────────────────┐
│                    DOCUMENTATION                     │
├─────────────────────────────────────────────────────┤
│                                                     │
│  SETUP_GUIDE.md                   ← This file       │
│     Installation and usage guide                    │
│                                                     │
│  README.md                                         │
│     Complete project overview                      │
│                                                     │
│  FRAMEWORK_VISUALIZATION.md                       │
│     Mermaid diagrams and flows                      │
│                                                     │
│  CLAUDE.md                                          │
│     Auto-loaded framework context                   │
│                                                     │
│  DIRECTORY_STRUCTURE.md                             │
│     Complete file listing                           │
│                                                     │
└─────────────────────────────────────────────────────┘
```

---

## QUICK CHECKLIST

Before starting your first project:

```
□ OCTALUME folder copied (including .claude hidden folder)
□ cd ~/projects/OCTALUME
□ Node.js 18+ installed (node --version)
□ npm install run in .claude/mcp-server/
□ Claude Code installed (npm install -g @anthropic-ai/claude-code)
□ Logged in with claude login
□ claude command works from OCTALUME directory
□ Read README.md for framework overview
```

---

## SUMMARY

OCTALUME helps you create:
- ✅ **Business Case** - Justify your project investment
- ✅ **PRD** - Define what you're building
- ✅ **MVP** - Build your minimum viable product
- ✅ **Full Product** - Scale through all 8 phases

**All with AI assistance via Claude Code!**

---

**Version:** 1.0.0
**Platform:** Linux
**Last Updated:** 2026
