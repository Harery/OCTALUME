---
name: "lifecycle_phase"
description: "Execute a specific phase of the lifecycle"
---

# Execute Lifecycle Phase

Execute Phase $ARGUMENTS of the Unified Enterprise Lifecycle.

## Phase Execution Steps

1. **Load Phase Skill**: Read the phase-specific SKILL.md file:
   ```
   skills/phase_{PHASE_NUMBER}_{PHASE_NAME}/SKILL.md
   ```

2. **Validate Entry Criteria**: Check that all entry criteria are met:
   - Previous phase deliverables complete
   - Required approvals obtained
   - Artifacts created and archived

3. **Read Project State**: Load current project state:
   - `.claude/project-state.json`
   - `claude-progress.txt`
   - `feature_list.json`

4. **Execute Phase Activities**: Follow the phase workflow:
   - Read phase steps from SKILL.md
   - Execute each step with appropriate owner and participants
   - Create required artifacts
   - Get required approvals

5. **Validate Exit Criteria**: Ensure all exit criteria are met:
   - All deliverables complete
   - All artifacts created
   - All approvals obtained
   - Quality gates passed

6. **Go/No-Go Decision**: Execute go/no-go decision:
   - Prepare recommendation
   - Get secondary owner review
   - Get executive sponsor approval
   - Document decision

7. **Update Project State**: Update all tracking files:
   - Update `.claude/project-state.json`
   - Update `claude-progress.txt`
   - Update `feature_list.json`
   - Archive artifacts to appropriate phase directory

8. **Commit Progress**: Commit all work to git:
   ```
   git add .
   git commit -m "feat: complete Phase {N} - {PHASE_NAME}

   - [Summary of deliverables]
   - [Artifacts created]
   - [Approvals obtained]

   Artifacts: P{N}-*
   Phase: phase_{N}_{PHASE_NAME}
   Status: complete
   "
   ```

## Output

Return JSON with:
```json
{
  "phase": "phase_{N}_{PHASE_NAME}",
  "status": "complete",
  "deliverables": ["..."],
  "artifacts": ["P{N}-*", ...],
  "next_phase": "phase_{N+1}_{NEXT_PHASE_NAME}",
  "recommendation": "go/no-go"
}
```

## Important

- Follow the phase workflow exactly as defined in the SKILL.md
- Do not skip any steps
- Get all required approvals
- Create all required artifacts
- Update all tracking files
- Leave the project in a clean state

---

**Review Completed By:** OCTALUME TEAM
**Date:** 2026-01-13
**Next Review Recommended:** After major framework updates or every 6 months
