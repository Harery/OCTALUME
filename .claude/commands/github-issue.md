# /github-issue - Create GitHub Issue

Create a new GitHub issue from Claude session.

## Usage
```
/github-issue <title> [description]
```

## Parameters
| Parameter | Required | Description |
|-----------|----------|-------------|
| `title` | Yes | Issue title |
| `description` | No | Issue body/description |

## Examples

### Simple Issue
```
/github-issue "Add user authentication"
```

### Issue with Description
```
/github-issue "Fix login redirect" "Users are not being redirected after successful login. Need to check the auth callback handler."
```

### Feature Request
```
/github-issue "Feature: Dark mode support" "Add dark mode theme toggle in settings. Should persist user preference."
```

## Prerequisites
- GitHub CLI (`gh`) installed
- Authenticated: `gh auth login`

## What Happens
1. Creates issue in current repo
2. Applies default labels (configurable)
3. Saves issue number to project memory
4. Returns issue URL

## Labels
Default labels from `.claude/integrations/github.json`:
- `enhancement` - for features
- `octalume` - framework tag

Custom labels:
```
/github-issue "Bug: Login fails" "Description" "bug,high-priority"
```

## Linking to Work
After creating, use the issue number:
```bash
git commit -m "Add auth handler (fixes #42)"
```

---
**Version 2.0.0 | OCTALUME Enterprise Lifecycle Framework**
