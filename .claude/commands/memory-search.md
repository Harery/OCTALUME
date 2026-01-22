# /memory-search - Search Project Memory

Search across all sessions, decisions, patterns, and lessons learned.

## Usage
```
/memory-search <query>
```

## What Gets Searched
- Session summaries
- Architecture decisions
- Code patterns learned
- Issues and gotchas encountered
- Best practices documented

## Examples
```
/memory-search authentication
/memory-search database design
/memory-search error handling patterns
```

## How It Works
1. Searches all historical sessions
2. Matches against knowledge base
3. Returns relevant context with source references
4. Ranks by relevance score

## Output Format
Returns JSON with:
- `relevant_decisions` - Past architectural decisions
- `relevant_patterns` - Code patterns that worked
- `relevant_issues` - Problems solved before
- `relevant_sessions` - Sessions with matching context

## Claude Code Integration
When starting a new task, use this to pull relevant historical context:

```
Before implementing <feature>, search memory for related work:
/memory-search <feature keywords>
```

---
**Version 2.0.0 | OCTALUME Enterprise Lifecycle Framework**
