"""
OCTALUME - AI-Native Enterprise SDLC Framework

8 Phases | Quality Gates | Multi-Agent Orchestration | Compliance Ready
"""

from importlib.metadata import version

__version__ = version("octalume") if __package__ else "2.0.0"
__author__ = "Mohamed ElHarery"
__email__ = "mohamed@harery.com"

from octalume.core.engine import PhaseEngine
from octalume.core.gates import GateValidator
from octalume.core.orchestrator import AgentOrchestrator
from octalume.core.state import ProjectState
from octalume.core.memory import MemoryBank

__all__ = [
    "__version__",
    "__author__",
    "__email__",
    "PhaseEngine",
    "GateValidator",
    "AgentOrchestrator",
    "ProjectState",
    "MemoryBank",
]
