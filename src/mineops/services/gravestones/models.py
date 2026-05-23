# src/mineops/services/gravestones/models.py

"""Models for Minecraft gravestone log scanning."""

from dataclasses import dataclass, field


Coord = tuple[int, int, int]


@dataclass(frozen=True)
class FoundGrave:
    """A gravestone found event from a server log."""

    file: str
    line_number: int
    event_number: int
    time: str
    player: str
    coord: Coord
    line: str


@dataclass
class PlacedGrave:
    """A gravestone placed event from a server log."""

    file: str
    line_number: int
    event_number: int
    time: str
    player: str
    coord: Coord
    dimension: str
    line: str
    found_entries: list[FoundGrave] = field(default_factory=list)


@dataclass
class GravestoneScanResult:
    """Results from scanning Minecraft server logs for gravestones."""

    placed: list[PlacedGrave] = field(default_factory=list)
    found: list[PlacedGrave] = field(default_factory=list)
    missing: list[PlacedGrave] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
