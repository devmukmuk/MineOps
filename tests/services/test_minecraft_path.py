"""Tests for Minecraft server path resolution helpers."""

from pathlib import Path
from types import SimpleNamespace

import pytest

from mineops.services.minecraft_paths import (
    get_server_config,
    iter_servers,
    resolve_all_server_roots,
    resolve_all_world_paths,
    resolve_server_logs_path,
    resolve_server_root,
    resolve_servers_root,
    resolve_world_path,
)


def make_settings() -> SimpleNamespace:
    """Create test settings."""

    return SimpleNamespace(
        minecraft=SimpleNamespace(
            servers_root="Z:\\",
            servers={
                "gravestone_26_1_2": {
                    "name": "Gravestone 26.1.2",
                    "status": "active",
                    "folder": "gravestone_26_1_2",
                    "world_folder": "world",
                    "logs_folder": "logs",
                },
                "arbor_1_21_10": {
                    "name": "Arbor 1.21.10",
                    "status": "inactive",
                    "folder": "arbor_1_21_10",
                    "world_folder": "world",
                    "logs_folder": "logs",
                },
            },
        )
    )


def test_get_server_config_returns_configured_server() -> None:
    """Verify a configured server can be returned."""

    settings = make_settings()

    server = get_server_config(settings, "gravestone_26_1_2")

    assert server["name"] == "Gravestone 26.1.2"
    assert server["status"] == "active"
    assert server["folder"] == "gravestone_26_1_2"


def test_get_server_config_raises_for_unknown_server() -> None:
    """Verify unknown server ids raise a helpful error."""

    settings = make_settings()

    with pytest.raises(ValueError) as exc_info:
        get_server_config(settings, "missing_server")

    assert "Unknown server_id 'missing_server'" in str(exc_info.value)
    assert "gravestone_26_1_2" in str(exc_info.value)
    assert "arbor_1_21_10" in str(exc_info.value)


def test_iter_servers_defaults_to_active_only() -> None:
    """Verify server iteration defaults to active servers only."""

    settings = make_settings()

    servers = iter_servers(settings)

    assert servers == [
        (
            "gravestone_26_1_2",
            settings.minecraft.servers["gravestone_26_1_2"],
        )
    ]


def test_iter_servers_can_include_active_and_inactive() -> None:
    """Verify server iteration can include all statuses."""

    settings = make_settings()

    servers = iter_servers(
        settings,
        include_active=True,
        include_inactive=True,
    )

    assert servers == [
        (
            "gravestone_26_1_2",
            settings.minecraft.servers["gravestone_26_1_2"],
        ),
        (
            "arbor_1_21_10",
            settings.minecraft.servers["arbor_1_21_10"],
        ),
    ]


def test_iter_servers_can_return_inactive_only() -> None:
    """Verify server iteration can return inactive servers only."""

    settings = make_settings()

    servers = iter_servers(
        settings,
        include_active=False,
        include_inactive=True,
    )

    assert servers == [
        (
            "arbor_1_21_10",
            settings.minecraft.servers["arbor_1_21_10"],
        )
    ]


def test_resolve_servers_root() -> None:
    """Verify the configured Minecraft servers root is resolved."""

    settings = make_settings()

    assert resolve_servers_root(settings) == Path("Z:\\")


def test_resolve_server_root() -> None:
    """Verify a server root path is resolved."""

    settings = make_settings()

    assert resolve_server_root(
        settings,
        "gravestone_26_1_2",
    ) == Path("Z:\\") / "gravestone_26_1_2"


def test_resolve_server_logs_path() -> None:
    """Verify a server logs path is resolved."""

    settings = make_settings()

    assert resolve_server_logs_path(
        settings,
        "gravestone_26_1_2",
    ) == Path("Z:\\") / "gravestone_26_1_2" / "logs"


def test_resolve_world_path() -> None:
    """Verify a server world path is resolved."""

    settings = make_settings()

    assert resolve_world_path(
        settings,
        "gravestone_26_1_2",
    ) == Path("Z:\\") / "gravestone_26_1_2" / "world"


def test_resolve_all_server_roots_defaults_to_active_only() -> None:
    """Verify all server roots default to active servers only."""

    settings = make_settings()

    assert resolve_all_server_roots(settings) == [
        Path("Z:\\") / "gravestone_26_1_2",
    ]


def test_resolve_all_server_roots_can_include_inactive() -> None:
    """Verify all server roots can include inactive servers."""

    settings = make_settings()

    assert resolve_all_server_roots(
        settings,
        include_active=True,
        include_inactive=True,
    ) == [
        Path("Z:\\") / "gravestone_26_1_2",
        Path("Z:\\") / "arbor_1_21_10",
    ]


def test_resolve_all_world_paths_defaults_to_active_only() -> None:
    """Verify all world paths default to active servers only."""

    settings = make_settings()

    assert resolve_all_world_paths(settings) == [
        Path("Z:\\") / "gravestone_26_1_2" / "world",
    ]


def test_resolve_all_world_paths_can_include_inactive() -> None:
    """Verify all world paths can include inactive servers."""

    settings = make_settings()

    assert resolve_all_world_paths(
        settings,
        include_active=True,
        include_inactive=True,
    ) == [
        Path("Z:\\") / "gravestone_26_1_2" / "world",
        Path("Z:\\") / "arbor_1_21_10" / "world",
    ]
