# /changelog - Generate Changelog

Generate or update CHANGELOG.md from git commit history.

## Usage
```
/changelog [command] [options]
```

## Commands

### Preview
```
/changelog preview
```
Shows what would be added without writing.

### Generate
```
/changelog generate 1.2.0
```
Generate changelog entry for specific version.

### Release
```
/changelog release minor
```
Full release: bump version + generate changelog.

## Commit Convention
Use [Conventional Commits](https://www.conventionalcommits.org/):

| Prefix | Section |
|--------|---------|
| `feat:` | Added |
| `fix:` | Fixed |
| `docs:` | Documentation |
| `refactor:` | Changed |
| `perf:` | Changed |
| `test:` | Testing |
| `chore:` | Maintenance |
| `breaking:` | Breaking Changes |

## Example Commits
```bash
git commit -m "feat: add user authentication"
git commit -m "fix: resolve login redirect issue"
git commit -m "docs: update API documentation"
git commit -m "refactor(auth): simplify token validation"
```

## Output Example
```markdown
## [1.2.0] - 2025-01-15

### Added
- Add user authentication (`abc1234`)
- Add password reset flow (`def5678`)

### Fixed
- Resolve login redirect issue (`ghi9012`)

### Documentation
- Update API documentation (`jkl3456`)
```

## Release Workflow
```
/changelog release patch   # 1.0.0 → 1.0.1
/changelog release minor   # 1.0.0 → 1.1.0
/changelog release major   # 1.0.0 → 2.0.0
```

---
**Version 2.0.0 | OCTALUME Enterprise Lifecycle Framework**
