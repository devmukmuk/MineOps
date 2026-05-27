"""Typer CLI commands for Minecraft user reports."""

import typer
from rich.console import Console
from rich.table import Table

from mineops.config.settings import load_settings
from mineops.services.user_report_service import ServerUserReport, UserReportService


app = typer.Typer(
    help="Minecraft user report tools.",
    no_args_is_help=True,
)

console = Console()


@app.command("report")
def report_command() -> None:
    """Show Minecraft users by active and inactive servers."""

    settings = load_settings()

    service = UserReportService()
    report = service.build_report(settings)

    console.print()
    console.print("[bold]Minecraft User Report[/bold]")

    _print_group("Active Servers", report.active_servers)
    _print_group("Inactive Servers", report.inactive_servers)


def _print_group(
    title: str,
    servers: list[ServerUserReport],
) -> None:
    """Print a grouped server user report."""

    console.print()
    console.print(f"[bold]{title}[/bold]")
    console.print("=" * 60)

    if not servers:
        console.print("No servers found.")
        return

    for server in servers:
        console.print()
        console.print(f"[bold]{server.server_id}[/bold] - {server.server_name}")
        console.print(f"Logs: {server.log_folder}")

        for warning in server.warnings:
            console.print(f"[yellow]{warning}[/yellow]")

        if not server.users:
            console.print("No users found.")
            continue

        table = Table(show_header=True)
        table.add_column("Player")
        table.add_column("First Seen")
        table.add_column("Latest Seen")

        for user in sorted(server.users.values(), key=lambda item: item.player.lower()):
            table.add_row(
                user.player,
                user.first_seen.isoformat(),
                user.latest_seen.isoformat(),
            )

        console.print(table)
