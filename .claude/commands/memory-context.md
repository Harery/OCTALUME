# /memory-context - Set Working Context

Set the current working context for Claude to use during the session.

## Usage
```
/memory-context <field> <value>
```

## Fields
| Field | Description | Example |
|-------|-------------|---------|
| `phase` | Current OCTALUME phase (P1-P8) | P2 |
| `feature` | Feature being worked on | user-authentication |
| `objective` | Current session objective | Implement login flow |
| `constraints` | Technical constraints | No external auth providers |
| `dependencies` | Dependencies to consider | bcrypt, jsonwebtoken |

## Examples

### Set Phase
```
/memory-context phase P3
```

### Set Feature
```
/memory-context feature payment-integration
```

### Set Full Context
```
/memory-context objective "Refactor database layer to use connection pooling"
/memory-context constraints "Must maintain backward compatibility with existing queries"
/memory-context dependencies "pg-pool, node-postgres"
```

## Auto-Detection
When you start a session, Claude will:
1. Load previous context from memory
2. Detect current git branch → infer phase
3. Analyze recent commits → infer feature

Use this command to override or clarify context.

## View Current Context
```
node .claude/memory/memory-manager.js context
```

---
**Version 2.0.0 | OCTALUME Enterprise Lifecycle Framework**
