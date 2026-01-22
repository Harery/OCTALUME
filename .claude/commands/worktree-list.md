# /worktree-list - List Active Worktrees

Display all active Git worktrees and their status.

## Usage
```
/worktree-list
```

## Output
```
🌳 Active Worktrees
====================
→ feature/user-auth
   Path: ../worktrees/user-auth
   HEAD: a1b2c3d4

→ feature/payment-api
   Path: ../worktrees/payment-api
   HEAD: e5f6g7h8

→ main (bare)
   Path: /project/root
   HEAD: i9j0k1l2
```

## Detailed Status
For detailed status of a specific worktree:
```
/worktree-status user-auth
```

Shows:
- Branch name
- Commits ahead of base
- Modified files count
- Recent commits

## Programmatic Access
```bash
./scripts/worktree-manager.sh list
```

Or directly with Git:
```bash
git worktree list
```

## Tracking File
Active worktrees are tracked in:
`.claude/worktrees/active.json`

Contains:
- Creation timestamp
- Base branch
- Current status
- Commit count

---
**Version 2.0.0 | OCTALUME Enterprise Lifecycle Framework**
