"""Tests for Minecraft user report service."""

from pathlib import Path
from types import SimpleNamespace

from mineops.services.user_report_service import UserReportService


def make_settings(tmp_path: Path) -> SimpleNamespace:
    """Create test settings."""

    return SimpleNamespace(
        minecraft=SimpleNamespace(
            servers_root=tmp_path,
            servers={
                "active_server": {
                    "name": "Active Server",
                    "status": "active",
                    "folder": "active_server",
                    "world_folder": "world",
                    "logs_folder": "logs",
                },
                "inactive_server": {
                    "name": "Inactive Server",
                    "status": "inactive",
                    "folder": "inactive_server",
                    "world_folder": "world",
                    "logs_folder": "logs",
                },
            },
        )
    )


def test_user_report_groups_active_and_inactive_servers(tmp_path: Path) -> None:
    """Verify user report groups active and inactive servers."""

    active_logs = tmp_path / "active_server" / "logs"
    inactive_logs = tmp_path / "inactive_server" / "logs"

    active_logs.mkdir(parents=True)
    inactive_logs.mkdir(parents=True)

    (active_logs / "2026-05-01-1.log").write_text(
        "[12:00:01] [Server thread/INFO]: MohawkBoy6 joined the game\n",
        encoding="utf-8",
    )

    (active_logs / "2026-05-27-1.log").write_text(
        "[12:00:01] [Server thread/INFO]: MohawkBoy6 left the game\n",
        encoding="utf-8",
    )

    (inactive_logs / "2025-09-10-1.log").write_text(
        "[12:00:01] [Server thread/INFO]: OldPlayer joined the game\n",
        encoding="utf-8",
    )

    settings = make_settings(tmp_path)

    report = UserReportService().build_report(settings)

    active_server = report.active_servers[0]
    inactive_server = report.inactive_servers[0]

    active_user = active_server.users["MohawkBoy6"]
    inactive_user = inactive_server.users["OldPlayer"]

    assert active_server.server_id == "active_server"
    assert active_user.first_seen.isoformat() == "2026-05-01"
    assert active_user.latest_seen.isoformat() == "2026-05-27"

    assert inactive_server.server_id == "inactive_server"
    assert inactive_user.first_seen.isoformat() == "2025-09-10"
    assert inactive_user.latest_seen.isoformat() == "2025-09-10"
