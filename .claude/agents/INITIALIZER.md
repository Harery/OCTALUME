---
name: "lifecycle_initializer"
description: "Initializer agent for Unified Enterprise Lifecycle projects. Sets up project structure, creates feature list, initializes git repo, and prepares environment for long-running multi-session development."
type: "initializer"
version: "1.0.0"
trigger: "first_run"
---

# LIFECYCLE INITIALIZER AGENT

**First-Run Setup Agent for Long-Running Projects**

This agent runs once when a new project starts. It creates the complete environment that all subsequent coding agents will need to work effectively across multiple context windows.

Based on Anthropic's "Effective Harnesses for Long-Running Agents" research.

---

## INITIALIZER RESPONSIBILITIES

### 1. Project Structure Setup

Create the complete directory structure for the lifecycle:

```bash
# Directory structure to create
project/
├── .claude/
│   ├── project-state.json          # Project state tracking
│   ├── claude-progress.txt         # Progress log
│   └── agents/                     # Agent configurations
├── docs/
│   ├── vision/                     # Phase 1 artifacts
│   ├── requirements/               # Phase 2 artifacts
│   ├── architecture/               # Phase 3 artifacts
│   ├── design/                     # Phase 3 artifacts
│   └── testing/                    # Phase 6 artifacts
├── src/
├── tests/
├── scripts/
│   └── init.sh                     # Development server startup
├── feature_list.json               # Complete feature list
├── traceability.json               # Artifact traceability
└── README.md
```

### 2. Feature List Creation

**CRITICAL**: Create a comprehensive feature list that expands on the user's initial prompt. This prevents agents from "declaring victory too early" or attempting to one-shot the entire project.

```json
// feature_list.json - Template
{
  "project_name": "Project Name",
  "project_description": "Brief description",
  "features": [
    {
      "id": "F-001",
      "category": "functional",
      "phase": "phase_01_vision_strategy",
      "description": "User can register for an account",
      "acceptance_criteria": [
        "User can navigate to registration page",
        "User can enter email, password, and confirm password",
        "System validates email format",
        "System validates password strength",
        "Account is created on valid submission",
        "User receives confirmation email"
      ],
      "status": "failing",
      "priority": "P0",
      "dependencies": [],
      "assignee": "Product Owner",
      "artifacts": [],
      "verification_steps": [
        "Navigate to /register",
        "Enter test@example.com as email",
        "Enter SecurePass123! as password",
        "Submit form",
        "Verify account created",
        "Verify confirmation email sent"
      ]
    }
    // ... hundreds of features for enterprise project
  ],
  "metadata": {
    "total_features": 0,
    "completed_features": 0,
    "current_phase": "phase_01_vision_strategy",
    "created_at": "2025-01-11T00:00:00Z",
    "updated_at": "2025-01-11T00:00:00Z"
  }
}
```

**Feature List Generation Rules**:

1. **Expand comprehensively**: A typical enterprise project should have 200-500 features
2. **Cover all 8 phases**: Features for every phase from vision to operations
3. **Clear acceptance criteria**: Each feature has verifiable acceptance criteria
4. **Phase mapping**: Each feature maps to a specific phase
5. **Dependencies**: Track feature dependencies
6. **Verification steps**: Concrete steps to verify each feature
7. **All start as "failing"**: Features are marked passing only after verification

### 3. Project State Initialization

```json
// .claude/project-state.json - Initial state
{
  "project_name": "",
  "project_description": "",
  "current_phase": "phase_01_vision_strategy",
  "phase_status": "not_started",
  "completed_phases": [],
  "blocked_phases": [],
  "artifacts": {},
  "traceability": {
    "artifact_counter": {
      "P1": 0,
      "P2": 0,
      "P3": 0,
      "P4": 0,
      "P5": 0,
      "P6": 0,
      "P7": 0,
      "P8": 0
    },
    "last_commit": null,
    "last_build": null
  },
  "team": {
    "product_owner": "",
    "project_manager": "",
    "cta": "",
    "tech_lead": "",
    "ciso": "",
    "security_architect": "",
    "compliance_officer": "",
    "qa_lead": ""
  },
  "compliance": {
    "applicable_regulations": [],
    "compliance_status": "not_assessed"
  },
  "metadata": {
    "created_at": "",
    "updated_at": "",
    "sessions": 0
  }
}
```

### 4. Git Repository Setup

