#!/usr/bin/env python3

import asyncio
from pathlib import Path

import click
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table

from octalume import __version__
from octalume.core.engine import PhaseEngine
from octalume.core.gates import GateValidator
from octalume.core.memory import MemoryBank
from octalume.core.orchestrator import AgentOrchestrator
from octalume.core.state import ProjectStateManager
from octalume.utils.logging import configure_logging

console = Console()


@click.group()
@click.version_option(version=__version__, prog_name="octalume")
@click.option("--debug", is_flag=True, help="Enable debug logging")
def main(debug: bool) -> None:
    configure_logging(level="DEBUG" if debug else "INFO")
    pass


@main.command()
@click.argument("name")
@click.option("--description", "-d", help="Project description")
@click.option(
    "--compliance",
    "-c",
    multiple=True,
    type=click.Choice(["hipaa", "soc2", "pci_dss", "gdpr", "sox", "dod_itar"]),
    help="Compliance standards to configure",
)
def init(name: str, description: str | None, compliance: tuple[str, ...]) -> None:
    state_manager = ProjectStateManager()

    async def _init() -> None:
        state = await state_manager.create(
            name=name,
            description=description,
            compliance_standards=list(compliance),
        )

        console.print(
            Panel.fit(
                f"[bold green]Project initialized![/bold green]\n\n"
                f"Name: {state.name}\n"
                f"ID: {state.id}\n"
                f"Compliance: {', '.join(c.value for c in state.compliance_standards) or 'None'}\n"
                f"State: {state_manager.state_file}",
                title="OCTALUME",
            )
        )

    asyncio.run(_init())


@main.command()
def status() -> None:
    state_manager = ProjectStateManager()

    async def _status() -> None:
        state = await state_manager.load()

        if not state:
            console.print("[yellow]No project found. Run 'octalume init' first.[/yellow]")
            return

        table = Table(title=f"Project: {state.name}")
        table.add_column("Phase", style="cyan")
        table.add_column("Name", style="green")
        table.add_column("Status", style="yellow")
        table.add_column("Artifacts", style="blue")
        table.add_column("Owner", style="magenta")

        for phase_num in sorted(state.phases.keys()):
            phase = state.phases[phase_num]
            status_color = {
                "completed": "green",
                "in_progress": "yellow",
                "blocked": "red",
                "not_started": "dim",
            }.get(phase.status.value, "white")

            table.add_row(
                str(phase.number),
                phase.name,
                f"[{status_color}]{phase.status.value}[/{status_color}]",
                str(len(phase.artifacts)),
                phase.owner,
            )

        console.print(table)

        console.print(f"\nCurrent Phase: [bold cyan]{state.current_phase}[/bold cyan]")
        console.print(f"Phase Status: [bold]{state.phase_status.value}[/bold]")
        console.print(f"Total Artifacts: [bold blue]{len(state.artifacts)}[/bold]")

    asyncio.run(_status())


@main.command()
@click.argument("phase", type=int)
def start(phase: int) -> None:
    state_manager = ProjectStateManager()
    gate_validator = GateValidator(state_manager)
    orchestrator = AgentOrchestrator(state_manager)
    engine = PhaseEngine(state_manager, gate_validator, orchestrator)

    async def _start() -> None:
        state = await state_manager.load()

        if not state:
            console.print("[red]No project found. Run 'octalume init' first.[/red]")
            return

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            progress.add_task(f"Starting Phase {phase}...", total=None)

            try:
                state = await engine.start_phase(state, phase)
                phase_obj = state.phases[phase]

                console.print(f"\n[bold green]Phase {phase} started![/bold green]")
                console.print(f"Name: {phase_obj.name}")
                console.print(f"Owner: {phase_obj.owner}")

            except Exception as e:
                console.print(f"[red]Error: {e}[/red]")

    asyncio.run(_start())


