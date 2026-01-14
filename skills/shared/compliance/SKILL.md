---
name: "compliance"
description: "Shared compliance and audit framework across all phases. Regulatory requirements, compliance matrix, audit readiness, documentation requirements, and gap analysis."
type: "shared"
used_by: ["all_phases"]
---

# COMPLIANCE FRAMEWORK - SHARED ACROSS ALL PHASES

This shared skill provides compliance and audit guidance that applies across all phases of the Unified Enterprise Lifecycle.

**Compliance First**: Compliance requirements identified early, not added later.

---

## COMMON REGULATORY FRAMEWORKS

### HIPAA (Health Insurance Portability and Accountability Act)
- **Applies to**: Healthcare PHI (Protected Health Information)
- **Key Requirements**:
  - Privacy Rule: PHI protection
  - Security Rule: Administrative, physical, technical safeguards
  - Breach Notification: Report breaches within 60 days
  - Minimum Necessary: Limit PHI access
- **Audits**: Annual HIPAA audits required

### SOC 2 (Service Organization Control 2)
- **Applies to**: Service organizations handling customer data
- **Key Requirements**:
  - Trust Services Criteria: Security, Availability, Privacy, Confidentiality
  - Control Implementation: Documented controls
  - Evidence Collection: Audit trail for all controls
  - Annual Audit: SOC 2 Type II audit
- **Audits**: Annual SOC 2 Type II audit required

### PCI DSS (Payment Card Industry Data Security Standard)
- **Applies to**: Payment card data handling
- **Key Requirements**:
  - 12 Requirements: Network security, data protection, vulnerability management, etc.
  - PCI Scans: Quarterly vulnerability scans
  - Annual ROV: Review of vulnerability scans
  - Annual Audit: PCI DSS audit
- **Audits**: Annual PCI DSS audit required

### SOX (Sarbanes-Oxley Act)
- **Applies to**: Public companies, financial reporting
- **Key Requirements**:
  - Section 404: Internal control over financial reporting
  - Section 302: Executive certification of financial reports
  - Segregation of Duties: Separate roles for financial processes
  - Audit Trail: Complete audit trail for financial transactions
- **Audits**: Quarterly SOX audits, annual audit

### GDPR (General Data Protection Regulation)
- **Applies to**: EU personal data
- **Key Requirements**:
  - Lawful Basis: Legal basis for data processing
  - Data Subject Rights: Access, rectification, erasure, portability
  - Data Protection: Data protection by design and default
  - Breach Notification: Report breaches within 72 hours
  - DPO: Data Protection Officer required
- **Audits**: Potential audits by data protection authorities

### DoD/ITAR (Department of Defense / International Traffic in Arms Regulations)
- **Applies to**: Defense contractors, controlled technical data
- **Key Requirements**:
  - CMMC: Cybersecurity Maturity Model Certification (Level 1-5)
  - ITAR: Control of defense articles and services
  - NIST 800-171: Protecting CUI (Controlled Unclassified Information)
  - DFARS: Defense Federal Acquisition Regulation Supplement
- **Audits**: CMMC assessment, DoD audits

---

## COMPLIANCE BY PHASE

### Phase 1: Vision & Strategy
**Compliance Activities**:
- Identify applicable regulations
- Conduct compliance gap analysis
- Define compliance requirements
- Estimate compliance costs

**Deliverables**:
- Applicable regulations identified
- Compliance gap analysis
- Compliance requirements documented
- Compliance budget estimate

**Owner**: Compliance Officer

---

### Phase 2: Requirements & Scope
**Compliance Activities**:
- Map regulatory requirements to technical requirements
- Define compliance requirements specification
- Define audit requirements
- Define documentation requirements
- Define data retention requirements
- Create compliance matrix

**Deliverables**:
- Compliance requirements specification
- Regulatory compliance matrix
- Audit requirements
- Documentation requirements list
- Data retention policies
- Compliance gap analysis

**Owner**: Compliance Officer / Audit Manager

---

### Phase 3: Architecture & Design
**Compliance Activities**:
- Design compliance controls into architecture
- Design audit trail capabilities
- Design data protection controls
- Design access controls (segregation of duties)
- Validate compliance requirements in design

**Deliverables**:
- Compliance controls in architecture
- Audit trail design
- Data protection controls design
- Access control design (RBAC, segregation of duties)
- Compliance validation report

**Owner**: Compliance Officer, Security Architect

---

### Phase 4: Development Planning
**Compliance Activities**:
- Plan compliance testing
- Plan audit readiness activities
- Plan documentation generation
- Plan compliance training
- Define compliance metrics

**Deliverables**:
- Compliance testing plan
- Audit readiness plan
- Documentation plan
- Training plan
- Compliance metrics

**Owner**: Compliance Officer

---

### Phase 5: Development Execution
**Compliance Activities**:
- Implement compliance controls
- Generate audit trail logs
- Implement access controls
- Implement data protection
- Document compliance features

**Deliverables**:
- Implemented compliance controls
- Audit trail logging
- Access control implementation
- Data protection implementation
- Compliance documentation

**Owner**: Developers, Tech Lead, Security Architect

---

### Phase 6: Quality & Security Validation
**Compliance Activities**:
- Test compliance controls
- Validate audit trail completeness
- Validate access controls
- Validate data protection
- Conduct compliance gap analysis
- Prepare for external audit

