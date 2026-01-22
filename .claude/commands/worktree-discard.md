# /worktree-discard - Discard Feature Worktree

Remove a feature worktree without merging (for abandoned experiments).

## Usage
```
/worktree-discard <feature-name>
```

## ⚠️ Warning
This is a **destructive operation**:
- Deletes the worktree directory
- Deletes the feature branch
- Removes all uncommitted changes
- **Cannot be undone**

## Example
```
/worktree-discard failed-experiment
```

## When to Use
- Experiment didn't work out
- Feature requirements changed
- Starting fresh on same feature
- Cleanup after testing

## Alternative: Keep History
If you want to preserve the work but not merge:
```bash
# Create archive branch first
cd ../worktrees/feature-name
git checkout -b archive/feature-name
git push origin archive/feature-name

# Then discard
/worktree-discard feature-name
```

## Confirmation
The command will show:
```
⚠ Discarding worktree: feature-name
   This will delete the branch and all uncommitted changes!

✓ Worktree discarded
```

## Recovery
If accidentally discarded:
- Check `git reflog` for recent commits
- Look in `.claude/worktrees/active.json` history
- Contact team if pushed to remote

---
**Version 2.0.0 | OCTALUME Enterprise Lifecycle Framework**
