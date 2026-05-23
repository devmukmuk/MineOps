"""MineOps command-line interface."""

from __future__ import annotations

import typer
from rich.console import Console

from mineops.config import load_settings

from mineops.commands.gravestones.cli import app as gravestones_app


app = typer.Typer(
    help="MineOps command-line tools.",
    invoke_without_command=True,
)

app.add_typer(
    gravestones_app,
    name="gravestones",
)

console = Console()


@app.callback()
def main(ctx: typer.Context) -> None:
    """Run MineOps."""

    if ctx.invoked_subcommand is None:
        about()


@app.command()
def about() -> None:
    """Print MineOps environment details."""

    settings = load_settings()

    console.print("[bold]MineOps[/bold]")
    console.print(f"Server ID: {settings.server_id}")
    console.print()

    console.print("[bold]Config[/bold]")
    console.print(f"Path: {settings.metadata.config_path}")
    console.print(f"Source: {settings.metadata.config_source}")
    console.print(f"Defaults Created: {settings.metadata.defaults_created}")
    console.print()

    console.print("[bold]Resolved Paths[/bold]")
    console.print(f"Data Root: {settings.data_root}")
    console.print(f"Metadata Root: {settings.metadata_root}")
    console.print(f"Backups Root: {settings.backups_root}")
    console.print(f"Logs Root: {settings.logs_root}")
    console.print()
    
    console.print("[bold]Minecraft[/bold]")
    console.print(f"Server Logs Root: {settings.minecraft.server_logs_root}")
