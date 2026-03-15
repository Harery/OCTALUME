"""Artifact management API router."""

from typing import Any

from fastapi import APIRouter, Depends, HTTPException

from octalume.core.models import Artifact, ArtifactType
from octalume.core.state import ProjectStateManager
from web.backend.main import get_state_manager

router = APIRouter()


@router.get("/")
async def list_artifacts(
    phase: int | None = None,
    artifact_type: str | None = None,
    search: str | None = None,
    limit: int = 50,
    state_manager: ProjectStateManager = Depends(get_state_manager),
) -> dict[str, Any]:
    state = await state_manager.load()
    if not state:
        raise HTTPException(status_code=404, detail="Project not found")

    artifacts = []
    for artifact in state.artifacts.values():
        if phase is not None and artifact.phase != phase:
            continue
        if artifact_type and artifact.artifact_type.value != artifact_type:
            continue
        if search:
            search_lower = search.lower()
            if search_lower not in artifact.name.lower():
                if isinstance(artifact.content, str):
                    if search_lower not in artifact.content.lower():
                        continue
                else:
                    continue

        artifacts.append(artifact.model_dump())

        if len(artifacts) >= limit:
            break

    return {"artifacts": artifacts, "count": len(artifacts)}


@router.get("/{artifact_id}")
async def get_artifact(
    artifact_id: str,
    state_manager: ProjectStateManager = Depends(get_state_manager),
) -> dict[str, Any]:
    state = await state_manager.load()
    if not state:
        raise HTTPException(status_code=404, detail="Project not found")

    if artifact_id not in state.artifacts:
        raise HTTPException(status_code=404, detail=f"Artifact not found: {artifact_id}")

    return {"artifact": state.artifacts[artifact_id].model_dump()}


@router.post("/")
async def create_artifact(
    phase: int,
    artifact_type: str,
    name: str,
    content: str | dict[str, Any] | None = None,
    file_path: str | None = None,
    compliance_tags: list[str] | None = None,
    state_manager: ProjectStateManager = Depends(get_state_manager),
) -> dict[str, Any]:
    state = await state_manager.load()
    if not state:
        raise HTTPException(status_code=404, detail="Project not found")

    if phase < 1 or phase > 8:
        raise HTTPException(status_code=400, detail="Phase must be 1-8")

    try:
        art_type = ArtifactType(artifact_type)
    except ValueError:
        raise HTTPException(status_code=400, detail=f"Invalid artifact type: {artifact_type}")

    section_map = {
        ArtifactType.DOCUMENT: "DOC",
        ArtifactType.CODE: "CODE",
        ArtifactType.TEST: "TEST",
        ArtifactType.CONFIGURATION: "CFG",
        ArtifactType.DESIGN: "DSN",
        ArtifactType.REPORT: "RPT",
        ArtifactType.DECISION: "DEC",
    }
    section = section_map[art_type]
    counter = state.artifact_counter.get(section, 0) + 1

    artifact = Artifact(
        id=f"P{phase}-{section}-{counter:03d}",
        phase=phase,
        name=name,
        artifact_type=art_type,
        content=content,
        file_path=file_path,
        compliance_tags=[],
    )

    state.artifacts[artifact.id] = artifact
    state.phases[phase].artifacts.append(artifact.id)
    state.artifact_counter[section] = counter

    await state_manager.save(state)

    return {"success": True, "artifact": artifact.model_dump()}


@router.post("/{artifact_id}/link/{target_id}")
async def link_artifacts(
    artifact_id: str,
    target_id: str,
    state_manager: ProjectStateManager = Depends(get_state_manager),
) -> dict[str, Any]:
    state = await state_manager.load()
    if not state:
        raise HTTPException(status_code=404, detail="Project not found")

    if artifact_id not in state.artifacts:
        raise HTTPException(status_code=404, detail=f"Artifact not found: {artifact_id}")
    if target_id not in state.artifacts:
        raise HTTPException(status_code=404, detail=f"Target artifact not found: {target_id}")

    if target_id not in state.artifacts[artifact_id].linked_artifacts:
        state.artifacts[artifact_id].linked_artifacts.append(target_id)
        await state_manager.save(state)

    return {"success": True, "source": artifact_id, "target": target_id}


@router.get("/stats")
async def artifact_stats(
    state_manager: ProjectStateManager = Depends(get_state_manager),
) -> dict[str, Any]:
    state = await state_manager.load()
    if not state:
        raise HTTPException(status_code=404, detail="Project not found")

    by_phase: dict[int, int] = {}
    by_type: dict[str, int] = {}

    for artifact in state.artifacts.values():
        by_phase[artifact.phase] = by_phase.get(artifact.phase, 0) + 1
        by_type[artifact.artifact_type.value] = by_type.get(artifact.artifact_type.value, 0) + 1

    return {
        "total": len(state.artifacts),
        "by_phase": by_phase,
        "by_type": by_type,
    }
