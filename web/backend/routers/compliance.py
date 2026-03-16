"""Compliance API router."""

from typing import Any

from fastapi import APIRouter, Depends, HTTPException

from octalume.compliance.scanner import ComplianceScanner
from octalume.core.models import ComplianceStandard
from octalume.core.state import ProjectStateManager
from web.backend.dependencies import get_state_manager

router = APIRouter()
scanner = ComplianceScanner()


@router.get("/standards")
async def list_standards() -> dict[str, Any]:
    return {
        "standards": [
            {
                "id": "hipaa",
                "name": "HIPAA",
                "description": "Health Insurance Portability and Accountability Act",
            },
            {"id": "soc2", "name": "SOC 2", "description": "Service Organization Control 2"},
            {
                "id": "pci_dss",
                "name": "PCI DSS",
                "description": "Payment Card Industry Data Security Standard",
            },
            {"id": "gdpr", "name": "GDPR", "description": "General Data Protection Regulation"},
            {"id": "sox", "name": "SOX", "description": "Sarbanes-Oxley Act"},
            {"id": "dod_itar", "name": "DoD/ITAR", "description": "Defense regulations"},
        ]
    }


@router.post("/scan")
async def run_compliance_scan(
    standards: list[str] | None = None,
    scope: str = "all",
    state_manager: ProjectStateManager = Depends(get_state_manager),
) -> dict[str, Any]:
    state = await state_manager.load()
    if not state:
        raise HTTPException(status_code=404, detail="Project not found")

    if not standards:
        standards = [s.value for s in state.compliance_standards]

    if not standards:
        raise HTTPException(status_code=400, detail="No compliance standards configured")

    try:
        standard_enums = [ComplianceStandard(s) for s in standards]
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid standard: {e}")

    result = await scanner.scan(
        state=state,
        standards=standard_enums,
        scope=scope,
    )

    return result


@router.get("/report/{standard}")
async def get_compliance_report(
    standard: str,
    format: str = "json",
    state_manager: ProjectStateManager = Depends(get_state_manager),
) -> dict[str, Any]:
    state = await state_manager.load()
    if not state:
        raise HTTPException(status_code=404, detail="Project not found")

    try:
        standard_enum = ComplianceStandard(standard)
    except ValueError:
        raise HTTPException(status_code=400, detail=f"Invalid standard: {standard}")

    report = await scanner.generate_report(
        state=state,
        standard=standard_enum,
        format=format,
    )

    return report


@router.post("/configure")
async def configure_compliance(
    standards: list[str],
    state_manager: ProjectStateManager = Depends(get_state_manager),
) -> dict[str, Any]:
    state = await state_manager.load()
    if not state:
        raise HTTPException(status_code=404, detail="Project not found")

    try:
        standard_enums = [ComplianceStandard(s) for s in standards]
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Invalid standard: {e}")

    state.compliance_standards = standard_enums
    await state_manager.save(state)

    return {
        "success": True,
        "configured_standards": [s.value for s in state.compliance_standards],
    }


@router.get("/status")
async def get_compliance_status(
    state_manager: ProjectStateManager = Depends(get_state_manager),
) -> dict[str, Any]:
    state = await state_manager.load()
    if not state:
        raise HTTPException(status_code=404, detail="Project not found")

    return {
        "configured_standards": [s.value for s in state.compliance_standards],
        "gate_results": [
            {
                "gate_id": gr.gate_id,
                "passed": gr.passed,
                "compliance_issues": gr.compliance_issues,
            }
            for gr in state.gate_results
            if gr.compliance_issues
        ],
    }
