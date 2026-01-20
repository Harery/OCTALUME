---
name: "phase_07_deployment_release"
description: "Deploy validated build to production. Deployment strategy, pre-deployment checklist, staging deployment, production deployment, post-deployment validation, rollback planning, release documentation, and release closure."
phase: 7
phase_name: "Deployment & Release"
owner: "DevOps Lead"
secondary_owner: "Technical Lead"
participants: ["DevOps", "SRE", "Tech Lead", "QA Lead", "Security Lead", "Product Owner", "Project Manager"]
entry_criteria: [
  "Functional tests passing",
  "Integration tests passing",
  "Performance tests meeting SLAs",
  "Security tests passing",
  "Compliance validation complete",
  "UAT signed off",
  "Go/no-go approval received"
]
exit_criteria: [
  "Staging deployment successful",
  "Production deployment successful",
  "Post-deployment validation passing",
  "Monitoring and alerting active",
  "Release documentation published",
  "Stakeholders notified",
  "Rollback plan tested",
  "Release closure completed"
]
estimated_duration: "2-4 weeks"
dependencies: ["phase_06_quality_security"]
outputs: [
  "Deployment Plan",
  "Staging Deployment",
  "Production Deployment",
  "Release Notes",
  "Deployment Runbook",
  "Rollback Plan",
  "Monitoring Dashboards",
  "Release Sign-off"
]
next_phase: "phase_08_operations_maintenance"
---

# PHASE 7: DEPLOYMENT & RELEASE

## Overview

**Objective**: Deploy validated build to production safely

**Entry Point**: Validated Build with Go/No-Go Approval from Phase 6
**Exit Point**: Released to Production

---

## Key Roles in This Phase

| Role | Responsibility |
|------|----------------|
| **DevOps Lead** | Owns deployment execution |
| **SRE** | Production readiness and validation |
| **Tech Lead** | Technical validation |
| **QA Lead** | Pre and post-deployment testing |
| **Security Lead** | Security validation |
| **Product Owner** | Release coordination |

---

## Step 1: Deployment Strategy

**Owner**: DevOps Lead
**Participants**: SRE, Tech Lead, Security Lead
**Timeline**: 1 week

### Tasks
- Define deployment strategy (blue-green, canary, rolling)
- Define deployment windows and schedules
- Define rollback strategy and triggers
- Define deployment communication plan
- Define stakeholder notification plan
- Create deployment runbook

### Deliverables
- Deployment strategy document
- Deployment schedule
- Rollback strategy
- Communication plan
- Deployment runbook

### Approvals
- DevOps: Own deployment strategy
- SRE: Validate operability
- Tech Lead: Validate technical approach
- Product Owner: Validate schedule

### Deployment Strategies

| Strategy | Description | Use When |
|----------|-------------|----------|
| **Blue-Green** | Two identical environments, switch traffic | Zero-downtime required |
| **Canary** | Gradual rollout to subset of users | Risk mitigation, gradual validation |
| **Rolling** | Incremental replacement of instances | Large-scale deployments |
| **Big Bang** | All at once (cutover) | Simple systems, maintenance windows |

---

## Step 2: Pre-Deployment Checklist

**Owner**: DevOps / SRE
**Participants**: All leads
**Timeline**: 1 week

### Tasks
- Verify staging environment is production-like
- Verify all monitoring and alerting configured
- Verify backup and recovery procedures tested
- Verify security controls in place
- Verify compliance requirements met
- Verify rollback procedures tested
- Verify documentation complete
- Verify stakeholders notified

### Deliverables
- Pre-deployment checklist (completed)
- Staging validation report
- Monitoring configuration validation
- Backup verification
- Rollback test results

### Approvals
- DevOps: Validate deployment readiness
- SRE: Validate operational readiness
- Security Lead: Validate security readiness
- QA Lead: Validate quality readiness

### Pre-Deployment Checklist

- ☐ Staging tests passing
- ☐ Monitoring and alerting configured
- ☐ Log aggregation active
- ☐ Backup procedures verified
- ☐ Rollback procedures tested
- ☐ Security scan passed
- ☐ Compliance check passed
- ☐ Documentation complete
- ☐ Stakeholders notified
- ☐ Deployment window confirmed

---

## Step 3: Staging Deployment

**Owner**: DevOps
**Participants**: QA, SRE, Tech Lead
**Timeline: 1 week

### Tasks
- Deploy build to staging environment
- Execute smoke tests in staging
- Execute full regression tests in staging
- Execute performance tests in staging
- Conduct security validation in staging
- Validate monitoring and observability
- Conduct stakeholder demo
- Fix any staging issues

### Deliverables
- Staging deployment
- Staging test results
- Staging validation report
- Issue fixes (if any)

### Approvals
- DevOps: Complete staging deployment
- QA: Validate staging tests
- SRE: Validate staging operations
- Product Owner: Approve for production

---

## Step 4: Production Deployment

**Owner**: DevOps Lead
**Participants**: SRE, Tech Lead, Security Lead (on standby)
**Timeline: Deployment window (varies)

