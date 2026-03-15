"""FastAPI backend main application."""

from contextlib import asynccontextmanager
from pathlib import Path
from typing import Any

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from octalume.core.engine import PhaseEngine
from octalume.core.gates import GateValidator
from octalume.core.orchestrator import AgentOrchestrator
from octalume.core.state import ProjectStateManager
from octalume.core.memory import MemoryBank
from octalume.utils.logging import configure_logging, get_logger

from web.backend.routers import phases, agents, artifacts, compliance, dashboard

logger = get_logger(__name__)

state_manager: ProjectStateManager | None = None
engine: PhaseEngine | None = None
orchestrator: AgentOrchestrator | None = None
memory_bank: MemoryBank | None = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    global state_manager, engine, orchestrator, memory_bank

    configure_logging(level="INFO", json_format=False)

    state_manager = ProjectStateManager(Path(".octalume"))
    memory_bank = MemoryBank(Path(".octalume/memory"))
    gate_validator = GateValidator(state_manager)
    orchestrator = AgentOrchestrator(state_manager)
    engine = PhaseEngine(state_manager, gate_validator, orchestrator)

    logger.info("octalume_backend_started")

    yield

    logger.info("octalume_backend_shutdown")


app = FastAPI(
    title="OCTALUME Dashboard",
    description="AI-Native Enterprise SDLC Framework Dashboard",
    version="2.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(phases.router, prefix="/api/phases", tags=["Phases"])
app.include_router(agents.router, prefix="/api/agents", tags=["Agents"])
app.include_router(artifacts.router, prefix="/api/artifacts", tags=["Artifacts"])
app.include_router(compliance.router, prefix="/api/compliance", tags=["Compliance"])
app.include_router(dashboard.router, prefix="/api/dashboard", tags=["Dashboard"])


@app.get("/")
async def root() -> dict[str, str]:
    return {
        "name": "OCTALUME",
        "version": "2.0.0",
        "status": "running",
    }


@app.get("/health")
async def health() -> dict[str, Any]:
    return {
        "status": "healthy",
        "services": {
            "state_manager": state_manager is not None,
            "engine": engine is not None,
            "orchestrator": orchestrator is not None,
            "memory": memory_bank is not None,
        },
    }


def get_state_manager() -> ProjectStateManager:
    if state_manager is None:
        raise HTTPException(status_code=503, detail="Service not initialized")
    return state_manager


def get_engine() -> PhaseEngine:
    if engine is None:
        raise HTTPException(status_code=503, detail="Service not initialized")
    return engine


def get_orchestrator() -> AgentOrchestrator:
    if orchestrator is None:
        raise HTTPException(status_code=503, detail="Service not initialized")
    return orchestrator


def get_memory() -> MemoryBank:
    if memory_bank is None:
        raise HTTPException(status_code=503, detail="Service not initialized")
    return memory_bank
