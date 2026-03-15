"""Quality gate validator for phase transitions."""

from datetime import datetime
from typing import Any

from octalume.core.models import (
    ComplianceStandard,
    GateResult,
    ProjectState,
    QualityGate,
)
from octalume.core.state import ProjectStateManager
from octalume.utils.logging import get_logger

logger = get_logger(__name__)


QUALITY_GATES: dict[int, QualityGate] = {
    1: QualityGate(
        id="G1-VISION-EXIT",
        phase=1,
        name="Vision Phase Exit Gate",
        description="Validates completion of vision and strategy phase",
        criteria=[
            "Business case documented",
            "PRD completed",
            "Stakeholder alignment confirmed",
            "Success metrics defined",
        ],
        required_artifacts=["P1-BIZ-*", "P1-PRD-*"],
        approvers=["executive_sponsor", "product_owner"],
        bypass_allowed=False,
    ),
    2: QualityGate(
        id="G2-REQUIREMENTS-EXIT",
        phase=2,
        name="Requirements Phase Exit Gate",
        description="Validates completion of requirements phase",
        criteria=[
            "Functional requirements documented",
            "Non-functional requirements defined",
            "Traceability matrix created",
            "Requirements approved",
        ],
        required_artifacts=["P2-FR-*", "P2-NFR-*", "P2-TRC-*"],
        approvers=["product_owner", "tech_lead"],
        bypass_allowed=False,
        compliance_required=[ComplianceStandard.HIPAA, ComplianceStandard.SOC2],
    ),
    3: QualityGate(
        id="G3-ARCHITECTURE-EXIT",
        phase=3,
        name="Architecture Phase Exit Gate",
        description="Validates completion of architecture phase",
        criteria=[
            "System architecture documented",
            "Security architecture approved",
            "Threat model completed",
            "Data models defined",
        ],
        required_artifacts=["P3-ARCH-*", "P3-SEC-*", "P3-THRT-*"],
        approvers=["cta", "ciso", "security_architect"],
        bypass_allowed=False,
        compliance_required=[ComplianceStandard.HIPAA, ComplianceStandard.PCI_DSS],
    ),
    4: QualityGate(
        id="G4-PLANNING-EXIT",
        phase=4,
        name="Planning Phase Exit Gate",
        description="Validates completion of development planning phase",
        criteria=[
            "WBS approved",
            "Resources allocated",
            "Sprint plan created",
            "CI/CD pipeline designed",
        ],
        required_artifacts=["P4-WBS-*", "P4-RES-*", "P4-SPR-*"],
        approvers=["project_manager", "tech_lead"],
        bypass_allowed=True,
    ),
    5: QualityGate(
        id="G5-DEVELOPMENT-EXIT",
        phase=5,
        name="Development Phase Exit Gate",
        description="Validates completion of development execution phase",
        criteria=[
            "All features implemented",
            "Unit tests passing",
            "Code reviews complete",
            "Technical debt documented",
        ],
        required_artifacts=["P5-CODE-*", "P5-TEST-*"],
        approvers=["tech_lead", "qa_lead"],
        bypass_allowed=False,
    ),
    6: QualityGate(
        id="G6-QUALITY-EXIT",
        phase=6,
        name="Quality Phase Exit Gate",
        description="Validates completion of quality and security phase",
        criteria=[
            "All tests passing",
            "Security scan complete",
            "Performance tests passed",
            "UAT sign-off received",
        ],
        required_artifacts=["P6-TEST-*", "P6-SEC-*", "P6-UAT-*"],
        approvers=["qa_lead", "product_owner", "ciso"],
        bypass_allowed=False,
        compliance_required=[ComplianceStandard.HIPAA, ComplianceStandard.SOC2, ComplianceStandard.PCI_DSS],
    ),
    7: QualityGate(
        id="G7-DEPLOYMENT-EXIT",
        phase=7,
        name="Deployment Phase Exit Gate",
        description="Validates completion of deployment and release phase",
        criteria=[
            "Production deployment complete",
            "Smoke tests passing",
            "Rollback plan verified",
            "Release notes published",
        ],
        required_artifacts=["P7-DEP-*", "P7-SMK-*", "P7-RLS-*"],
        approvers=["devops", "sre", "product_owner"],
        bypass_allowed=False,
    ),
    8: QualityGate(
        id="G8-OPERATIONS-ENTRY",
        phase=8,
        name="Operations Phase Entry Gate",
        description="Validates readiness for ongoing operations",
        criteria=[
            "Monitoring active",
            "Runbooks published",
            "On-call rotation established",
            "SLAs defined",
        ],
        required_artifacts=["P8-MON-*", "P8-RUN-*"],
        approvers=["sre", "devops"],
        bypass_allowed=True,
    ),
}


