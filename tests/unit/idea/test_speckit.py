"""Tests for the spec-kit codepath."""

from __future__ import annotations

from pathlib import Path

from click.testing import CliRunner

from octalume.cli import main
from octalume.idea.parser import parse_brain_dump
from octalume.idea.speckit import render_all_speckit

SAMPLE = """# Sample App

A small SaaS for testing. Users can log in.

- feature: login with magic link
- feature: per-tenant billing
- risk: spam signups
- unclear: should we use Stripe or Paddle?
"""


def test_speckit_default_target_emits_full_tree(tmp_path: Path):
    src = tmp_path / "dump.md"
    src.write_text(SAMPLE, encoding="utf-8")
    out = tmp_path / "plan"
    runner = CliRunner()
    result = runner.invoke(main, ["idea", "quick", str(src), "--output-dir", str(out)])
    assert result.exit_code == 0
    assert (out / "memory" / "constitution.md").exists()
    feature = out / "specs" / "sample-app"
    for name in ("spec.md", "plan.md", "research.md", "data-model.md", "quickstart.md", "tasks.md"):
        assert (feature / name).exists(), f"missing {name}"
    assert (feature / "contracts" / "README.md").exists()


def test_speckit_plan_carries_octalum_phase_mapping(tmp_path: Path):
    src = tmp_path / "dump.md"
    src.write_text(SAMPLE, encoding="utf-8")
    out = tmp_path / "plan"
    runner = CliRunner()
    runner.invoke(main, ["idea", "quick", str(src), "--output-dir", str(out)])
    plan = (out / "specs" / "sample-app" / "plan.md").read_text(encoding="utf-8")
    assert "OCTALUM 8-phase mapping" in plan
    assert "Phase 0" in plan
    assert "Phase 7" in plan


def test_speckit_spec_lists_user_stories(tmp_path: Path):
    src = tmp_path / "dump.md"
    src.write_text(SAMPLE, encoding="utf-8")
    out = tmp_path / "plan"
    runner = CliRunner()
    runner.invoke(main, ["idea", "quick", str(src), "--output-dir", str(out)])
    spec = (out / "specs" / "sample-app" / "spec.md").read_text(encoding="utf-8")
    assert "US-01" in spec
    assert "Functional requirements" in spec


def test_speckit_tasks_has_parallel_markers_and_phase_structure(tmp_path: Path):
    src = tmp_path / "dump.md"
    src.write_text(SAMPLE, encoding="utf-8")
    out = tmp_path / "plan"
    runner = CliRunner()
    runner.invoke(main, ["idea", "quick", str(src), "--output-dir", str(out)])
    tasks = (out / "specs" / "sample-app" / "tasks.md").read_text(encoding="utf-8")
    assert "[P]" in tasks
    assert "**T0" in tasks
    assert "Phase 3" in tasks


def test_speckit_data_model_picks_saas_starter(tmp_path: Path):
    src = tmp_path / "dump.md"
    src.write_text(SAMPLE, encoding="utf-8")
    out = tmp_path / "plan"
    runner = CliRunner()
    runner.invoke(main, ["idea", "quick", str(src), "--output-dir", str(out)])
    dm = (out / "specs" / "sample-app" / "data-model.md").read_text(encoding="utf-8")
    assert "Tenant" in dm or "User" in dm


def test_speckit_constitution_has_six_principles(tmp_path: Path):
    src = tmp_path / "dump.md"
    src.write_text(SAMPLE, encoding="utf-8")
    out = tmp_path / "plan"
    runner = CliRunner()
    runner.invoke(main, ["idea", "quick", str(src), "--output-dir", str(out)])
    c = (out / "memory" / "constitution.md").read_text(encoding="utf-8")
    for token in ("## I.", "## II.", "## III.", "## IV.", "## V.", "## VI."):
        assert token in c, f"missing principle marker {token}"


def test_speckit_render_all_keys_are_relative_paths():
    project = parse_brain_dump(SAMPLE)
    artifacts = render_all_speckit(project)
    keys = list(artifacts.keys())
    assert "memory/constitution.md" in keys
    assert any(k.startswith("specs/") and k.endswith("/spec.md") for k in keys)
    for k in keys:
        assert not k.startswith("/") and "\\" not in k
