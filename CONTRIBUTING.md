# Contributing to OCTALUME

**Thank you for your interest in contributing to OCTALUME!**

---

<!-- SEO Metadata -->
**Keywords:** OCTALUME, contributing, guidelines, pull request, issue reporting, code of conduct
**Tags:** #OCTALUME #Contributing #OpenSource
**Author:** Mohamed ElHarery
**Version:** 1.0.0
**LastUpdated:** 2026

---

**Copyright (c) 2026 Mohamed ElHarery**
**Email:** mohamed@harery.com
**Website:** https://www.harery.com/
**GitHub:** https://github.com/Harery
**License:** MIT License - See LICENSE file for details

---

## How to Contribute

### Reporting Bugs

1. Check existing issues first
2. Use the bug report template
3. Include:
   - Steps to reproduce
   - Expected behavior
   - Actual behavior
   - Environment details (OS, Node.js version)
   - Screenshots if applicable

### Suggesting Features

1. Check existing feature requests
2. Use the feature request template
3. Describe the use case clearly
4. Explain why it would benefit the framework

### Submitting Pull Requests

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/your-feature`)
3. Make your changes
4. Add tests if applicable
5. Ensure all tests pass
6. Commit your changes (`git commit -m 'feat: add your feature'`)
7. Push to your fork (`git push origin feature/your-feature`)
8. Open a Pull Request

### Code Style

- Follow existing code style
- Use clear, descriptive names
- Add comments for complex logic
- Update documentation as needed
- Keep commits atomic and focused

### Commit Message Format

```
<type>: <description>

[optional body]

[optional footer]

Artifacts: P{N}-{SECTION}-{###}
Feature: F-{XXX}
Status: passing
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

## Development Setup

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/OCTALUME.git
cd OCTALUME

# Install dependencies
cd .claude/mcp-server
npm install

# Start development
npm run dev
```

## Testing

```bash
# Run tests
npm test

# Run linting
npm run lint
```

## Questions?

- Open an issue with the "question" label
- Email: mohamed@harery.com
- Website: https://www.harery.com/

---

**Thank you for contributing to OCTALUME!**
