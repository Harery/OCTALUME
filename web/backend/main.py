"""FastAPI backend main application with full OpenAPI documentation."""

from contextlib import asynccontextmanager
from pathlib import Path
from typing import Any

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from fastapi.responses import JSONResponse

from octalume.core.engine import PhaseEngine
from octalume.core.gates import GateValidator
from octalume.core.memory import MemoryBank
from octalume.core.orchestrator import AgentOrchestrator
from octalume.core.state import ProjectStateManager
from octalume.utils.logging import configure_logging, get_logger
from web.backend.routers import agents, artifacts, compliance, dashboard, phases

logger = get_logger(__name__)

state_manager: ProjectStateManager | None = None
engine: PhaseEngine | None = None
orchestrator: AgentOrchestrator | None = None
memory_bank: MemoryBank | None = None


@asynccontextmanager
async def lifespan(_app: FastAPI):
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


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title="OCTALUME API",
        version="2.0.0",
        description="""
## OCTALUME - AI-Native Enterprise SDLC Framework

**Octa** = 8 phases | **Lume** = light/guidance

### Overview

OCTALUME is an AI-native software development lifecycle framework that guides projects from initial vision through production operations with built-in quality gates, multi-agent orchestration, and compliance support.

### Features

- **8 Sequential Phases** - Clear progression from idea to production
- **30+ MCP Tools** - Full Claude Code integration
- **Quality Gates** - Go/no-go decisions at each phase
- **Multi-Agent Orchestration** - 9 specialized AI agents
- **Compliance Ready** - HIPAA, SOC 2, PCI DSS, GDPR, SOX

### API Categories

| Category | Description |
|----------|-------------|
| `/api/phases` | Phase lifecycle management |
| `/api/agents` | AI agent orchestration |
| `/api/artifacts` | Artifact tracking and traceability |
| `/api/compliance` | Compliance scanning and reporting |
| `/api/dashboard` | Dashboard metrics and summaries |

### Authentication

Currently no authentication required. For production, implement API keys or OAuth2.

### Rate Limits

Default: 100 requests per minute per IP.
        """,
        routes=app.routes,
        tags=[
            {"name": "Phases", "description": "Manage the 8 SDLC phases with quality gates"},
            {"name": "Agents", "description": "Spawn and manage AI agents for each phase"},
            {"name": "Artifacts", "description": "Create and track project artifacts"},
            {"name": "Compliance", "description": "Run compliance scans and generate reports"},
            {"name": "Dashboard", "description": "Get metrics and summaries for the dashboard"},
            {"name": "Health", "description": "System health and status endpoints"},
        ],
    )

    openapi_schema["info"]["x-logo"] = {
        "url": "https://octalume.dev/logo.png",
        "altText": "OCTALUME Logo",
    }

    app.openapi_schema = openapi_schema
    return app.openapi_schema


app = FastAPI(
    title="OCTALUME API",
    description="AI-Native Enterprise SDLC Framework",
    version="2.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

app.openapi = custom_openapi

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


@app.get(
    "/",
    summary="API Root",
    description="Returns basic API information and available endpoints",
    response_description="API metadata",
    responses={
        200: {
            "description": "API information",
            "content": {
                "application/json": {
                    "example": {
                        "name": "OCTALUME",
                        "version": "2.0.0",
                        "status": "running",
                        "docs": "/docs",
                        "redoc": "/redoc",
                    }
                }
            },
        }
    },
)
async def root() -> dict[str, str]:
    return {
        "name": "OCTALUME",
        "version": "2.0.0",
        "status": "running",
        "docs": "/docs",
        "redoc": "/redoc",
    }


@app.get(
    "/health",
    summary="Health Check",
    description="Returns the health status of all services",
    response_description="Health status of all components",
    responses={
        200: {
            "description": "All services healthy",
            "content": {
                "application/json": {
                    "example": {
                        "status": "healthy",
                        "services": {
                            "state_manager": True,
                            "engine": True,
                            "orchestrator": True,
                            "memory": True,
                        },
                    }
                }
            },
        },
        503: {
            "description": "Service unavailable",
            "content": {"application/json": {"example": {"detail": "Service not initialized"}}},
        },
    },
    tags=["Health"],
)
async def health() -> dict[str, Any]:
    services = {
        "state_manager": state_manager is not None,
        "engine": engine is not None,
        "orchestrator": orchestrator is not None,
        "memory": memory_bank is not None,
    }

    all_healthy = all(services.values())

    if not all_healthy:
        return JSONResponse(
            status_code=503,
            content={
                "status": "degraded",
                "services": services,
            },
        )

    return {
        "status": "healthy",
        "services": services,
    }


@app.get(
    "/ready",
    summary="Readiness Check",
    description="Returns whether the API is ready to accept requests",
    tags=["Health"],
)
async def readiness() -> dict[str, bool]:
    return {
        "ready": all(
            [
                state_manager is not None,
                engine is not None,
                orchestrator is not None,
                memory_bank is not None,
            ]
        )
    }
