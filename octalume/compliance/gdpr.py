"""GDPR compliance module."""

from typing import Any

from octalume.core.models import ProjectState

GDPR_PRINCIPLES = {
    "lawfulness_fairness_transparency": {
        "description": "Article 5(1)(a): Lawfulness, fairness and transparency",
        "checks": ["legal_basis_documented", "processing_transparency", "fair_processing"],
    },
    "purpose_limitation": {
        "description": "Article 5(1)(b): Purpose limitation",
        "checks": ["purposes_defined", "purpose_documentation", "purpose_limitation_controls"],
    },
    "data_minimization": {
        "description": "Article 5(1)(c): Data minimization",
        "checks": ["minimal_data_collection", "data_necessity_assessment"],
    },
    "accuracy": {
        "description": "Article 5(1)(d): Accuracy",
        "checks": ["data_accuracy_measures", "correction_procedures"],
    },
    "storage_limitation": {
        "description": "Article 5(1)(e): Storage limitation",
        "checks": ["retention_periods", "deletion_procedures", "retention_policy"],
    },
    "integrity_confidentiality": {
        "description": "Article 5(1)(f): Integrity and confidentiality",
        "checks": ["security_measures", "encryption", "access_controls"],
    },
    "data_subject_rights": {
        "description": "Articles 12-22: Data subject rights",
        "checks": [
            "access_right_procedure",
            "rectification_right",
            "erasure_right",
            "portability_right",
            "objection_right",
        ],
    },
    "accountability": {
        "description": "Article 5(2): Accountability",
        "checks": ["privacy_by_design", "dpia_process", "records_of_processing", "dpo_appointed"],
    },
    "data_breach": {
        "description": "Articles 33-34: Data breach notification",
        "checks": ["breach_detection", "notification_procedure_72h", "communication_to_subjects"],
    },
}


class GDPRCompliance:
    """GDPR compliance scanner and validator."""

    async def scan(
        self,
        state: ProjectState,
        scope: str = "all",
    ) -> dict[str, Any]:
        """Scan project for GDPR compliance."""
        findings = []
        passed_checks = 0
        total_checks = 0

        for principle, details in GDPR_PRINCIPLES.items():
            for check in details["checks"]:
                total_checks += 1
                result = await self._check_requirement(state, check)

                if result["passed"]:
                    passed_checks += 1
                else:
                    findings.append(
                        {
                            "principle": principle,
                            "check": check,
                            "description": details["description"],
                            "severity": self._get_severity(check),
                            "remediation": result.get("remediation", ""),
                        }
                    )

        score = int((passed_checks / total_checks) * 100) if total_checks > 0 else 0
        status = "compliant" if score >= 100 else "partial" if score >= 70 else "non-compliant"

        return {
            "standard": "gdpr",
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
        """Check a specific GDPR requirement."""
        pattern_map = {
            "legal_basis_documented": "P2-REQ-",
            "processing_transparency": "P2-REQ-",
            "purposes_defined": "P2-REQ-",
            "minimal_data_collection": "P2-NFR-",
            "data_accuracy_measures": "P6-TEST-",
            "retention_periods": "P2-NFR-",
            "deletion_procedures": "P8-RUN-",
            "security_measures": "P3-SEC-",
            "encryption": "P3-SEC-",
            "access_controls": "P3-SEC-",
            "access_right_procedure": "P5-CODE-",
            "rectification_right": "P5-CODE-",
            "erasure_right": "P5-CODE-",
            "portability_right": "P5-CODE-",
            "privacy_by_design": "P3-ARCH-",
            "dpia_process": "P3-SEC-",
            "records_of_processing": "P8-MON-",
            "breach_detection": "P6-SEC-",
            "notification_procedure_72h": "P8-RUN-",
        }

        prefix = pattern_map.get(check, "P2-REQ-")

        for artifact_id in state.artifacts:
            if artifact_id.startswith(prefix):
                return {"passed": True}

        return {"passed": False, "remediation": f"Implement: {check}"}

    def _get_severity(self, check: str) -> str:
        """Get severity for a GDPR check."""
        critical = ["breach_detection", "notification_procedure_72h", "erasure_right"]
        high = ["legal_basis_documented", "privacy_by_design", "security_measures"]

        if check in critical:
            return "critical"
        elif check in high:
            return "high"
        return "medium"

    def _generate_recommendations(
        self,
        findings: list[dict[str, Any]],
    ) -> list[str]:
        """Generate GDPR recommendations."""
        return [
            f"[{f['severity'].upper()}] {f['check']}: {f.get('remediation', '')}"
            for f in sorted(
                findings, key=lambda x: ["critical", "high", "medium"].index(x["severity"])
            )
        ][:10]
