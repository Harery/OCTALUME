---
description: Run AI-powered QA review for current phase
argument-name: phase
argument-description: Phase to review (P1-P8), optional - uses current phase if not specified
---

# AI QA Review

Performs an AI-powered quality assurance review against phase-specific criteria.

## What It Reviews

1. **Required Files** - All phase deliverables exist
2. **Code Quality** - Conventions, error handling, documentation
3. **Test Coverage** - Tests exist and pass thresholds
4. **Security** - No secrets, proper validation
5. **Documentation** - README, API docs, comments

## Running Review

For current phase (from memory):
```bash
./scripts/qa-ai-review.sh
```

For specific phase:
```bash
./scripts/qa-ai-review.sh P3
./scripts/qa-ai-review.sh P5
```

## Understanding Results

The AI returns a JSON report with:

| Field | Description |
|-------|-------------|
| `verdict` | PASS, FAIL, or NEEDS_REVIEW |
| `passed` | List of passing criteria with evidence |
| `failed` | List of failures with fix suggestions |
| `warnings` | Non-blocking concerns |
| `score` | Numerical breakdown |
| `next_steps` | Recommended actions |

## Verdict Rules

- **PASS**: All criteria pass, warnings acceptable
- **FAIL**: Any critical criterion fails
- **NEEDS_REVIEW**: Edge cases requiring human judgment

## Reports

Reports are saved to:
```
.claude/qa/reports/{PHASE}_{timestamp}.json
```

## Fixing Issues

After review, address failed items:

1. Read the `suggestion` field for each failure
2. Make the fix
3. Re-run the review
4. Repeat until PASS

## Tips

- Run before committing significant changes
- Use phase-specific criteria files for custom checks
- Check warnings even on PASS verdicts
- Save reports for audit trail
