---
name: "lifecycle_init"
description: "Initialize a new lifecycle project"
---

# Initialize New Lifecycle Project

Please initialize a new Unified Enterprise Lifecycle project with the following requirements:

$ARGUMENTS

## Initialization Steps

1. **Gather Requirements**: Ask the user for any missing information:
   - Project name
   - Project description
   - Target users
   - Key features
   - Compliance requirements (HIPAA, SOC 2, PCI DSS, GDPR, SOX, etc.)
   - Team members and roles

2. **Create Project Structure**: Set up the complete directory structure:
   - `.claude/` directory with agent configurations
   - `docs/` directory with phase subdirectories
   - `src/` directory for source code
   - `tests/` directory for tests
   - `scripts/` directory for utility scripts
   - `artifacts/` directory with phase subdirectories

3. **Generate Feature List**: Create a comprehensive feature list:
   - Expand to 200-500 features across all 8 phases
   - Each feature must have clear acceptance criteria
   - Each feature must have verification steps
   - All features start with status "failing"
   - Include governance, security, quality, and compliance features

4. **Initialize Project State**: Create `.claude/project-state.json`:
   - Project metadata
   - Current phase (phase_01_vision_strategy)
   - Phase status (not_started)
   - Artifact counters
   - Team information
   - Compliance information

5. **Set Up Git Repository**:
   - Initialize git repository
   - Create `.gitignore` file
   - Make initial commit

6. **Create init.sh Script**: Create `scripts/init.sh`:
   - Development environment setup
   - Dependency installation
   - Database setup
   - Development server startup

7. **Create Progress Tracking**: Create `claude-progress.txt`:
   - Session history
   - Phase progress
   - Feature progress

8. **Verify Setup**: Verify everything is working:
   - Check all directories created
   - Check all files created
   - Verify feature list is comprehensive
   - Test init.sh script

## Output

Return JSON with:
```json
{
  "status": "complete",
  "project_name": "...",
  "feature_count": N,
  "next_steps": "Begin Phase 1: Vision & Strategy"
}
```

## Important

- The feature list MUST be comprehensive (200-500 features)
- Every feature must have acceptance criteria and verification steps
- All features start with status "failing"
- Features must cover all 8 phases of the lifecycle
- Include governance, security, quality, and compliance features

---

---

**Version 1.0.0 | OCTALUME Enterprise Lifecycle Framework**
