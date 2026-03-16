"""Project templates for scaffolding."""

from pathlib import Path
from typing import Any

from pydantic import BaseModel, Field


class ProjectTemplate(BaseModel):
    id: str
    name: str
    description: str
    category: str
    compliance_standards: list[str] = Field(default_factory=list)
    phases: dict[int, dict[str, Any]] = Field(default_factory=dict)
    artifacts: list[dict[str, Any]] = Field(default_factory=list)
    agents: list[str] = Field(default_factory=list)


TEMPLATES: dict[str, ProjectTemplate] = {
    "healthcare-saas": ProjectTemplate(
        id="healthcare-saas",
        name="Healthcare SaaS Application",
        description="HIPAA-compliant healthcare application with patient data management",
        category="healthcare",
        compliance_standards=["hipaa", "soc2"],
        phases={
            1: {
                "artifacts": ["Business Case", "PRD", "Market Analysis"],
                "duration_weeks": 2,
            },
            2: {
                "artifacts": ["Functional Requirements", "Security Requirements", "User Stories"],
                "duration_weeks": 3,
            },
            3: {
                "artifacts": ["System Architecture", "Security Architecture", "Data Flow Diagram"],
                "duration_weeks": 2,
            },
        },
        artifacts=[
            {"name": "HIPAA Risk Assessment", "type": "report", "phase": 2},
            {"name": "PHI Data Model", "type": "design", "phase": 3},
            {"name": "Audit Log Specification", "type": "document", "phase": 2},
        ],
        agents=["vision", "requirements", "architecture"],
    ),
    "fintech-api": ProjectTemplate(
        id="fintech-api",
        name="FinTech API Platform",
        description="PCI DSS compliant payment processing API",
        category="fintech",
        compliance_standards=["pci_dss", "soc2", "gdpr"],
        phases={
            1: {
                "artifacts": ["Business Case", "PRD", "Competitive Analysis"],
                "duration_weeks": 2,
            },
            2: {
                "artifacts": ["API Requirements", "Security Requirements", "PCI Scope Document"],
                "duration_weeks": 4,
            },
            3: {
                "artifacts": ["API Architecture", "Security Architecture", "PCI Network Diagram"],
                "duration_weeks": 3,
            },
        },
        artifacts=[
            {"name": "PCI DSS Self-Assessment", "type": "report", "phase": 2},
            {"name": "Payment Flow Diagram", "type": "design", "phase": 3},
            {"name": "Encryption Standards", "type": "document", "phase": 3},
        ],
        agents=["vision", "requirements", "architecture", "quality"],
    ),
    "ecommerce-platform": ProjectTemplate(
        id="ecommerce-platform",
        name="E-Commerce Platform",
        description="GDPR-compliant e-commerce with checkout and inventory",
        category="ecommerce",
        compliance_standards=["gdpr", "pci_dss"],
        phases={
            1: {
                "artifacts": ["Business Case", "PRD", "Revenue Model"],
                "duration_weeks": 1,
            },
            2: {
                "artifacts": ["Product Requirements", "Checkout Flow", "Inventory Requirements"],
                "duration_weeks": 2,
            },
            3: {
                "artifacts": ["Platform Architecture", "Payment Integration", "GDPR Compliance"],
                "duration_weeks": 2,
            },
        },
        artifacts=[
            {"name": "Checkout Flow", "type": "design", "phase": 2},
            {"name": "Product Catalog Schema", "type": "design", "phase": 3},
            {"name": "Privacy Policy", "type": "document", "phase": 1},
        ],
        agents=["vision", "requirements", "architecture"],
    ),
    "saas-mvp": ProjectTemplate(
        id="saas-mvp",
        name="SaaS MVP",
        description="General SaaS MVP template with SOC 2 readiness",
        category="saas",
        compliance_standards=["soc2"],
        phases={
            1: {
                "artifacts": ["Business Case", "PRD"],
                "duration_weeks": 1,
            },
            2: {
                "artifacts": ["Core Features", "User Stories", "NFR"],
                "duration_weeks": 2,
            },
            3: {
                "artifacts": ["System Architecture", "Database Design"],
                "duration_weeks": 1,
            },
        },
        artifacts=[
            {"name": "Feature Prioritization", "type": "document", "phase": 1},
            {"name": "Tech Stack Decision", "type": "decision", "phase": 3},
        ],
        agents=["vision", "requirements", "planning"],
    ),
    "internal-tool": ProjectTemplate(
        id="internal-tool",
        name="Internal Tool",
        description="Internal business tool with basic compliance",
        category="internal",
        compliance_standards=[],
        phases={
            1: {
                "artifacts": ["Requirements Document"],
                "duration_weeks": 1,
            },
            2: {
                "artifacts": ["User Requirements", "Integration Requirements"],
                "duration_weeks": 1,
            },
            3: {
                "artifacts": ["System Design"],
                "duration_weeks": 1,
            },
        },
        artifacts=[
            {"name": "Integration Spec", "type": "design", "phase": 2},
        ],
        agents=["requirements", "development"],
    ),
    "api-backend": ProjectTemplate(
        id="api-backend",
        name="API Backend Service",
        description="REST API backend with authentication",
        category="backend",
        compliance_standards=["soc2"],
        phases={
            1: {
                "artifacts": ["API Vision"],
                "duration_weeks": 1,
            },
            2: {
                "artifacts": ["API Specification", "Auth Requirements"],
                "duration_weeks": 2,
            },
            3: {
                "artifacts": ["API Architecture", "Database Schema"],
                "duration_weeks": 2,
            },
        },
        artifacts=[
            {"name": "OpenAPI Spec", "type": "design", "phase": 2},
            {"name": "Auth Flow", "type": "design", "phase": 3},
        ],
        agents=["architecture", "development"],
    ),
}


def get_template(template_id: str) -> ProjectTemplate | None:
    return TEMPLATES.get(template_id)


def list_templates(category: str | None = None) -> list[ProjectTemplate]:
    templates = list(TEMPLATES.values())
    if category:
        templates = [t for t in templates if t.category == category]
    return templates


def get_template_categories() -> list[str]:
    return list({t.category for t in TEMPLATES.values()})


def scaffold_from_template(
    template_id: str,
    project_name: str,
    output_dir: Path,
) -> dict[str, Any]:
    template = get_template(template_id)
    if not template:
        raise ValueError(f"Template not found: {template_id}")

    output_dir.mkdir(parents=True, exist_ok=True)

    result = {
        "template": template_id,
        "project_name": project_name,
        "created_files": [],
        "created_dirs": [],
    }

    for phase_num, phase_config in template.phases.items():
        phase_dir = output_dir / f"phase-{phase_num}"
        phase_dir.mkdir(exist_ok=True)
        result["created_dirs"].append(str(phase_dir))

        for artifact_name in phase_config.get("artifacts", []):
            artifact_file = phase_dir / f"{artifact_name.lower().replace(' ', '-')}.md"
            artifact_file.write_text(f"# {artifact_name}\n\n_TODO: Complete this document_\n")
            result["created_files"].append(str(artifact_file))

    for artifact in template.artifacts:
        artifact_dir = output_dir / f"phase-{artifact['phase']}"
        artifact_dir.mkdir(exist_ok=True)
        artifact_file = artifact_dir / f"{artifact['name'].lower().replace(' ', '-')}.md"
        if not artifact_file.exists():
            artifact_file.write_text(f"# {artifact['name']}\n\n_TODO: Complete this {artifact['type']}_\n")
            result["created_files"].append(str(artifact_file))

    return result
