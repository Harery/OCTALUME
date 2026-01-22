# Testing OCTALUME on a Fresh Linux System

**Welcome, future tester!** You're about to take OCTALUME for a spin on a clean Linux installation. I know testing can feel intimidating—especially with a new framework—but don't worry. We've designed this guide to be your patient companion through every step.

---

## What You'll Need

Let's make sure your system is ready before we begin. Think of this as checking your toolkit before starting a project—you want everything in place before you dive in.

### System Checklist

- [ ] **Operating System**: Ubuntu 20.04+, Debian 11+, or CentOS 8+
- [ ] **RAM**: At least 4GB (8GB will make your life nicer)
- [ ] **Disk Space**: 500MB free
- [ ] **Internet**: Required for downloads and Claude Code login

---

## Let's Verify Your System

Before we install anything, let's check what you're working with. These commands will tell us about your environment.

```bash
# Check your OS version
cat /etc/os-release

# Check available memory
free -h

# Check disk space
df -h
```

**What you should see:**
- OS version matching the requirements above
- Memory showing at least 4GB total
- Disk space showing at least 500MB available

<details>
<summary> Something doesn't match?</summary>

**Problem:** Your OS version is older than required.

**Solution:** Consider upgrading to a supported version, or proceed with caution—you may encounter dependency issues.

**Problem:** Low on memory or disk space.

**Solution:** Close unnecessary programs to free RAM. For disk space, clear temporary files with `sudo apt clean` (Ubuntu/Debian) or `sudo yum clean all` (CentOS).

</details>

---

## Step 1: Installing Node.js and npm

Node.js is the foundation that Claude Code runs on. Let's get it installed.

```bash
# Install Node.js 18+ (Ubuntu/Debian)
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs

# Verify the installation
node --version
npm --version
```

**What you should see:**
```
v18.x.x  # (or higher - this is good!)
9.x.x    # (or higher - this is good!)
```

<details>
<summary> Error: "node: command not found"</summary>

This means Node.js didn't install properly. Let's fix it:

```bash
# Try installing build essentials first
sudo apt-get update
sudo apt-get install -y build-essential

# Then reinstall Node.js
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs
```

</details>

<details>
<summary> Warning: Version too old</summary>

If you see a version lower than 18, you'll need to update:

```bash
# Remove old version
sudo apt-get remove -y nodejs npm

# Install fresh Node.js 18+
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs
```

</details>

---

## Step 2: Installing Git

Git helps us clone the OCTALUME repository. Let's make sure it's available.

```bash
# Install git
sudo apt-get update
sudo apt-get install -y git

# Verify the installation
git --version
```

**What you should see:**
```
git version 2.x.x  # (any 2.x version is fine)
```

<details>
<summary> Error: "git: command not found"</summary>

If git isn't found, the install command above should fix it. If you still have issues, try:

```bash
# For Ubuntu/Debian
sudo apt-get install -y git-core

# For CentOS
sudo yum install -y git
```

</details>

---

## Step 3: Installing Claude Code

This is the exciting part—installing the AI assistant that will help you build amazing things!

```bash
# Install Claude Code globally
npm install -g @anthropic-ai/claude-code

# Verify the installation
claude --version
```

**What you should see:**
```
claude version x.x.x  # (any version number means success!)
```

**Celebrate!** You've just installed Claude Code. Now let's log in so you can start using it.

```bash
claude login
```

**What will happen:**
1. Your default browser will open automatically
2. You'll be prompted to log in to your Anthropic account
3. After successful login, you'll see a confirmation message
4. Return to your terminal—you're ready to go!

<details>
<summary> Error: Browser doesn't open</summary>

If your browser doesn't open automatically (common on headless servers), you'll see a URL in the terminal. Copy it and paste it manually into your browser.

</details>

<details>
<summary> Error: "Cannot find module '@anthropic-ai/claude-code'"</summary>

This usually means npm's global path isn't set up. Try:

```bash
# Add npm global path to your .bashrc
echo 'export PATH="$PATH:$(npm config get prefix)/bin"' >> ~/.bashrc
source ~/.bashrc

# Then try claude --version again
claude --version
```

</details>

---

## Step 4: Cloning OCTALUME

Now let's get the OCTALUME framework onto your system.

```bash
# Clone the repository
git clone https://github.com/Harery/OCTALUME.git
cd OCTALUME

# Look at what we got
ls -la
```

**What you should see:**
```
 README.md              # Framework overview
 SETUP_GUIDE.md         # How to use it
 CLAUDE.md              # Auto-loaded context
 .claude/               # Configuration (hidden directory)
 skills/                # Phase and shared skills
 LICENSE                # License information
```

