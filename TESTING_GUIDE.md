# OCTALUME Testing Guide

**Fresh Installation Testing on Linux**

---

## 📋 Testing Checklist

Use this guide to test OCTALUME on a fresh Linux installation with Claude Code.

---

## 🖥️ Test Environment

### System Requirements
- [ ] **OS**: Ubuntu 20.04+, Debian 11+, or CentOS 8+
- [ ] **RAM**: Minimum 4GB (8GB recommended)
- [ ] **Disk**: 500MB free space
- [ ] **Network**: Internet connection required

### Prerequisites Verification
```bash
# Check OS version
cat /etc/os-release

# Check available memory
free -h

# Check disk space
df -h
```

---

## 🚀 Step-by-Step Installation

### Step 1: Install Node.js and npm

```bash
# Install Node.js 18+ (Ubuntu/Debian)
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs

# Verify installation
node --version  # Should be v18.x.x or higher
npm --version   # Should be 9.x.x or higher
```

**Expected Result:**
```
✅ Node.js: v18.x.x
✅ npm: 9.x.x
```

**❌ If Failed:** Node.js version too old
```bash
# Install Node.js 18+
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs
```

---

### Step 2: Install Git

```bash
# Install git
sudo apt-get update
sudo apt-get install -y git

# Verify installation
git --version  # Should be 2.x.x or higher
```

**Expected Result:**
```
✅ git version 2.x.x
```

---

### Step 3: Install Claude Code (First Time)

```bash
# Install Claude Code globally
npm install -g @anthropic-ai/claude-code

# Verify installation
claude --version
```

**Expected Result:**
```
✅ claude version x.x.x
```

**Login to Claude:**
```bash
claude login
```

**Expected Result:**
- Browser opens
- Login to Anthropic account
- "Successfully logged in" message

---

### Step 4: Clone OCTALUME Repository

```bash
# Clone the repository
git clone https://github.com/Harery/OCTALUME.git
cd OCTALUME

# Verify structure
ls -la
```

**Expected Result:**
```
✅ README.md
✅ SETUP_GUIDE.md
✅ CLAUDE.md
✅ .claude/ (hidden directory)
✅ skills/
✅ LICENSE
```

---

### Step 5: Install MCP Server Dependencies

```bash
# Navigate to MCP server directory
cd .claude/mcp-server

# Install dependencies
npm install

# Verify installation
ls node_modules/@modelcontextprotocol/
```

**Expected Result:**
```
✅ node_modules/@modelcontextprotocol/sdk/ created
```

---

### Step 6: Verify Installation

```bash
# Return to project root
cd ../..

# Check all required files exist
ls -la .claude/
ls -la skills/
```

**Expected Result:**
```
.claude/
├── mcp-server/
│   ├── index.js
│   ├── package.json
│   └── node_modules/
├── agents/
├── commands/
├── skills/
└── ...

skills/
├── phase_01_vision_strategy/
├── phase_02_requirements_scope/
├── shared/
└── ...
```

---

## 🧪 Testing OCTALUME

### Test 1: Start Claude Code in OCTALUME Directory

```bash
# From OCTALUME root directory
claude
```

**Expected Result:**
- Claude Code starts
- CLAUDE.md is automatically loaded
- OCTALUME framework context is available

**Verification Prompt:**
```
What is OCTALUME and what are its 8 phases?
```

**Expected Response:**
Claude should explain:
- OCTALUME is an enterprise 8-phase SDLC framework
- List all 8 phases (Vision, Requirements, Architecture, Planning, Development, Quality, Deployment, Operations)

---

### Test 2: Initialize a New Project

**Prompt in Claude Code:**
```
Initialize a new OCTALUME project for a simple todo list application with:
- Add new tasks
- Mark tasks as complete
- Delete tasks
- Simple user interface

Target: Personal users
Budget: $5,000
Timeline: 2 months
```

**Expected Result:**
Claude should:
1. ✅ Create project structure
2. ✅ Generate feature list (200-500 features)
3. ✅ Initialize git repository
4. ✅ Create artifacts directory
5. ✅ Start Phase 1: Vision & Strategy

**Verification:**
```bash
# Check if project was created
ls -la
cat .claude/project-state.json
```

---

### Test 3: Create Business Case

**Prompt in Claude Code:**
```
Create the Business Case for this todo list application project.
```

**Expected Result:**
- Business case document created
- Includes executive summary, market analysis, financial projections
- Saved to artifacts/P1/

**Verification:**
```bash
cat artifacts/P1/P1-VISION-001-business-case.md
```

---

### Test 4: Create PRD

**Prompt in Claude Code:**
```
Create the Product Requirements Document (PRD) for this project.
```

**Expected Result:**
- PRD document created
- Includes user personas, user stories, requirements
- Saved to artifacts/P1/

**Verification:**
```bash
cat artifacts/P1/P1-VISION-002-prd.md
```

---

### Test 5: Check Traceability

**Prompt in Claude Code:**
```
Show me the current project status and traceability information.
```

