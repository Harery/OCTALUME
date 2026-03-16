"""Agent management API router."""

from typing import Any

from fastapi import APIRouter, Depends, HTTPException

from octalume.core.models import AgentStatus
from octalume.core.orchestrator import AgentOrchestrator
from octalume.core.state import ProjectStateManager
from web.backend.dependencies import get_orchestrator, get_state_manager

router = APIRouter()


@router.get("/")
async def list_agents(
    phase: int | None = None,
    status: str | None = None,
    orchestrator: AgentOrchestrator = Depends(get_orchestrator),
    state_manager: ProjectStateManager = Depends(get_state_manager),
) -> dict[str, Any]:
    state = await state_manager.load()
    if not state:
        raise HTTPException(status_code=404, detail="Project not found")

    status_enum = AgentStatus(status) if status else None

    agents = await orchestrator.list_agents(
        state=state,
        phase=phase,
        status=status_enum,
    )

    return {"agents": agents}


@router.post("/spawn")
async def spawn_agent(
    agent_type: str,
    task: str,
    config: dict[str, Any] | None = None,
    orchestrator: AgentOrchestrator = Depends(get_orchestrator),
    state_manager: ProjectStateManager = Depends(get_state_manager),
) -> dict[str, Any]:
    state = await state_manager.load()
    if not state:
        raise HTTPException(status_code=404, detail="Project not found")

    try:
        agent_id = await orchestrator.spawn_agent(
            state=state,
            agent_type=agent_type,
            task=task,
            config=config,
        )
        return {"success": True, "agent_id": agent_id}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{agent_id}")
async def get_agent(
    agent_id: str,
    orchestrator: AgentOrchestrator = Depends(get_orchestrator),
    state_manager: ProjectStateManager = Depends(get_state_manager),
) -> dict[str, Any]:
    state = await state_manager.load()
    if not state:
        raise HTTPException(status_code=404, detail="Project not found")

    try:
        return await orchestrator.get_agent_status(state, agent_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/{agent_id}/terminate")
async def terminate_agent(
    agent_id: str,
    reason: str = "manual_termination",
    orchestrator: AgentOrchestrator = Depends(get_orchestrator),
    state_manager: ProjectStateManager = Depends(get_state_manager),
) -> dict[str, Any]:
    state = await state_manager.load()
    if not state:
        raise HTTPException(status_code=404, detail="Project not found")

    try:
        result = await orchestrator.terminate_agent(
            state=state,
            agent_id=agent_id,
            reason=reason,
        )
        return {"success": result}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/{agent_id}/delegate")
async def delegate_to_agent(
    agent_id: str,
    task: str,
    context: dict[str, Any] | None = None,
    orchestrator: AgentOrchestrator = Depends(get_orchestrator),
    state_manager: ProjectStateManager = Depends(get_state_manager),
) -> dict[str, Any]:
    state = await state_manager.load()
    if not state:
        raise HTTPException(status_code=404, detail="Project not found")

    try:
        task_id = await orchestrator.delegate_task(
            state=state,
            agent_id=agent_id,
            task=task,
            context=context,
        )
        return {"success": True, "task_id": task_id}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/types")
async def list_agent_types(
    orchestrator: AgentOrchestrator = Depends(get_orchestrator),
) -> dict[str, Any]:
    return {"types": orchestrator.list_agent_types()}


@router.get("/health")
async def agent_health_check(
    orchestrator: AgentOrchestrator = Depends(get_orchestrator),
    state_manager: ProjectStateManager = Depends(get_state_manager),
) -> dict[str, Any]:
    state = await state_manager.load()
    if not state:
        raise HTTPException(status_code=404, detail="Project not found")

    return await orchestrator.health_check(state)
