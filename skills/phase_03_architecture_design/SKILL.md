---
name: "phase_03_architecture_design"
description: "Design system architecture, security architecture, data architecture, infrastructure/cloud design, API/integration design, UI/UX design, and technical specifications."
phase: 3
phase_name: "Architecture & Design"
owner: "Chief Technology Architect (CTA)"
secondary_owner: "Technical Lead"
participants: ["Tech Lead", "Security Architect", "DevOps", "Data Architect", "Cloud Architect", "SRE", "UX Lead", "Product Designer", "Users"]
entry_criteria: [
  "Functional requirements documented and approved",
  "Non-functional requirements defined",
  "Security requirements documented",
  "Compliance requirements identified",
  "Data requirements documented"
]
exit_criteria: [
  "System architecture approved by CTA",
  "Security architecture approved by CISO",
  "Data architecture approved and validated",
  "Infrastructure design approved and cost-validated",
  "API and integration design completed",
  "UI/UX design validated with users",
  "Technical specifications documented",
  "Threat modeling completed and reviewed",
  "Design review conducted with all stakeholders",
  "ADRs created",
  "Go/no-go decision to proceed to Phase 4"
]
estimated_duration: "14-19 weeks"
dependencies: ["phase_02_requirements_scope"]
outputs: [
  "System Architecture Document",
  "Security Architecture Document",
  "Data Architecture (ERD, Schemas)",
  "Cloud Infrastructure Design",
  "API Specifications (OpenAPI/Swagger)",
  "UI/UX Mockups and Prototypes",
  "Technical Specifications",
  "Architecture Decision Records (ADRs)",
  "Threat Models"
]
next_phase: "phase_04_development_planning"
---

# PHASE 3: ARCHITECTURE & DESIGN

## Overview

**Objective**: Design the system, security, data, and infrastructure

**Entry Point**: Approved Requirements from Phase 2
**Exit Point**: Approved Design

---

## Key Roles in This Phase

| Role | Responsibility |
|------|----------------|
| **CTA** | Owns overall architecture |
| **Security Architect** | Designs security architecture |
| **Data Architect** | Designs data architecture |
| **Cloud Architect** | Designs infrastructure |
| **UX Lead** | Designs UI/UX |
| **Tech Lead** | Implementation validation |

---

## Step 1: System Architecture Design

**Owner**: CTA / Solution Architect
**Participants**: Tech Lead, Security Architect, DevOps, Data Architect, Cloud Architect
**Timeline**: 3-4 weeks

### Tasks
- Define system architecture patterns (monolith, microservices, serverless)
- Design component architecture
- Define integration patterns (sync vs async)
- Design for scalability and performance
- Design for high availability
- Create Architecture Decision Records (ADRs)
- Document technical trade-offs

### Deliverables
- System architecture document
- Component diagrams (C4 model)
- Sequence diagrams
- Architecture Decision Records (ADRs)
- Technology stack definition
- Technical trade-offs analysis

### Approvals
- CTA: Own and approve architecture
- Security Architect: Security review
- DevOps: Operability review
- Cloud Architect: Infrastructure feasibility
- Tech Lead: Implementation feasibility

---

## Step 2: Security Architecture Design

**Owner**: Security Architect / Security Lead
**Participants**: CTA, CISO, Compliance Officer, DevOps
**Timeline**: 2-3 weeks

### Tasks
- Design security architecture (defense in depth)
- Design authentication and authorization (OAuth2, OIDC, SAML)
- Design encryption strategy (at rest: AES-256, in transit: TLS 1.3)
- Design network security (VPC, subnets, security groups, WAF)
- Design secrets management (HashiCorp Vault, AWS Secrets Manager)
- Design audit logging and monitoring
- Conduct threat modeling (STRIDE, PASTA, LINDDUN)
- Define security controls implementation

### Deliverables
- Security architecture document
- Authentication and authorization design
- Network security design
- Secrets management design
- Threat models
- Security controls matrix
- Security test plan

### Approvals
- Security Architect: Own security design
- CISO: Approve security posture
- CTA: Validate technical integration
- Compliance Officer: Validate compliance
- DevOps: Validate implementation feasibility

**Reference**: `../shared/security/SKILL.md`

---

## Step 3: Data Architecture Design

**Owner**: Data Architect / DBA
**Participants**: CTA, Business Analyst, Compliance Officer
**Timeline**: 2-3 weeks

### Tasks
- Design logical data model (ERD)
- Design physical data model
- Define database schemas (PostgreSQL recommended, MongoDB for flexibility, MySQL for traditional, Redis for caching)
- Design data integration patterns (ETL, ELT, CDC)
- Design data migration strategy
- Define data retention and archival
- Design backup and recovery (RPO/RTO)
- Define data security controls (encryption, masking)

### Deliverables
- Logical data model (ERD)
- Physical data model
- Database schema definitions
- Data integration design
- Data migration strategy
- Backup and recovery design
- Data security controls

### Approvals
- Data Architect: Own data design
- CTA: Validate architecture fit
- Security Architect: Validate security controls
- Compliance Officer: Validate compliance
- DBA: Validate implementation feasibility

---

## Step 4: Infrastructure and Cloud Design

**Owner**: Cloud Architect / DevOps Lead
**Participants**: CTA, Security Architect, SRE, Network Lead
**Timeline**: 3-4 weeks

