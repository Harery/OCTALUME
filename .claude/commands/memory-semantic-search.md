---
description: Semantic search across memory using embeddings
argument-name: query
argument-description: Search query (natural language)
---

# Semantic Memory Search

Search the project memory using semantic similarity rather than exact keyword matching.

## Running Search

```bash
node .claude/memory/semantic-search.js search "$ARGUMENTS"
```

## Understanding Results

Results are ranked by semantic similarity (0-100%):
- **90%+**: Very strong match
- **70-90%**: Good match
- **50-70%**: Related content

## Filtering Options

Search specific types:
```bash
# Only decisions
node .claude/memory/semantic-search.js search "$ARGUMENTS" --type decision

# Only patterns
node .claude/memory/semantic-search.js search "$ARGUMENTS" --type pattern

# Only lessons
node .claude/memory/semantic-search.js search "$ARGUMENTS" --type lesson
```

## When to Use

- Finding related decisions across phases
- Discovering patterns you may have forgotten
- Connecting lessons learned to current work
- Understanding context behind past choices

## Tips

1. Use natural language queries ("how did we handle authentication?")
2. Try synonyms if results are poor
3. Run `index` after adding many entries
4. Use `similar <id>` to explore related entries
