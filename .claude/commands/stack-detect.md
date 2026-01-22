# /stack-detect - Detect Technology Stack

Automatically analyze and detect the project's technology stack.

## Usage
```
/stack-detect
```

## What It Detects

| Category | Examples |
|----------|----------|
| **Language** | TypeScript, JavaScript, Python, Go, Rust, Java |
| **Framework** | Next.js, React, Vue, Django, FastAPI, Express |
| **Package Manager** | npm, yarn, pnpm, pip, poetry, cargo |
| **Database** | PostgreSQL, MongoDB, MySQL, Redis, SQLite |
| **Testing** | Jest, Vitest, Pytest, Cypress, Playwright |
| **CI/CD** | GitHub Actions, GitLab CI, Jenkins |
| **Container** | Docker, Kubernetes, Docker Compose |
| **Tooling** | ESLint, Prettier, Biome |
| **Deployment** | Vercel, Netlify, AWS, Fly.io |

## Example Output
```
🔍 OCTALUME Stack Detector
===========================

Analyzing project structure...

━━━ Detected Stack ━━━

  Language:         typescript
  Framework:        nextjs
  Package Manager:  npm
  Database:         prisma,postgresql
  Testing:          jest,testing-library
  CI/CD:            github-actions
  Container:        docker
  Tooling:          eslint,prettier
  Deployment:       vercel

✓ Stack saved to: .claude/specs/detected-stack.json
```

## Benefits

### Context for Claude
Claude automatically loads detected stack for:
- Better code suggestions
- Framework-specific patterns
- Appropriate QA checks

### QA Recommendations
Generates recommended checks based on stack:
- React → lint, type-check, test, build
- Express → lint, test, security-audit

### Command Recommendations
Suggests common commands:
```json
{
  "install": "npm install",
  "dev": "npm run dev",
  "build": "npm run build",
  "test": "npm test"
}
```

## View Saved Stack
```
./scripts/stack-detector.sh show
```

---
**Version 2.0.0 | OCTALUME Enterprise Lifecycle Framework**
