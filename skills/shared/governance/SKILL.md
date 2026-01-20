---
name: "governance"
description: "Shared governance framework across all phases. Decision-making authority, RACI matrix, approval workflows, change management, and escalation procedures."
type: "shared"
used_by: ["all_phases"]
---

# GOVERNANCE FRAMEWORK - SHARED ACROSS ALL PHASES

This shared skill provides governance guidance that applies across all phases of the Unified Enterprise Lifecycle.

**Clear Authority**: Every decision has a clear owner and approval process.

---

## GOVERNANCE PRINCIPLES

### Delegated Authority
- Decisions pushed to appropriate level (not all to PMO)
- Clear RACI for all activities
- Empowered teams with clear boundaries

### Parallel Approvals
- Risk-based approval tracks (3/5/7 stages)
- Faster approvals for low-risk items
- Emergency process for critical items

### Transparency and Traceability
- All decisions documented
- Clear audit trail
- Status visible to stakeholders

---

## RACI MATRIX

### RACI Definitions
| Letter | Meaning | Responsibility |
|--------|----------|----------------|
| **R** | Responsible | Does the work |
| **A** | Accountable | Owns the decision (only ONE) |
| **C** | Consulted | Provides input (two-way communication) |
| **I** | Informed | Notified of results (one-way communication) |

### RACI by Phase and Activity

| Phase | Activity | Product Owner | PM | CTA | Tech Lead | Security | Compliance | Exec Sponsor |
|-------|----------|--------------|----|-----|-----------|----------|------------|--------------|
| **P1** | Business Case | A | C | C | I | I | I | A |
| **P1** | PRD | A | C | C | I | I | I | A |
| **P1** | Go/No-Go | R | C | C | I | I | I | A |
| **P2** | Requirements | A | C | I | C | I | C | I |
| **P2** | NFRs | I | I | A | C | I | I | I |
| **P2** | Security Reqs | I | I | C | I | A | C | I |
| **P2** | Go/No-Go | R | C | C | I | I | I | A |
| **P3** | Architecture | I | C | A | C | C | I | I |
| **P3** | Security Arch | I | C | C | I | A | C | I |
| **P3** | Go/No-Go | R | C | C | I | I | I | A |
| **P4** | WBS | C | A | C | C | I | I | I |
| **P4** | Resources | C | A | C | C | I | I | A |
| **P4** | Go/No-Go | R | C | C | I | I | I | A |
| **P5** | Code | I | I | I | A | C | I | I |
| **P5** | Code Review | I | I | I | A | C | I | I |
| **P6** | Testing | C | I | I | C | I | C | I |
| **P6** | UAT Sign-off | A | I | I | I | I | I | A |
| **P7** | Deploy | I | I | I | C | C | I | I |
| **P8** | Operations | I | I | I | C | C | C | I |

---

## APPROVAL WORKFLOWS

### Go/No-Go Decisions (End of Each Phase)

**Approval Chain**:
1. Phase Owner prepares recommendation (R)
2. Secondary Owner reviews (C)
3. Key stakeholders review (C)
4. Executive Sponsor decides (A)

**Timeline**: 1-2 weeks for standard process
**Emergency**: 24-hour approval for critical issues

### Code Approvals
**Approval Chain**:
1. Developer self-review (R)
2. Peers review (C)
3. Tech Lead approves (A)

**Timeline**: Within 24-48 hours of submission

### Architecture Approvals
**Approval Chain**:
1. CTA proposes architecture (R)
2. Security Architect reviews (C)
3. Tech Lead reviews (C)
4. CTA approves (A)

**Timeline**: 1-2 weeks for major architectures

### Security Approvals
**Approval Chain**:
1. Security Architect proposes (R)
2. CISO reviews (C)
3. CTA validates technical (C)
4. CISO approves (A)

**Timeline**: 1 week for security designs

### Compliance Approvals
**Approval Chain**:
1. Compliance Officer proposes (R)
2. Legal reviews (C)
3. CISO reviews security (C)
4. Executive Sponsor approves (A)

**Timeline**: 2 weeks for compliance frameworks

---

## CHANGE MANAGEMENT

### Change Request Process

1. **Submit Change Request**: Document change, rationale, impact
2. **Impact Assessment**: Analyze impact on scope, schedule, budget, risk
3. **Review**: Review by appropriate authority (based on impact)
4. **Approve/Reject**: Decision on change request
5. **Update**: Update plans and documentation if approved
6. **Communicate**: Notify stakeholders of change

### Change Tiers

| Tier | Description | Approval | Timeline |
|------|-------------|----------|----------|
| **Tier 1** | Low impact, low risk | Tech Lead | 24 hours |
| **Tier 2** | Medium impact, medium risk | Project Manager | 1 week |
| **Tier 3** | High impact, high risk | Executive Sponsor | 2 weeks |