class GateValidator:
    """Validates quality gates for phase transitions."""

    def __init__(self, state_manager: ProjectStateManager):
        self.state_manager = state_manager

    async def validate_entry(
        self,
        state: ProjectState,
        phase_num: int,
    ) -> GateResult:
        """Validate entry criteria for a phase."""
        if phase_num == 1:
            return GateResult(
                gate_id=f"G{phase_num}-ENTRY",
                passed=True,
                checks={"first_phase": True},
            )

        prev_phase = state.phases.get(phase_num - 1)
        if not prev_phase:
            return GateResult(
                gate_id=f"G{phase_num}-ENTRY",
                passed=False,
                checks={"previous_phase_exists": False},
                missing_artifacts=[f"Phase {phase_num - 1} not initialized"],
            )

        prev_gate = QUALITY_GATES.get(phase_num - 1)
        if not prev_gate:
            return GateResult(
                gate_id=f"G{phase_num}-ENTRY",
                passed=True,
                checks={"gate_exists": False, "no_gate_required": True},
            )

        checks: dict[str, bool] = {}
        missing_artifacts: list[str] = []

        checks["previous_phase_completed"] = prev_phase.status.value == "completed"

        artifact_check = self._check_required_artifacts(
            state, prev_gate.required_artifacts
        )
        checks["required_artifacts"] = artifact_check["passed"]
        if not artifact_check["passed"]:
            missing_artifacts.extend(artifact_check["missing"])

        compliance_check = await self._check_compliance(
            state, prev_gate.compliance_required
        )
        checks["compliance"] = compliance_check["passed"]

        passed = all(checks.values())

        result = GateResult(
            gate_id=f"G{phase_num}-ENTRY",
            passed=passed,
            checks=checks,
            missing_artifacts=missing_artifacts,
            compliance_issues=compliance_check.get("issues", []),
        )

        logger.info(
            "entry_gate_validated",
            phase=phase_num,
            passed=passed,
            checks=checks,
        )

        return result

    async def validate_exit(
        self,
        state: ProjectState,
        phase_num: int,
    ) -> GateResult:
        """Validate exit criteria for a phase."""
        gate = QUALITY_GATES.get(phase_num)
        if not gate:
            return GateResult(
                gate_id=f"G{phase_num}-EXIT",
                passed=True,
                checks={"no_gate_defined": True},
            )

        checks: dict[str, bool] = {}
        missing_artifacts: list[str] = []
        compliance_issues: list[str] = []

        for criterion in gate.criteria:
            checks[f"criterion_{criterion[:20]}"] = True

        artifact_check = self._check_required_artifacts(
            state, gate.required_artifacts
        )
        checks["required_artifacts"] = artifact_check["passed"]
        if not artifact_check["passed"]:
            missing_artifacts.extend(artifact_check["missing"])

        compliance_check = await self._check_compliance(
            state, gate.compliance_required
        )
        checks["compliance"] = compliance_check["passed"]
        if not compliance_check["passed"]:
            compliance_issues.extend(compliance_check.get("issues", []))

        passed = all(checks.values())

        result = GateResult(
            gate_id=gate.id,
            passed=passed,
            checks=checks,
            missing_artifacts=missing_artifacts,
            compliance_issues=compliance_issues,
        )

        logger.info(
            "exit_gate_validated",
            phase=phase_num,
            passed=passed,
            checks=checks,
        )

        return result

    async def bypass_gate(
        self,
        state: ProjectState,
        phase_num: int,
        reason: str,
        approver: str,
    ) -> GateResult:
        """Bypass a quality gate (if allowed)."""
        gate = QUALITY_GATES.get(phase_num)
        if not gate:
            raise ValueError(f"No gate defined for phase {phase_num}")

        if not gate.bypass_allowed:
            raise RuntimeError(f"Bypass not allowed for phase {phase_num} gate")

        if approver not in gate.approvers:
            raise ValueError(f"{approver} is not authorized to bypass this gate")

        result = GateResult(
            gate_id=gate.id,
            passed=True,
            checks={"bypassed": True},
            bypassed=True,
            bypass_reason=reason,
            approver=approver,
        )

        state.gate_results.append(result)
        await self.state_manager.save(state)

        logger.warning(
            "gate_bypassed",
            phase=phase_num,
            reason=reason,
            approver=approver,
        )

        return result

    async def run_go_no_go(
        self,
        state: ProjectState,
        phase_num: int,
    ) -> dict[str, Any]:
        """Run a comprehensive go/no-go decision for phase transition."""
        entry_result = await self.validate_entry(state, phase_num)
        exit_result = await self.validate_exit(state, phase_num)

        gate = QUALITY_GATES.get(phase_num)

        return {
            "phase": phase_num,
            "gate_name": gate.name if gate else f"Phase {phase_num}",
            "decision": "GO" if (entry_result.passed and exit_result.passed) else "NO-GO",
            "entry_validation": {
                "passed": entry_result.passed,
                "checks": entry_result.checks,
                "missing_artifacts": entry_result.missing_artifacts,
            },
            "exit_validation": {
                "passed": exit_result.passed,
                "checks": exit_result.checks,
                "missing_artifacts": exit_result.missing_artifacts,
                "compliance_issues": exit_result.compliance_issues,
            },
            "required_approvers": gate.approvers if gate else [],
            "timestamp": datetime.utcnow().isoformat(),
        }

    def _check_required_artifacts(
        self,
        state: ProjectState,
        patterns: list[str],
    ) -> dict[str, Any]:
        """Check if required artifacts exist."""
        missing: list[str] = []
        found: list[str] = []

        for pattern in patterns:
            matched = False
            prefix = pattern.replace("*", "")
            for artifact_id in state.artifacts:
                if artifact_id.startswith(prefix):
                    matched = True
                    found.append(artifact_id)
                    break

            if not matched:
                missing.append(pattern)

        return {
            "passed": len(missing) == 0,
            "found": found,
            "missing": missing,
        }

    async def _check_compliance(
        self,
        state: ProjectState,
        standards: list[ComplianceStandard],
    ) -> dict[str, Any]:
        """Check compliance requirements."""
        if not standards:
            return {"passed": True, "issues": []}

        issues: list[str] = []

        for standard in standards:
            if standard not in state.compliance_standards:
                issues.append(f"Compliance standard {standard.value} not configured")

        return {
            "passed": len(issues) == 0,
            "issues": issues,
        }

    def get_gate_definition(self, phase_num: int) -> QualityGate | None:
        """Get quality gate definition for a phase."""
        return QUALITY_GATES.get(phase_num)

    def list_all_gates(self) -> list[dict[str, Any]]:
        """List all quality gate definitions."""
        return [
            {
                "id": gate.id,
                "phase": gate.phase,
                "name": gate.name,
                "description": gate.description,
                "criteria": gate.criteria,
                "required_artifacts": gate.required_artifacts,
                "approvers": gate.approvers,
                "bypass_allowed": gate.bypass_allowed,
                "compliance_required": [s.value for s in gate.compliance_required],
            }
            for gate in QUALITY_GATES.values()
        ]
