"""Heuristic parser: extract structure from a raw brain-dump.

This is deliberately deterministic. No LLM required — we use keyword
spotting, sectioning, and lightweight NLP to slot raw text into a
structured ``Project`` model. An optional ``--llm`` flag (see the CLI)
can re-rank or enrich, but the base path must always work offline.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field

# Domain signals — keyword buckets that hint at the project type.
DOMAIN_SIGNALS = {
    "saas": [
        "users",
        "subscription",
        "billing",
        "stripe",
        "auth",
        "login",
        "signup",
        "dashboard",
        "tenant",
        "saas",
        "web app",
        "frontend",
        "backend",
        "database",
        "api",
    ],
    "cli": [
        "cli",
        "command line",
        "terminal",
        "shell",
        "script",
        "argv",
        "stdin",
        "stdout",
        "pipe",
        "unix",
        "tool",
    ],
    "iot": [
        "sensor",
        "device",
        "hardware",
        "raspberry",
        "arduino",
        "esp32",
        "mqtt",
        "firmware",
        "gpio",
        "embedded",
        "iot",
        "edge",
    ],
    "data": [
        "etl",
        "pipeline",
        "data",
        "warehouse",
        "analytics",
        "dashboard",
        "report",
        "pandas",
        "spark",
        "airflow",
        "dbt",
    ],
    "mobile": [
        "ios",
        "android",
        "mobile",
        "swift",
        "kotlin",
        "react native",
        "flutter",
    ],
    "ml": [
        "model",
        "training",
        "inference",
        "ml",
        "ai",
        "llm",
        "embedding",
        "neural",
        "pytorch",
        "tensorflow",
    ],
}

STACK_RECOMMENDATIONS = {
    "saas": {
        "frontend": "Next.js 14 + TypeScript + Tailwind",
        "backend": "FastAPI (Python) or Node/Express",
        "database": "PostgreSQL + Prisma/SQLAlchemy",
        "auth": "Clerk or Auth.js",
        "hosting": "Vercel (frontend) + Fly.io/Render (backend)",
        "payments": "Stripe",
    },
    "cli": {
        "language": "Python 3.11+ with Click or Typer",
        "packaging": "pyproject.toml, pipx-distributable",
        "testing": "pytest",
        "ci": "GitHub Actions",
    },
    "iot": {
        "device": "ESP32 / Raspberry Pi",
        "firmware": "MicroPython or PlatformIO (C++)",
        "transport": "MQTT (Mosquitto) over TLS",
        "backend": "Node-RED or FastAPI ingest",
        "storage": "TimescaleDB or InfluxDB",
    },
    "data": {
        "orchestration": "Prefect or Airflow",
        "warehouse": "DuckDB (local) → BigQuery/Snowflake",
        "transform": "dbt",
        "viz": "Metabase or Streamlit",
    },
    "mobile": {
        "framework": "React Native (Expo) for cross-platform speed",
        "backend": "Supabase or Firebase",
        "ci": "EAS Build",
    },
    "ml": {
        "framework": "PyTorch or Hugging Face Transformers",
        "serving": "FastAPI + Modal/Replicate",
        "tracking": "Weights & Biases or MLflow",
        "data": "DVC for versioning",
    },
    "generic": {
        "language": "Python 3.11+",
        "testing": "pytest",
        "ci": "GitHub Actions",
        "packaging": "pyproject.toml",
    },
}


@dataclass
class Project:
    """Structured project parsed from a brain-dump."""

    title: str = "Untitled Project"
    summary: str = ""
    domains: list[str] = field(default_factory=list)
    goals: list[str] = field(default_factory=list)
    features: list[str] = field(default_factory=list)
    risks: list[str] = field(default_factory=list)
    unknowns: list[str] = field(default_factory=list)
    constraints: list[str] = field(default_factory=list)
    raw: str = ""

    @property
    def primary_domain(self) -> str:
        return self.domains[0] if self.domains else "generic"

    @property
    def stack(self) -> dict:
        return STACK_RECOMMENDATIONS.get(self.primary_domain, STACK_RECOMMENDATIONS["generic"])

    @property
    def slug(self) -> str:
        s = re.sub(r"[^a-zA-Z0-9]+", "-", self.title.lower()).strip("-")
        return s or "untitled-project"


# ----- Extraction helpers --------------------------------------------------

_BULLET_RE = re.compile(r"^\s*(?:[-*•]|\d+\.)\s+(.*)$", re.MULTILINE)
_QUESTION_RE = re.compile(r"^[^\n?]{3,200}\?\s*$", re.MULTILINE)


def _extract_title(text: str) -> str:
    # First Markdown heading wins.
    m = re.search(r"^#\s+(.+)$", text, re.MULTILINE)
    if m:
        return m.group(1).strip()
    # Else first non-empty line, truncated.
    for line in text.splitlines():
        line = line.strip()
        if line and not line.startswith(("-", "*", "#")):
            return line[:80].rstrip(".")
    return "Untitled Project"


def _extract_summary(text: str) -> str:
    # First paragraph after title.
    paragraphs = [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]
    for p in paragraphs:
        if p.startswith("#"):
            continue
        # Strip leading bullet if present.
        first_line = p.splitlines()[0]
        if _BULLET_RE.match(first_line):
            continue
        return " ".join(p.split())[:400]
    return ""


def _detect_domains(text: str) -> list[str]:
    text_l = text.lower()
    scored = []
    for domain, signals in DOMAIN_SIGNALS.items():
        score = sum(1 for s in signals if s in text_l)
        if score > 0:
            scored.append((score, domain))
    scored.sort(reverse=True)
    return [d for _, d in scored] or ["generic"]


def _extract_bullets(text: str) -> list[str]:
    return [m.group(1).strip() for m in _BULLET_RE.finditer(text)]


def _classify_bullet(bullet: str) -> str:
    b = bullet.lower()
    if any(w in b for w in ("risk", "concern", "worry", "scary", "afraid", "might fail")):
        return "risk"
    if "?" in bullet or any(w in b for w in ("unclear", "tbd", "decide", "not sure", "unknown")):
        return "unknown"
    if any(
        w in b for w in ("must", "cannot", "constraint", "limited to", "budget", "deadline", "by ")
    ):
        return "constraint"
    if any(w in b for w in ("goal", "want to", "aim to", "objective", "outcome")):
        return "goal"
    return "feature"


def parse_brain_dump(text: str) -> Project:
    """Parse a raw brain-dump string into a structured :class:`Project`."""
    if not text or not text.strip():
        raise ValueError("brain-dump is empty")

    project = Project(raw=text)
    project.title = _extract_title(text)
    project.summary = _extract_summary(text)
    project.domains = _detect_domains(text)

    for bullet in _extract_bullets(text):
        kind = _classify_bullet(bullet)
        getattr(project, kind + "s").append(bullet)

    # Questions in prose -> unknowns.
    for m in _QUESTION_RE.finditer(text):
        q = m.group(0).strip()
        if q not in project.unknowns:
            project.unknowns.append(q)

    # If we got nothing meaningful, scrape sentences.
    if not project.features and not project.goals:
        sentences = re.split(r"(?<=[.!?])\s+", text)
        for s in sentences:
            s = s.strip()
            if 20 <= len(s) <= 200 and not s.startswith("#"):
                project.features.append(s)
            if len(project.features) >= 8:
                break

    return project
