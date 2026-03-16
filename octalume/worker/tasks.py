"""Background task definitions for Celery."""

from datetime import datetime, timedelta
from typing import Any

from octalume.utils.logging import get_logger
from octalume.worker.celery_app import celery_app, run_async

logger = get_logger(__name__)


@celery_app.task(bind=True, name="octalume.worker.tasks.run_compliance_scan")
def run_compliance_scan(
    self,
    project_id: str,
    standards: list[str],
    scope: str = "all",
) -> dict[str, Any]:
    logger.info(
        "compliance_scan_started",
        task_id=self.request.id,
        project_id=project_id,
        standards=standards,
    )

    self.update_state(
        state="PROGRESS",
        meta={"status": "starting", "progress": 0},
    )

    try:

        from octalume.compliance.scanner import ComplianceScanner
        from octalume.core.models import ComplianceStandard
        from octalume.core.state import ProjectStateManager

        manager = ProjectStateManager()
        state = run_async(manager.load())

        if state is None:
            return {"success": False, "error": "Project not found"}

        scanner = ComplianceScanner()
        standards_enum = [ComplianceStandard(s) for s in standards]

        self.update_state(
            state="PROGRESS",
            meta={"status": "scanning", "progress": 30},
        )

        result = run_async(
            scanner.scan(
                state=state,
                standards=standards_enum,
                scope=scope,
            )
        )

        self.update_state(
            state="PROGRESS",
            meta={"status": "generating_report", "progress": 80},
        )

        logger.info(
            "compliance_scan_completed",
            task_id=self.request.id,
            project_id=project_id,
        )

        return {
            "success": True,
            "scan_id": f"scan-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}",
            "project_id": project_id,
            "standards": standards,
            "results": result,
        }

    except Exception as e:
        logger.error(
            "compliance_scan_failed",
            task_id=self.request.id,
            error=str(e),
        )
        return {"success": False, "error": str(e)}


@celery_app.task(bind=True, name="octalume.worker.tasks.run_health_check")
def run_health_check(self, agent_ids: list[str] | None = None) -> dict[str, Any]:
    logger.info("health_check_started", task_id=self.request.id)

    try:
        from octalume.core.orchestrator import AgentOrchestrator
        from octalume.core.state import ProjectStateManager

        manager = ProjectStateManager()
        state = run_async(manager.load())

        if state is None:
            return {"success": False, "error": "No project state"}

        orchestrator = AgentOrchestrator(manager)
        health = run_async(orchestrator.health_check(state))

        return {
            "success": True,
            "timestamp": datetime.utcnow().isoformat(),
            "health": health,
        }

    except Exception as e:
        logger.error("health_check_failed", error=str(e))
        return {"success": False, "error": str(e)}


@celery_app.task(bind=True, name="octalume.worker.tasks.cleanup_expired_data")
def cleanup_expired_data(self, days_old: int = 30) -> dict[str, Any]:
    logger.info("cleanup_started", task_id=self.request.id, days_old=days_old)

    try:
        from pathlib import Path

        from octalume.core.memory import MemoryBank

        memory = MemoryBank(Path(".octalume/memory"))
        cutoff = datetime.utcnow() - timedelta(days=days_old)

        cleaned = 0
        traces = memory.get_traces(limit=10000)

        for trace in traces:
            trace_time = datetime.fromisoformat(trace.get("timestamp", ""))
            if trace_time < cutoff:
                cleaned += 1

        logger.info("cleanup_completed", task_id=self.request.id, cleaned=cleaned)

        return {
            "success": True,
            "cleaned_items": cleaned,
            "cutoff_date": cutoff.isoformat(),
        }

    except Exception as e:
        logger.error("cleanup_failed", error=str(e))
        return {"success": False, "error": str(e)}


@celery_app.task(bind=True, name="octalume.worker.tasks.generate_compliance_report")
def generate_compliance_report(
    self,
    project_id: str,
    standard: str,
    report_format: str = "json",
) -> dict[str, Any]:
    logger.info(
        "report_generation_started",
        task_id=self.request.id,
        project_id=project_id,
        standard=standard,
    )

    try:
        from octalume.compliance.scanner import ComplianceScanner
        from octalume.core.models import ComplianceStandard
        from octalume.core.state import ProjectStateManager

        manager = ProjectStateManager()
        state = run_async(manager.load())

        if state is None:
            return {"success": False, "error": "Project not found"}

        scanner = ComplianceScanner()
        report = run_async(
            scanner.generate_report(
                state=state,
                standard=ComplianceStandard(standard),
                format=report_format,
            )
        )

        return {
            "success": True,
            "report": report,
            "format": report_format,
        }

    except Exception as e:
        logger.error("report_generation_failed", error=str(e))
        return {"success": False, "error": str(e)}
