---
name: "phase_06_quality_security"
description: "Validate quality and security through comprehensive testing. Functional testing, integration/system testing, performance testing, security testing, compliance validation, user acceptance testing (UAT), and defect management."
phase: 6
phase_name: "Quality & Security Validation"
owner: "QA Lead"
secondary_owner: "Security Lead"
participants: ["QA Engineers", "Performance Engineer", "Security Lead", "Compliance Officer", "Product Owner", "Users", "Developers"]
entry_criteria: [
  "All planned features implemented",
  "Unit tests passing",
  "Code reviews completed",
  "Build artifacts ready"
]
exit_criteria: [
  "Functional tests passing",
  "Integration tests passing",
  "Performance tests meeting SLAs",
  "Security tests passing with no critical vulnerabilities",
  "Compliance validation complete",
  "UAT signed off",
  "Known defects documented and prioritized",
  "Test report completed",
  "Go/no-go decision to proceed to Phase 7"
]
estimated_duration: "4-8 weeks"
dependencies: ["phase_05_development_execution"]
outputs: [
  "Test Plan and Test Cases",
  "Test Execution Results",
  "Performance Test Report",
  "Security Test Report",
  "Penetration Test Report",
  "Compliance Validation Report",
  "UAT Sign-off",
  "Defect Register",
  "Test Summary Report"
]
next_phase: "phase_07_deployment_release"
---

# PHASE 6: QUALITY & SECURITY VALIDATION

## Overview

**Objective**: Validate quality and security through comprehensive testing

**Entry Point**: Complete Build from Phase 5
**Exit Point**: Validated Build with UAT Sign-off

---

## Key Roles in This Phase

| Role | Responsibility |
|------|----------------|
| **QA Lead** | Owns quality validation |
| **Security Lead** | Owns security validation |
| **Performance Engineer** | Performance testing |
| **Compliance Officer** | Compliance validation |
| **Product Owner** | UAT coordination |
| **Users** | UAT participants |

---

## Step 1: Functional Testing

**Owner**: QA Lead / QA Engineers
**Participants**: Product Owner, Developers
**Timeline**: 2-3 weeks

### Tasks
- Execute functional test cases
- Test all user stories and acceptance criteria
- Test positive and negative scenarios
- Test edge cases and boundary conditions
- Test user workflows end-to-end
- Test integrations with external systems
- Log defects and track to resolution

### Deliverables
- Functional test results
- Defect reports
- Test coverage report
- Feature validation matrix

### Approvals
- QA Lead: Validate functional testing complete
- Product Owner: Validate acceptance criteria met

---

## Step 2: Integration and System Testing

**Owner**: QA Lead
**Participants**: Developers, Tech Lead
**Timeline**: 2 weeks

### Tasks
- Test integration between components
- Test API integrations
- Test database integrations
- Test third-party service integrations
- Test end-to-end workflows
- Test data flow across systems
- Test error handling and recovery

### Deliverables
- Integration test results
- System test results
- Integration defect reports
- API test results

### Approvals
- QA Lead: Validate integration testing
- Tech Lead: Validate technical integration

---

## Step 3: Performance Testing

**Owner**: Performance Engineer
**Participants**: DevOps, SRE, Tech Lead
**Timeline**: 2 weeks

### Tasks
- Design performance test scenarios
- Conduct load testing (normal load)
- Conduct stress testing (peak load)
- Conduct endurance testing (sustained load)
- Conduct spike testing (sudden load increases)
- Measure response times, throughput, resource utilization
- Identify performance bottlenecks
- Validate SLA compliance

### Deliverables
- Performance test plan
- Performance test results
- Performance analysis report
- Bottleneck identification
- Optimization recommendations

### Approvals
- Performance Engineer: Validate performance testing
- SRE: Validate operability under load
- Tech Lead: Validate optimizations

### Performance Targets

| Metric | Target | Actual |
|--------|--------|--------|
| Response Time (p95) | <200ms | TBD |
| Response Time (p99) | <500ms | TBD |
| Throughput | 1000 req/sec | TBD |
| Concurrent Users | 10,000 | TBD |
| Error Rate | <0.1% | TBD |

---

## Step 4: Security Testing

**Owner**: Security Lead / Security Architect
**Participants**: Developers, Compliance Officer, CISO
**Timeline**: 2-3 weeks

### Tasks
- Conduct Static Application Security Testing (SAST)
- Conduct Dynamic Application Security Testing (DAST)
- Conduct Software Composition Analysis (SCA)
- Conduct penetration testing (internal and external)
- Conduct authentication and authorization testing
- Conduct input validation testing
- Conduct session management testing
- Test for OWASP Top 10 vulnerabilities
- Validate encryption implementation
- Validate secrets management