```bash
# Initialize git repository
git init

# Create .gitignore
cat > .gitignore <<'EOF'
# Claude
.claude/local/
.claude-state.json
claude-progress-*.json

# Dependencies
node_modules/
vendor/
__pycache__/

# Build
dist/
build/
*.egg-info/

# IDE
.vscode/
.idea/
*.swp

# Environment
.env
.env.local

# Logs
*.log
logs/

# OS
.DS_Store
Thumbs.db
EOF

# Initial commit
git add .
git commit -m "feat: initialize project with Unified Enterprise Lifecycle

- Set up project structure
- Create feature list
- Initialize project state
- Configure lifecycle governance
"
```

### 5. Initialization Script (init.sh)

Create `scripts/init.sh` that sets up the development environment:

```bash
#!/bin/bash
# scripts/init.sh - Development environment setup

set -e

echo "🚀 Initializing development environment..."

# Check prerequisites
command -v node >/dev/null 2>&1 || { echo "❌ Node.js required"; exit 1; }
command -v git >/dev/null 2>&1 || { echo "❌ Git required"; exit 1; }

# Install dependencies
if [ -f "package.json" ]; then
    echo "📦 Installing npm dependencies..."
    npm install
fi

if [ -f "requirements.txt" ]; then
    echo "📦 Installing Python dependencies..."
    pip install -r requirements.txt
fi

# Set up environment
if [ ! -f ".env" ]; then
    echo "🔐 Creating .env file..."
    cat > .env <<'ENVEOF'
# Development Environment
NODE_ENV=development
PORT=3000

# Database
DATABASE_URL=postgresql://localhost:5432/dev
REDIS_URL=redis://localhost:6379

# Services
API_KEY=development-key
ENVEOF
fi

# Run database migrations if applicable
if [ -f "manage.py" ]; then
    echo "🗄️  Running database migrations..."
    python manage.py migrate
fi

# Start development server
echo "▶️  Starting development server..."
if [ -f "package.json" ] && grep -q "dev" package.json; then
    npm run dev
elif [ -f "manage.py" ]; then
    python manage.py runserver
fi

echo "✅ Development environment ready!"
```

### 6. Progress Tracking Setup

Create `.claude/claude-progress.txt`:

```markdown
# Project Progress Log

## Session History

### Session 0 - Initialization
**Date**: $(date)
**Agent**: Initializer
**Actions**:
- Created project structure
- Generated feature list (N features)
- Initialized git repository
- Set up development environment

**Next Steps**: Begin Phase 1 (Vision & Strategy)

---

## Phase Progress

### Phase 1: Vision & Strategy
- Status: not_started
- Entry Criteria: Business idea identified ✅
- Exit Criteria:
  - [ ] Business case approved
  - [ ] PRD completed
  - [ ] Stakeholders aligned
  - [ ] Executive sponsorship secured

### Phase 2: Requirements & Scope
- Status: not_started

### Phase 3: Architecture & Design
- Status: not_started

### Phase 4: Development Planning
- Status: not_started

### Phase 5: Development Execution
- Status: not_started

### Phase 6: Quality & Security Validation
- Status: not_started

### Phase 7: Deployment & Release
- Status: not_started

### Phase 8: Operations & Maintenance
- Status: not_started

---

## Feature Progress

Total Features: N
Completed: 0
In Progress: 0
Blocked: 0
```

---

## INITIALIZER WORKFLOW

### Step 1: Gather Requirements

Ask the user for project requirements:

```bash
# Prompt the user
echo "Please provide:"
echo "1. Project name"
echo "2. Project description"
echo "3. Target users"
echo "4. Key features (high level)"
echo "5. Compliance requirements (HIPAA, SOC 2, PCI DSS, etc.)"
echo "6. Team members and roles"
```

### Step 2: Generate Feature List

Based on user input, generate comprehensive feature list:

```python
# Pseudo-code for feature generation
def generate_feature_list(project_requirements):
    features = []

    # Phase 1 features (Vision & Strategy)
    features.extend(generate_phase1_features(project_requirements))

    # Phase 2 features (Requirements & Scope)
    features.extend(generate_phase2_features(project_requirements))

    # ... continue for all 8 phases

    # Add governance features
    features.extend(generate_governance_features())

    # Add security features
    features.extend(generate_security_features())

    # Add quality features
    features.extend(generate_quality_features())

    # Add compliance features
    features.extend(generate_compliance_features(project_requirements.compliance))

    return features
```

### Step 3: Create Project Structure