---

## ESCALATION PROCEDURES

### Escalation Levels

| Level | Trigger | Escalation To | Timeline |
|-------|---------|---------------|----------|
| **L1** | Issue blocking work | Tech Lead / PM | Immediate |
| **L2** | Issue unresolved for 24h | Phase Owner | Within 24h |
| **L3** | Issue unresolved for 1 week | Executive Sponsor | Within 1 week |
| **L4** | Critical issue (system down) | Executive Sponsor | Immediate |

### Escalation Process
1. **Identify Issue**: Clearly define the issue and impact
2. **Attempt Resolution**: Try to resolve at current level first
3. **Document**: Document issue, attempts, impact
4. **Escalate**: Escalate to next level with documentation
5. **Follow Up**: Ensure escalation is addressed

---

## DECISION-MAKING AUTHORITY

### Decision Categories and Owners

| Decision Category | Owner | Consulted | Informed |
|-------------------|-------|-----------|----------|
| **Business Case** | Executive Sponsor | PM, Finance | All |
| **Product Requirements** | Product Owner | Users, Tech Lead | All |
| **Architecture** | CTA | Tech Lead, Security | All |
| **Security** | CISO | Security Architect, Compliance | All |
| **Compliance** | Compliance Officer | Legal, Security | All |
| **Technical** | Tech Lead | CTA, Developers | All |
| **Budget** | Executive Sponsor | PM, Finance | All |
| **Timeline** | Project Manager | Tech Lead, Product Owner | All |
| **Quality** | QA Lead | Tech Lead, Product Owner | All |
| **Resources** | Project Manager | Tech Lead, HR | All |
| **Go/No-Go (Phase)** | Executive Sponsor | Phase Owner, PM | All |

---

## DOCUMENTATION AND TRACEABILITY

### Decision Records

All significant decisions must be documented:

**Format**:
- Decision ID
- Date
- Decision Maker
- Decision Description
- Rationale
- Alternatives Considered
- Impact
- Approvals

**Storage**: Version controlled, accessible to all stakeholders

### Traceability Format

All artifacts follow traceability format: `P{N}-{SECTION}-###`

**Examples**:
- `P1-VISION-001`: Phase 1, Vision document, item 1
- `P3-ARCH-015`: Phase 3, Architecture, item 15
- `P5-CODE-427`: Phase 5, Code commit/story, item 427

**Traceability Chain**:
```
Epic → Feature → Story → Commit → Build → Artifact → Release → Test → Result
```

---

## STAKEHOLDER COMMUNICATION

### Communication Cadence

| Stakeholder | Frequency | Format | Owner |
|-------------|-----------|--------|-------|
| **Executive Sponsor** | Monthly | Executive Summary | PM |
| **Product Owner** | Weekly | Status Report | PM |
| **Tech Team** | Daily | Standup | Tech Lead |
| **Users** | Per Sprint | Demo | Product Owner |
| **Security** | Weekly | Security Report | Security Lead |
| **Compliance** | Monthly | Compliance Report | Compliance Officer |

### Status Reports

**Content**:
- Progress against plan
- Milestones achieved
- Risks and issues
- Next steps
- Decisions required

**Format**: Standard template, distributed via email/dashboard

---

## GOVERNANCE TOOLS

| Category | Tools |
|----------|-------|
| **Project Management** | Jira, Azure DevOps, Asana |
| **Documentation** | Confluence, Notion, SharePoint |
| **Decision Tracking** | Decision log, ADRs |
| **Approvals** | Jira workflows, email, sign-off sheets |
| **Reporting** | Dashboards, status reports, exec summaries |
| **Auditing** | Audit logs, access logs, change logs |

---

## GOVERNANCE BEST PRACTICES

1. **Clear Authority**: Every decision has clear owner
2. **Documented Decisions**: All decisions documented and traceable
3. **Appropriate Review**: Right level of review for risk
4. **Transparency**: Status visible to all stakeholders
5. **Escalation Path**: Clear escalation procedures
6. **Continuous Improvement**: Regular governance review and improvement

---

## TEMPLATES

See `./templates/` for:
- Change Request Template
- Decision Record Template
- Escalation Template
- Status Report Template

---

## TROUBLESHOOTING GOVERNANCE ISSUES

| Issue | Symptom | Resolution |
|-------|----------|------------|
| **Bottleneck** | Decisions delayed | Escalate to executive, adjust authority |
| **Unclear Authority** | Who decides? | Consult RACI matrix |
| **Poor Communication** | Stakeholders unaware | Improve communication cadence |
| **Scope Creep** | Requirements expanding | Enforce change management |

---

**This shared skill is referenced by all phase skills.**

---

**Review Completed By:** OCTALUME TEAM
**Date:** 2026-01-13
**Next Review Recommended:** After major framework updates or every 12 months
