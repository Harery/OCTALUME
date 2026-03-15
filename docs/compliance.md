# Compliance

OCTALUME provides built-in compliance support for major regulatory standards.

## Supported Standards

| Standard | Description | Controls |
|----------|-------------|----------|
| HIPAA | Healthcare data protection | Privacy, Security, Breach rules |
| SOC 2 | Service organization controls | Security, Availability, Confidentiality |
| PCI DSS | Payment card security | 12 requirements |
| GDPR | EU data protection | Data subject rights, processing |
| SOX | Financial controls | Internal controls, audit |
| DoD/ITAR | Defense requirements | Export control, security |

---

## Configuration

### Enable Compliance Standards

```bash
octalume init my-app --compliance hipaa soc2
```

### Update Compliance

```bash
octalume scan --configure hipaa pci gdpr
```

### Python API

```python
from octalume.core.state import ProjectStateManager
from octalume.core.models import ComplianceStandard

manager = ProjectStateManager()
state = await manager.create(
    name="healthcare-app",
    compliance_standards=["hipaa", "soc2"]
)

# Or update existing project
state.compliance_standards = [
    ComplianceStandard.HIPAA,
    ComplianceStandard.SOC2,
    ComplianceStandard.GDPR
]
await manager.save(state)
```

---

## Compliance Scanning

### CLI

```bash
# Scan all configured standards
octalume scan

# Scan specific standards
octalume scan --standard hipaa soc2

# Scope the scan
octalume scan --scope artifacts

# Generate report
octalume scan --report markdown > compliance-report.md
```

### Python API

```python
from octalume.compliance.scanner import ComplianceScanner
from octalume.core.models import ComplianceStandard

scanner = ComplianceScanner()

# Run scan
result = await scanner.scan(
    state=state,
    standards=[ComplianceStandard.HIPAA, ComplianceStandard.SOC2],
    scope="all"  # all, artifacts, processes, documentation
)

# Result structure:
{
    "scan_id": "scan-20260315-001",
    "timestamp": "2026-03-15T10:00:00Z",
    "standards": {
        "hipaa": {
            "compliant": false,
            "score": 0.75,
            "findings": [
                {
                    "control": "164.312(a)(1)",
                    "name": "Access Control",
                    "status": "pass",
                    "evidence": "P2-DOC-003"
                },
                {
                    "control": "164.312(b)",
                    "name": "Audit Controls",
                    "status": "fail",
                    "description": "Missing audit log configuration"
                }
            ]
        },
        "soc2": {
            "compliant": true,
            "score": 0.92
        }
    }
}

# Generate report
report = await scanner.generate_report(
    state=state,
    standard=ComplianceStandard.HIPAA,
    format="markdown"  # json, markdown, html
)
```

---

## Standard Details

### HIPAA (Health Insurance Portability and Accountability Act)

**Applicable to:** Healthcare organizations, health plans, clearinghouses

**Key Controls:**
- Privacy Rule (164.500-534)
- Security Rule (164.302-318)
- Breach Notification Rule (164.400-414)

**Required Artifacts:**
- Privacy Policy
- Security Risk Assessment
- Business Associate Agreements
- Access Control Documentation
- Audit Log Configuration
- Incident Response Plan

**Scanning:**
```python
result = await scanner.scan(state, standards=[ComplianceStandard.HIPAA])
```

---

### SOC 2 (Service Organization Control 2)

**Applicable to:** SaaS providers, service organizations

**Trust Service Criteria:**
- Security (Common Criteria)
- Availability
- Confidentiality
- Processing Integrity
- Privacy

**Required Artifacts:**
- System Description
- Risk Assessment
- Control Matrix
- Penetration Test Results
- Incident Response Plan
- Change Management Process

**Scanning:**
```python
result = await scanner.scan(state, standards=[ComplianceStandard.SOC2])
```

---

### PCI DSS (Payment Card Industry Data Security Standard)

**Applicable to:** Organizations handling payment cards

**12 Requirements:**
1. Install and maintain firewall
2. Do not use vendor defaults
3. Protect stored cardholder data
4. Encrypt transmission
5. Use anti-virus
6. Develop secure systems
7. Restrict access by need-to-know
8. Identify and authenticate access
9. Restrict physical access
10. Track and monitor access
11. Test security systems
12. Maintain information security policy

