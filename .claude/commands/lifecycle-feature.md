---
name: "lifecycle_feature"
description: "Work on a specific feature"
---

# Work on Feature

Work on feature $ARGUMENTS following the incremental development approach.

## Feature Workflow

1. **Get Oriented**: Start each session by getting oriented:
   ```bash
   pwd
   cat .claude/project-state.json
   cat claude-progress.txt
   git log --oneline -20
   git status
   ```

2. **Select Feature**: Choose ONE feature to work on:
   ```bash
   cat feature_list.json | jq '.features[] | select(.status == "failing")'
   ```
   - Select the highest priority failing feature (P0 > P1 > P2 > P3)
   - Do NOT work on multiple features in one session

3. **Read Feature Details**: Get complete feature information:
   ```bash
   cat feature_list.json | jq ".features[] | select(.id == \"F-XXX\")"
   ```

4. **Plan Implementation**: Create an implementation plan:
   - Current state
   - Changes required
   - Files to modify
   - Acceptance criteria
   - Verification steps

5. **Implement Feature**: Write the code:
   - Follow coding standards
   - Write clear comments
   - Handle errors properly
   - Consider security implications

6. **Write Tests**: Write comprehensive tests:
   - Unit tests for individual functions
   - Integration tests for component interactions
   - E2E tests for user workflows

7. **Test Manually**: Test as a human user would:
   - Start development server: `source scripts/init.sh`
   - Navigate to the feature
   - Test all acceptance criteria
   - Verify all verification steps

8. **Update Feature Status**: Only after thorough testing:
   ```bash
   jq '.features[] |= if .id == "F-XXX" then .status = "passing" else . end' feature_list.json > feature_list.json.tmp
   mv feature_list.json.tmp feature_list.json
   ```

9. **Commit Progress**: Commit to git with descriptive message:
   ```bash
   git add .
   git commit -m "feat: [feature description] (F-XXX)

   - [what was done]
   - [tests added]
   - [verification steps completed]

   Artifacts: P5-CODE-XXX, P5-TEST-XXX
   Feature: F-XXX
   Status: passing
   "
   ```

10. **Update Progress**: Update claude-progress.txt:
    ```bash
    cat >> claude-progress.txt <<EOF

    ### Session N - F-XXX Complete
    **Feature**: [feature description]
    **Status**: ✅ PASSING
    **Tests**: Unit + Integration + E2E
    **Artifacts**: P5-CODE-XXX, P5-TEST-XXX
    EOF
    ```

## Clean State Requirements

Before finishing, ensure:
- ✅ All tests pass (`npm test`)
- ✅ No linting errors (`npm run lint`)
- ✅ No type errors (`npm run typecheck`)
- ✅ Code is well-documented
- ✅ No major bugs
- ✅ Ready to merge to main branch

## Important

- Work on ONE feature at a time
- Test as a human user would
- Never mark a feature as "passing" without testing
- Leave the codebase in a clean state
- Commit progress after each feature

---

**Review Completed By:** OCTALUME TEAM
**Date:** 2026-01-13
**Next Review Recommended:** After major framework updates or every 6 months