@main.command()
@click.argument("phase", type=int)
def complete(phase: int) -> None:
    state_manager = ProjectStateManager()
    gate_validator = GateValidator(state_manager)
    orchestrator = AgentOrchestrator(state_manager)
    engine = PhaseEngine(state_manager, gate_validator, orchestrator)

    async def _complete() -> None:
        state = await state_manager.load()

        if not state:
            console.print("[red]No project found.[/red]")
            return

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            progress.add_task(f"Validating Phase {phase} exit criteria...", total=None)

            try:
                state, gate_result = await engine.complete_phase(state, phase)

                if gate_result.passed:
                    console.print(f"\n[bold green]Phase {phase} completed![/bold green]")
                else:
                    console.print(f"\n[bold red]Phase {phase} blocked![/bold red]")
                    console.print(f"Missing: {gate_result.missing_artifacts}")

            except Exception as e:
                console.print(f"[red]Error: {e}[/red]")

    asyncio.run(_complete())


@main.command()
@click.argument("phase", type=int)
def gate(phase: int) -> None:
    state_manager = ProjectStateManager()
    gate_validator = GateValidator(state_manager)

    async def _gate() -> None:
        state = await state_manager.load()

        if not state:
            console.print("[red]No project found.[/red]")
            return

        result = await gate_validator.run_go_no_go(state, phase)

        table = Table(title=f"Go/No-Go Decision: Phase {phase}")
        table.add_column("Check", style="cyan")
        table.add_column("Status", style="green")

        for check, passed in result["entry_validation"]["checks"].items():
            status = "[green]PASS[/green]" if passed else "[red]FAIL[/red]"
            table.add_row(f"Entry: {check}", status)

        for check, passed in result["exit_validation"]["checks"].items():
            status = "[green]PASS[/green]" if passed else "[red]FAIL[/red]"
            table.add_row(f"Exit: {check}", status)

        console.print(table)

        decision_color = "green" if result["decision"] == "GO" else "red"
        console.print(
            f"\nDecision: [bold {decision_color}]{result['decision']}[/bold {decision_color}]"
        )

    asyncio.run(_gate())


@main.command()
def agents() -> None:
    state_manager = ProjectStateManager()
    orchestrator = AgentOrchestrator(state_manager)

    async def _agents() -> None:
        state = await state_manager.load()

        if not state:
            console.print("[red]No project found.[/red]")
            return

        agents_list = await orchestrator.list_agents(state)

        table = Table(title="Agents")
        table.add_column("ID", style="cyan")
        table.add_column("Name", style="green")
        table.add_column("Phase", style="yellow")
        table.add_column("Status", style="magenta")
        table.add_column("Task", style="blue")

        for agent in agents_list:
            table.add_row(
                agent["id"],
                agent["name"],
                str(agent["phase"]) if agent["phase"] else "-",
                agent["status"],
                (
                    agent["current_task"][:30] + "..."
                    if agent["current_task"] and len(agent["current_task"]) > 30
                    else agent["current_task"] or "-"
                ),
            )

        console.print(table)

    asyncio.run(_agents())


@main.command()
@click.option("--standard", "-s", type=click.Choice(["hipaa", "soc2", "pci_dss", "gdpr"]))
def scan(standard: str | None) -> None:
    state_manager = ProjectStateManager()

    async def _scan() -> None:
        from octalume.compliance.scanner import ComplianceScanner
        from octalume.core.models import ComplianceStandard

        state = await state_manager.load()

        if not state:
            console.print("[red]No project found.[/red]")
            return

        scanner = ComplianceScanner()
        standards = [ComplianceStandard(standard)] if standard else state.compliance_standards

        if not standards:
            console.print("[yellow]No compliance standards configured.[/yellow]")
            return

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            progress.add_task("Scanning compliance...", total=None)

            result = await scanner.scan(state, standards, "all")

        console.print("\n[bold]Compliance Scan Results[/bold]")
        console.print(
            f"Overall Status: [bold {'green' if result['summary']['overall_status'] == 'compliant' else 'red'}]{result['summary']['overall_status']}[/bold]"
        )
        console.print(f"Total Findings: {result['summary']['total_findings']}")
        console.print(f"Critical: {result['summary']['critical_findings']}")

    asyncio.run(_scan())


