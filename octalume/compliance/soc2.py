"""SOC 2 compliance module."""

from typing import Any

from octalume.core.models import ProjectState
from octalume.utils.logging import get_logger

logger = get_logger(__name__)


SOC2_TRUST_SERVICES = {
    "security": {
        "description": "Security (Common Criteria)",
        "checks": [
            "access_control_policy",
            "risk_assessment_documented",
            "security_incident_response",
            "change_management_process",
            "vulnerability_management",
            "logging_monitoring_enabled",
        ],
    },
    "availability": {
        "description": "Availability",
        "checks": [
            "capacity_management",
            "disaster_recovery_plan",
            "backup_procedures",
            "service_level_agreements",
        ],
    },
    "processing_integrity": {
        "description": "Processing Integrity",
        "checks": [
            "data_validation_controls",
            "error_handling_procedures",
            "processing_monitoring",
        ],
    },
    "confidentiality": {
        "description": "Confidentiality",
        "checks": [
            "data_classification_policy",
            "confidentiality_agreements",
            "encryption_standards",
        ],
    },
    "privacy": {
        "description": "Privacy",
        "checks": [
            "privacy_policy",
            "consent_management",
            "data_retention_policy",
            "data_subject_rights",
        ],
    },
}


class SOC2Compliance:
    """SOC 2 compliance scanner and validator."""

    async def scan(
        self,
        state: ProjectState,
        scope: str = "all",
    ) -> dict[str, Any]:
        """Scan project for SOC 2 compliance."""
        findings = []
        passed_checks = 0
        total_checks = 0

        for principle, requirements in SOC2_TRUST_SERVICES.items():
            for check in requirements["checks"]:
                total_checks += 1
                result = await self._check_requirement(state, check)

                if result["passed"]:
                    passed_checks += 1
                else:
                    findings.append({
                        "principle": principle,
                        "check": check,
                        "description": requirements["description"],
                        "severity": self._get_severity(check),
                        "remediation": result.get("remediation", ""),
                    })

        score = int((passed_checks / total_checks) * 100) if total_checks > 0 else 0
        status = "compliant" if score >= 100 else "partial" if score >= 70 else "non-compliant"

        return {
            "standard": "soc2",
            "type": "Type II",
            "status": status,
            "score": score,
            "passed_checks": passed_checks,
            "total_checks": total_checks,
            "findings": findings,
            "recommendations": self._generate_recommendations(findings),
        }

    async def _check_requirement(
        self,
        state: ProjectState,
        check: str,
    ) -> dict[str, Any]:
        """Check a specific SOC 2 requirement."""
        required_patterns = {
            "access_control_policy": ["P3-SEC-*", "P2-NFR-*"],
            "risk_assessment_documented": ["P1-BIZ-*", "P3-THRT-*"],
            "security_incident_response": ["P8-RUN-*", "P6-SEC-*"],
            "change_management_process": ["P4-WBS-*", "P7-DEP-*"],
            "vulnerability_management": ["P6-SEC-*", "P8-MON-*"],
            "logging_monitoring_enabled": ["P3-SEC-*", "P8-MON-*"],
            "capacity_management": ["P3-ARCH-*", "P4-RES-*"],
            "disaster_recovery_plan": ["P3-ARCH-*", "P8-RUN-*"],
            "backup_procedures": ["P7-DEP-*", "P8-RUN-*"],
            "service_level_agreements": ["P1-PRD-*", "P8-RUN-*"],
            "data_validation_controls": ["P5-TEST-*", "P6-TEST-*"],
            "error_handling_procedures": ["P5-CODE-*", "P8-RUN-*"],
            "processing_monitoring": ["P8-MON-*"],
            "data_classification_policy": ["P2-NFR-*", "P3-SEC-*"],
            "confidentiality_agreements": ["P1-PRD-*", "P4-RES-*"],
            "encryption_standards": ["P3-SEC-*"],
            "privacy_policy": ["P1-PRD-*", "P2-REQ-*"],
            "consent_management": ["P3-ARCH-*", "P5-CODE-*"],
            "data_retention_policy": ["P2-NFR-*", "P3-ARCH-*"],
            "data_subject_rights": ["P2-REQ-*", "P5-CODE-*"],
        }

        patterns = required_patterns.get(check, [])

        for pattern in patterns:
            prefix = pattern.replace("*", "")
            for artifact_id in state.artifacts:
                if artifact_id.startswith(prefix):
                    return {"passed": True}

        return {
            "passed": False,
            "remediation": f"Create artifact for: {check}",
        }

    def _get_severity(self, check: str) -> str:
        """Get severity for a SOC 2 check."""
        critical = ["access_control_policy", "security_incident_response", "vulnerability_management"]
        high = ["risk_assessment_documented", "disaster_recovery_plan", "encryption_standards"]

        if check in critical:
            return "critical"
        elif check in high:
            return "high"
        else:
            return "medium"

    def _generate_recommendations(
        self,
        findings: list[dict[str, Any]],
    ) -> list[str]:
        """Generate SOC 2 recommendations."""
        return [
            f"[{f['severity'].upper()}] {f['check']}: {f.get('remediation', 'Address this control')}"
            for f in sorted(findings, key=lambda x: ["critical", "high", "medium"].index(x["severity"]))
        ][:10]
