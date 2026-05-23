# src/mineops/services/gravestones/gravestone_service.py

"""Scan Minecraft server logs for gravestone events."""

from __future__ import annotations

import gzip
import re
from collections import defaultdict
from pathlib import Path

from mineops.services.gravestones.models import Coord, FoundGrave, GravestoneScanResult, PlacedGrave


PLACED_RE = re.compile(
    r"\[(?P<time>\d\d:\d\d:\d\d)\].*INFO\]: Placed (?P<player>.+?)'s Gravestone at "
    r"\((?P<x>-?\d+),\s*(?P<y>-?\d+),\s*(?P<z>-?\d+)\) in (?P<dim>[\w:]+)"
)

FOUND_RE = re.compile(
    r"\[(?P<time>\d\d:\d\d:\d\d)\].*INFO\]: (?P<player>\S+) has found .*grave at "
    r"\((?P<x>-?\d+),\s*(?P<y>-?\d+),\s*(?P<z>-?\d+)\)"
)


class GravestoneService:
    """Scan Minecraft logs for placed and found gravestones."""

    def scan_logs(self, log_folder: Path, player: str | None = None) -> GravestoneScanResult:
        """Scan log files and return gravestone results."""
        result = GravestoneScanResult()
        found_by_key: dict[tuple[str, Coord], list[FoundGrave]] = defaultdict(list)

        event_number = 0

        for file_path in self._iter_log_files(log_folder):
            try:
                text = self._read_log_file(file_path)
            except OSError as exc:
                result.warnings.append(f"Could not read {file_path}: {exc}")
                continue

            for line_number, line in enumerate(text.splitlines(), start=1):
                event_number += 1

                placed_match = PLACED_RE.search(line)
                if placed_match:
                    placed_player = placed_match.group("player")

                    if self._player_matches(placed_player, player):
                        result.placed.append(
                            PlacedGrave(
                                file=file_path.name,
                                line_number=line_number,
                                event_number=event_number,
                                time=placed_match.group("time"),
                                player=placed_player,
                                coord=self._coord_key(placed_match),
                                dimension=placed_match.group("dim"),
                                line=line,
                            )
                        )

                found_match = FOUND_RE.search(line)
                if found_match:
                    found_player = found_match.group("player")

                    if self._player_matches(found_player, player):
                        found_grave = FoundGrave(
                            file=file_path.name,
                            line_number=line_number,
                            event_number=event_number,
                            time=found_match.group("time"),
                            player=found_player,
                            coord=self._coord_key(found_match),
                            line=line,
                        )

                        key = (found_player.lower(), found_grave.coord)
                        found_by_key[key].append(found_grave)

        self._classify_graves(result, found_by_key)
        return result

    def _classify_graves(
        self,
        result: GravestoneScanResult,
        found_by_key: dict[tuple[str, Coord], list[FoundGrave]],
    ) -> None:
        """Classify placed graves as found or missing."""
        for grave in result.placed:
            key = (grave.player.lower(), grave.coord)

            matching_found = sorted(
                [
                    entry
                    for entry in found_by_key.get(key, [])
                    if entry.event_number > grave.event_number
                ],
                key=lambda entry: entry.event_number,
            )

            if matching_found:
                grave.found_entries = [matching_found[0]]
                result.found.append(grave)
            else:
                result.missing.append(grave)

    def _iter_log_files(self, log_folder: Path) -> list[Path]:
        """Return supported log files in scan order."""
        return sorted(
            list(log_folder.glob("*.log"))
            + list(log_folder.glob("*.log.gz"))
            + list(log_folder.glob("*.txt"))
        )

    def _read_log_file(self, file_path: Path) -> str:
        """Read a plain text or gzipped log file."""
        if file_path.suffix == ".gz":
            with gzip.open(file_path, "rt", encoding="utf-8", errors="replace") as file:
                return file.read()

        return file_path.read_text(encoding="utf-8", errors="replace")

    def _coord_key(self, match: re.Match[str]) -> Coord:
        """Return a coordinate tuple from a regex match."""
        return (
            int(match.group("x")),
            int(match.group("y")),
            int(match.group("z")),
        )

    def _player_matches(self, log_player: str, requested_player: str | None) -> bool:
        """Return whether a log player matches the requested player."""
        if requested_player is None:
            return True

        return log_player.lower() == requested_player.lower()