@main.command()
@click.option("--host", "-h", default="0.0.0.0", help="Host to bind to")
@click.option("--port", "-p", default=8000, help="Port to bind to")
def dashboard(host: str, port: int) -> None:
    import uvicorn

    console.print(f"[bold green]Starting OCTALUME Dashboard on http://{host}:{port}[/bold green]")

    uvicorn.run(
        "web.backend.main:app",
        host=host,
        port=port,
        reload=True,
    )


@main.command()
def memory() -> None:
    memory_bank = MemoryBank()

    stats = memory_bank.get_statistics()

    console.print(
        Panel.fit(
            f"[bold]Memory Statistics[/bold]\n\n"
            f"Total Entries: {stats['total_entries']}\n"
            f"Decisions: {stats['decisions']}\n"
            f"Progress: {stats['progress']}\n"
            f"Blockers: {stats['blockers']}\n"
            f"Notes: {stats['notes']}",
            title="Memory Bank",
        )
    )

    table = Table(title="Recent Activity")
    table.add_column("Category", style="cyan")
    table.add_column("Key", style="green")
    table.add_column("Created", style="yellow")

    recent = memory_bank.query(limit=10)
    for entry in recent:
        table.add_row(
            entry["category"],
            entry["key"][:30],
            entry["entry"].get("created_at", "N/A")[:19],
        )

    console.print(table)


# ============================================================================
# Phase 0 — Idea (formerly octalum-bdtb, merged into OCTALUME)
# ============================================================================


def _read_idea_input(input_arg: str | None) -> str:
    """Read the brain-dump from a file path or stdin."""
    import sys
    from pathlib import Path

    if input_arg and input_arg != "-":
        p = Path(input_arg)
        if p.exists():
            return p.read_text(encoding="utf-8")
        return input_arg
    if not sys.stdin.isatty():
        return sys.stdin.read()
    raise click.UsageError(
        "No brain-dump provided. Pass a file path, a quoted string, or pipe text on stdin."
    )


def _ask_interactive() -> str:
    """Lightweight Q&A to assemble a dump for users who don't have one."""
    print("Interactive mode. Press Enter twice to finish each answer.\n")
    questions = [
        "1) In one sentence, what are you building?",
        "2) Who is it for?",
        "3) Top 3-5 features (one per line):",
        "4) Hard constraints (deadline, budget, regulatory)?",
        "5) What scares you / what could go wrong?",
        "6) Any open questions you don't know the answer to?",
    ]
    chunks: list[str] = []
    for q in questions:
        print(q)
        lines: list[str] = []
        while True:
            try:
                line = input()
            except EOFError:
                break
            if line == "" and lines and lines[-1] == "":
                break
            lines.append(line)
        chunks.append("\n".join(lines).strip())
        print()

    title = chunks[0].splitlines()[0] if chunks[0] else "Untitled Project"
    body = [f"# {title}", "", chunks[0], ""]
    if chunks[1]:
        body.append(f"Target users: {chunks[1]}")
    if chunks[2]:
        body.append("\n## Features\n")
        for line in chunks[2].splitlines():
            line = line.strip("-* \t")
            if line:
                body.append(f"- {line}")
    if chunks[3]:
        body.append("\n## Constraints\n")
        for line in chunks[3].splitlines():
            if line.strip():
                body.append(f"- {line.strip()}")
    if chunks[4]:
        body.append("\n## Risks\n")
        for line in chunks[4].splitlines():
            if line.strip():
                body.append(f"- risk: {line.strip()}")
    if chunks[5]:
        body.append("\n## Unknowns\n")
        for line in chunks[5].splitlines():
            if line.strip():
                q = line.strip()
                if not q.endswith("?"):
                    q += "?"
                body.append(f"- {q}")
    return "\n".join(body)


