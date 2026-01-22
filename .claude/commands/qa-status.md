# /qa-status - QA Status

Show the status of the last QA run.

## Usage
```
/qa-status
```

## Example Output
```
📊 Last QA Report
=================

  Time:    2025-01-15T14:30:00Z
  Phase:   all
  Passed:  42
  Failed:  2
  Score:   95%

  Status:  ✗ FAIL
```

## Report Details
Full reports are saved in:
```
.claude/qa/reports/qa-report-<phase>-<timestamp>.json
```

## Report Format
```json
{
  "timestamp": "2025-01-15T14:30:00Z",
  "phase": "all",
  "summary": {
    "passed": 42,
    "failed": 2,
    "skipped": 5,
    "warnings": 3,
    "total": 52,
    "score": 95
  },
  "status": "fail"
}
```

## Score Calculation
```
Score = (Passed / (Passed + Failed)) × 100
```
- Skipped checks don't affect score
- Warnings don't affect score
- Only required failed checks cause overall failure

## History
View all reports:
```bash
ls -la .claude/qa/reports/
```

Reports are kept for 30 days by default (configurable in config.json).

---
**Version 2.0.0 | OCTALUME Enterprise Lifecycle Framework**