**Required Artifacts:**
- Network Diagram
- Data Flow Diagram
- Vulnerability Scan Results
- Penetration Test Report
- Access Control Matrix
- Security Policy

**Scanning:**
```python
result = await scanner.scan(state, standards=[ComplianceStandard.PCI_DSS])
```

---

### GDPR (General Data Protection Regulation)

**Applicable to:** Organizations processing EU residents' data

**Key Requirements:**
- Lawful basis for processing
- Data subject rights (access, erasure, portability)
- Privacy by design
- Data protection impact assessments
- Breach notification (72 hours)
- Data processing records

**Required Artifacts:**
- Privacy Policy
- Data Processing Records
- Consent Management
- Data Subject Rights Procedures
- DPA (Data Protection Impact Assessment)
- Breach Notification Procedure

**Scanning:**
```python
result = await scanner.scan(state, standards=[ComplianceStandard.GDPR])
```

---

### SOX (Sarbanes-Oxley Act)

**Applicable to:** Public companies

**Key Sections:**
- Section 302: Corporate Responsibility
- Section 404: Internal Controls
- Section 409: Real-time Disclosure

**Required Artifacts:**
- Internal Control Documentation
- Access Control Matrix
- Change Management Process
- Audit Trail
- Segregation of Duties

**Scanning:**
```python
result = await scanner.scan(state, standards=[ComplianceStandard.SOX])
```

---

### DoD/ITAR (Defense/International Traffic in Arms Regulations)

**Applicable to:** Defense contractors, manufacturers

**Key Requirements:**
- Export control compliance
- Security clearance requirements
- Controlled access environments
- Incident reporting

**Required Artifacts:**
- Export Control Plan
- Access Control Matrix
- Security Incident Procedures
- Training Records

**Scanning:**
```python
result = await scanner.scan(state, standards=[ComplianceStandard.DOD_ITAR])
```

---

## Compliance in Phases

### Phase 2: Requirements
- Identify compliance requirements
- Document regulatory constraints
- Define security requirements

### Phase 3: Architecture
- Design security controls
- Perform threat modeling
- Document compliance architecture

### Phase 6: Quality
- Run compliance tests
- Validate control effectiveness
- Generate compliance reports

### Phase 8: Operations
- Maintain audit logs
- Monitor compliance drift
- Prepare for audits

---

## Artifact Tagging

Tag artifacts for compliance traceability:

```bash
octalume artifact create \
  --phase 3 \
  --type design \
  --name "Security Architecture" \
  --tags hipaa soc2 pci
```

```python
from octalume.core.models import Artifact, ArtifactType, ComplianceStandard

artifact = Artifact(
    id="P3-DSN-001",
    phase=3,
    name="Security Architecture",
    artifact_type=ArtifactType.DESIGN,
    compliance_tags=[
        ComplianceStandard.HIPAA,
        ComplianceStandard.SOC2,
        ComplianceStandard.PCI_DSS
    ]
)
```

---

## MCP Integration

```json
{
  "name": "lifecycle_compliance_scan",
  "arguments": {
    "standards": ["hipaa", "soc2"],
    "scope": "all"
  }
}
```

```json
{
  "name": "lifecycle_compliance_report",
  "arguments": {
    "standard": "hipaa",
    "format": "markdown"
  }
}
```

```json
{
  "name": "lifecycle_compliance_configure",
  "arguments": {
    "standards": ["hipaa", "soc2", "gdpr"]
  }
}
```

---

## Compliance Reports

### JSON Format

```json
{
  "standard": "hipaa",
  "compliant": false,
  "score": 0.75,
  "findings": [...]
}
```

### Markdown Format

```markdown
# HIPAA Compliance Report

**Generated:** 2026-03-15
**Score:** 75%
**Status:** Non-Compliant

## Summary
3 of 4 controls passed.

## Findings

### ✅ 164.312(a) - Access Control
Status: PASS
Evidence: P2-DOC-003

### ❌ 164.312(b) - Audit Controls
Status: FAIL
Description: Missing audit log configuration
Recommendation: Enable audit logging for all data access
```

### HTML Format

Full HTML report suitable for executive review.
