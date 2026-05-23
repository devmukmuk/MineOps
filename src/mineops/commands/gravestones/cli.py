# src/mineops/commands/gravestones/cli.py

"""Typer CLI commands for Minecraft gravestone reports."""

from pathlib import Path

import typer
from rich.console import Console

from mineops.config.settings import load_settings
from mineops.services.gravestones.gravestone_service import GravestoneService


app = typer.Typer(help="Minecraft gravestone log tools.")

console = Console()


@app.command("scan")
def scan_command(
    log_folder: Path | None = typer.Argument(
        None,
        exists=True,
        file_okay=False,
        dir_okay=True,
        readable=True,
        help="Folder containing Minecraft server logs. Uses config default when omitted.",
    ),
    player: str | None = typer.Option(
        None,
        "--player",
        "-p",
        help="Optional player filter.",
    ),
    not_found_only: bool = typer.Option(
        False,
        "--not-found-only",
        help="Only show gravestones that have not been found.",
    ),
) -> None:
    """Scan Minecraft logs for gravestones."""
    settings = load_settings()

    resolved_server_log_folder = log_folder or settings.minecraft.server_logs_root

    if resolved_server_log_folder is None:
        raise typer.BadParameter(
            "log_folder is required when server_logs_root is not configured."
        )

    service = GravestoneService()
    result = service.scan_logs(
        log_folder=resolved_server_log_folder,
        player=player,
    )

    report_name = player if player else "all players"

    console.print()
    console.print(f"Gravestone report for [bold]{report_name}[/bold]")
    console.print("=" * 60)
    console.print(f"Log folder: {resolved_server_log_folder}")
    console.print(f"Placed:    {len(result.placed)}")
    console.print(f"Found:     {len(result.found)}")
    console.print(f"Not found: {len(result.missing)}")

    if result.warnings:
        console.print()
        console.print("[yellow]Warnings[/yellow]")
        console.print("-" * 60)

        for warning in result.warnings:
            console.print(warning)

    console.print()
    console.print("[bold red]NOT FOUND[/bold red]")
    console.print("-" * 60)

    for grave in result.missing:
        x, y, z = grave.coord
        console.print(
            f"{grave.player}  "
            f"{grave.time}  "
            f"{grave.dimension}  "
            f"({x}, {y}, {z})  "
            f"file={grave.file}"
        )

    if not not_found_only:
        console.print()
        console.print("[bold green]FOUND[/bold green]")
        console.print("-" * 60)

        for grave in result.found:
            x, y, z = grave.coord
            found_entry = grave.found_entries[0]
            console.print(
                f"{grave.player}  "
                f"{grave.time}  "
                f"{grave.dimension}  "
                f"({x}, {y}, {z})  "
                f"found at {found_entry.time}  "
                f"file={grave.file}"
            )
