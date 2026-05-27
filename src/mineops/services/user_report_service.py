"""Build Minecraft user activity reports from server logs."""

from __future__ import annotations

import gzip
import re
from dataclasses import dataclass, field
from datetime import date, datetime
from pathlib import Path
from typing import Iterable

from mineops.services.minecraft_paths import iter_servers, resolve_server_logs_path


LOG_DATE_PATTERN = re.compile(r"(?P<date>\d{4}-\d{2}-\d{2})")
PLAYER_EVENT_PATTERN = re.compile(
    r"\]: (?P<player>[A-Za-z0-9_]+) (?P<event>joined|left) the game"
)


@dataclass
class UserActivity:
    """Store first and latest observed play dates for a user."""

    player: str
    first_seen: date
    latest_seen: date


@dataclass
class ServerUserReport:
    """Store user activity for one Minecraft server."""

    server_id: str
    server_name: str
    status: str
    log_folder: Path
    users: dict[str, UserActivity] = field(default_factory=dict)
    warnings: list[str] = field(default_factory=list)


@dataclass
class UserReport:
    """Store grouped user activity for configured Minecraft servers."""

    active_servers: list[ServerUserReport] = field(default_factory=list)
    inactive_servers: list[ServerUserReport] = field(default_factory=list)


class UserReportService:
    """Build Minecraft user reports from configured server logs."""

    def build_report(
        self,
        settings,
        include_active: bool = True,
        include_inactive: bool = True,
    ) -> UserReport:
        """Build a user report for configured Minecraft servers."""

        report = UserReport()

        for server_id, server in iter_servers(
            settings,
            include_active=include_active,
            include_inactive=include_inactive,
        ):
            server_report = self.build_server_report(
                settings=settings,
                server_id=server_id,
                server=server,
            )

            if server_report.status == "active":
                report.active_servers.append(server_report)
            else:
                report.inactive_servers.append(server_report)

        return report

    def build_server_report(
        self,
        settings,
        server_id: str,
        server: dict,
    ) -> ServerUserReport:
        """Build a user report for one configured Minecraft server."""

        log_folder = resolve_server_logs_path(settings, server_id)

        report = ServerUserReport(
            server_id=server_id,
            server_name=str(server.get("name", server_id)),
            status=str(server.get("status", "inactive")).lower(),
            log_folder=log_folder,
        )

        if not log_folder.exists():
            report.warnings.append(f"Log folder does not exist: {log_folder}")
            return report

        for log_file in self._iter_log_files(log_folder):
            log_date = self._date_for_log_file(log_file)

            for player in self._players_from_log_file(log_file):
                self._record_user_activity(report, player, log_date)

        return report

    def _iter_log_files(self, log_folder: Path) -> Iterable[Path]:
        """Return Minecraft log files from a log folder."""

        yield from sorted(log_folder.glob("*.log"))
        yield from sorted(log_folder.glob("*.log.gz"))

    def _date_for_log_file(self, log_file: Path) -> date:
        """Return the best available date for a log file."""

        match = LOG_DATE_PATTERN.search(log_file.name)

        if match:
            return date.fromisoformat(match.group("date"))

        modified_at = datetime.fromtimestamp(log_file.stat().st_mtime)
        return modified_at.date()

    def _players_from_log_file(self, log_file: Path) -> Iterable[str]:
        """Yield player names found in a Minecraft log file."""

        opener = gzip.open if log_file.suffix == ".gz" else open

        with opener(log_file, "rt", encoding="utf-8", errors="ignore") as file:
            for line in file:
                match = PLAYER_EVENT_PATTERN.search(line)

                if match:
                    yield match.group("player")

    def _record_user_activity(
        self,
        report: ServerUserReport,
        player: str,
        played_on: date,
    ) -> None:
        """Record player activity for one date."""

        existing = report.users.get(player)

        if existing is None:
            report.users[player] = UserActivity(
                player=player,
                first_seen=played_on,
                latest_seen=played_on,
            )
            return

        existing.first_seen = min(existing.first_seen, played_on)
        existing.latest_seen = max(existing.latest_seen, played_on)
