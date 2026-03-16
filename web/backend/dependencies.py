"""Dependency injection for FastAPI routers."""

from functools import lru_cache
from pathlib import Path

from octalume.core.engine import PhaseEngine
from octalume.core.gates import GateValidator
from octalume.core.memory import MemoryBank
from octalume.core.orchestrator import AgentOrchestrator
from octalume.core.state import ProjectStateManager


@lru_cache
def get_state_manager() -> ProjectStateManager:
    return ProjectStateManager(Path(".octalume"))


@lru_cache
def get_memory() -> MemoryBank:
    return MemoryBank(Path(".octalume/memory"))


@lru_cache
def get_orchestrator() -> AgentOrchestrator:
    return AgentOrchestrator(get_state_manager())


@lru_cache
def get_engine() -> PhaseEngine:
    state_manager = get_state_manager()
    gate_validator = GateValidator(state_manager)
    orchestrator = get_orchestrator()
    return PhaseEngine(state_manager, gate_validator, orchestrator)
