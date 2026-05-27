"""MineOps command-line interface."""

from __future__ import annotations

import typer
from rich.console import Console

from mineops.config import load_settings

from mineops.commands.gravestones.cli import app as gravestones_app
from mineops.commands.users.cli import app as users_app


from mineops.services.minecraft_paths import (
    iter_servers,
    resolve_server_logs_path,
    resolve_server_root,
    resolve_world_path,
)


app = typer.Typer(
    help="MineOps command-line tools.",
    invoke_without_command=True,
)

app.add_typer(
    gravestones_app,
    name="gravestones",
)

app.add_typer(users_app, name="users")

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
    console.print(
        f"Defaults Created: "
        f"{settings.metadata.defaults_created}"
    )
    console.print()

    console.print("[bold]Resolved Paths[/bold]")
    console.print(f"Data Root: {settings.data_root}")
    console.print(f"Metadata Root: {settings.metadata_root}")
    console.print(f"Backups Root: {settings.backups_root}")
    console.print(f"Logs Root: {settings.logs_root}")
    console.print()

    console.print("[bold]Minecraft[/bold]")
    console.print(
        f"Servers Root: "
        f"{settings.minecraft.servers_root}"
    )
    console.print(
        f"Default Server: "
        f"{settings.minecraft.default_server_id}"
    )
    console.print()

    active_servers = iter_servers(
        settings,
        include_active=True,
        include_inactive=False,
    )

    inactive_servers = iter_servers(
        settings,
        include_active=False,
        include_inactive=True,
    )

    console.print("[bold]Active Servers[/bold]")

    if active_servers:
        for server_id, server in active_servers:
            console.print(f"- {server_id}")
            console.print(
                f"  Name: {server['name']}"
            )
            console.print(
                f"  Root: "
                f"{resolve_server_root(settings, server_id)}"
            )
            console.print(
                f"  World: "
                f"{resolve_world_path(settings, server_id)}"
            )
            console.print(
                f"  Logs: "
                f"{resolve_server_logs_path(settings, server_id)}"
            )
    else:
        console.print("- None")

    console.print()

    console.print("[bold]Inactive Servers[/bold]")

    if inactive_servers:
        for server_id, server in inactive_servers:
            console.print(f"- {server_id}")
            console.print(
                f"  Name: {server['name']}"
            )
            console.print(
                f"  Root: "
                f"{resolve_server_root(settings, server_id)}"
            )
            console.print(
                f"  World: "
                f"{resolve_world_path(settings, server_id)}"
            )
            console.print(
                f"  Logs: "
                f"{resolve_server_logs_path(settings, server_id)}"
            )
    else:
        console.print("- None")