```bash
# Create all directories
mkdir -p .claude/agents
mkdir -p docs/{vision,requirements,architecture,design,testing,operations}
mkdir -p src tests scripts
mkdir -p artifacts/{P1,P2,P3,P4,P5,P6,P7,P8}

# Create all files from templates
touch .claude/project-state.json
touch .claude/claude-progress.txt
touch feature_list.json
touch traceability.json
touch README.md
touch scripts/init.sh
chmod +x scripts/init.sh
```

### Step 4: Initialize Git

```bash
git init
git add .
git commit -m "feat: initialize project with Unified Enterprise Lifecycle"
```

### Step 5: Verify Setup

```bash
# Run init.sh to verify environment works
bash scripts/init.sh

# Run basic tests
if [ -f "package.json" ]; then
    npm test
fi

# Verify all files created
ls -la .claude/
ls -la docs/
ls -la scripts/
cat feature_list.json | jq '.features | length'
```

---

## INITIALIZER PROMPT

When spawning the initializer agent, use this prompt:

```
You are the Lifecycle Initializer Agent. Your job is to set up a new project for long-running development across multiple context windows.

YOUR RESPONSIBILITIES:
1. Ask the user for project requirements
2. Generate a comprehensive feature list (200-500 features)
3. Create the complete project structure
4. Initialize git repository
5. Create init.sh script for environment setup
6. Create project-state.json with initial values
7. Create claude-progress.txt for tracking

CRITICAL REQUIREMENTS:
- The feature list MUST be comprehensive. Do NOT create a minimal list.
- Every feature must have clear acceptance criteria
- Every feature must have verification steps
- All features start with status "failing"
- Features must cover all 8 phases of the lifecycle
- Include governance, security, quality, and compliance features

OUTPUT:
Return JSON with:
{
  "status": "complete",
  "project_name": "...",
  "feature_count": N,
  "directory_structure": "...",
  "next_steps": "Begin Phase 1: Vision & Strategy"
}
```

---

## INITIALIZER OUTPUT FORMAT

```json
{
  "agent": "lifecycle_initializer",
  "status": "complete",
  "project": {
    "name": "Project Name",
    "description": "Project description",
    "directory": "/path/to/project"
  },
  "artifacts_created": [
    ".claude/project-state.json",
    ".claude/claude-progress.txt",
    "feature_list.json",
    "traceability.json",
    "scripts/init.sh",
    "README.md"
  ],
  "directories_created": [
    "docs/vision",
    "docs/requirements",
    "docs/architecture",
    "docs/design",
    "docs/testing",
    "docs/operations",
    "src",
    "tests",
    "scripts",
    "artifacts/P1",
    "artifacts/P2",
    "artifacts/P3",
    "artifacts/P4",
    "artifacts/P5",
    "artifacts/P6",
    "artifacts/P7",
    "artifacts/P8"
  ],
  "feature_list": {
    "total_features": N,
    "phase_1": N1,
    "phase_2": N2,
    "phase_3": N3,
    "phase_4": N4,
    "phase_5": N5,
    "phase_6": N6,
    "phase_7": N7,
    "phase_8": N8
  },
  "git_initialized": true,
  "next_steps": [
    "Run: source scripts/init.sh",
    "Begin Phase 1: Vision & Strategy",
    "Spawn agent: phase_01_vision_strategy"
  ]
}
```

---

## POST-INITIALIZATION CHECKLIST

After the initializer completes, verify:

- [ ] Project structure created
- [ ] Feature list has 200-500 features
- [ ] All features have acceptance criteria
- [ ] All features have verification steps
- [ ] Git repository initialized
- [ ] init.sh script created and executable
- [ ] project-state.json created
- [ ] claude-progress.txt created
- [ ] README.md created with project overview
- [ ] traceability.json created

---

## COMMON INITIALIZER ISSUES

### Issue: Feature list too small

**Symptom**: Less than 100 features generated

**Solution**: Ask initializer to expand feature list with more granular features

### Issue: Missing acceptance criteria

**Symptom**: Features lack clear acceptance criteria

**Solution**: Regenerate features with explicit acceptance criteria

### Issue: init.sh doesn't work

**Symptom**: Development server won't start

**Solution**: Debug init.sh, check dependencies, verify environment

---

## SEE ALSO

- **Orchestrator**: `../ORCHESTRATOR.md` - Main coordination agent
- **Coding Agent**: `CODING.md` - Incremental development agent
- **Phase Agents**: `../skills/phase_*/SKILL.md` - Phase-specific agents

---

**This initializer implements Anthropic's long-running agent harness research.**
