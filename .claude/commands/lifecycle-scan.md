---
name: "lifecycle_scan"
description: "Run security and compliance scans"
---

# Run Security and Compliance Scans

Run comprehensive security and compliance scans for $ARGUMENTS.

## Scan Types

### 1. SAST (Static Application Security Testing)

Scan source code for security vulnerabilities:

```bash
# Using Snyk
snyk test
snyk monitor

# Using SonarQube
sonar-scanner

# Using Semgrep
semgrep --config=auto src/
```

**Output**: Security vulnerabilities in source code with severity ratings

### 2. SCA (Software Composition Analysis)

Scan dependencies for known vulnerabilities:

```bash
# Using Snyk
snyk test --dev

# Using Dependabot
dependabot check

# Using npm audit
npm audit

# Using pip-audit
pip-audit
```

**Output**: Vulnerable dependencies with upgrade recommendations

### 3. DAST (Dynamic Application Security Testing)

Scan running application for runtime vulnerabilities:

```bash
# Using OWASP ZAP
zap-cli quick-scan --self-contained http://localhost:3000
zap-cli active-scan http://localhost:3000

# Using Burp Suite
burp-scan http://localhost:3000
```

**Output**: Runtime vulnerabilities with exploit details

### 4. Container Security

Scan Docker images for vulnerabilities:

```bash
# Using Trivy
trivy image myapp:latest

# Using Clair
clair-scanner myapp:latest

# Using Snyk
snyk container test myapp:latest
```

**Output**: Container image vulnerabilities

### 5. Infrastructure as Code Security

Scan Terraform/CloudFormation for security issues:

```bash
# Using tfsec
tfscan .

# Using checkov
checkov -d .

# Using Snyk Infrastructure
snyk iac test .
```

**Output**: Infrastructure security misconfigurations

### 6. Compliance Scans

Check compliance with regulations:

```bash
# HIPAA compliance check
python scripts/compliance/hipaa_check.py

# SOC 2 compliance check
python scripts/compliance/soc2_check.py

# PCI DSS compliance check
python scripts/compliance/pci_dss_check.py

# GDPR compliance check
python scripts/compliance/gdpr_check.py
```

**Output**: Compliance status with gap analysis

## Scan Workflow

1. **Start Application**: Ensure application is running:
   ```bash
   source scripts/init.sh
   ```

2. **Run SAST Scan**: Scan source code:
   ```bash
   snyk test --json > reports/sast-report.json
   semgrep --json --output=reports/semgrep-report.json src/
   ```

3. **Run SCA Scan**: Scan dependencies:
   ```bash
   snyk test --dev --json > reports/sca-report.json
   npm audit --json > reports/npm-audit.json
   ```

4. **Run DAST Scan**: Scan running application:
   ```bash
   zap-cli quick-scan --self-contained --output-file=reports/zap-report.html http://localhost:3000
   ```

5. **Run Container Scan**: Scan Docker image:
   ```bash
   trivy image --format json --output=reports/trivy-report.json myapp:latest
   ```

6. **Run IaC Scan**: Scan infrastructure:
   ```bash
   tfscan --format json --output=reports/tfsec-report.json
   checkov -o json --output=reports/checkov-report.json
   ```

7. **Run Compliance Checks**: Check compliance:
   ```bash
   python scripts/compliance/all_checks.py --output=reports/compliance-report.json
   ```

8. **Aggregate Results**: Combine all reports:
   ```bash
   python scripts/aggregate_reports.py reports/ > reports/summary-report.md
   ```

9. **Create Findings**: Document all findings:
   ```bash
   python scripts/create_findings.py reports/ > artifacts/P6-SEC-XXX.md
   ```

10. **Prioritize Remediation**: Prioritize by severity:
    - P1-Critical: Fix within 4 hours
    - P2-High: Fix within 24 hours
    - P3-Medium: Fix within 1 week
    - P4-Low: Fix in next release

## Output Format

```json
{
  "scan_date": "2025-01-11T00:00:00Z",
  "scan_type": ["SAST", "SCA", "DAST", "Container", "IaC", "Compliance"],
  "summary": {
    "total_findings": 50,
    "critical": 2,
    "high": 8,
    "medium": 20,
    "low": 20
  },
  "findings": [
    {
      "id": "SEC-001",
      "type": "SAST",
      "severity": "critical",
      "title": "SQL Injection Vulnerability",
      "description": "...",
      "file": "src/auth/login.ts",
      "line": 42,
      "remediation": "..."
    }
  ],
  "compliance": {
    "HIPAA": "pass",
    "SOC 2": "pass",
    "PCI DSS": "fail",
    "GDPR": "pass"
  },
  "recommendations": [
    "Fix critical findings immediately",
    "Update vulnerable dependencies",
    "Fix infrastructure misconfigurations"
  ]
}
```

## Remediation

For each finding:

1. **Assess Impact**: Determine the security impact
2. **Plan Fix**: Plan the remediation approach
3. **Implement Fix**: Write the fix
4. **Test Fix**: Verify the fix works
5. **Re-scan**: Verify vulnerability is resolved
6. **Document**: Document the remediation

## Important

- Run all scans before each release
- Fix critical findings immediately
- Document all findings and remediation
- Maintain scan history
- Track security metrics

---

**Review Completed By:** OCTALUME TEAM
**Date:** 2026-01-13
**Next Review Recommended:** After major framework updates or every 6 months
