# /memory-stats - View Memory Statistics

Display memory system statistics and usage information.

## Usage
```
/memory-stats
```

## Output Includes
- Total sessions recorded
- Knowledge base counts by category
- Most recent session info
- Memory file size
- Storage health

## Example Output
```
📊 OCTALUME Memory Statistics
============================
Sessions: 47 recorded
Last Session: 2025-01-15T10:30:00Z (2 hours ago)

Knowledge Base:
  📐 Architecture Decisions: 12
  🔄 Code Patterns: 23
  ⚠️  Gotchas: 8
  ✅ Best Practices: 15
  📚 Lessons Learned: 19

Feature History: 5 features tracked
Storage: 124 KB (healthy)

Recent Activity:
  - P3: user-authentication (completed)
  - P3: payment-integration (in-progress)
```

## Programmatic Access
```bash
node .claude/memory/memory-manager.js stats
```

## Export Memory
To export memory for backup or migration:
```bash
node .claude/memory/memory-manager.js export > backup.json
```

---
**Version 2.0.0 | OCTALUME Enterprise Lifecycle Framework**
