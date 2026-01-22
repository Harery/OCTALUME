# Requirements Traceability Matrix (RTM) Template

**Document ID:** P2-TRACE-{XXX}  
**Version:** 1.0  
**Status:** Draft | In Review | Approved  
**Author:** {Author Name}  
**Date:** {YYYY-MM-DD}

---

## 1. Document Control

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | {Date} | {Author} | Initial matrix |

---

## 2. Purpose

This Requirements Traceability Matrix (RTM) provides bidirectional traceability from business needs through implementation and testing, ensuring complete coverage and impact analysis capability.

---

## 3. Traceability Chain

```
Business Need → PRD Feature → Requirement → Design → Code → Test → Deployment
     ↑              ↑             ↑          ↑        ↑      ↑         ↑
   P1-BN-XXX   P1-VISION-XXX  P2-REQ-XXX  P3-ARCH  Code   TC-XXX   Deploy
```

---

## 4. Forward Traceability Matrix

### 4.1 Business Need to Requirements

| Business Need ID | Business Need | PRD Feature | Requirement IDs | Priority |
|------------------|---------------|-------------|-----------------|----------|
| BN-001 | {Need description} | P1-VISION-001 §3.1 | UR-001, UR-002 | Must |
| BN-002 | {Need description} | P1-VISION-001 §3.2 | UR-003, UR-004 | Should |
| BN-003 | {Need description} | P1-VISION-001 §3.3 | UR-005 | Could |

### 4.2 Requirements to Design

| Requirement ID | Requirement | Design Component | Architecture Section |
|----------------|-------------|------------------|---------------------|
| UR-001 | {Requirement} | {Component} | P3-ARCH-001 §4.1 |
| UR-002 | {Requirement} | {Component} | P3-ARCH-001 §4.2 |
| SR-001 | {Requirement} | {Component} | P3-ARCH-001 §5.1 |

### 4.3 Requirements to Test Cases

| Requirement ID | Requirement | Test Case IDs | Test Type |
|----------------|-------------|---------------|-----------|
| UR-001 | {Requirement} | TC-001, TC-002 | Functional |
| UR-002 | {Requirement} | TC-003 | Functional |
| NFR-PERF-001 | {Requirement} | TC-PERF-001 | Performance |
| NFR-SEC-001 | {Requirement} | TC-SEC-001 | Security |

---

## 5. Backward Traceability Matrix

### 5.1 Test Cases to Requirements

| Test Case ID | Test Description | Requirement IDs | Status |
|--------------|------------------|-----------------|--------|
| TC-001 | {Test description} | UR-001 | Not Run |
| TC-002 | {Test description} | UR-001, UR-002 | Not Run |
| TC-003 | {Test description} | UR-002 | Not Run |

### 5.2 Code Modules to Requirements

| Module/Component | File Path | Requirement IDs | Coverage |
|------------------|-----------|-----------------|----------|
| {Module name} | src/{path} | UR-001, UR-002 | 100% |
| {Module name} | src/{path} | UR-003 | 80% |

---

## 6. Complete Traceability View

| BN ID | PRD Ref | Req ID | Design Ref | Code Module | Test Cases | Deploy Config | Status |
|-------|---------|--------|------------|-------------|------------|---------------|--------|
| BN-001 | P1-V-001 §3.1 | UR-001 | P3-A-001 §4.1 | auth-module | TC-001, TC-002 | auth.yaml | ⬜ Not Started |
| BN-001 | P1-V-001 §3.1 | UR-002 | P3-A-001 §4.2 | auth-module | TC-003 | auth.yaml | ⬜ Not Started |
| BN-002 | P1-V-001 §3.2 | UR-003 | P3-A-001 §5.1 | user-module | TC-004, TC-005 | user.yaml | ⬜ Not Started |

**Status Legend:**
- ⬜ Not Started
- 🔄 In Progress
- ✅ Complete
- ❌ Blocked
- ⚠️ At Risk

---

## 7. Coverage Analysis

### 7.1 Requirements Coverage

| Category | Total | Covered | Untested | Coverage % |
|----------|-------|---------|----------|------------|
| User Requirements | {X} | {Y} | {Z} | {%} |
| System Requirements | {X} | {Y} | {Z} | {%} |
| NFR - Performance | {X} | {Y} | {Z} | {%} |
| NFR - Security | {X} | {Y} | {Z} | {%} |
| NFR - Other | {X} | {Y} | {Z} | {%} |
| **Total** | **{X}** | **{Y}** | **{Z}** | **{%}** |

### 7.2 Test Coverage

| Test Type | Planned | Executed | Passed | Failed | Blocked |
|-----------|---------|----------|--------|--------|---------|
| Unit | {X} | {Y} | {Z} | {A} | {B} |
| Integration | {X} | {Y} | {Z} | {A} | {B} |
| System | {X} | {Y} | {Z} | {A} | {B} |
| UAT | {X} | {Y} | {Z} | {A} | {B} |
| Performance | {X} | {Y} | {Z} | {A} | {B} |
| Security | {X} | {Y} | {Z} | {A} | {B} |

---

## 8. Gap Analysis

### 8.1 Untraceable Requirements

| Requirement ID | Issue | Action Required |
|----------------|-------|-----------------|
| {ID} | No design mapping | Create design spec |
| {ID} | No test case | Create test case |

### 8.2 Orphan Items

| Item Type | Item ID | Description | Action |
|-----------|---------|-------------|--------|
| Test Case | TC-XXX | No linked requirement | Review and link or remove |
| Code Module | {Module} | No linked requirement | Review for removal |

---

## 9. Change Impact Analysis

### 9.1 Impact Template

When a requirement changes, use this to assess impact:

| Changed Item | {Requirement ID} |
|--------------|------------------|
| **Business Needs Affected** | {List} |
| **Design Components Affected** | {List} |
| **Code Modules Affected** | {List} |
| **Test Cases Affected** | {List} |
| **Deployment Configs Affected** | {List} |
| **Estimated Effort** | {Hours/Days} |
| **Risk Level** | {High/Medium/Low} |

---

## 10. Approval Sign-off

| Role | Name | Signature | Date |
|------|------|-----------|------|
| Product Owner | | | |
| Technical Architect | | | |
| QA Lead | | | |
| Security Lead | | | |

---

**Document End**