**Welcome home!** You're now standing in the OCTALUME directory. This is where the magic happens.

---

## Step 5: Installing MCP Server Dependencies

OCTALUME includes a custom MCP server that provides powerful lifecycle management tools. Let's set it up.

```bash
# Navigate to the MCP server directory
cd .claude/mcp-server

# Install dependencies
npm install

# Check that everything installed
ls node_modules/@modelcontextprotocol/
```

**What you should see:**
```
 node_modules/@modelcontextprotocol/sdk/  # Success!
```

<details>
<summary> Error: "EACCES: permission denied"</summary>

This is a common permission issue. Let's fix it:

```bash
# Fix npm permissions
mkdir -p ~/.npm-global
npm config set prefix '~/.npm-global'
echo 'export PATH=~/.npm-global/bin:$PATH' >> ~/.bashrc
source ~/.bashrc

# Try npm install again
npm install
```

</details>

---

## Step 6: Verifying Your Installation

Let's make sure everything is in place before we start testing.

```bash
# Return to project root
cd ../..

# Check all required directories
ls -la .claude/
ls -la skills/
```

**What you should see:**

For `.claude/`:
```
 mcp-server/      # MCP server with dependencies
 agents/          # Agent configurations
 commands/        # Claude Code commands
 skills/          # Additional skill files
 hooks/           # Event hook scripts
```

For `skills/`:
```
 phase_01_vision_strategy/
 phase_02_requirements_scope/
 phase_03_architecture_design/
 phase_04_development_planning/
 phase_05_development_execution/
 phase_06_quality_security/
 phase_07_deployment_release/
 phase_08_operations_maintenance/
 shared/          # Cross-cutting skills
```

**You're ready to test!** Everything should be in place now.

---

## Testing OCTALUME

Now for the moment of truth—let's see if OCTALUME works as expected.

### Test 1: Starting Claude Code

```bash
# From the OCTALUME root directory
claude
```

**What should happen:**
- Claude Code starts and displays a welcome message
- CLAUDE.md is automatically loaded (this gives Claude context about OCTALUME)
- You see the OCTALUME framework context available

**Let's verify it's working:**

Ask Claude:
```
What is OCTALUME and what are its 8 phases?
```

**Expected response:**
Claude should explain that OCTALUME is an enterprise 8-phase software development lifecycle framework and list all 8 phases:
1. Vision & Strategy
2. Requirements & Scope
3. Architecture & Design
4. Development Planning
5. Development Execution
6. Quality & Security
7. Deployment & Release
8. Operations & Maintenance

<details>
<summary> Claude doesn't know about OCTALUME</summary>

If Claude doesn't respond with OCTALUME information, CLAUDE.md might not be loading. Check:

```bash
# Verify CLAUDE.md exists
ls -la CLAUDE.md

# If it exists, try restarting Claude
exit  # Exit Claude
claude # Start it again
```

</details>

---

### Test 2: Creating Your First Project

Let's initialize a simple project to see the framework in action.

**Ask Claude:**
```
Initialize a new OCTALUME project for a simple todo list application with:
- Add new tasks
- Mark tasks as complete
- Delete tasks
- Simple user interface

Target: Personal users
Budget: Project resources
Timeline: 2 months
```

**What should happen:**
1.  Claude creates the project directory structure
2.  Claude generates a feature list (200-500 features for a full project)
3.  Claude initializes a git repository
4.  Claude creates an artifacts directory for documentation
5.  Claude starts Phase 1: Vision & Strategy

**Let's verify:**

```bash
# Check if project was created
ls -la

# Check the project state
cat .claude/project-state.json

# Check for artifacts directory
ls -la artifacts/
```

**What you should see:**
```
 .claude/project-state.json  # Project tracking
 artifacts/P1/               # Phase 1 artifacts directory
 feature_list.json           # Generated feature list
 .git/                       # Git repository initialized
```

<details>
<summary> Error: "Project state not found"</summary>

If the project didn't initialize properly, try again with a clearer prompt:

```
Initialize a new OCTALUME project for a todo app.
```

If that fails, check that you're in the OCTALUME directory and that CLAUDE.md exists.

</details>

---

### Test 3: Creating a Business Case

Let's create your first artifact!

**Ask Claude:**
```
Create the Business Case for this todo list application project.
```

**What should happen:**
- Claude creates a comprehensive business case document
- Includes executive summary, market analysis, and financial projections
- Saves it to the artifacts directory with proper naming

**Let's verify:**

```bash
# Check if the file was created
ls -la artifacts/P1/

# View the business case
cat artifacts/P1/P1-VISION-001-business-case.md
```

**What you should see:**
```
 P1-VISION-001-business-case.md
```

