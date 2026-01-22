# /qa-run - Run QA Checks

Execute automated quality assurance checks for the current phase.

## Usage
```
/qa-run [phase]
```

## Parameters
| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| `phase` | No | all | Specific phase (P1-P8) or "all" |

## Examples

### Run All Phases
```
/qa-run
```

### Run Specific Phase
```
/qa-run P3
```
Runs only Development phase checks.

### Run Before Merge
```
/qa-run P4
```
Verify all tests pass before merging.

## Output
```
🔍 OCTALUME v2.0 QA Runner
=================================

━━━ Phase P3 ━━━
Development

  Lint Clean                              ✓ PASS
  Type Safety                             ✓ PASS
  Unit Tests                              ✓ PASS
  Test Coverage                           ⚠ WARN
  No Console Logs                         ✓ PASS
  No TODO in Code                         ○ SKIP

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 QA Summary
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  Passed:   4
  Failed:   0
  Warnings: 1
  Skipped:  1

  Score:    100%

✓ All required checks passed!
```

## Phase Reference
| Phase | Focus |
|-------|-------|
| P1 | Project Initialization |
| P2 | Requirements & Planning |
| P3 | Development |
| P4 | Testing |
| P5 | Security & Compliance |
| P6 | Documentation |
| P7 | Deployment |
| P8 | Maintenance & Monitoring |

## Auto-Fix
If checks fail, try:
```
/qa-fix
```

---
**Version 2.0.0 | OCTALUME Enterprise Lifecycle Framework**
