---
name: "phase_05_development_execution"
description: "Execute development in sprints with continuous quality. Sprint planning, code development, code reviews, security in development (shift left), unit testing, integration, and documentation."
phase: 5
phase_name: "Development Execution"
owner: "Technical Lead"
secondary_owner: "Project Manager (coordination)"
participants: ["Developers", "QA", "Product Owner", "Security Lead", "Tech Lead", "Scrum Master"]
entry_criteria: [
  "Work breakdown structure completed",
  "Resource plan approved",
  "Risk register created",
  "Quality and test plan approved",
  "Security and compliance plan approved",
  "CI/CD pipeline implemented",
  "Sprint 0 completed",
  "Development environment ready"
]
exit_criteria: [
  "All planned features implemented",
  "Unit tests passing (70-80% coverage)",
  "Code reviews completed for all changes",
  "Security reviews completed",
  "Integration tests passing",
  "Documentation updated",
  "Build artifacts ready",
  "Go/no-go decision to proceed to Phase 6"
]
estimated_duration: "8-16 weeks (multiple sprints)"
dependencies: ["phase_04_development_planning"]
outputs: [
  "Source code (version controlled)",
  "Unit tests (passing)",
  "Code review records",
  "Security review findings",
  "Integration test results",
  "Technical documentation",
  "Sprint deliverables"
]
next_phase: "phase_06_quality_security"
---

# PHASE 5: DEVELOPMENT EXECUTION

## Overview

**Objective**: Build the software with continuous quality

**Entry Point**: Approved Plan from Phase 4
**Exit Point**: Complete Build

---

## Key Roles in This Phase

| Role | Responsibility |
|------|----------------|
| **Technical Lead** | Owns development execution |
| **Developers** | Implement features and tests |
| **Scrum Master** | Facilitates sprint ceremonies |
| **Security Lead** | Security in development (shift left) |
| **QA Lead** | Quality validation throughout |

---

## Step 1: Sprint Planning and Execution

**Owner**: Tech Lead / Scrum Master
**Participants**: Developers, QA, Product Owner
**Timeline**: Per sprint (typically 2 weeks)

### Tasks (Per Sprint)
- Sprint planning (select stories for sprint)
- Daily stand-ups (progress and blockers)
- Development execution (coding)
- Code reviews
- Unit testing
- Integration with other teams
- Sprint demo (show completed work)
- Sprint retrospective (improvement)

### Deliverables (Per Sprint)
- Sprint backlog
- Working software features
- Unit tests
- Code review records
- Sprint demo recording
- Sprint retrospective action items

### Approvals
- Tech Lead: Approve sprint completion
- Product Owner: Accept stories
- QA Lead: Validate quality gates

---

## Step 2: Code Development

**Owner**: Developers (each owns their tasks)
**Participants**: Tech Lead (review), Peers (collaboration)
**Timeline**: Continuous throughout development

### Tasks
- Implement features per specifications
- Follow coding standards
- Write unit tests (TDD encouraged)
- Document code
- Conduct self-review
- Submit for code review

### Deliverables
- Source code (version controlled: Git, GitHub, GitLab)
- Unit tests (passing)
- Code documentation
- Technical comments in code

### Approvals
- Developer: Self-review complete
- Tech Lead/Peers: Code review approval
- QA Lead: Test coverage validation

---

## Step 3: Code Review Process

**Owner**: Tech Lead / Senior Developers
**Participants**: All developers
**Timeline**: Continuous, within 24-48 hours of submission

### Tasks
- Review code for correctness
- Review code for security vulnerabilities
- Review code for performance issues
- Review code for maintainability
- Review code for standards compliance
- Provide constructive feedback
- Ensure test coverage
- Approve or request changes

### Deliverables
- Code review comments
- Code review approval records
- Code quality metrics
- Security review findings

### Approvals
- Reviewer: Approve code changes
- Tech Lead: Final approval for merge
- Security Lead: Review for security (if applicable)

### Code Review Checklist
- ☐ Code follows coding standards
- ☐ Logic is correct and efficient
- ☐ No security vulnerabilities
- ☐ No performance issues
- ☐ Proper error handling
- ☐ Adequate test coverage
- ☐ Documentation updated
- ☐ No hardcoded secrets/credentials

---

## Step 4: Security in Development (Shift Left)

**Owner**: Security Lead / Security Architect
**Participants**: Developers, Tech Lead
**Timeline**: Continuous throughout development

