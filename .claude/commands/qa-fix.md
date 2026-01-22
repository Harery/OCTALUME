# /qa-fix - Auto-Fix QA Issues

Automatically fix common QA issues like linting and formatting.

## Usage
```
/qa-fix
```

## What It Fixes
| Issue | Tool | Action |
|-------|------|--------|
| Lint errors | ESLint | `eslint --fix` |
| Formatting | Prettier | `prettier --write` |
| Import order | ESLint | Auto-sort imports |
| Trailing whitespace | Prettier | Remove |
| Missing semicolons | ESLint/Prettier | Add/remove per config |

## Process
1. Detects available fixers in project
2. Runs lint:fix if available
3. Runs prettier if configured
4. Reports number of fixes applied

## Example Output
```
🔧 Attempting auto-fix...

  Running lint:fix...
  Running prettier...

✓ Applied 2 auto-fixes
  Run QA again to verify: ./scripts/qa-runner.sh
```

## What It Won't Fix
- Test failures (requires code changes)
- Security vulnerabilities (requires updates)
- Missing files (requires creation)
- Type errors (requires type fixes)

## After Fixing
Always re-run QA to verify:
```
/qa-run
```

## Manual Fixes
For issues that can't be auto-fixed:
1. Check the QA report in `.claude/qa/reports/`
2. Address each failed check manually
3. Re-run QA to verify

---
**Version 2.0.0 | OCTALUME Enterprise Lifecycle Framework**
