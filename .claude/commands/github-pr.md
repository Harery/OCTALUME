# /github-pr - Create Pull Request

Create a pull request from current branch.

## Usage
```
/github-pr [title] [description] [base-branch]
```

## Parameters
| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| `title` | No | From branch | PR title (auto-generated if omitted) |
| `description` | No | From commits | PR body |
| `base-branch` | No | main | Target branch for merge |

## Examples

### Auto-Generated PR
```
/github-pr
```
Creates PR with:
- Title from branch name
- Description from commit history

### Custom Title
```
/github-pr "Feature: User Authentication"
```

### Full Custom
```
/github-pr "Add Login Flow" "Implements OAuth2 login with JWT tokens" "develop"
```

### Draft PR
```
/github-pr --draft "WIP: New Feature"
```

## Auto-Generated Body
When no description provided:
```markdown
## Summary

<!-- Brief description of changes -->

## Changes

- abc1234 Add login component
- def5678 Implement token refresh
- ghi9012 Add tests

## Checklist

- [ ] Tests pass locally
- [ ] Documentation updated
- [ ] QA checks pass (`/qa-run`)
```

## Prerequisites
- GitHub CLI (`gh`) installed
- Authenticated: `gh auth login`
- On a feature branch (not main)
- Commits pushed to remote

## Workflow
1. Complete feature work
2. Run `/qa-run` to verify quality
3. Push changes: `git push -u origin <branch>`
4. Create PR: `/github-pr`

---
**Version 2.0.0 | OCTALUME Enterprise Lifecycle Framework**