def _write_idea_artifacts(
    out_dir: Path,
    artifacts: dict[str, str],
    force: bool,
) -> list[str]:
    """Write idea artifacts to ``out_dir``. Returns list of written paths."""
    import os

    written: list[str] = []
    for name, content in artifacts.items():
        target = out_dir / name
        target.parent.mkdir(parents=True, exist_ok=True)
        if target.exists() and not force:
            console.print(f"  [dim]skip: {target} (exists; use --force to overwrite)[/dim]")
            continue
        target.write_text(content, encoding="utf-8")
        if name.endswith(".sh"):
            os.chmod(target, 0o755)
        written.append(str(target))
    return written


@main.group()
def idea() -> None:
    """Phase 0 — turn a raw brain-dump into a structured project plan."""


@idea.command()
@click.argument("input_str", required=False)
@click.option(
    "--output-dir", "-o", default="./plan", help="Directory to write generated artifacts."
)
@click.option(
    "--target",
    "-t",
    type=click.Choice(["spec-kit", "octalum-classic"]),
    default="spec-kit",
    help="Output shape.",
)
@click.option("--force", "-f", is_flag=True, help="Overwrite existing files.")
@click.option("--llm", metavar="MODEL", default=None, help="Optional LLM model for enrichment.")
def quick(
    input_str: str | None,
    output_dir: str,
    target: str,
    force: bool,
    llm: str | None,
) -> None:
    """Quick mode — parse a brain-dump and emit artifacts."""
    from octalume.idea.parser import parse_brain_dump
    from octalume.idea.speckit import render_all_speckit
    from octalume.idea.templates import render_all

    text = _read_idea_input(input_str)
    project = parse_brain_dump(text)

    if llm:
        console.print(
            f"[dim][--llm {llm}] enrichment not invoked: no SDK wired. "
            "See README > LLM enrichment.[/dim]"
        )

    out_dir = Path(output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    artifacts = render_all_speckit(project) if target == "spec-kit" else render_all(project)
    written = _write_idea_artifacts(out_dir, artifacts, force)

    console.print(f"\n[bold green]Project:[/bold green] {project.title}")
    console.print(f"[bold]Domain:[/bold]  {project.primary_domain}")
    console.print(f"[bold]Target:[/bold]  {target}")
    console.print(f"[bold]Wrote:[/bold]   {len(written)} file(s) \u2192 {out_dir}")
    for w in written:
        console.print(f"  [cyan]- {w}[/cyan]")

    if target == "spec-kit":
        console.print(
            f"\nNext: cd {out_dir} && open specs/{project.slug}/spec.md  "
            f"# then /speckit.plan, /speckit.tasks, /speckit.implement"
        )


@idea.command()
@click.argument("input_str", required=False)
@click.option(
    "--output-dir", "-o", default="./plan", help="Directory to write generated artifacts."
)
@click.option(
    "--target",
    "-t",
    type=click.Choice(["spec-kit", "octalum-classic"]),
    default="spec-kit",
    help="Output shape.",
)
@click.option("--force", "-f", is_flag=True, help="Overwrite existing files.")
def bootstrap(
    input_str: str | None,
    output_dir: str,
    target: str,
    force: bool,
) -> None:
    """Bootstrap mode — plan + runnable BUILD_NOW.sh (octalum-classic only)."""
    from octalume.idea.parser import parse_brain_dump
    from octalume.idea.templates import render_all

    text = _read_idea_input(input_str)
    project = parse_brain_dump(text)

    out_dir = Path(output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    artifacts = render_all(project)
    written = _write_idea_artifacts(out_dir, artifacts, force)

    console.print(f"\n[bold green]Project:[/bold green] {project.title}")
    console.print(f"[bold]Domain:[/bold]  {project.primary_domain}")
    console.print(f"[bold]Wrote:[/bold]   {len(written)} file(s) \u2192 {out_dir}")
    for w in written:
        console.print(f"  [cyan]- {w}[/cyan]")

    console.print(f"\nNext: bash {out_dir / 'BUILD_NOW.sh'}")


@idea.command()
@click.option(
    "--output-dir", "-o", default="./plan", help="Directory to write generated artifacts."
)
@click.option(
    "--target",
    "-t",
    type=click.Choice(["spec-kit", "octalum-classic"]),
    default="spec-kit",
    help="Output shape.",
)
@click.option("--force", "-f", is_flag=True, help="Overwrite existing files.")
def interactive(
    output_dir: str,
    target: str,
    force: bool,
) -> None:
    """Interactive mode — Q&A wizard to assemble the brain-dump."""
    from octalume.idea.parser import parse_brain_dump
    from octalume.idea.speckit import render_all_speckit
    from octalume.idea.templates import render_all

    text = _ask_interactive()
    project = parse_brain_dump(text)

    out_dir = Path(output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    artifacts = render_all_speckit(project) if target == "spec-kit" else render_all(project)
    written = _write_idea_artifacts(out_dir, artifacts, force)

    console.print(f"\n[bold green]Project:[/bold green] {project.title}")
    console.print(f"[bold]Domain:[/bold]  {project.primary_domain}")
    console.print(f"[bold]Target:[/bold]  {target}")
    console.print(f"[bold]Wrote:[/bold]   {len(written)} file(s) \u2192 {out_dir}")
    for w in written:
        console.print(f"  [cyan]- {w}[/cyan]")


@idea.command()
@click.argument("stage_num", type=click.IntRange(1, 12))
@click.argument("input_str", required=False)
@click.option(
    "--output-dir", "-o", default="./plan", help="Directory to write generated artifacts."
)
@click.option("--force", "-f", is_flag=True, help="Overwrite existing files.")
def stage(
    stage_num: int,
    input_str: str | None,
    output_dir: str,
    force: bool,
) -> None:
    """Run a specific pipeline stage (1-12)."""
    from octalume.idea.parser import parse_brain_dump
    from octalume.idea.pipeline import get_stage, run_stage_scaffold

    s = get_stage(stage_num)

    text = _read_idea_input(input_str)
    project = parse_brain_dump(text)

    scaffold = run_stage_scaffold(project, stage_num)

    table = Table(title=f"Stage {s.number} \u2014 {s.name}")
    table.add_column("Field", style="cyan")
    table.add_column("Value", style="green")
    table.add_row("Stage", f"{s.number} \u2014 {s.name}")
    table.add_row("Layer", s.layer)
    table.add_row("Skill File", s.skill_file)
    table.add_row("Expected Output", s.output_file)
    table.add_row("Description", s.description)
    table.add_row("Project", project.title)
    table.add_row("Domain", project.primary_domain)
    console.print(table)

    console.print(f"\n[bold yellow]{scaffold['approval_prompt']}[/bold yellow]")
    console.print(f"\n[dim]Load the Claude Code Skill: .claude/skills/idea/{s.skill_file}[/dim]")

    if stage_num <= 5:
        from octalume.idea.speckit import render_all_speckit

        out_dir = Path(output_dir)
        out_dir.mkdir(parents=True, exist_ok=True)
        artifacts = render_all_speckit(project)
        written = _write_idea_artifacts(out_dir, artifacts, force)
        if written:
            console.print(f"\n[bold]Wrote:[/bold] {len(written)} file(s) \u2192 {out_dir}")
    else:
        console.print(
            "\n[dim]Stages 6\u201312 are LLM-driven. Use the Claude Code Skill "
            "(.claude/skills/idea/) to execute.[/dim]"
        )


@idea.command()
def stages() -> None:
    """List all 12 pipeline stages."""
    from octalume.idea.pipeline import list_stages

    table = Table(title="Idea Pipeline \u2014 12 Stages")
    table.add_column("#", style="cyan", width=3)
    table.add_column("Name", style="green")
    table.add_column("Layer", style="yellow")
    table.add_column("Output", style="blue")
    table.add_column("Description", style="dim")

    for s in list_stages():
        table.add_row(
            s["number"],
            s["name"],
            s["layer"],
            s["output_file"],
            s["description"][:60],
        )

    console.print(table)


if __name__ == "__main__":
    main()