### Tasks
- Design cloud infrastructure architecture (AWS: 30% market, Azure: 20%, GCP: 13%)
- Select cloud providers and services (AWS: most mature, Azure: enterprise/AI, GCP: data/analytics)
- Design network architecture (VPC, subnets, routing)
- Design high availability (multi-AZ, multi-region)
- Design disaster recovery strategy
- Design CI/CD pipeline architecture (GitHub Actions: most popular, GitLab CI: all-in-one)
- Design monitoring and observability (Grafana + Prometheus: open source standard, Datadog/New Relic: enterprise)
- Design cost optimization strategy
- Define Infrastructure as Code (IaC) approach (Terraform: industry standard, Pulumi: developer-friendly, Ansible: configuration)

### Deliverables
- Cloud architecture diagram
- Network architecture diagram
- Infrastructure design document
- Disaster recovery plan
- CI/CD pipeline design
- Monitoring and observability design
- Cost model and optimization plan
- IaC templates and standards

### Approvals
- Cloud Architect: Own infrastructure design
- CTA: Validate technical fit
- Security Architect: Validate security design
- SRE: Validate operability
- Finance: Validate cost model

---

## Step 5: API and Integration Design

**Owner**: CTA / Tech Lead
**Participants**: Security Architect, Data Architect
**Timeline**: 2 weeks

### Tasks
- Design API architecture (REST: default choice, GraphQL: complex data/mobile, gRPC: microservices/internal)
- Define API specifications (OpenAPI/Swagger)
- Design integration patterns
- Design event-driven architecture (Kafka: analytics/events, RabbitMQ: transactions/reliable, Redis: simple/pub-sub)
- Define API versioning strategy
- Design API security (OAuth 2.0 + OIDC, API keys, rate limiting)
- Define API documentation approach

### Deliverables
- API architecture document
- API specifications (OpenAPI/Swagger)
- Integration design document
- Event architecture design
- API security design
- API documentation template

### Approvals
- CTA: Own API design
- Tech Lead: Validate implementation
- Security Architect: Validate API security
- Data Architect: Validate data integration

---

## Step 6: User Interface (UI/UX) Design

**Owner**: UX Lead / Product Designer
**Participants**: Product Owner, Users, Tech Lead
**Timeline**: 3-4 weeks

### Tasks
- Conduct user research and testing
- Create user journey maps
- Design wireframes and mockups
- Design prototypes (Figma: market leader 2025, best collaboration; Sketch: Mac teams; Adobe XD: Creative Cloud)
- Define design system and components
- Conduct usability testing
- Create UI specifications

### Deliverables
- User research report
- User journey maps
- Wireframes and mockups
- Interactive prototypes
- Design system documentation
- UI specifications
- Usability test results

### Approvals
- UX Lead: Own design
- Product Owner: Validate user needs
- Tech Lead: Validate implementation
- Users: Validate through testing

---

## Step 7: Technical Specifications

**Owner**: Tech Lead / CTA
**Participants**: All technical leads
**Timeline**: 2 weeks

### Tasks
- Compile all technical designs
- Create technical specifications document
- Define development standards and guidelines
- Define coding standards
- Define testing strategy
- Define deployment strategy
- Create design review presentation

### Deliverables
- Technical specifications document
- Development standards and guidelines
- Coding standards document
- Testing strategy document
- Deployment strategy document
- Design review presentation

### Approvals
- CTA: Approve technical specifications
- Tech Lead: Validate implementation details
- Security Architect: Validate security included
- QA Lead: Validate testing strategy
- DevOps: Validate deployment strategy
- All stakeholders: Design review sign-off

---

## Quality Gates (Exit Criteria)

Before proceeding to Phase 4, ensure:

- ☐ System architecture approved by CTA
- ☐ Security architecture approved by CISO
- ☐ Data architecture approved and validated
- ☐ Infrastructure design approved and cost-validated
- ☐ API and integration design completed
- ☐ UI/UX design validated with users
- ☐ Technical specifications documented
- ☐ Threat modeling completed and reviewed
- ☐ Design review conducted with all stakeholders
- ☐ Architecture Decision Records (ADRs) created
- ☐ Go/no-go decision to proceed to Phase 4

---

## Architecture Decision Records (ADRs)

ADRs document significant architectural decisions:

| ADR ID | Title | Status | Date |
|--------|-------|--------|------|
| ADR-001 | Microservices Architecture | Accepted | 2025-01-15 |
| ADR-002 | PostgreSQL as Primary Database | Accepted | 2025-01-16 |
| ADR-003 | Kubernetes for Orchestration | Proposed | 2025-01-17 |

---

## Threat Modeling Methodologies

Use one or more methodologies:

- **STRIDE**: Spoofing, Tampering, Repudiation, Information Disclosure, Denial of Service, Elevation of Privilege
- **PASTA**: Process for Attack Simulation and Threat Analysis
- **LINDDUN**: Linkability, Identifiability, Non-repudiation, Detectability, Disclosure of Information, Unawareness, Non-compliance

---

## Templates and Examples

See `./templates/` for:
- System Architecture Template
- Security Architecture Template
- ADR Template
- Threat Modeling Template

See `./examples/` for:
- Sample Architecture Document
- Sample ADR

---

**Previous Phase**: `../phase_02_requirements_scope/SKILL.md`
**Next Phase**: `../phase_04_development_planning/SKILL.md`

---

**Review Completed By:** OCTALUME TEAM
**Date:** 2026-01-14
**Next Review Recommended:** After major framework updates or every 12 months
