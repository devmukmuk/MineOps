"""Minecraft server path resolution helpers."""

from pathlib import Path
from typing import Any


def get_server_config(
    settings: Any,
    server_id: str,
) -> dict:
    """Return the configured Minecraft server definition."""

    servers = settings.minecraft.servers

    if server_id not in servers:
        available = ", ".join(sorted(servers.keys()))

        raise ValueError(
            f"Unknown server_id '{server_id}'. "
            f"Available servers: {available}"
        )

    return servers[server_id]


def iter_servers(
    settings: Any,
    include_active: bool = True,
    include_inactive: bool = False,
) -> list[tuple[str, dict]]:
    """Return configured servers filtered by status."""

    results: list[tuple[str, dict]] = []

    for server_id, server in settings.minecraft.servers.items():
        status = str(server.get("status", "")).lower()

        if status == "active" and include_active:
            results.append((server_id, server))

        elif status == "inactive" and include_inactive:
            results.append((server_id, server))

    return results


def resolve_servers_root(
    settings: Any,
) -> Path:
    """Resolve the Minecraft servers root path."""

    return Path(settings.minecraft.servers_root)


def resolve_server_root(
    settings: Any,
    server_id: str,
) -> Path:
    """Resolve a Minecraft server root path."""

    server = get_server_config(settings, server_id)

    return (
        resolve_servers_root(settings)
        / server["folder"]
    )


def resolve_server_logs_path(
    settings: Any,
    server_id: str,
) -> Path:
    """Resolve a Minecraft server logs path."""

    server = get_server_config(settings, server_id)

    return (
        resolve_server_root(settings, server_id)
        / server["logs_folder"]
    )

def resolve_world_path(
    settings: Any,
    server_id: str,
) -> Path:
    """Resolve a Minecraft server world path."""

    server = get_server_config(settings, server_id)

    return (
        resolve_server_root(settings, server_id)
        / server["world_folder"]
    )


def resolve_all_server_roots(
    settings: Any,
    include_active: bool = True,
    include_inactive: bool = False,
) -> list[Path]:
    """Resolve all configured Minecraft server roots."""

    return [
        resolve_server_root(settings, server_id)
        for server_id, _server
        in iter_servers(
            settings,
            include_active=include_active,
            include_inactive=include_inactive,
        )
    ]


def resolve_all_world_paths(
    settings: Any,
    include_active: bool = True,
    include_inactive: bool = False,
) -> list[Path]:
    """Resolve all configured Minecraft world paths."""

    return [
        resolve_world_path(settings, server_id)
        for server_id, _server
        in iter_servers(
            settings,
            include_active=include_active,
            include_inactive=include_inactive,
        )
    ]
