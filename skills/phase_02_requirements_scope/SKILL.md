---
name: "phase_02_requirements_scope"
description: "Define detailed functional, non-functional, security, compliance, and data requirements. Create requirements traceability matrix and get stakeholder sign-off."
phase: 2
phase_name: "Requirements & Scope"
owner: "Product Owner (functional), CTA (technical)"
secondary_owner: "Business Analyst / Systems Analyst"
participants: ["Tech Lead", "CTA", "Security Lead", "Compliance Officer", "Data Architect", "DevOps", "SRE", "Performance Engineer", "Users", "Subject Matter Experts"]
entry_criteria: [
  "Business case approved by Executive Sponsor",
  "PRD completed and reviewed",
  "Technical feasibility confirmed",
  "Security considerations documented",
  "Stakeholders aligned and committed"
]
exit_criteria: [
  "Functional requirements documented and approved",
  "Non-functional requirements defined and baselined",
  "Security requirements documented and approved",
  "Compliance requirements identified and validated",
  "Data requirements documented",
  "Requirements traceability matrix created",
  "All requirements signed off by stakeholders",
  "Go/no-go decision to proceed to Phase 3"
]
estimated_duration: "8-12 weeks"
dependencies: ["phase_01_vision_strategy"]
outputs: [
  "Functional Requirements Specification",
  "User Stories and Use Cases",
  "Acceptance Criteria",
  "Prioritized Backlog",
  "Non-Functional Requirements Specification",
  "Performance SLAs",
  "Security Requirements Specification",
  "Compliance Requirements Specification",
  "Data Requirements Specification",
  "Requirements Traceability Matrix"
]
next_phase: "phase_03_architecture_design"
---

# PHASE 2: REQUIREMENTS & SCOPE

## Overview

**Objective**: Define detailed requirements for all aspects of the system

**Entry Point**: Approved PRD from Phase 1
**Exit Point**: Approved Requirements Specification

---

## Key Roles in This Phase

| Role | Responsibility |
|------|----------------|
| **Product Owner** | Owns functional requirements |
| **CTA** | Owns technical/non-functional requirements |
| **Business Analyst** | Elicits and documents requirements |
| **Security Lead** | Defines security requirements |
| **Compliance Officer** | Defines compliance requirements |
| **Data Architect** | Defines data requirements |
| **Tech Lead** | Technical feasibility review |
| **Users/SMEs** | Validate requirements |

---

## Step 1: Functional Requirements

**Owner**: Business Analyst / Product Owner
**Participants**: Tech Lead, Users, Subject Matter Experts
**Timeline**: 2-3 weeks

