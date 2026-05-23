from pathlib import Path

import typer
from rich.console import Console
from rich.table import Table

from mineops import __version__

app = typer.Typer(
    help="MineOps - Minecraft utility scripts and tools."
)

console = Console()


@app.command()
def about() -> None:
    """
    Show MineOps application information.
    """

    project_root = Path.cwd()

    table = Table(title="MineOps")

    table.add_column("Setting", style="cyan")
    table.add_column("Value", style="green")

    table.add_row("Version", __version__)
    table.add_row("Project Root", str(project_root))
    table.add_row("Python Package", "mineops")

    console.print(table)


if __name__ == "__main__":
    app()
