---
description: Discover potential improvements and technical debt in the codebase
---

# Find Improvements

Analyze the codebase to identify improvement opportunities, technical debt, and optimization possibilities.

## Analysis Categories

### 1. Code Quality
- Duplicated code that could be refactored
- Functions that are too long or complex
- Missing error handling
- Inconsistent patterns

### 2. Performance
- N+1 queries or inefficient data fetching
- Missing caching opportunities
- Unnecessary re-renders (React)
- Heavy computations that could be optimized

### 3. Security
- Hardcoded credentials or secrets
- Missing input validation
- Insecure dependencies
- Missing authentication/authorization checks

### 4. Maintainability
- Missing or outdated documentation
- Complex logic without tests
- Tightly coupled components
- Missing TypeScript types

### 5. Developer Experience
- Slow build times
- Missing tooling (linting, formatting)
- Complex setup process
- Unclear contribution guidelines

### 6. Technical Debt
- TODO/FIXME comments
- Deprecated API usage
- Legacy patterns that should be updated
- Missing migrations

## Output Format

Provide findings prioritized by impact:

```markdown
## Improvement Opportunities

### 🔴 High Priority (Address Soon)

#### 1. [Title]
- **Location**: `path/to/file.js:123`
- **Issue**: Description of the problem
- **Impact**: Why this matters
- **Suggestion**: How to fix
- **Effort**: Low/Medium/High

### 🟡 Medium Priority (Plan For)

#### 1. [Title]
...

### 🟢 Low Priority (Nice to Have)

#### 1. [Title]
...

### 📊 Summary

| Priority | Count | Est. Effort |
|----------|-------|-------------|
| High | X | Y days |
| Medium | X | Y days |
| Low | X | Y days |

### Recommended Order
1. Start with...
2. Then...
3. Finally...
```

## Begin Analysis

Please scan the codebase and identify improvement opportunities, focusing on high-impact items first.