The file should contain:
- Executive summary
- Problem statement
- Market analysis
- Financial projections (ROI, costs)
- Recommendation

<details>
<summary> Artifact not created</summary>

If the artifact wasn't created, check the artifacts directory:

```bash
# Check if directory exists
ls -la artifacts/

# If P1 doesn't exist, create it
mkdir -p artifacts/P1

# Try creating the business case again
```

</details>

---

### Test 4: Creating a PRD (Product Requirements Document)

**Ask Claude:**
```
Create the Product Requirements Document (PRD) for this project.
```

**What should happen:**
- Claude creates a detailed PRD
- Includes user personas, user stories, and requirements
- Saves with proper traceability naming

**Verify:**

```bash
cat artifacts/P1/P1-VISION-002-prd.md
```

**What you should see:**
```
 P1-VISION-002-prd.md
```

The file should contain:
- Product overview
- User personas
- User stories
- Functional requirements
- Non-functional requirements

---

### Test 5: Checking Traceability

One of OCTALUME's superpowers is complete traceability. Let's see it in action.

**Ask Claude:**
```
Show me the current project status and traceability information.
```

**What you should see:**
- Current phase (Phase 1: Vision & Strategy)
- List of artifacts created with their P{N}-{SECTION}-### identifiers
- Feature list with traceability information
- Project progress summary

**Why this matters:**
Every artifact, decision, and deliverable is tracked. You can always trace back to see why something was built a certain way.

---

### Test 6: Quality Gate Validation

OCTALUME has quality gates at every phase transition. Let's test one.

**Ask Claude:**
```
Complete Phase 1 and run go/no-go decision to move to Phase 2.
```

**What should happen:**
1. Claude validates Phase 1 exit criteria
2. Claude checks Phase 2 entry criteria
3. Claude provides a go/no-go recommendation
4. Claude updates the project state if approved

**What you should see:**
- Validation of Phase 1 deliverables
- Assessment of Phase 2 readiness
- Clear recommendation (Go or No-Go)
- Explanation of the decision

<details>
<summary> No-Go decision: What now?</summary>

A No-Go decision isn't failure—it's quality control! Claude will tell you exactly what's missing. For example:
- "Business case incomplete—missing financial projections"
- "PRD lacks user stories for admin features"

Address the missing items and run the quality gate again.

</details>

---

## Edge Case Testing

Great frameworks handle edge cases gracefully. Let's test a few.

### Edge Case 1: Empty Project State

**Scenario:** Starting OCTALUME with no existing project.

```bash
# Remove project state if it exists
rm -f .claude/project-state.json

# Start Claude
claude
```

**Expected behavior:**
- Claude detects no project exists
- Claude prompts you to initialize a new project
- Framework continues to work normally

**Why this matters:** Users should be able to start fresh at any time.

---

### Edge Case 2: Corrupted Project State

**Scenario:** Project state file gets corrupted.

```bash
# Create a corrupted project state (don't worry, we'll fix it)
echo '{"invalid": json}' > .claude/project-state.json

# Start Claude
claude
```

**Expected behavior:**
- Claude detects the corruption
- Claude offers to recover or reinitialize
- Framework provides clear guidance

**Recovery:**
```bash
# Remove the corrupted file
rm .claude/project-state.json

# Start fresh
claude
```

**Why this matters:** Files get corrupted. The framework should handle it gracefully.

---

### Edge Case 3: Missing Skill Files

**Scenario:** A skill file is accidentally deleted.

```bash
# Temporarily move a skill file
mv skills/phase_01_vision_strategy/SKILL.md /tmp/

# Start Claude
claude
```

**Expected behavior:**
- Claude detects the missing skill
- Claude provides a clear warning message
- Framework continues to function (other phases still work)

**Recovery:**
```bash
# Restore the skill file
mv /tmp/SKILL.md skills/phase_01_vision_strategy/
```

**Why this matters:** Accidents happen. The framework should be resilient.

---

### Edge Case 4: Large Feature Lists

**Scenario:** Projects with hundreds of features.

OCTALUME is designed to handle projects with 200-500 features. Let's verify performance remains good.

**Ask Claude:**
```
Show me how many features are in this project and display the first 10.
```

**Expected behavior:**
- Claude displays the feature count
- Claude shows the first 10 features
- Performance remains snappy

**Why this matters:** Enterprise projects have lots of features. The framework shouldn't slow down.

---

### Edge Case 5: Concurrent Sessions

**Scenario:** Multiple Claude sessions accessing the same project.

```bash
# Terminal 1
cd /path/to/OCTALUME
claude

# Terminal 2 (open a new terminal window)
cd /path/to/OCTALUME
claude
```

