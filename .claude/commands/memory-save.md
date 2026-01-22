# /memory-save - Save Insight to Memory

Persist important decisions, patterns, or lessons to project memory.

## Usage
```
/memory-save <category> <content>
```

## Categories
| Category | Use For |
|----------|---------|
| `decision` | Architecture/design decisions with rationale |
| `pattern` | Code patterns that worked well |
| `gotcha` | Issues encountered and solutions |
| `practice` | Best practices discovered |
| `lesson` | Lessons learned from the session |

## Examples

### Save a Decision
```
/memory-save decision {"decision": "Use JWT for auth", "rationale": "Stateless, scalable", "alternatives": ["sessions", "oauth"]}
```

### Save a Pattern
```
/memory-save pattern {"pattern": "Repository pattern for data access", "context": "Clean separation of concerns", "example": "UserRepository.findById()"}
```

### Save a Gotcha
```
/memory-save gotcha {"issue": "Race condition in token refresh", "solution": "Added mutex lock", "impact": "high"}
```

### Save a Best Practice
```
/memory-save practice {"practice": "Always validate input at API boundary", "reason": "Prevents injection attacks"}
```

## Automatic Saving
Sessions automatically save:
- Files modified
- Git branch context
- Timestamp and phase

For important insights, explicitly save with this command.

---
**Version 2.0.0 | OCTALUME Enterprise Lifecycle Framework**
