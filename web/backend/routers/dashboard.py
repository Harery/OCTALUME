"""Dashboard API router."""

from typing import Any

from fastapi import APIRouter, Depends, HTTPException

from octalume.core.state import ProjectStateManager
from octalume.core.memory import MemoryBank
from web.backend.main import get_state_manager, get_memory

router = APIRouter()


@router.get("/summary")
async def get_dashboard_summary(
    state_manager: ProjectStateManager = Depends(get_state_manager),
) -> dict[str, Any]:
    state = await state_manager.load()
    if not state:
        return {
            "initialized": False,
            "message": "No project initialized. Use 'octalume init' to create one.",
        }

    summary = await state_manager.get_summary(state)

    summary["initialized"] = True
    summary["progress_percentage"] = 0

    completed_phases = sum(
        1 for p in state.phases.values() if p.status.value == "completed"
    )
    if len(state.phases) > 0:
        summary["progress_percentage"] = int((completed_phases / len(state.phases)) * 100)

    return summary


@router.get("/timeline")
async def get_timeline(
    state_manager: ProjectStateManager = Depends(get_state_manager),
) -> dict[str, Any]:
    state = await state_manager.load()
    if not state:
        raise HTTPException(status_code=404, detail="Project not found")

    timeline = []
    for phase_num in sorted(state.phases.keys()):
        phase = state.phases[phase_num]
        timeline.append({
            "phase": phase_num,
            "name": phase.name,
            "status": phase.status.value,
            "started_at": phase.started_at.isoformat() if phase.started_at else None,
            "completed_at": phase.completed_at.isoformat() if phase.completed_at else None,
            "duration_days": phase.duration_estimate_days,
            "artifacts_count": len(phase.artifacts),
            "owner": phase.owner,
        })

    return {"timeline": timeline}


@router.get("/metrics")
async def get_metrics(
    state_manager: ProjectStateManager = Depends(get_state_manager),
    memory: MemoryBank = Depends(get_memory),
) -> dict[str, Any]:
    state = await state_manager.load()
    if not state:
        raise HTTPException(status_code=404, detail="Project not found")

    memory_stats = memory.get_statistics()

    total_artifacts = len(state.artifacts)
    total_agents = len(state.agents)
    active_agents = sum(
        1 for a in state.agents.values() if a.status.value == "running"
    )

    gates_passed = sum(1 for gr in state.gate_results if gr.passed)
    gates_failed = len(state.gate_results) - gates_passed

    return {
        "artifacts": {
            "total": total_artifacts,
            "by_phase": {
                str(p): len([a for a in state.artifacts.values() if a.phase == p])
                for p in range(1, 9)
            },
        },
        "agents": {
            "total": total_agents,
            "active": active_agents,
        },
        "gates": {
            "total": len(state.gate_results),
            "passed": gates_passed,
            "failed": gates_failed,
        },
        "memory": memory_stats,
        "compliance_standards": [s.value for s in state.compliance_standards],
    }


@router.get("/activity")
async def get_recent_activity(
    limit: int = 20,
    memory: MemoryBank = Depends(get_memory),
) -> dict[str, Any]:
    traces = memory.get_traces(limit=limit)

    progress = memory.query(category="progress", limit=limit)

    return {
        "traces": traces,
        "recent_progress": progress,
    }
