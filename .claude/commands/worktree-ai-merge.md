---
description: Resolve git merge conflicts using AI assistance
argument-name: action
argument-description: Action - check, resolve <file>, or worktree <name>
---

# AI Merge Resolver

Resolves git merge conflicts using AI assistance. Generates prompts for Claude to resolve conflicts intelligently.

## Quick Check

```bash
# Check for conflicts
./scripts/ai-merge-resolver.sh --check
```

## Resolve a Specific File

```bash
# Generate AI prompt for a file
./scripts/ai-merge-resolver.sh --resolve src/index.js
```

This will:
1. Extract the conflict markers
2. Generate an AI prompt
3. Save to `.claude/qa/.merge-prompts/`

## Apply Resolution

After getting AI's resolved code:

```bash
# Save AI output to a file
echo "resolved code here" > /tmp/resolved.txt

# Apply it
./scripts/ai-merge-resolver.sh --apply src/index.js /tmp/resolved.txt
```

## Resolve Worktree Conflicts

```bash
# Resolve all conflicts in a worktree
./scripts/ai-merge-resolver.sh --worktree feature-auth
```

## Full Workflow

1. **Start merge** (conflict occurs)
   ```bash
   git merge feature-branch
   # CONFLICT in src/auth.js
   ```

2. **Check conflicts**
   ```bash
   ./scripts/ai-merge-resolver.sh --check
   ```

3. **Generate AI prompts**
   ```bash
   ./scripts/ai-merge-resolver.sh --resolve src/auth.js
   ```

4. **Get AI resolution**
   - Open the prompt file
   - Send to Claude
   - Save resolved code

5. **Apply resolution**
   ```bash
   ./scripts/ai-merge-resolver.sh --apply src/auth.js /tmp/resolved.txt
   ```

6. **Complete merge**
   ```bash
   git merge --continue
   ```

## Tips

- AI understands context from both branches
- Always review AI's resolution before applying
- Backup is saved as `{file}.conflict-backup`
- Complex conflicts may need manual tweaking
