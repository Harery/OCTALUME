---
name: "quality"
description: "Shared quality framework across all phases. Quality principles, testing strategy, quality gates, defect management, and continuous improvement."
type: "shared"
used_by: ["all_phases"]
---

# QUALITY FRAMEWORK - SHARED ACROSS ALL PHASES

This shared skill provides quality guidance that applies across all phases of the Unified Enterprise Lifecycle.

**Quality First**: Quality is built in, not inspected in.

---

## QUALITY PRINCIPLES

### Quality Gates
- Each phase has entry and exit criteria
- No phase proceeds without meeting quality gates
- Go/no-go decisions at each phase transition

### Shift Left
- Quality activities start as early as Phase 2 (requirements)
- Testing integrated throughout development (Phase 5)
- Security and performance considered from Phase 1

### Continuous Quality
- Quality is continuous, not a final step
- Automated testing in CI/CD pipeline
- Continuous monitoring in production

### Test-Driven Development (TDD)
- Write tests before code (encouraged)
- Unit tests as part of development
- Test coverage targets (70-80%)

---

## QUALITY BY PHASE

### Phase 1: Vision & Strategy
**Quality Activities**:
- Define quality metrics and KPIs
- Identify quality requirements
- Define success criteria

**Deliverables**:
- Quality metrics and KPIs
- Success criteria

**Owner**: Product Owner, QA Lead

---

### Phase 2: Requirements & Scope
**Quality Activities**:
- Define testable requirements
- Define acceptance criteria
- Define non-functional requirements (performance, security)
- Create requirements traceability matrix (RTM)

**Deliverables**:
- Testable requirements
- Acceptance criteria
- Non-functional requirements
- Requirements traceability matrix

**Owner**: QA Lead, Product Owner

---

### Phase 3: Architecture & Design
**Quality Activities**:
- Design for testability
- Design for performance
- Design for reliability
- Define quality attributes

**Deliverables**:
- Testability design
- Quality attributes
- Performance targets

**Owner**: CTA, QA Lead

---

### Phase 4: Development Planning
**Quality Activities**:
- Define quality and test strategy
- Define test coverage targets
- Define testing tools and frameworks
- Define test data management strategy
- Define defect management process

**Deliverables**:
- Quality and test strategy
- Test coverage targets
- Testing tools and framework selection
- Test data management strategy
- Defect management process

**Owner**: QA Lead

---

### Phase 5: Development Execution
**Quality Activities**:
- Write unit tests (TDD encouraged)
- Conduct code reviews
- Maintain test coverage (70-80%)
- Continuous integration testing
- Quality in development practices

**Deliverables**:
- Unit tests (passing)
- Code review records
- Test coverage reports
- CI/CD test results

**Owner**: Developers, Tech Lead, QA Lead

---

### Phase 6: Quality & Security Validation
**Quality Activities**:
- Functional testing
- Integration testing
- System testing
- Performance testing
- Security testing
- User acceptance testing (UAT)
- Defect management and resolution

**Deliverables**:
- Test plan and test cases
- Test execution results
- Performance test report
- Security test report
- UAT sign-off
- Defect register
- Test summary report

**Owner**: QA Lead

---

### Phase 7: Deployment & Release
**Quality Activities**:
- Pre-deployment testing
- Staging validation
- Post-deployment testing
- Smoke testing in production
- Production validation

**Deliverables**:
- Pre-deployment test results
- Staging validation report
- Post-deployment test results
- Production validation report

**Owner**: QA Lead, SRE

---

### Phase 8: Operations & Maintenance
**Quality Activities**:
- Monitor quality metrics
- Track defect trends
- Conduct root cause analysis
- Continuous improvement
- Customer satisfaction monitoring

**Deliverables**:
- Quality metrics dashboard
- Defect trend analysis
- Root cause analysis reports
- Improvement backlog
- Customer satisfaction reports

**Owner**: SRE, Support Lead

---

## TESTING LEVELS

### Unit Testing
- **Who**: Developers
- **What**: Individual functions, classes, modules
- **When**: During development (TDD)
- **Tools**: JUnit, pytest, Jest, etc.
- **Coverage**: 70-80%

### Integration Testing
- **Who**: QA Engineers
- **What**: Component interactions, API integrations
- **When**: After unit testing
- **Tools**: Postman, REST Assured, etc.
- **Coverage**: All integrations

### System Testing
- **Who**: QA Engineers
- **What**: End-to-end workflows
- **When**: After integration testing
- **Tools**: Selenium, Cypress, Playwright
- **Coverage**: All user workflows

### Performance Testing
- **Who**: Performance Engineer
- **What**: Load, stress, endurance testing
- **When**: After system testing
- **Tools**: JMeter, Gatling, k6
- **Coverage**: All SLAs

### Security Testing
- **Who**: Security Lead, Security Architect
- **What**: Vulnerability scanning, penetration testing
- **When**: After system testing
- **Tools**: OWASP ZAP, Burp Suite, Snyk
- **Coverage**: OWASP Top 10

### User Acceptance Testing (UAT)
- **Who**: Users, Business Stakeholders
- **What**: Business workflows and requirements
- **When**: After all testing complete
- **Tools**: Manual testing, production-like environment
- **Coverage**: All acceptance criteria

---

## TEST COVERAGE TARGETS