**Deliverables**:
- Compliance control testing results
- Audit trail verification
- Access control validation
- Data protection validation
- Compliance gap analysis
- Audit readiness report

**Owner**: Compliance Officer, QA Lead

---

### Phase 7: Deployment & Release
**Compliance Activities**:
- Validate compliance in production
- Configure compliance monitoring
- Validate audit trail in production
- Conduct pre-production compliance check
- Define compliance rollback triggers

**Deliverables**:
- Production compliance validation
- Compliance monitoring configuration
- Audit trail validation
- Pre-production compliance check

**Owner**: Compliance Officer, SRE

---

### Phase 8: Operations & Maintenance
**Compliance Activities**:
- Maintain compliance documentation
- Monitor compliance controls
- Conduct internal compliance audits
- Prepare for and coordinate external audits
- Manage compliance exceptions
- Update compliance documentation

**Deliverables**:
- Compliance documentation (maintained)
- Internal audit reports
- External audit coordination
- Compliance status reports
- Remediation plans
- Compliance metrics

**Owner**: Compliance Officer / Audit Manager

---

## COMPLIANCE MATRIX

Use this matrix to map requirements to controls:

| Regulation | Requirement | Control | Status | Evidence Location |
|------------|------------|---------|--------|-------------------|
| HIPAA | Access Control | RBAC, MFA | Implemented | `docs/access-control.md` |
| SOC 2 | Change Management | Change approvals | In Progress | `docs/change-log.md` |
| PCI DSS | Encryption | TLS 1.3, AES-256 | Planned | `docs/encryption.md` |
| SOX | Audit Trail | Logging all changes | Implemented | `logs/audit-trail.log` |
| GDPR | Data Subject Rights | Data export, deletion | Implemented | `docs/dsr-process.md` |

---

## AUDIT READINESS CHECKLIST

### Pre-Audit Preparation
- ☐ Compliance documentation complete and up-to-date
- ☐ Audit trail complete and verifiable
- ☐ All compliance controls implemented and tested
- ☐ Evidence collection procedures defined
- ☐ Audit response team assigned
- ☐ Audit workspace prepared

### During Audit
- ☐ Provide evidence requested by auditors
- ☐ Facilitate auditor interviews
- ☐ Document audit findings
- ☐ Track audit progress

### Post-Audit
- ☐ Address audit findings
- ☐ Implement remediation plans
- ☐ Follow up on auditor recommendations
- ☐ Update compliance documentation

---

## DOCUMENTATION REQUIREMENTS

### Common Documentation
| Regulation | Documentation Required | Retention |
|------------|----------------------|-----------|
| **HIPAA** | Policies, procedures, risk assessments, BAAs | 6 years |
| **SOC 2** | Policies, procedures, evidence, reports | 7 years |
| **PCI DSS** | Policies, procedures, evidence, scan reports | Retention varies |
| **SOX** | Control documentation, evidence, reports | 7 years |
| **GDPR** | Records of consent, processing activities, DSR responses | Varies |
| **DoD/ITAR** | CMMC documentation, ITAR documentation | Varies |

### Evidence Collection
- **Automated Evidence**: Collect evidence through automation (logs, metrics)
- **Manual Evidence**: Collect evidence manually (policies, procedures)
- **Evidence Storage**: Store evidence securely with access controls
- **Evidence Retention**: Retain evidence per regulatory requirements

---

## COMPLIANCE TOOLS

| Category | Tools |
|----------|-------|
| **Compliance Management** | Vanta, Drata, Secureframe, Aiera |
| **Audit Management** | AuditBoard, Galvanize (HighBond) |
| **Documentation** | Confluence, Notion, SharePoint |
| **Policy Management** | LogicGate, OneTrust, Convercent |
| **Risk Management** | RSA Archer, ServiceNow, Resolver GRC |
| **Evidence Collection** | Automated scripts, manual collection |

---

## COMPLIANCE METRICS

Track these metrics for compliance:

| Metric | Target | Purpose |
|--------|--------|---------|
| **Control Implementation** | 100% | All controls implemented |
| **Evidence Availability** | 100% | All evidence available |
| **Audit Findings** | Zero findings | No audit findings |
| **Compliance Training** | 100% completed | All staff trained |
| **Policy Acknowledgment** | 100% signed | All policies acknowledged |
| **Exception Handling** | <5 exceptions | Minimal exceptions |

---

## COMPLIANCE ROLES AND RESPONSIBILITIES

### Compliance Officer
- Owns compliance framework
- Conducts internal audits
- Coordinates external audits
- Maintains compliance documentation

### CISO
- Approves security compliance
- Validates security controls
- Reports on security posture

### Legal
- Reviews compliance position
- Provides legal guidance
- Validates regulatory interpretations

### Executive Sponsor
- Approves compliance approach
- Provides compliance budget
- Champions compliance culture

---

## TEMPLATES

See `./templates/` for:
- Compliance Matrix Template
- Audit Readiness Checklist Template
- Compliance Gap Analysis Template
- Remediation Plan Template

---

## BEST PRACTICES

1. **Identify Early**: Identify applicable regulations in Phase 1
2. **Design In**: Design compliance controls into architecture
3. **Document**: Maintain complete and accurate documentation
4. **Test**: Test compliance controls regularly
5. **Monitor**: Monitor compliance metrics continuously
6. **Train**: Provide compliance training to all staff
7. **Audit Ready**: Maintain audit readiness at all times

---

**This shared skill is referenced by all phase skills.**
