# /worktree-init - Create Feature Worktree

Create an isolated Git worktree for parallel feature development.

## Usage
```
/worktree-init <feature-name> [base-branch]
```

## Parameters
| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| `feature-name` | Yes | - | Name for the feature (will be sanitized) |
| `base-branch` | No | main | Branch to base the worktree on |

## Examples

### Basic Feature
```
/worktree-init user-authentication
```
Creates:
- Branch: `feature/user-authentication`
- Path: `../worktrees/user-authentication`

### Feature from Develop Branch
```
/worktree-init payment-api develop
```

### Multi-word Feature
```
/worktree-init "Shopping Cart Refactor"
```
Creates: `feature/shopping-cart-refactor`

## What Happens
1. Creates new branch from base
2. Creates worktree directory
3. Registers in active.json tracking
4. Ready for isolated development

## Benefits
- Work on multiple features simultaneously
- No stashing required
- Clean separation of concerns
- Easy to discard failed experiments

## After Creation
```bash
cd ../worktrees/user-authentication
# Work on feature in isolation
```

Or continue using Claude - it will detect the active worktrees.

---
**Version 2.0.0 | OCTALUME Enterprise Lifecycle Framework**