### Tasks
- Elicit requirements from stakeholders
- Document functional requirements
- Create user stories and use cases
- Define acceptance criteria
- Prioritize requirements (MoSCoW: Must, Should, Could, Won't)
- Create requirements traceability matrix

### Deliverables
- Functional requirements specification
- User stories and use cases
- Acceptance criteria
- Prioritized backlog
- Requirements traceability matrix

### Approvals
- Product Owner: Approve functional requirements
- Tech Lead: Technical feasibility review
- Users: Validate requirements

---

## Step 2: Non-Functional Requirements (NFRs)

**Owner**: CTA / Tech Lead
**Participants**: DevOps, SRE, Performance Engineer
**Timeline**: 1-2 weeks

### Tasks
- Define performance requirements (response time, throughput)
- Define scalability requirements (users, transactions, data)
- Define availability and reliability requirements (uptime, SLA)
- Define usability requirements (UI/UX standards)
- Define maintainability requirements (code quality, documentation)
- Define operability requirements (monitoring, alerting, deployment)

### Deliverables
- Non-functional requirements specification
- Performance SLAs
- Availability targets (e.g., 99%, 99.9%)
- Scalability requirements
- Capacity planning estimates

### Approvals
- CTA: Approve NFRs
- DevOps: Validate operability
- Performance Engineer: Validate performance
- SRE: Validate reliability requirements

---

## Step 3: Security Requirements

**Owner**: Security Lead / Security Architect
**Participants**: CTA, Compliance Officer, CISO
**Timeline**: 2 weeks

### Tasks
- Identify security requirements (CIA triad: Confidentiality, Integrity, Availability)
- Define authentication requirements (MFA, SSO, OIDC)
- Define authorization requirements (RBAC, ABAC)
- Define data protection requirements (encryption at rest, in transit)
- Define audit and logging requirements
- Identify applicable security standards (NIST, ISO 27001, OWASP)
- Create security risk assessment

### Deliverables
- Security requirements specification
- Authentication and authorization design
- Data protection requirements
- Audit and logging requirements
- Security risk assessment
- Compliance matrix (security)

### Approvals
- Security Lead: Own security requirements
- CISO: Approve security posture
- Compliance Officer: Validate compliance
- CTA: Validate technical feasibility

**Reference**: `../shared/security/SKILL.md` for security framework

---

## Step 4: Compliance Requirements

**Owner**: Compliance Officer / Audit Manager
**Participants**: Legal, CISO, Executive Sponsor
**Timeline**: 2 weeks

### Tasks
- Identify applicable regulations (GDPR, HIPAA, SOC 2, PCI DSS, SOX, DoD/ITAR)
- Map regulatory requirements to technical controls
- Define audit requirements (internal, external)
- Define documentation requirements
- Define data retention requirements
- Create compliance gap analysis

### Deliverables
- Compliance requirements specification
- Regulatory compliance matrix
- Audit requirements
- Documentation requirements list
- Data retention policies
- Compliance gap analysis

### Approvals
- Compliance Officer: Own compliance requirements
- Legal: Review and validate
- CISO: Approve security compliance
- Executive Sponsor: Approve compliance approach

**Reference**: `../shared/compliance/SKILL.md` for compliance framework

---

## Step 5: Data Requirements

**Owner**: Data Architect
**Participants**: Business Analyst, CTA, Compliance Officer
**Timeline**: 1-2 weeks

### Tasks
- Identify data entities and attributes
- Define data models and relationships
- Define data volumes and growth projections
- Define data lifecycle requirements (create, read, update, archive, delete)
- Define data privacy requirements (classification, PII handling)
- Create data dictionary

### Deliverables
- Data requirements specification
- Conceptual data model
- Data dictionary
- Data volume projections
- Data privacy classification

### Approvals
- Data Architect: Own data requirements
- CTA: Validate technical fit
- Compliance Officer: Validate privacy requirements
- Product Owner: Validate business needs

---

## Quality Gates (Exit Criteria)

Before proceeding to Phase 3, ensure:

- ☐ Functional requirements documented and approved
- ☐ Non-functional requirements defined and baselined
- ☐ Security requirements documented and approved
- ☐ Compliance requirements identified and validated
- ☐ Data requirements documented
- ☐ Requirements traceability matrix created
- ☐ All requirements signed off by stakeholders
- ☐ Go/no-go decision to proceed to Phase 3

---

## Requirements Traceability Matrix (RTM)

The RTM links requirements to their origin and tracks them through all phases:

| Requirement ID | Source | Description | Owner | Status | Phase | Verified |
|----------------|--------|-------------|-------|--------|-------|----------|
| REQ-FUNC-001 | PRD-5.2 | User authentication | Product Owner | Approved | P5 | ☐ |
| REQ-NFR-001 | NFR-2.1 | Response time <200ms | CTA | Baseline | P6 | ☐ |
| REQ-SEC-001 | SEC-1.1 | MFA required | Security Lead | Approved | P5 | ☐ |

---

## MoSCoW Prioritization

| Priority | Description | Example |
|----------|-------------|---------|
| **Must Have** | Critical for MVP | User login, core feature |
| **Should Have** | Important but not critical | Password reset, reporting |
| **Could Have** | Nice to have if time permits | Advanced search, notifications |
| **Won't Have** | Out of scope for now | Multi-language, advanced analytics |

---

## Templates and Examples

See `./templates/` for:
- Functional Requirements Template
- User Story Template
- NFR Template
- Security Requirements Template
- RTM Template

See `./examples/` for:
- Sample Requirements Specification
- Sample RTM

---

**Previous Phase**: `../phase_01_vision_strategy/SKILL.md`
**Next Phase**: `../phase_03_architecture_design/SKILL.md`

---

**Review Completed By:** OCTALUME TEAM
**Date:** 2026-01-13
**Next Review Recommended:** After major framework updates or every 12 months
