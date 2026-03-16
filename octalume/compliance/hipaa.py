"""HIPAA compliance module."""

from typing import Any

from octalume.core.models import ProjectState
from octalume.utils.logging import get_logger

logger = get_logger(__name__)


HIPAA_REQUIREMENTS = {
    "privacy_rule": {
        "description": "Privacy Rule - Protected Health Information (PHI)",
        "checks": [
            "phi_identification_documented",
            "minimum_necessary_standard_implemented",
            "patient_rights_documented",
            "disclosure_tracking_enabled",
        ],
    },
    "security_rule": {
        "description": "Security Rule - Administrative, Physical, Technical Safeguards",
        "checks": [
            "access_controls_implemented",
            "audit_controls_enabled",
            "integrity_controls_implemented",
            "transmission_security_enabled",
            "encryption_at_rest",
            "encryption_in_transit",
        ],
    },
    "breach_notification": {
        "description": "Breach Notification Rule",
        "checks": [
            "breach_detection_process",
            "notification_procedures",
            "incident_response_plan",
        ],
    },
    "enforcement_rule": {
        "description": "Enforcement Rule - Compliance and Penalties",
        "checks": [
            "compliance_officer_designated",
            "training_program_documented",
            "policy_review_schedule",
        ],
    },
}


class HIPAACompliance:
    """HIPAA compliance scanner and validator."""

    async def scan(
        self,
        state: ProjectState,
        scope: str = "all",
    ) -> dict[str, Any]:
        """Scan project for HIPAA compliance."""
        findings = []
        passed_checks = 0
        total_checks = 0

        for rule_id, rule in HIPAA_REQUIREMENTS.items():
            for check in rule["checks"]:
                total_checks += 1
                result = await self._check_requirement(state, check)

                if result["passed"]:
                    passed_checks += 1
                else:
                    findings.append(
                        {
                            "rule": rule_id,
                            "check": check,
                            "description": rule["description"],
                            "severity": self._get_severity(check),
                            "remediation": result.get("remediation", "Address this requirement"),
                        }
                    )

        score = int((passed_checks / total_checks) * 100) if total_checks > 0 else 0
        status = "compliant" if score >= 100 else "non-compliant"

        return {
            "standard": "hipaa",
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
        """Check a specific HIPAA requirement."""
        required_artifacts = {
            "phi_identification_documented": ["P2-REQ-*", "P3-SEC-*"],
            "minimum_necessary_standard_implemented": ["P3-SEC-*"],
            "patient_rights_documented": ["P2-REQ-*"],
            "disclosure_tracking_enabled": ["P3-SEC-*", "P8-MON-*"],
            "access_controls_implemented": ["P3-SEC-*"],
            "audit_controls_enabled": ["P3-SEC-*", "P8-MON-*"],
            "integrity_controls_implemented": ["P3-SEC-*"],
            "transmission_security_enabled": ["P3-SEC-*"],
            "encryption_at_rest": ["P3-SEC-*"],
            "encryption_in_transit": ["P3-SEC-*"],
            "breach_detection_process": ["P6-SEC-*", "P8-RUN-*"],
            "notification_procedures": ["P8-RUN-*"],
            "incident_response_plan": ["P8-RUN-*"],
            "compliance_officer_designated": ["P1-PRD-*"],
            "training_program_documented": ["P4-RES-*"],
            "policy_review_schedule": ["P8-RUN-*"],
        }

        patterns = required_artifacts.get(check, [])

        for pattern in patterns:
            prefix = pattern.replace("*", "")
            for artifact_id in state.artifacts:
                if artifact_id.startswith(prefix):
                    return {"passed": True}

        return {
            "passed": False,
            "remediation": f"Create artifact matching pattern: {patterns[0] if patterns else 'N/A'}",
        }

    def _get_severity(self, check: str) -> str:
        """Get severity level for a check."""
        critical_checks = [
            "encryption_at_rest",
            "encryption_in_transit",
            "access_controls_implemented",
            "audit_controls_enabled",
        ]

        high_checks = [
            "breach_detection_process",
            "incident_response_plan",
            "phi_identification_documented",
        ]

        if check in critical_checks:
            return "critical"
        elif check in high_checks:
            return "high"
        else:
            return "medium"

    def _generate_recommendations(
        self,
        findings: list[dict[str, Any]],
    ) -> list[str]:
        """Generate remediation recommendations."""
        recommendations = []

        for finding in findings:
            if finding["severity"] == "critical":
                recommendations.append(
                    f"CRITICAL: {finding['check']} - {finding.get('remediation', '')}"
                )

        for finding in findings:
            if finding["severity"] == "high":
                recommendations.append(
                    f"HIGH: {finding['check']} - {finding.get('remediation', '')}"
                )

        return recommendations[:10]