**Expected Result:**
- Displays project phase
- Shows artifacts created with P{N}-{SECTION}-### format
- Shows feature list

---

### Test 6: Quality Gate Validation

**Prompt in Claude Code:**
```
Complete Phase 1 and run go/no-go decision to move to Phase 2.
```

**Expected Result:**
- Validates Phase 1 exit criteria
- Checks Phase 2 entry criteria
- Provides go/no-go decision
- Updates project state

---

## 🔳 Edge Case Testing

### Edge Case 1: Empty Project State

**Test:** Starting with no project state

```bash
# Remove project state if exists
rm -f .claude/project-state.json

# Test if framework still loads
claude

# Expected: Should work without project state
```

**Expected Result:** ✅ Framework loads successfully, prompts for initialization

---

### Edge Case 2: Corrupted Project State

**Test:** Handling corrupted JSON in project-state.json

```bash
# Create corrupted project state
echo '{"invalid": json}' > .claude/project-state.json

# Test if framework handles gracefully
claude

# Expected: Should detect corruption and offer recovery
```

**Expected Result:** ✅ Framework detects corruption and prompts for recovery

---

### Edge Case 3: Missing Skill Files

**Test:** Operating with missing skill files

```bash
# Temporarily move a skill file
mv skills/phase_01_vision_strategy/SKILL.md /tmp/

# Test if framework handles missing skill
claude

# Expected: Should warn about missing skill

# Restore skill file
mv /tmp/SKILL.md skills/phase_01_vision_strategy/
```

**Expected Result:** ✅ Framework warns about missing skill but continues

---

### Edge Case 4: Concurrent Claude Sessions

**Test:** Multiple Claude instances accessing same project

```bash
# Terminal 1
cd /path/to/OCTALUME
claude

# Terminal 2 (in another terminal)
cd /path/to/OCTALUME
claude

# Expected: Should handle gracefully with file locking
```

**Expected Result:** ✅ Framework handles concurrent access with appropriate warnings

---

### Edge Case 5: Large Feature List

**Test:** Framework with 500+ features

```bash
# Create test project with large feature list
claude
# Prompt: "Initialize a project with 500 features"

# Expected: Should handle large feature list efficiently
```

**Expected Result:** ✅ Framework handles large feature lists without performance degradation

---

## ⚡ Performance Testing

### Performance Test 1: Framework Loading Time

**Test:** Measure time to load CLAUDE.md

```bash
# Time framework loading
time claude --prompt "Show me the framework structure"

# Expected: Should load in < 5 seconds
```

**Expected Result:** ✅ Loads within 5 seconds on modern hardware

---

### Performance Test 2: Memory Usage

**Test:** Monitor memory consumption during operation

```bash
# Monitor memory while running Claude
/usr/bin/time -v claude --prompt "List all phases"

# Check maximum memory used
# Expected: < 2GB for typical operations
```

**Expected Result:** ✅ Memory usage stays reasonable (< 2GB)

---

### Performance Test 3: Large File Processing

**Test:** Framework behavior with large artifacts

```bash
# Create large test artifact
echo "Large content..." > artifacts/P1/test-large.txt

# Test framework can handle large files
claude --prompt "Show me all artifacts"

# Expected: Should handle large files efficiently
```

**Expected Result:** ✅ Framework processes large files without slowdown

---

### Performance Test 4: MCP Server Response Time

**Test:** Measure MCP server tool response

```bash
# Test MCP tool response time
time echo '{"method":"tools/list"}' | nc localhost 3000

# Expected: Response time < 100ms
```

**Expected Result:** ✅ MCP server responds within 100ms

---

### Performance Benchmarks

| Metric | Target | Acceptable | Failing |
|--------|--------|------------|---------|
| Framework Load Time | < 3s | < 5s | ≥ 5s |
| Memory Usage (Idle) | < 500MB | < 1GB | ≥ 1GB |
| Memory Usage (Active) | < 1GB | < 2GB | ≥ 2GB |
| MCP Response Time | < 50ms | < 100ms | ≥ 100ms |
| File I/O Operations | < 100ms | < 200ms | ≥ 200ms |

---

## 🔍 Verification Tests

### MCP Server Test

```bash
# Test MCP server runs
cd .claude/mcp-server
node index.js
```

**Expected Result:**
- Server starts without errors
- MCP tools are loaded

**Press Ctrl+C to stop**

---

### File Permissions Test

```bash
# Check file permissions
ls -la .claude/hooks/*.sh
ls -la .claude/memory/*.sh
```

**Expected Result:**
```
✅ -rwxr-xr-x (755) - Executable scripts
```

---

## 📧 Submit Feedback

If you encounter any issues or have suggestions during testing, please submit your feedback:

- **GitHub Issues:** https://github.com/Harery/OCTALUME/issues
- **Email:** mohamed@harery.com
- **Website:** https://www.harery.com/

---

**Thank you for testing OCTALUME!**

---

**Version:** 1.0.0
**Review Completed By:** OCTALUME TEAM
**Date:** 2026-01-14
**Next Review Recommended:** After major framework updates or every 6 months
