"""OCTALUME project templates."""

from octalume.templates.project_templates import (
    TEMPLATES,
    ProjectTemplate,
    get_template,
    get_template_categories,
    list_templates,
    scaffold_from_template,
)

__all__ = [
    "ProjectTemplate",
    "TEMPLATES",
    "get_template",
    "list_templates",
    "get_template_categories",
    "scaffold_from_template",
]
