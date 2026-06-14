"""
octalume.idea — Phase 0 "Idea" component (formerly octalum-bdtb).

Turn a raw brain-dump into a structured project plan, spec-kit artifacts,
and a full 12-stage pipeline from idea to deployed product.

This module was merged into OCTALUME from the standalone octalum-bdtb project.
"""

from octalume.idea.parser import Project, parse_brain_dump
from octalume.idea.speckit import render_all_speckit
from octalume.idea.templates import render_all

__version__ = "0.2.0"

__all__ = [
    "Project",
    "parse_brain_dump",
    "render_all_speckit",
    "render_all",
]
