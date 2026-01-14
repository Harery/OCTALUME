---
name: "security"
description: "Shared security framework across all phases. Security principles, requirements, architecture, testing, operations, and compliance integration."
type: "shared"
used_by: ["all_phases"]
---

# SECURITY FRAMEWORK - SHARED ACROSS ALL PHASES

This shared skill provides security guidance that applies across all phases of the Unified Enterprise Lifecycle.

**Security First**: Security is integrated from Phase 1, not added later.

---

## SECURITY PRINCIPLES

### CIA Triad
- **Confidentiality**: Data accessible only to authorized users
- **Integrity**: Data accuracy and completeness maintained
- **Availability**: System and data available when needed

### Defense in Depth
- Multiple layers of security controls
- No single point of failure
- Compromise resilience

### Least Privilege
- Minimum access required for role
- Time-bound access
- Regular access reviews

---

## SECURITY BY PHASE

### Phase 1: Vision & Strategy
**Security Activities**:
- Identify data types (PII, financial, health)
- Identify regulatory requirements (HIPAA, SOC 2, PCI DSS, GDPR)
- Initial security risk assessment
- Security considerations in business case

**Deliverables**:
- Security considerations document
- Regulatory requirements identified
- Initial risk assessment

**Owner**: Security Lead

---

### Phase 2: Requirements & Scope
**Security Activities**:
- Define security requirements (CIA triad)
- Define authentication requirements (MFA, SSO, OIDC)
- Define authorization requirements (RBAC, ABAC)
- Define data protection requirements
- Define audit and logging requirements
- Identify applicable security standards (NIST, ISO 27001, OWASP)
- Create security risk assessment

**Deliverables**:
- Security requirements specification
- Authentication and authorization design
- Data protection requirements
- Audit and logging requirements
- Security risk assessment

**Owner**: Security Architect

---

### Phase 3: Architecture & Design
**Security Activities**:
- Design security architecture (defense in depth)
- Design authentication and authorization
- Design encryption strategy (at rest, in transit)
- Design network security (VPC, subnets, firewalls, WAF)
- Design secrets management
- Design audit logging and monitoring
- Conduct threat modeling (STRIDE, PASTA, LINDDUN)
- Define security controls implementation

**Deliverables**:
- Security architecture document
- Authentication and authorization design
- Network security design
- Secrets management design
- Threat models
- Security controls matrix
- Security test plan

**Owner**: Security Architect

---

### Phase 4: Development Planning
**Security Activities**:
- Define security controls implementation plan
- Define security testing approach (SAST, DAST, SCA)
- Define vulnerability management process
- Integrate security into CI/CD pipeline
- Define security documentation requirements

**Deliverables**:
- Security controls implementation plan
- Security testing approach
- Vulnerability management process
- CI/CD security integration plan

**Owner**: Security Lead

---

### Phase 5: Development Execution (Shift Left)
**Security Activities**:
- Conduct security code reviews
- Use Static Application Security Testing (SAST)
- Use Software Composition Analysis (SCA)
- Conduct threat modeling sessions
- Provide secure coding guidance
- Review secrets management
- Validate security controls implementation

**Deliverables**:
- Security code review reports
- SAST scan results
- SCA scan results (dependency vulnerabilities)
- Threat model updates
- Secure coding guidelines
- Security exception requests (if needed)

**Owner**: Security Lead / Security Architect

---

### Phase 6: Quality & Security Validation
**Security Activities**:
- Conduct comprehensive security testing
- Conduct penetration testing (internal, external)
- Validate all security controls
- Conduct vulnerability assessment
- Validate compliance requirements
- Conduct security regression testing
- Create security test report

**Deliverables**:
- Security test plan
- SAST scan results
- DAST scan results
- SCA scan results
- Penetration test report
- Vulnerability assessment
- Security sign-off

**Owner**: Security Lead / Security Architect

---

### Phase 7: Deployment & Release
**Security Activities**:
- Validate security controls in production
- Conduct pre-deployment security scan
- Validate secrets management in production
- Configure security monitoring and alerting
- Validate compliance controls in production
- Define security rollback triggers

**Deliverables**:
- Pre-deployment security validation
- Production security validation
- Security monitoring configuration
- Security rollback triggers

**Owner**: Security Lead / DevOps

---

### Phase 8: Operations & Maintenance
**Security Activities**:
- Monitor security alerts and incidents
- Conduct security log analysis
- Manage vulnerabilities (scanning, patching)
- Conduct security assessments
- Manage access controls
- Update security documentation
- Coordinate incident response

**Deliverables**:
- Security monitoring dashboard
- Vulnerability assessments
- Security patch reports
- Access review reports
- Security metrics
- Incident response reports

