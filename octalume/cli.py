#!/usr/bin/env python3

import asyncio

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

        console.print(Panel.fit(
            f"[bold green]Project initialized![/bold green]\n\n"
            f"Name: {state.name}\n"
            f"ID: {state.id}\n"
            f"Compliance: {', '.join(c.value for c in state.compliance_standards) or 'None'}\n"
            f"State: {state_manager.state_file}",
            title="OCTALUME",
        ))

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
        console.print(f"\nDecision: [bold {decision_color}]{result['decision']}[/bold {decision_color}]")

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
                agent["current_task"][:30] + "..." if agent["current_task"] and len(agent["current_task"]) > 30 else agent["current_task"] or "-",
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
        console.print(f"Overall Status: [bold {'green' if result['summary']['overall_status'] == 'compliant' else 'red'}]{result['summary']['overall_status']}[/bold]")
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

    console.print(Panel.fit(
        f"[bold]Memory Statistics[/bold]\n\n"
        f"Total Entries: {stats['total_entries']}\n"
        f"Decisions: {stats['decisions']}\n"
        f"Progress: {stats['progress']}\n"
        f"Blockers: {stats['blockers']}\n"
        f"Notes: {stats['notes']}",
        title="Memory Bank",
    ))

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


if __name__ == "__main__":
    main()
