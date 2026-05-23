# tests/services/test_gravestone_service.py

"""Tests for Minecraft gravestone log scanning."""

import gzip
from pathlib import Path

from mineops.services.gravestones.gravestone_service import GravestoneService


def test_scan_logs_detects_placed_gravestone(tmp_path: Path) -> None:
    """Scan logs and detect a placed gravestone."""
    log_file = tmp_path / "latest.log"
    log_file.write_text(
        "[12:00:01] [Server thread/INFO]: Placed MohawkBoy6's Gravestone at "
        "(10, 64, -20) in minecraft:overworld\n",
        encoding="utf-8",
    )

    result = GravestoneService().scan_logs(tmp_path)

    assert len(result.placed) == 1
    assert len(result.missing) == 1
    assert result.placed[0].player == "MohawkBoy6"
    assert result.placed[0].coord == (10, 64, -20)
    assert result.placed[0].dimension == "minecraft:overworld"


def test_scan_logs_detects_found_gravestone_after_placed_event(tmp_path: Path) -> None:
    """Scan logs and classify a later found grave as found."""
    log_file = tmp_path / "latest.log"
    log_file.write_text(
        "\n".join(
            [
                "[12:00:01] [Server thread/INFO]: Placed MohawkBoy6's Gravestone at "
                "(10, 64, -20) in minecraft:overworld",
                "[12:05:01] [Server thread/INFO]: MohawkBoy6 has found a grave at "
                "(10, 64, -20)",
            ]
        ),
        encoding="utf-8",
    )

    result = GravestoneService().scan_logs(tmp_path)

    assert len(result.placed) == 1
    assert len(result.found) == 1
    assert len(result.missing) == 0
    assert result.found[0].found_entries[0].time == "12:05:01"


def test_scan_logs_ignores_found_event_before_placed_event(tmp_path: Path) -> None:
    """Ignore found events that happened before the placed grave event."""
    log_file = tmp_path / "latest.log"
    log_file.write_text(
        "\n".join(
            [
                "[12:00:01] [Server thread/INFO]: MohawkBoy6 has found a grave at "
                "(10, 64, -20)",
                "[12:05:01] [Server thread/INFO]: Placed MohawkBoy6's Gravestone at "
                "(10, 64, -20) in minecraft:overworld",
            ]
        ),
        encoding="utf-8",
    )

    result = GravestoneService().scan_logs(tmp_path)

    assert len(result.placed) == 1
    assert len(result.found) == 0
    assert len(result.missing) == 1


def test_scan_logs_filters_player_case_insensitive(tmp_path: Path) -> None:
    """Filter gravestone results by player name case-insensitively."""
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

    result = GravestoneService().scan_logs(tmp_path, player="mohawkboy6")

    assert len(result.placed) == 1
    assert result.placed[0].player == "MohawkBoy6"


def test_scan_logs_reads_gzipped_logs(tmp_path: Path) -> None:
    """Scan gzipped Minecraft log files."""
    log_file = tmp_path / "latest.log.gz"

    with gzip.open(log_file, "wt", encoding="utf-8") as file:
        file.write(
            "[12:00:01] [Server thread/INFO]: Placed MohawkBoy6's Gravestone at "
            "(10, 64, -20) in minecraft:overworld\n"
        )

    result = GravestoneService().scan_logs(tmp_path)

    assert len(result.placed) == 1
    assert result.placed[0].file == "latest.log.gz"