### Tasks
- Conduct pre-deployment briefing
- Execute production deployment
- Monitor deployment execution
- Execute post-deployment smoke tests
- Monitor system health metrics
- Conduct stakeholder notification
- Execute rollback if needed (emergency)

### Deliverables
- Production deployment
- Deployment execution log
- Smoke test results
- System health metrics
- Deployment notification

### Approvals
- DevOps: Execute deployment
- SRE: Monitor and validate production
- Tech Lead: Technical validation
- Product Owner: Approve release

---

## Step 5: Post-Deployment Validation

**Owner**: SRE / QA Lead
**Participants**: DevOps, Tech Lead, Security Lead
**Timeline: 1-2 weeks (validation period)

### Tasks
- Execute post-deployment smoke tests
- Execute monitoring and health checks
- Validate all features working
- Validate performance metrics
- Validate security controls
- Validate compliance controls
- Monitor for issues and anomalies
- Collect user feedback

### Deliverables
- Post-deployment test results
- System health report
- Performance validation report
- Security validation report
- User feedback summary
- Issue log (if any)

### Approvals
- SRE: Validate operational health
- QA Lead: Validate quality
- Security Lead: Validate security
- Product Owner: Validate user acceptance

---

## Step 6: Rollback Planning and Execution

**Owner**: DevOps / SRE
**Participants**: Tech Lead, Security Lead
**Timeline: Planned during strategy, executed if needed

### Tasks
- Define rollback triggers and criteria
- Document rollback procedures
- Test rollback procedures in staging
- Define rollback communication plan
- Execute rollback if critical issues detected
- Conduct post-rollback analysis

### Deliverables
- Rollback plan
- Rollback test results
- Rollback execution log (if executed)
- Post-rollback analysis (if executed)

### Rollback Triggers

| Trigger Type | Example | Action |
|--------------|---------|--------|
| **Critical** | System down, data corruption | Immediate rollback |
| **High** | Major feature broken, performance degraded | Rollback within 1 hour |
| **Medium** | Minor issues, workaround available | Monitor, decide within 4 hours |
| **Low** | Cosmetic issues, documentation | Fix in place |

---

## Step 7: Release Documentation

**Owner**: Tech Lead / Product Owner
**Participants**: All leads
**Timeline: 1 week

### Tasks
- Create release notes
- Document new features and enhancements
- Document bug fixes
- Document known issues
- Document upgrade instructions
- Document configuration changes
- Document API changes
- Publish release documentation

### Deliverables
- Release notes
- Feature documentation
- Upgrade guide
- Configuration guide
- API documentation (if changed)
- Known issues document

### Approvals
- Tech Lead: Validate technical documentation
- Product Owner: Validate user-facing documentation
- QA Lead: Validate test coverage

---

## Step 8: Release Closure

**Owner**: Project Manager
**Participants**: All stakeholders
**Timeline: 1 week

### Tasks
- Conduct post-release review
- Document lessons learned
- Update project metrics
- Close project financials
- Conduct stakeholder sign-off
- Archive project artifacts
- Celebrate success (team recognition)

### Deliverables
- Post-release review
- Lessons learned document
- Project closure report
- Stakeholder sign-off
- Project archive

### Approvals
- Project Manager: Close release
- Product Owner: Accept release
- Executive Sponsor: Approve closure

---

## Quality Gates (Exit Criteria)

Before declaring release complete:

- ☐ Staging deployment successful
- ☐ Production deployment successful
- ☐ Post-deployment validation passing
- ☐ Monitoring and alerting active
- ☐ Release documentation published
- ☐ Stakeholders notified
- ☐ Rollback plan tested
- ☐ Release closure completed

---

## Deployment Monitoring

Monitor these metrics during and after deployment:

| Metric | Target | Actual |
|--------|--------|--------|
| Deployment Time | <30 minutes | TBD |
| Rollback Time | <15 minutes | TBD |
| Error Rate | <0.1% | TBD |
| Response Time (p95) | <200ms | TBD |
| Availability | >99.9% | TBD |
| Critical Incidents | 0 | TBD |

---

## Communication Plan

Notify stakeholders at each stage:

| Stage | Who | When |
|-------|-----|------|
| **Deployment Scheduled** | All stakeholders | 2 weeks before |
| **Staging Complete** | All stakeholders | 1 week before |
| **Production Imminent** | All stakeholders | 24 hours before |
| **Production Complete** | All stakeholders | Immediately after |
| **Post-Deployment Validation** | All stakeholders | 1-2 weeks after |
| **Release Closed** | All stakeholders | After closure |

---

## Templates and Examples

See `./templates/` for:
- Deployment Plan Template
- Release Notes Template
- Rollback Plan Template
- Pre-Deployment Checklist

See `./examples/` for:
- Sample Deployment Plan
- Sample Release Notes

---

**Previous Phase**: `../phase_06_quality_security/SKILL.md`
**Next Phase**: `../phase_08_operations_maintenance/SKILL.md`

---

**Review Completed By:** OCTALUME TEAM
**Date:** 2026-01-13
**Next Review Recommended:** After major framework updates or every 12 months
