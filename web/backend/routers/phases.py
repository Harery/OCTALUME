"""Phase management API router."""

from typing import Any

from fastapi import APIRouter, Depends, HTTPException

from octalume.core.engine import PhaseEngine
from octalume.core.state import ProjectStateManager
from web.backend.main import get_engine, get_state_manager

router = APIRouter()


@router.get("/")
async def list_phases(
    state_manager: ProjectStateManager = Depends(get_state_manager),
) -> dict[str, Any]:
    state = await state_manager.load()
    if not state:
        raise HTTPException(status_code=404, detail="Project not found")

    phases = []
    for phase_num in sorted(state.phases.keys()):
        phase = state.phases[phase_num]
        phases.append({
            "number": phase.number,
            "name": phase.name,
            "description": phase.description,
            "status": phase.status.value,
            "owner": phase.owner,
            "artifacts_count": len(phase.artifacts),
            "started_at": phase.started_at.isoformat() if phase.started_at else None,
            "completed_at": phase.completed_at.isoformat() if phase.completed_at else None,
        })

    return {
        "current_phase": state.current_phase,
        "phase_status": state.phase_status.value,
        "phases": phases,
    }


@router.get("/{phase_number}")
async def get_phase(
    phase_number: int,
    engine: PhaseEngine = Depends(get_engine),
) -> dict[str, Any]:
    if phase_number < 1 or phase_number > 8:
        raise HTTPException(status_code=400, detail="Phase must be 1-8")

    state_manager = engine.state_manager
    state = await state_manager.load()
    if not state:
        raise HTTPException(status_code=404, detail="Project not found")

    return await engine.get_phase_status(state, phase_number)


@router.post("/{phase_number}/start")
async def start_phase(
    phase_number: int,
    engine: PhaseEngine = Depends(get_engine),
) -> dict[str, Any]:
    if phase_number < 1 or phase_number > 8:
        raise HTTPException(status_code=400, detail="Phase must be 1-8")

    state_manager = engine.state_manager
    state = await state_manager.load()
    if not state:
        raise HTTPException(status_code=404, detail="Project not found")

    try:
        state = await engine.start_phase(state, phase_number)
        phase = state.phases[phase_number]
        return {
            "success": True,
            "phase": phase.model_dump(),
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/{phase_number}/complete")
async def complete_phase(
    phase_number: int,
    engine: PhaseEngine = Depends(get_engine),
) -> dict[str, Any]:
    if phase_number < 1 or phase_number > 8:
        raise HTTPException(status_code=400, detail="Phase must be 1-8")

    state_manager = engine.state_manager
    state = await state_manager.load()
    if not state:
        raise HTTPException(status_code=404, detail="Project not found")

    try:
        state, gate_result = await engine.complete_phase(state, phase_number)
        return {
            "success": gate_result.passed,
            "phase": state.phases[phase_number].model_dump(),
            "gate_result": gate_result.model_dump(),
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/{phase_number}/transition")
async def transition_phase(
    phase_number: int,
    engine: PhaseEngine = Depends(get_engine),
) -> dict[str, Any]:
    if phase_number < 1 or phase_number > 7:
        raise HTTPException(status_code=400, detail="Can only transition from phases 1-7")

    state_manager = engine.state_manager
    state = await state_manager.load()
    if not state:
        raise HTTPException(status_code=404, detail="Project not found")

    try:
        state, gate_result = await engine.transition_phase(
            state, phase_number, phase_number + 1
        )
        return {
            "success": gate_result.passed,
            "current_phase": state.current_phase,
            "gate_result": gate_result.model_dump(),
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{phase_number}/gate")
async def get_phase_gate(
    phase_number: int,
    engine: PhaseEngine = Depends(get_engine),
) -> dict[str, Any]:
    if phase_number < 1 or phase_number > 8:
        raise HTTPException(status_code=400, detail="Phase must be 1-8")

    state_manager = engine.state_manager
    state = await state_manager.load()
    if not state:
        raise HTTPException(status_code=404, detail="Project not found")

    return await engine.gate_validator.run_go_no_go(state, phase_number)
