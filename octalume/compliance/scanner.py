"""Compliance scanner for multiple standards."""

from datetime import datetime
from typing import Any

from octalume.core.models import ComplianceStandard, ProjectState
from octalume.utils.logging import get_logger

logger = get_logger(__name__)


class ComplianceScanner:
    """Scans project for compliance across multiple standards."""

    def __init__(self) -> None:
        self._scanners: dict[ComplianceStandard, Any] = {}

    async def scan(
        self,
        state: ProjectState,
        standards: list[ComplianceStandard],
        scope: str = "all",
    ) -> dict[str, Any]:
        """Run compliance scan for specified standards."""
        results = {}

        for standard in standards:
            scanner = self._get_scanner(standard)
            if scanner:
                result = await scanner.scan(state, scope)
                results[standard.value] = result

        return {
            "scan_id": f"scan-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}",
            "timestamp": datetime.utcnow().isoformat(),
            "scope": scope,
            "standards_scanned": [s.value for s in standards],
            "results": results,
            "summary": self._generate_summary(results),
        }

    async def generate_report(
        self,
        state: ProjectState,
        standard: ComplianceStandard,
        format: str = "json",
    ) -> dict[str, Any]:
        """Generate a detailed compliance report."""
        scanner = self._get_scanner(standard)

        if not scanner:
            return {
                "error": f"No scanner available for {standard.value}",
            }

        scan_result = await scanner.scan(state, "all")

        report = {
            "report_id": f"rpt-{standard.value}-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}",
            "standard": standard.value,
            "generated_at": datetime.utcnow().isoformat(),
            "project_name": state.name,
            "compliance_status": scan_result.get("status", "unknown"),
            "findings": scan_result.get("findings", []),
            "recommendations": scan_result.get("recommendations", []),
            "score": scan_result.get("score", 0),
        }

        if format == "markdown":
            report["content"] = self._to_markdown(report)
        elif format == "html":
            report["content"] = self._to_html(report)

        return report

    def _get_scanner(self, standard: ComplianceStandard) -> Any | None:
        """Get scanner instance for a compliance standard."""
        if standard not in self._scanners:
            if standard == ComplianceStandard.HIPAA:
                from octalume.compliance.hipaa import HIPAACompliance

                self._scanners[standard] = HIPAACompliance()
            elif standard == ComplianceStandard.SOC2:
                from octalume.compliance.soc2 import SOC2Compliance

                self._scanners[standard] = SOC2Compliance()
            elif standard == ComplianceStandard.PCI_DSS:
                from octalume.compliance.pci import PCICompliance

                self._scanners[standard] = PCICompliance()
            elif standard == ComplianceStandard.GDPR:
                from octalume.compliance.gdpr import GDPRCompliance

                self._scanners[standard] = GDPRCompliance()

        return self._scanners.get(standard)

    def _generate_summary(self, results: dict[str, Any]) -> dict[str, Any]:
        """Generate summary across all scanned standards."""
        total_findings = 0
        critical_findings = 0
        compliant_standards = 0

        for _standard, result in results.items():
            findings = result.get("findings", [])
            total_findings += len(findings)

            critical = [f for f in findings if f.get("severity") == "critical"]
            critical_findings += len(critical)

            if result.get("status") == "compliant":
                compliant_standards += 1

        return {
            "total_standards": len(results),
            "compliant_standards": compliant_standards,
            "total_findings": total_findings,
            "critical_findings": critical_findings,
            "overall_status": "compliant" if critical_findings == 0 else "non-compliant",
        }

    def _to_markdown(self, report: dict[str, Any]) -> str:
        """Convert report to markdown format."""
        lines = [
            f"# Compliance Report: {report['standard'].upper()}",
            "",
            f"**Report ID:** {report['report_id']}",
            f"**Generated:** {report['generated_at']}",
            f"**Status:** {report['compliance_status'].upper()}",
            f"**Score:** {report['score']}%",
            "",
            "## Findings",
            "",
        ]

        for finding in report.get("findings", []):
            severity = finding.get("severity", "info").upper()
            description = finding.get("description", "No description")
            lines.append(f"- **[{severity}]** {description}")

        if report.get("recommendations"):
            lines.extend(
                [
                    "",
                    "## Recommendations",
                    "",
                ]
            )
            for rec in report["recommendations"]:
                lines.append(f"- {rec}")

        return "\n".join(lines)

    def _to_html(self, report: dict[str, Any]) -> str:
        """Convert report to HTML format."""
        findings_html = ""
        for finding in report.get("findings", []):
            severity = finding.get("severity", "info")
            description = finding.get("description", "No description")
            findings_html += f'<li class="finding-{severity}">{description}</li>\n'

        return f"""<!DOCTYPE html>
<html>
<head>
    <title>Compliance Report: {report['standard'].upper()}</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; }}
        .status-compliant {{ color: green; }}
        .status-non-compliant {{ color: red; }}
        .finding-critical {{ color: red; font-weight: bold; }}
        .finding-high {{ color: orange; }}
        .finding-medium {{ color: yellow; }}
    </style>
</head>
<body>
    <h1>Compliance Report: {report['standard'].upper()}</h1>
    <p><strong>Report ID:</strong> {report['report_id']}</p>
    <p><strong>Generated:</strong> {report['generated_at']}</p>
    <p><strong>Status:</strong> <span class="status-{report['compliance_status']}">{report['compliance_status'].upper()}</span></p>
    <p><strong>Score:</strong> {report['score']}%</p>
    <h2>Findings</h2>
    <ul>
        {findings_html}
    </ul>
</body>
</html>"""
