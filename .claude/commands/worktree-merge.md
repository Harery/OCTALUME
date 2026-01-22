# /worktree-merge - Merge Feature Back

Merge completed feature worktree back to its base branch.

## Usage
```
/worktree-merge <feature-name> [--delete]
```

## Parameters
| Parameter | Required | Description |
|-----------|----------|-------------|
| `feature-name` | Yes | Name of the feature worktree |
| `--delete` | No | Remove worktree after successful merge |

## Examples

### Merge and Keep
```
/worktree-merge user-authentication
```
Merges but keeps worktree for further work.

### Merge and Cleanup
```
/worktree-merge user-authentication --delete
```
Merges and removes worktree + branch.

## Merge Process
1. Switches to base branch (usually `main`)
2. Performs `git merge --no-ff` to preserve history
3. Records merge in history tracking
4. Optionally removes worktree and branch

## Conflict Handling
If conflicts occur:
```
⚠ Merge failed - resolve conflicts manually
```

Then resolve in main worktree:
```bash
git status          # See conflicts
# Edit files to resolve
git add .
git commit
```

## Pre-Merge Checklist
Before merging, ensure:
- [ ] All tests pass in worktree
- [ ] Code reviewed (if required)
- [ ] Commits are clean and atomic
- [ ] No WIP commits

Use `/qa-run` in the worktree first!

---
**Version 2.0.0 | OCTALUME Enterprise Lifecycle Framework**
