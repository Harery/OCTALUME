"""Tests for the `octalum idea` Click CLI sub-commands."""

from __future__ import annotations

import io
from pathlib import Path

from click.testing import CliRunner

from octalume.cli import main

SAMPLE = """# Sample App

A small SaaS for testing. Users can log in.

- feature: login with magic link
- risk: spam signups
- unclear: should we use Stripe or Paddle?
"""

CLASSIC = ["--target", "octalum-classic"]


def test_idea_quick_generates_spec_kit_files(tmp_path: Path):
    src = tmp_path / "dump.md"
    src.write_text(SAMPLE, encoding="utf-8")
    out = tmp_path / "plan"
    runner = CliRunner()
    result = runner.invoke(main, ["idea", "quick", str(src), "--output-dir", str(out)])
    assert result.exit_code == 0
    assert (out / "memory" / "constitution.md").exists()
    assert (out / "specs" / "sample-app" / "spec.md").exists()


def test_idea_quick_classic_generates_all_files(tmp_path: Path):
    src = tmp_path / "dump.md"
    src.write_text(SAMPLE, encoding="utf-8")
    out = tmp_path / "plan"
    runner = CliRunner()
    result = runner.invoke(main, ["idea", "quick", str(src), "--output-dir", str(out), *CLASSIC])
    assert result.exit_code == 0
    for name in ("STRUCTURE.md", "STACK.md", "PHASES.md", "RISKS.md", "BUILD_NOW.sh"):
        assert (out / name).exists(), f"missing {name}"


def test_idea_bootstrap_generates_build_now(tmp_path: Path):
    src = tmp_path / "dump.md"
    src.write_text(SAMPLE, encoding="utf-8")
    out = tmp_path / "plan"
    runner = CliRunner()
    result = runner.invoke(main, ["idea", "bootstrap", str(src), "--output-dir", str(out)])
    assert result.exit_code == 0
    assert (out / "BUILD_NOW.sh").exists()


def test_idea_no_overwrite_without_force(tmp_path: Path):
    src = tmp_path / "dump.md"
    src.write_text(SAMPLE, encoding="utf-8")
    out = tmp_path / "plan"
    runner = CliRunner()
    runner.invoke(main, ["idea", "quick", str(src), "--output-dir", str(out), *CLASSIC])
    (out / "STACK.md").write_text("MINE", encoding="utf-8")
    runner.invoke(main, ["idea", "quick", str(src), "--output-dir", str(out), *CLASSIC])
    assert (out / "STACK.md").read_text() == "MINE"


def test_idea_force_overwrites(tmp_path: Path):
    src = tmp_path / "dump.md"
    src.write_text(SAMPLE, encoding="utf-8")
    out = tmp_path / "plan"
    runner = CliRunner()
    runner.invoke(main, ["idea", "quick", str(src), "--output-dir", str(out), *CLASSIC])
    (out / "STACK.md").write_text("MINE", encoding="utf-8")
    runner.invoke(main, ["idea", "quick", str(src), "--output-dir", str(out), "--force", *CLASSIC])
    assert (out / "STACK.md").read_text() != "MINE"


def test_idea_literal_string_input(tmp_path: Path):
    out = tmp_path / "plan"
    runner = CliRunner()
    result = runner.invoke(
        main,
        [
            "idea",
            "quick",
            "# Tiny\n\nA tiny CLI tool with stdin.",
            "--output-dir",
            str(out),
            *CLASSIC,
        ],
    )
    assert result.exit_code == 0
    assert (out / "STACK.md").exists()


def test_idea_stages_command():
    runner = CliRunner()
    result = runner.invoke(main, ["idea", "stages"])
    assert result.exit_code == 0
    assert "Brain dump intake" in result.output
    assert "12 Stages" in result.output


def test_idea_stage_command(tmp_path: Path):
    src = tmp_path / "dump.md"
    src.write_text(SAMPLE, encoding="utf-8")
    out = tmp_path / "plan"
    runner = CliRunner()
    result = runner.invoke(main, ["idea", "stage", "1", str(src), "--output-dir", str(out)])
    assert result.exit_code == 0
    assert "Stage 1" in result.output


