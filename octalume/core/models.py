"""Pydantic models for OCTALUME core entities."""

from datetime import datetime
from enum import Enum
from typing import Any
from uuid import UUID

from pydantic import BaseModel, Field


class PhaseStatus(str, Enum):
    """Status of a lifecycle phase."""

    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    BLOCKED = "blocked"
    COMPLETED = "completed"
    SKIPPED = "skipped"


class ArtifactType(str, Enum):
    """Types of artifacts in the lifecycle."""

    DOCUMENT = "document"
    CODE = "code"
    TEST = "test"
    CONFIGURATION = "configuration"
    DESIGN = "design"
    REPORT = "report"
    DECISION = "decision"


class AgentStatus(str, Enum):
    """Status of an agent."""

    IDLE = "idle"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    TIMEOUT = "timeout"


class AgentType(str, Enum):
    """Types of agents in the system."""

    VISION = "vision"
    REQUIREMENTS = "requirements"
    ARCHITECTURE = "architecture"
    PLANNING = "planning"
    DEVELOPMENT = "development"
    QUALITY = "quality"
    DEPLOYMENT = "deployment"
    OPERATIONS = "operations"
    ORCHESTRATOR = "orchestrator"


class ComplianceStandard(str, Enum):
    """Supported compliance standards."""

    HIPAA = "hipaa"
    SOC2 = "soc2"
    PCI_DSS = "pci_dss"
    GDPR = "gdpr"
    SOX = "sox"
    DOD_ITAR = "dod_itar"


class TimestampMixin(BaseModel):
    """Mixin for timestamp fields."""

    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class Artifact(TimestampMixin):
    """Represents a lifecycle artifact with traceability."""

    id: str = Field(..., pattern=r"^P\d+-[A-Z]+-\d+$", description="Artifact ID (e.g., P1-PRD-001)")
    phase: int = Field(..., ge=1, le=8, description="Phase number (1-8)")
    name: str = Field(..., min_length=1, max_length=200)
    artifact_type: ArtifactType
    content: str | dict[str, Any] | None = None
    file_path: str | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)
    linked_artifacts: list[str] = Field(default_factory=list)
    compliance_tags: list[ComplianceStandard] = Field(default_factory=list)


class QualityGate(BaseModel):
    """Quality gate definition for phase transitions."""

    id: str
    phase: int = Field(..., ge=1, le=8)
    name: str
    description: str
    criteria: list[str] = Field(default_factory=list)
    required_artifacts: list[str] = Field(default_factory=list)
    approvers: list[str] = Field(default_factory=list)
    bypass_allowed: bool = False
    compliance_required: list[ComplianceStandard] = Field(default_factory=list)


class GateResult(BaseModel):
    """Result of a quality gate check."""

    gate_id: str
    passed: bool
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    checks: dict[str, bool] = Field(default_factory=dict)
    missing_artifacts: list[str] = Field(default_factory=list)
    compliance_issues: list[str] = Field(default_factory=list)
    bypassed: bool = False
    bypass_reason: str | None = None
    approver: str | None = None


class Phase(TimestampMixin):
    """Represents a lifecycle phase."""

    number: int = Field(..., ge=1, le=8)
    name: str
    description: str
    status: PhaseStatus = PhaseStatus.NOT_STARTED
    owner: str
    duration_estimate_days: int = Field(default=7, ge=1)
    entry_criteria: list[str] = Field(default_factory=list)
    exit_criteria: list[str] = Field(default_factory=list)
    artifacts: list[str] = Field(default_factory=list)
    quality_gates: list[str] = Field(default_factory=list)
    started_at: datetime | None = None
    completed_at: datetime | None = None
    blockers: list[str] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)


class Agent(TimestampMixin):
    """Represents an AI agent in the system."""

    id: str
    name: str
    agent_type: AgentType
    phase: int | None = None
    status: AgentStatus = AgentStatus.IDLE
    current_task: str | None = None
    capabilities: list[str] = Field(default_factory=list)
    config: dict[str, Any] = Field(default_factory=dict)
    last_heartbeat: datetime | None = None
    timeout_seconds: int = Field(default=3600, ge=60)
    retry_count: int = Field(default=0, ge=0)
    max_retries: int = Field(default=3, ge=0)


class ProjectState(TimestampMixin):
    """Complete state of an OCTALUME project."""

    id: UUID
    name: str
    description: str | None = None
    current_phase: int = Field(default=1, ge=1, le=8)
    phase_status: PhaseStatus = PhaseStatus.NOT_STARTED
    phases: dict[int, Phase] = Field(default_factory=dict)
    artifacts: dict[str, Artifact] = Field(default_factory=dict)
    agents: dict[str, Agent] = Field(default_factory=dict)
    gate_results: list[GateResult] = Field(default_factory=list)
    compliance_standards: list[ComplianceStandard] = Field(default_factory=list)
    artifact_counter: dict[str, int] = Field(default_factory=dict)
    metadata: dict[str, Any] = Field(default_factory=dict)


PHASE_DEFINITIONS: dict[int, dict[str, Any]] = {
    1: {
        "name": "Vision and Strategy",
        "description": "Define product vision, market opportunity, and business case",
        "owner": "Product Owner",
        "duration_estimate_days": 7,
        "exit_criteria": [
            "Business case approved",
            "PRD completed",
            "Stakeholder alignment confirmed",
            "Success metrics defined",
        ],
    },
    2: {
        "name": "Requirements and Scope",
        "description": "Define functional, non-functional, and security requirements",
        "owner": "Product Owner",
        "duration_estimate_days": 14,
        "exit_criteria": [
            "Functional requirements documented",
            "NFRs defined",
            "Traceability matrix created",
            "Requirements approved",
        ],
    },
    3: {
        "name": "Architecture and Design",
        "description": "Design system, security, and data architecture",
        "owner": "CTA",
        "duration_estimate_days": 7,
        "exit_criteria": [
            "System architecture documented",
            "Security architecture approved",
            "Threat model completed",
            "Data models defined",
        ],
    },
    4: {
        "name": "Development Planning",
        "description": "Create WBS, resource plan, and sprint plan",
        "owner": "Project Manager",
        "duration_estimate_days": 7,
        "exit_criteria": [
            "WBS approved",
            "Resources allocated",
            "Sprint plan created",
            "CI/CD pipeline designed",
        ],
    },
    5: {
        "name": "Development Execution",
        "description": "Implement features in agile sprints",
        "owner": "Tech Lead",
        "duration_estimate_days": 30,
        "exit_criteria": [
            "All features implemented",
            "Unit tests passing",
            "Code reviews complete",
            "Technical debt documented",
        ],
    },
    6: {
        "name": "Quality and Security",
        "description": "Validate quality through comprehensive testing",
        "owner": "QA Lead",
        "duration_estimate_days": 14,
        "exit_criteria": [
            "All tests passing",
            "Security scan complete",
            "Performance tests passed",
            "UAT sign-off received",
        ],
    },
    7: {
        "name": "Deployment and Release",
        "description": "Deploy validated build to production",
        "owner": "DevOps",
        "duration_estimate_days": 7,
        "exit_criteria": [
            "Production deployment complete",
            "Smoke tests passing",
            "Rollback plan verified",
            "Release notes published",
        ],
    },
    8: {
        "name": "Operations and Maintenance",
        "description": "Monitoring, incident management, and continuous improvement",
        "owner": "SRE",
        "duration_estimate_days": 14,
        "exit_criteria": [
            "Monitoring active",
            "Runbooks published",
            "On-call rotation established",
            "SLAs met",
        ],
    },
}
