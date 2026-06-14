"""Tests for the idea pipeline module."""

from __future__ import annotations

import pytest

from octalume.idea.parser import parse_brain_dump
from octalume.idea.pipeline import (
    PIPELINE,
    approval_gate_prompt,
    context_compaction_checkpoint,
    get_stage,
    list_stages,
    question_budget,
    required_output_files,
    run_stage_scaffold,
    stage_info,
)

SAMPLE = """# Sample App

A small SaaS for testing.

- feature: login with magic link
- risk: spam signups
"""


def test_pipeline_has_12_stages():
    assert len(PIPELINE) == 12


def test_pipeline_stage_numbers_sequential():
    numbers = [s.number for s in PIPELINE]
    assert numbers == list(range(1, 13))


def test_get_stage_valid():
    s = get_stage(1)
    assert s.number == 1
    assert s.name == "Brain dump intake"


def test_get_stage_invalid():
    with pytest.raises(ValueError, match="Invalid stage number"):
        get_stage(0)
    with pytest.raises(ValueError, match="Invalid stage number"):
        get_stage(13)


def test_stage_info():
    info = stage_info(6)
    assert info["number"] == "6"
    assert "Technical" in info["name"]
    assert info["layer"] == "Nano"


def test_list_stages_returns_all():
    stages = list_stages()
    assert len(stages) == 12
    assert all("number" in s for s in stages)


def test_required_output_files_includes_key_docs():
    files = required_output_files()
    assert "CLAUDE.md" in files
    assert "MEMORY.md" in files
    assert "docs/product-spec.md" in files
    assert ".gitignore" in files


def test_context_compaction_checkpoint():
    cc = context_compaction_checkpoint()
    assert "trigger" in cc
    assert "After Stage 5" in cc["trigger"]


def test_approval_gate_prompt():
    prompt = approval_gate_prompt(3)
    assert "Stage 3" in prompt
    assert "complete" in prompt.lower()


def test_question_budget():
    assert "3" in question_budget(1, 2)
    assert "0" in question_budget(8, 9)


def test_run_stage_scaffold():
    project = parse_brain_dump(SAMPLE)
    scaffold = run_stage_scaffold(project, 1)
    assert scaffold["project_title"] == "Sample App"
    assert scaffold["stage_number"] == "1"
    assert scaffold["skill_file"] == "stages/s01-intake.md"