def test_idea_stage_invalid_number(tmp_path: Path):
    src = tmp_path / "dump.md"
    src.write_text(SAMPLE, encoding="utf-8")
    runner = CliRunner()
    result = runner.invoke(main, ["idea", "stage", "99", str(src)])
    assert result.exit_code != 0


def test_idea_phases_contains_octalume(tmp_path: Path):
    src = tmp_path / "d.md"
    src.write_text(SAMPLE, encoding="utf-8")
    out = tmp_path / "plan"
    runner = CliRunner()
    runner.invoke(main, ["idea", "quick", str(src), "--output-dir", str(out), *CLASSIC])
    text = (out / "PHASES.md").read_text()
    assert "OCTALUME" in text
    assert "Phase 0" in text
    assert "Phase 7" in text


def test_idea_llm_flag_prints_notice(tmp_path: Path):
    src = tmp_path / "dump.md"
    src.write_text(SAMPLE, encoding="utf-8")
    out = tmp_path / "plan"
    runner = CliRunner()
    result = runner.invoke(
        main, ["idea", "quick", str(src), "--output-dir", str(out), "--llm", "claude-sonnet"]
    )
    assert result.exit_code == 0
    assert "claude-sonnet" in result.output


def test_idea_unicode_input(tmp_path: Path):
    src = tmp_path / "dump.md"
    src.write_text(
        "# \u9879\u76ee \u2014 Caf\u00e9 r\u00e9sum\u00e9 app \U0001f680\n\n"
        "An app for \u0645\u0637\u0627\u0639\u0645 with Stripe.\n\n"
        "- feature: \u062a\u0633\u062c\u064a\u0644 \u0627\u0644\u062f\u062e\u0648\u0644 \U0001f510\n"
        "- risk: Unicode \u4e2d\u6587\n",
        encoding="utf-8",
    )
    out = tmp_path / "plan"
    runner = CliRunner()
    result = runner.invoke(main, ["idea", "quick", str(src), "--output-dir", str(out), *CLASSIC])
    assert result.exit_code == 0
    text = (out / "PHASES.md").read_text(encoding="utf-8")
    assert "\U0001f680" in text or "Caf\u00e9" in text


def test_idea_large_input_handled(tmp_path: Path):
    src = tmp_path / "big.md"
    with src.open("w", encoding="utf-8") as fh:
        fh.write("# Big dump\n\n")
        for i in range(50_000):
            fh.write(f"- feature: do thing number {i}\n")
    assert src.stat().st_size > 1_000_000
    out = tmp_path / "plan"
    runner = CliRunner()
    result = runner.invoke(main, ["idea", "quick", str(src), "--output-dir", str(out), *CLASSIC])
    assert result.exit_code == 0
    assert (out / "STRUCTURE.md").exists()


def test_idea_output_dir_created_recursively(tmp_path: Path):
    src = tmp_path / "dump.md"
    src.write_text(SAMPLE, encoding="utf-8")
    out = tmp_path / "deeply" / "nested" / "plan"
    runner = CliRunner()
    result = runner.invoke(main, ["idea", "quick", str(src), "--output-dir", str(out), *CLASSIC])
    assert result.exit_code == 0
    assert out.is_dir()


def test_idea_interactive_mode(tmp_path: Path, monkeypatch):
    inputs = iter(
        [
            "A tiny CLI",
            "",
            "",
            "Devs",
            "",
            "",
            "- arg parsing",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
            "",
        ]
    )

    def _input():
        try:
            return next(inputs)
        except StopIteration as exc:
            raise EOFError from exc

    monkeypatch.setattr("builtins.input", _input)
    out = tmp_path / "plan"
    runner = CliRunner()
    result = runner.invoke(main, ["idea", "interactive", "--output-dir", str(out), *CLASSIC])
    assert result.exit_code == 0
    assert (out / "STACK.md").exists()
