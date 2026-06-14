"""12-stage idea-to-product pipeline orchestration.

Each stage corresponds to a Claude Code Skill sub-skill (in
``.claude/skills/idea/stages/``).  The Python layer provides
metadata, ordering, and a deterministic scaffold so the pipeline can
be driven programmatically or by the CLI.
"""

from __future__ import annotations

from dataclasses import dataclass

from octalume.idea.parser import Project

# Pyramid layers — questions narrow as the pipeline descends.
LAYER_MACRO = "Macro"
LAYER_MESO = "Meso"
LAYER_MICRO = "Micro"
LAYER_NANO = "Nano"
LAYER_ATOMIC = "Atomic"
LAYER_BUILD = "Build"


@dataclass(frozen=True)
class Stage:
    """Metadata for one pipeline stage."""

    number: int
    name: str
    layer: str
    skill_file: str
    output_file: str
    description: str


PIPELINE: list[Stage] = [
    Stage(
        1,
        "Brain dump intake",
        LAYER_MACRO,
        "stages/s01-intake.md",
        "product-spec.md",
        "Dynamic intake: ask for the raw idea, then generate 9 gap-filling questions.",
    ),
    Stage(
        2,
        "BRD",
        f"{LAYER_MACRO}→{LAYER_MESO}",
        "stages/s02-brd.md",
        "BRD.md",
        "Business Requirements Document from the intake output.",
    ),
    Stage(
        3,
        "MVP definition",
        LAYER_MESO,
        "stages/s03-mvp.md",
        "MVP.md",
        "Define the minimum viable product scope from the BRD.",
    ),
    Stage(
        4,
        "Business analysis",
        f"{LAYER_MESO}→{LAYER_MICRO}",
        "stages/s04-business-analysis.md",
        "business-analyst-plan.md",
        "Market analysis, competitor intelligence, and business model.",
    ),
    Stage(
        5,
        "Business plan",
        LAYER_MICRO,
        "stages/s05-business-plan.md",
        "business-plan.md",
        "Detailed business plan with revenue model and go-to-market.",
    ),
    Stage(
        6,
        "Technical analysis + stack",
        LAYER_NANO,
        "stages/s06-tech-stack.md",
        "technical-analyst-plan.md",
        "Architecture decisions, stack selection, cost ledger starts here.",
    ),
    Stage(
        7,
        "SpecKit constitution + CLAUDE.md",
        LAYER_NANO,
        "stages/s07-constitution.md",
        "constitution.md",
        "Generate constitution.md, CLAUDE.md, MEMORY.md, and HANDOFF.md.",
    ),
    Stage(
        8,
        "Logic + workflow definitions",
        f"{LAYER_NANO}→{LAYER_ATOMIC}",
        "stages/s08-logic.md",
        "logic.md",
        "Core business logic and workflow definitions.",
    ),
    Stage(
        9,
        "Mermaid visual diagrams",
        LAYER_ATOMIC,
        "stages/s09-diagrams.md",
        "diagrams.md",
        "System diagrams: C4, sequence, ERD, deployment topology.",
    ),
    Stage(
        10,
        "Generate the build",
        LAYER_BUILD,
        "stages/s10-build.md",
        "codebase",
        "Code generation from all prior artifacts.",
    ),
    Stage(
        11,
        "Observability + monitoring",
        LAYER_BUILD,
        "stages/s11-monitoring.md",
        "monitoring config",
        "Monitoring, logging, tracing, and alerting configuration.",
    ),
    Stage(
        12,
        "AI maintenance + upgrade cycle",
        LAYER_BUILD,
        "stages/s12-maintenance.md",
        "MEMORY.md update",
        "Maintenance plan, MEMORY.md update, upgrade cycle schedule.",
    ),
]

STAGES_BY_NUMBER: dict[int, Stage] = {s.number: s for s in PIPELINE}


def get_stage(number: int) -> Stage:
    if number not in STAGES_BY_NUMBER:
        raise ValueError(f"Invalid stage number {number}. Must be 1–12.")
    return STAGES_BY_NUMBER[number]


def stage_info(number: int) -> dict[str, str]:
    s = get_stage(number)
    return {
        "number": str(s.number),
        "name": s.name,
        "layer": s.layer,
        "skill_file": s.skill_file,
        "output_file": s.output_file,
        "description": s.description,
    }


def list_stages() -> list[dict[str, str]]:
    return [stage_info(s.number) for s in PIPELINE]


def required_output_files() -> list[str]:
    return [
        "CLAUDE.md",
        "MEMORY.md",
        "HANDOFF.md",
        "cost-ledger.md",
        ".specify/memory/constitution.md",
        "docs/product-spec.md",
        "docs/BRD.md",
        "docs/MVP.md",
        "docs/business-analyst-plan.md",
        "docs/business-plan.md",
        "docs/technical-analyst-plan.md",
        "docs/tech-stack.md",
        "docs/logic.md",
        "docs/diagrams.md",
        ".gitignore",
    ]


def context_compaction_checkpoint() -> dict[str, str]:
    return {
        "trigger": "After Stage 5 is approved, before Stage 6 begins",
        "step_1": "Write HANDOFF.md — full session state snapshot",
        "step_2": "Recommend operator runs /compact in Claude Code CLI",
        "step_3": "Re-inject on resume: project name, approved stage summaries, key decisions",
        "step_4": "Continue Stage 6 in clean context",
    }


def approval_gate_prompt(stage_number: int) -> str:
    s = get_stage(stage_number)
    return f"Stage {s.number} — {s.name} complete. Does this match your vision?"


def question_budget(stage_from: int, stage_to: int) -> str:
    budgets = {
        (1, 2): "3 questions (Macro)",
        (2, 3): "3–4 questions (Meso)",
        (3, 4): "3–4 questions (Meso→Micro)",
        (4, 5): "3–5 questions (Micro)",
        (5, 6): "3–5 questions (Micro→Nano)",
        (6, 7): "3 questions (Nano)",
        (7, 8): "2–3 questions (Nano→Atomic)",
        (8, 9): "0 — no new questions (Build layer begins)",
    }
    return budgets.get((stage_from, stage_to), "0 — no new questions")


def run_stage_scaffold(project: Project, stage_number: int) -> dict[str, str]:
    """Return scaffold metadata for executing a stage on a parsed project.

    This does NOT execute the LLM-driven stage logic (that lives in the
    Claude Code Skill markdown files).  It returns the context a caller
    needs: which skill file to load, what output to produce, and the
    approval gate prompt.
    """
    s = get_stage(stage_number)
    return {
        "project_title": project.title,
        "project_slug": project.slug,
        "project_domain": project.primary_domain,
        "stage_number": str(s.number),
        "stage_name": s.name,
        "stage_layer": s.layer,
        "skill_file": s.skill_file,
        "expected_output": s.output_file,
        "approval_prompt": approval_gate_prompt(stage_number),
    }