### Tasks
- Conduct security code reviews
- Use Static Application Security Testing (SAST)
- Use Software Composition Analysis (SCA) for dependencies
- Conduct threat modeling sessions
- Provide secure coding guidance
- Review secrets management
- Validate security controls implementation

### Deliverables
- Security code review reports
- SAST scan results
- SCA scan results (dependency vulnerabilities)
- Threat model updates
- Secure coding guidelines
- Security exception requests (if needed)

### Approvals
- Security Lead: Validate security in code
- Tech Lead: Validate feasibility

**Reference**: `../shared/security/SKILL.md`

---

## Step 5: Unit Testing

**Owner**: Developers / QA Lead
**Participants**: Tech Lead
**Timeline**: Continuous, with each code change

### Tasks
- Write unit tests for all code (TDD encouraged)
- Achieve test coverage targets (70-80%)
- Test both positive and negative cases
- Test edge cases and boundary conditions
- Mock external dependencies
- Maintain test suite quality

### Deliverables
- Unit test suite (passing)
- Test coverage reports
- Test data fixtures
- Mock implementations

### Approvals
- Developers: Tests passing locally
- CI/CD: Tests passing in pipeline
- QA Lead: Validate test coverage

---

## Step 6: Integration and Continuous Integration

**Owner**: Tech Lead / DevOps
**Participants**: All developers
**Timeline**: Continuous

### Tasks
- Integrate code changes regularly
- Run CI/CD pipeline for each change
- Merge to main branch (trunk-based development or feature branches)
- Resolve merge conflicts
- Maintain build stability
- Handle integration issues

### Deliverables
- CI/CD pipeline runs (successful)
- Integration test results
- Build artifacts (Docker images, deployable packages)
- Merge records

### Approvals
- CI/CD: Pipeline passing
- Tech Lead: Merge approval

---

## Step 7: Documentation

**Owner**: Tech Lead / Developers
**Participants**: Product Owner, QA
**Timeline**: Continuous, with each feature

### Tasks
- Update technical documentation
- Update API documentation (OpenAPI/Swagger)
- Update user documentation
- Update runbooks and operational procedures
- Maintain architecture decision records (ADRs)
- Document known issues and workarounds

### Deliverables
- Technical documentation (updated)
- API documentation (updated)
- User documentation (updated)
- Runbooks and procedures
- Known issues document

### Approvals
- Tech Lead: Validate technical documentation
- Product Owner: Validate user documentation

---

## Quality Gates (Exit Criteria)

Before proceeding to Phase 6, ensure:

- ☐ All planned features implemented
- ☐ Unit tests passing (70-80% coverage)
- ☐ Code reviews completed for all changes
- ☐ Security reviews completed
- ☐ Integration tests passing
- ☐ Documentation updated
- ☐ Build artifacts ready
- ☐ Go/no-go decision to proceed to Phase 6

---

## Development Metrics

Track these metrics throughout Phase 5:

| Metric | Target | Current |
|--------|--------|---------|
| Sprint Velocity | Story points/sprint | TBD |
| Code Coverage | 70-80% | TBD |
| Code Review turnaround | <24 hours | TBD |
| Build Success Rate | >95% | TBD |
| Defect Escape Rate | <5% | TBD |
| Security Vulnerabilities | Zero critical | TBD |

---

## Coding Standards

Follow these standards (defined in Phase 3):

- Language-specific style guides (PEP 8 for Python, Google Style for Java, etc.)
- Naming conventions
- Comment and documentation standards
- Error handling patterns
- Security coding practices

---

## Git Workflow

Recommended workflow:

1. **Feature Branch**: Create branch from main
2. **Develop**: Implement feature + tests
3. **Pull Request**: Open PR with description
4. **Code Review**: Get reviews and address feedback
5. **CI/CD**: Pipeline must pass
6. **Merge**: Merge to main branch
7. **Delete**: Delete feature branch

---

## Templates and Examples

See `./templates/` for:
- Pull Request Template
- Code Review Checklist
- Unit Test Template
- Documentation Template

See `./examples/` for:
- Sample Sprint Plan
- Sample Code Review

---

**Previous Phase**: `../phase_04_development_planning/SKILL.md`
**Next Phase**: `../phase_06_quality_security/SKILL.md`

---

**Review Completed By:** OCTALUME TEAM
**Date:** 2026-01-13
**Next Review Recommended:** After major framework updates or every 12 months