**Expected behavior:**
- Both sessions start
- Framework provides warning about concurrent access
- File locking prevents corruption

**Why this matters:** Teams might accidentally work on the same project. The framework should handle it.

---

## Performance Testing

Let's make sure OCTALUME runs smoothly on your system.

### Performance Test 1: Framework Loading Time

**Test:** How fast does the framework load?

```bash
# Time the framework loading
time claude --prompt "Show me the framework structure"
```

**Expected results:**
-  < 3 seconds: Excellent
-  < 5 seconds: Good
-  ≥ 5 seconds: Acceptable but consider system resources

<details>
<summary> Slow loading? Here's why</summary>

Slow loading can be caused by:
- Low RAM (close other programs)
- Slow disk (consider SSD)
- Large project files (consider archiving old artifacts)

</details>

---

### Performance Test 2: Memory Usage

**Test:** How much memory does OCTALUME use?

```bash
# Monitor memory while running Claude
/usr/bin/time -v claude --prompt "List all phases"

# Look for "Maximum resident set size" in the output
```

**Expected results:**
-  < 1GB: Excellent
-  < 2GB: Good
-  ≥ 2GB: Monitor during extended use

---

### Performance Benchmarks

Here's what we aim for:

| Metric | Excellent | Good | Acceptable |
|--------|-----------|------|------------|
| Framework Load Time | < 3s | < 5s | < 10s |
| Memory Usage (Idle) | < 500MB | < 1GB | < 2GB |
| Memory Usage (Active) | < 1GB | < 2GB | < 4GB |
| MCP Response Time | < 50ms | < 100ms | < 200ms |

---

## Verification Tests

Let's verify specific components are working correctly.

### MCP Server Test

```bash
# Navigate to MCP server directory
cd .claude/mcp-server

# Start the server
node index.js
```

**What you should see:**
```
 MCP Server listening on port 3000
 Loaded 9 lifecycle tools
```

**Press Ctrl+C to stop the server**

<details>
<summary> Error: "Cannot find module 'express'"</summary>

Dependencies might not be installed. Run:

```bash
npm install
```

Then try starting the server again.

</details>

---

### File Permissions Test

Hook scripts need to be executable. Let's verify.

```bash
# Check hook script permissions
ls -la .claude/hooks/*.sh
ls -la .claude/memory/*.sh
```

**What you should see:**
```
 -rwxr-xr-x  # Executable script (755 permission)
```

<details>
<summary> Wrong permissions?</summary>

If scripts show `-rw-r--r--` (not executable), fix them:

```bash
# Make hook scripts executable
chmod +x .claude/hooks/*.sh
chmod +x .claude/memory/*.sh

# Verify the fix
ls -la .claude/hooks/*.sh
```

</details>

---

## Congratulations, Tester! 

You've completed the OCTALUME testing guide! Here's what you accomplished:

 Verified your system meets requirements
 Installed Node.js, npm, git, and Claude Code
 Cloned and configured OCTALUME
 Tested framework initialization
 Created artifacts (business case, PRD)
 Verified traceability system
 Tested quality gates
 Validated edge case handling
 Checked performance benchmarks

---

## What If Something Didn't Work?

Don't worry—testing is about finding issues, not perfection. Here's how to get help.

### Common Issues

**Problem:** Installation failed
- Check system requirements
- Verify internet connection
- Try with sudo (if permission denied)

**Problem:** Claude doesn't know about OCTALUME
- Verify CLAUDE.md exists
- Check you're in the OCTALUME directory
- Restart Claude Code

**Problem:** Performance is slow
- Close other programs
- Check available RAM and disk space
- Consider system capabilities

---

## Share Your Feedback

We'd love to hear about your testing experience—both successes and issues help us improve.

**Ways to reach us:**
- **GitHub Issues:** https://github.com/Harery/OCTALUME/issues
- **Email:** octalume@harery.com
- **Website:** https://harery.com/

**When reporting issues, please include:**
- Your OS and version
- Node.js and npm versions
- Steps to reproduce the problem
- Expected vs. actual behavior
- Any error messages

---

## Final Thoughts

Testing enterprise software frameworks isn't just about checking boxes—it's about building confidence that OCTALUME will handle real-world projects gracefully. You've just verified that OCTALUME can handle everything from fresh installations to edge cases.

**You're now ready to use OCTALUME on real projects!**

The framework is designed to grow with you—from simple todo apps to complex enterprise systems. Every test you've run validates that OCTALUME will be there when you need it.

Thank you for being a thorough tester. Your diligence makes OCTALUME better for everyone!

---


**OCTALUME Enterprise Lifecycle Framework

---

**Version 1.0.0 | OCTALUME Enterprise Lifecycle Framework**