**Owner**: Security Lead / SRE

---

## SECURITY CONTROLS

### Authentication Controls
- Multi-factor authentication (MFA)
- Single sign-on (SSO)
- OAuth 2.0 / OIDC / SAML
- Password policies (complexity, rotation)
- Session management (timeout, revocation)

### Authorization Controls
- Role-Based Access Control (RBAC)
- Attribute-Based Access Control (ABAC)
- Principle of least privilege
- Access review and certification
- Separation of duties

### Data Protection Controls
- Encryption at rest (AES-256)
- Encryption in transit (TLS 1.3)
- Data classification (public, internal, confidential, restricted)
- Data masking and redaction
- Key management (KMS, HashiCorp Vault)

### Network Security Controls
- Virtual Private Cloud (VPC)
- Security groups and firewalls
- Web Application Firewall (WAF)
- DDoS protection
- Network segmentation
- Intrusion detection/prevention (IDS/IPS)

### Application Security Controls
- Input validation
- Output encoding
- SQL injection prevention
- XSS prevention
- CSRF protection
- Secure headers (CSP, HSTS, X-Frame-Options)

### Logging and Monitoring Controls
- Audit logging (all access, changes)
- Security event logging
- Log aggregation (ELK, Splunk)
- SIEM (Security Information and Event Management)
- Alerting and notification
- Log retention and archival

---

## THREAT MODELING METHODOLOGIES

### STRIDE
- **S**poofing: False identity
- **T**ampering: Data modification
- **R**epudiation: Denying actions
- **I**nformation Disclosure: Data exposure
- **D**enial of Service: Availability impact
- **E**levation of Privilege: Unauthorized access

### PASTA (Process for Attack Simulation and Threat Analysis)
1. Define objectives
2. Define technical scope
3. Application decomposition
4. Threat analysis
5. Vulnerability and weakness analysis
6. Attack modeling

### LINDDUN
- **L**inkability
- **I**dentifiability
- **N**on-repudiation
- **D**etectability
- **D**isclosure of Information
- **U**nawareness
- **N**on-compliance

---

## SECURITY TESTING

### Static Application Security Testing (SAST)
- Tools: SonarQube, Fortify, Checkmarx, Veracode
- Scans source code for vulnerabilities
- Integrated into CI/CD pipeline
- Runs on every commit

### Dynamic Application Security Testing (DAST)
- Tools: OWASP ZAP, Burp Suite
- Tests running application
- Identifies runtime vulnerabilities
- Integrated into testing phase

### Software Composition Analysis (SCA)
- Tools: Snyk, Dependabot, WhiteSource
- Scans dependencies for vulnerabilities
- Checks license compliance
- Integrated into CI/CD pipeline

### Penetration Testing
- Internal penetration testing
- External penetration testing
- Conducted annually or after major changes
- Third-party or internal team

---

## SECURITY STANDARDS AND COMPLIANCE

### Common Standards
- **NIST Cybersecurity Framework**: US standard
- **ISO 27001**: International standard
- **OWASP**: Application security
- **CIS Controls**: Security best practices

### Regulatory Compliance
- **HIPAA**: Healthcare data
- **SOC 2**: Service organizations
- **PCI DSS**: Payment card data
- **GDPR**: EU data protection
- **SOX**: Financial reporting
- **DoD/ITAR**: Defense data

---

## SECURITY INCIDENT RESPONSE

### Incident Severity Levels
| Severity | Description | Response Time |
|----------|-------------|---------------|
| **SEV-1** | Critical (breach, data loss) | Immediate |
| **SEV-2** | High (system compromise) | 1 hour |
| **SEV-3** | Medium (potential impact) | 4 hours |
| **SEV-4** | Low (minor issue) | 1 business day |

### Incident Response Process
1. **Detect**: Identify security incident
2. **Contain**: Limit incident impact
3. **Eradicate**: Remove threat
4. **Recover**: Restore normal operations
5. **Lessons Learned**: Post-incident review

---

## SECURITY TOOLS

| Category | Tools |
|----------|-------|
| **SAST** | SonarQube, Fortify, Checkmarx |
| **DAST** | OWASP ZAP, Burp Suite |
| **SCA** | Snyk, Dependabot, WhiteSource |
| **Container Security** | Trivy, Clair, Aqua |
| **WAF** | CloudFlare, AWS WAF, ModSecurity |
| **SIEM** | Splunk, ELK, Sumo Logic |
| **Secrets Management** | HashiCorp Vault, AWS Secrets Manager |

---

## TEMPLATES

See `./templates/` for:
- Security Requirements Template
- Threat Modeling Template
- Security Test Plan Template
- Incident Response Template

---

**This shared skill is referenced by all phase skills.**