| Test Type | Coverage Target |
|-----------|-----------------|
| **Unit Tests** | 70-80% |
| **Integration Tests** | 100% of integrations |
| **System Tests** | 100% of user workflows |
| **API Tests** | 100% of API endpoints |
| **Security Tests** | OWASP Top 10 |
| **Performance Tests** | All SLAs |

---

## DEFECT MANAGEMENT

### Defect Severity Levels
| Severity | Description | Example | Resolution Target |
|----------|-------------|---------|-------------------|
| **P1 - Critical** | System down, data loss | Login failure, data corruption | 4 hours |
| **P2 - High** | Major feature broken | Cannot save, checkout fails | 24 hours |
| **P3 - Medium** | Workaround available | UI issue, minor error | 1 week |
| **P4 - Low** | Cosmetic, enhancement | Spelling, formatting | Next release |

### Defect Lifecycle
1. **New**: Defect logged
2. **Assigned**: Assigned to owner
3. **In Progress**: Being fixed
4. **Fixed**: Fix implemented
5. **Verified**: Fix verified by QA
6. **Closed**: Defect closed

### Root Cause Analysis
For P1 and P2 defects, conduct root cause analysis:
- **5 Whys**: Ask "why" 5 times to find root cause
- **Fishbone**: Diagram potential causes (people, process, technology, environment)
- **Action**: Implement corrective actions to prevent recurrence

---

## QUALITY METRICS

Track these metrics throughout the lifecycle:

| Metric | Target | Purpose |
|--------|--------|---------|
| **Test Coverage** | 70-80% | Code quality |
| **Defect Escape Rate** | <5% | Testing effectiveness |
| **Defect Reopen Rate** | <5% | Fix quality |
| **Code Review Pass Rate** | >80% | Code quality |
| **Automated Test Pass Rate** | >95% | Test stability |
| **Customer Satisfaction** | >4.5/5 | User perception |

---

## QUALITY TOOLS (2025-2026 Recommendations)

| Category | Recommended Tools | Alternatives |
|----------|-------------------|--------------|
| **Test Management** | Jira, Zephyr, TestRail | Xray, Azure DevOps |
| **Unit Testing** | Jest (JS), pytest (Python), JUnit (Java) | Mocha, NUnit, RSpec |
| **Integration Testing** | Postman, REST Assured | SoapUI, Insomnia |
| **E2E/UI Testing** | Playwright (fastest, modern), Cypress | Selenium (legacy), Puppeteer |
| **Performance Testing** | k6 (scriptable), JMeter | Gatling, Artillery, Locust |
| **API Testing** | Postman, REST Assured | SoapUI, Supertest |
| **Test Automation** | Playwright, Cypress | Selenium |
| **Code Coverage** | JaCoCo, Coverage.py, Istanbul | SimpleCov, ncov |
| **Code Quality** | SonarQube, ESLint, PyLint | Prettier, Black, Flake8 |

### 2025-2026 Testing Framework Highlights

**E2E Testing:**
- **Playwright** - Fastest, best for modern web apps, excellent cross-browser support
- **Cypress** - Great DX, component + E2E testing, good for React apps
- **Selenium** - Legacy support, most browser support but slower

**Unit Testing:**
- **Jest** - Most popular for JavaScript/TypeScript
- **pytest** - Python standard, excellent features
- **JUnit** - Java standard, mature ecosystem

**Performance Testing:**
- **k6** - Modern, scriptable with JavaScript, developer-friendly
- **JMeter** - Traditional choice, comprehensive
- **Gatling** - High-performance scenarios, Scala-based

---

## QUALITY GATES SUMMARY

Each phase requires:

### Phase 1 Quality Gates
- ☐ Quality metrics defined
- ☐ Success criteria defined
- ☐ Technical feasibility confirmed

### Phase 2 Quality Gates
- ☐ Testable requirements
- ☐ Acceptance criteria defined
- ☐ Requirements traceability matrix created

### Phase 3 Quality Gates
- ☐ Testability designed in
- ☐ Quality attributes defined
- ☐ Performance targets defined

### Phase 4 Quality Gates
- ☐ Test strategy defined
- ☐ Test coverage targets set
- ☐ Testing tools selected

### Phase 5 Quality Gates
- ☐ Unit tests passing (70-80%)
- ☐ Code reviews completed
- ☐ CI/CD tests passing

### Phase 6 Quality Gates
- ☐ Functional tests passing
- ☐ Integration tests passing
- ☐ Performance tests meeting SLAs
- ☐ Security tests passing
- ☐ UAT signed off

### Phase 7 Quality Gates
- ☐ Pre-deployment tests passing
- ☐ Staging validation passing
- ☐ Post-deployment tests passing
- ☐ Production validation passing

### Phase 8 Quality Gates
- ☐ Monitoring active
- ☐ Quality metrics within targets
- ☐ Customer satisfaction acceptable

---

## CONTINUOUS IMPROVEMENT

Quality is continuously improved through:

1. **Metrics Analysis**: Review quality metrics regularly
2. **Root Cause Analysis**: Analyze defects and incidents
3. **Process Improvements**: Implement process changes
4. **Training**: Train team on quality practices
5. **Tool Upgrades**: Upgrade tools and automation
6. **Best Practices**: Share and adopt best practices

---

## TEMPLATES

See `./templates/` for:
- Test Plan Template
- Test Case Template
- Defect Report Template
- Quality Metrics Template

---

**This shared skill is referenced by all phase skills.**

---

**Review Completed By:** OCTALUME TEAM
**Date:** 2026-01-14
**Next Review Recommended:** After major framework updates or every 12 months