### Deliverables
- Security test plan
- SAST scan results
- DAST scan results
- SCA scan results
- Penetration test report
- Vulnerability assessment
- Security remediation plan
- Security sign-off

### Approvals
- Security Lead: Validate security testing
- CISO: Approve security posture
- Compliance Officer: Validate compliance

**Reference**: `../shared/security/SKILL.md`

---

## Step 5: Compliance Validation

**Owner**: Compliance Officer / Audit Manager
**Participants**: Security Lead, Legal, CISO
**Timeline**: 2 weeks

### Tasks
- Validate compliance with applicable regulations
- Validate audit trail completeness
- Validate data protection controls
- Validate access controls
- Validate documentation requirements
- Conduct compliance gap analysis
- Prepare for external audits
- Validate retention policies

### Deliverables
- Compliance validation report
- Compliance gap analysis
- Audit trail verification
- Remediation plan (if gaps found)
- Compliance sign-off

### Approvals
- Compliance Officer: Validate compliance
- Legal: Review compliance position
- CISO: Approve security compliance

**Reference**: `../shared/compliance/SKILL.md`

---

## Step 6: User Acceptance Testing (UAT)

**Owner**: Product Owner
**Participants**: Users, Business Stakeholders, QA
**Timeline**: 2-3 weeks

### Tasks
- Define UAT scenarios and test cases
- Prepare UAT environment
- Conduct UAT training for users
- Execute UAT test cases
- Collect user feedback
- Address UAT issues
- Obtain UAT sign-off

### Deliverables
- UAT plan
- UAT test cases
- UAT environment
- User feedback
- UAT sign-off

### Approvals
- Product Owner: Coordinate UAT
- Users: Provide sign-off
- Business Stakeholders: Approve for production

---

## Step 7: Defect Management

**Owner**: QA Lead
**Participants**: Developers, Product Owner, Security Lead
**Timeline**: Continuous throughout Phase 6

### Tasks
- Log all defects found during testing
- Prioritize defects (P1: Critical, P2: High, P3: Medium, P4: Low)
- Assign defects to owners
- Track defect resolution
- Retest fixed defects
- Verify defect closure
- Create defect metrics and analysis

### Deliverables
- Defect register
- Defect metrics and analysis
- Root cause analysis for critical defects
- Known issues document

### Defect SLAs

| Priority | Description | Resolution Target |
|----------|-------------|-------------------|
| **P1** | Critical (system down, data loss) | 4 hours |
| **P2** | High (major feature broken) | 24 hours |
| **P3** | Medium (workaround available) | 1 week |
| **P4** | Low (cosmetic, enhancement) | Next release |

---

## Step 8: Quality Gates and Go/No-Go Decision

**Owner**: Project Manager / Product Owner
**Participants**: All leads, Executive Sponsor
**Timeline**: 1 week

### Tasks
- Compile all test results
- Assess quality gates
- Assess security posture
- Assess compliance position
- Assess residual risks
- Make go/no-go recommendation
- Obtain go/no-go approval

### Deliverables
- Test summary report
- Quality gates assessment
- Security assessment
- Compliance assessment
- Risk assessment
- Go/no-go recommendation
- Go/no-go approval

### Approvals
- Project Manager: Compile recommendation
- Product Owner: Validate readiness
- Tech Lead: Validate technical readiness
- QA Lead: Validate quality readiness
- Security Lead: Validate security readiness
- Executive Sponsor: Approve go/no-go

---

## Quality Gates (Exit Criteria)

Before proceeding to Phase 7, ensure:

- ☐ Functional tests passing
- ☐ Integration tests passing
- ☐ Performance tests meeting SLAs
- ☐ Security tests passing (no critical vulnerabilities)
- ☐ Compliance validation complete
- ☐ UAT signed off
- ☐ Known defects documented and prioritized
- ☐ Test report completed
- ☐ Go/no-go decision to proceed to Phase 7

---

## Testing Tools

Common tools used in this phase:

| Type | Tools |
|------|-------|
| **Functional Testing** | Selenium, Cypress, Playwright |
| **API Testing** | Postman, REST Assured |
| **Performance Testing** | JMeter, Gatling, k6 |
| **Security Testing** | OWASP ZAP, Burp Suite, SonarQube |
| **SAST/DAST** | Fortify, Checkmarx, Veracode |
| **SCA** | Snyk, Dependabot, WhiteSource |
| **Test Management** | Jira, Zephyr, TestRail |

---

## Templates and Examples

See `./templates/` for:
- Test Plan Template
- Test Case Template
- UAT Plan Template
- Defect Report Template

See `./examples/` for:
- Sample Test Report
- Sample Security Test Report

---

**Previous Phase**: `../phase_05_development_execution/SKILL.md`
**Next Phase**: `../phase_07_deployment_release/SKILL.md`
