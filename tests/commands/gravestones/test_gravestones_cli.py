# tests/commands/test_gravestones_cli.py

"""Tests for gravestone CLI commands."""

from pathlib import Path

from typer.testing import CliRunner

from mineops.cli import app


runner = CliRunner()


def test_gravestones_scan_command(tmp_path: Path) -> None:
    """Run the gravestones scan command."""
    log_file = tmp_path / "latest.log"

    log_file.write_text(
        "[12:00:01] [Server thread/INFO]: Placed MohawkBoy6's Gravestone at "
        "(10, 64, -20) in minecraft:overworld\n",
        encoding="utf-8",
    )

    result = runner.invoke(
        app,
        [
            "gravestones",
            "scan",
            str(tmp_path),
        ],
    )

    assert "Gravestone report" in result.stdout
    assert "Placed:" in result.stdout
    assert "Found:" in result.stdout
    assert "Not found:" in result.stdout
    assert "MohawkBoy6" in result.stdout


def test_gravestones_scan_command_player_filter(tmp_path: Path) -> None:
    """Filter gravestone CLI output by player."""
    log_file = tmp_path / "latest.log"

    log_file.write_text(
        "\n".join(
            [
                "[12:00:01] [Server thread/INFO]: Placed MohawkBoy6's Gravestone at "
                "(10, 64, -20) in minecraft:overworld",
                "[12:00:02] [Server thread/INFO]: Placed OtherPlayer's Gravestone at "
                "(1, 2, 3) in minecraft:overworld",
            ]
        ),
        encoding="utf-8",
    )

    result = runner.invoke(
        app,
        [
            "gravestones",
            "scan",
            str(tmp_path),
            "--player",
            "MohawkBoy6",
        ],
    )

    assert "Gravestone report" in result.stdout
    assert "Placed:" in result.stdout
    assert "Found:" in result.stdout
    assert "Not found:" in result.stdout
    assert "MohawkBoy6" in result.stdout
