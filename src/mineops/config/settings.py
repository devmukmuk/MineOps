"""Load MineOps configuration settings."""

from __future__ import annotations

import os
import sys
from dataclasses import dataclass
from pathlib import Path

import yaml


CONFIG_FILE_NAMES = ("config.yaml", "config.yml", "config.ini")


@dataclass(frozen=True)
class SettingsMetadata:
    """Describe where MineOps settings were loaded from."""

    config_path: Path
    config_source: str
    defaults_created: bool


@dataclass(frozen=True)
class MinecraftSettings:
    """Minecraft-specific settings."""

    drive_letter: str
    servers_root: Path
    default_server_id: str
    servers: dict

@dataclass(frozen=True)
class Settings:
    """MineOps runtime settings."""

    server_id: str
    data_root: Path
    metadata_root: Path
    backups_root: Path
    logs_root: Path
    minecraft: MinecraftSettings
    metadata: SettingsMetadata


class ConfigError(Exception):
    """Raised when MineOps configuration cannot be loaded."""


def is_frozen_app() -> bool:
    """Return whether MineOps is running from a bundled executable."""

    return bool(getattr(sys, "frozen", False))


def get_runtime_dir() -> Path:
    """Return the executable folder in dist or package folder in dev."""

    if is_frozen_app():
        return Path(sys.executable).resolve().parent

    return Path(__file__).resolve().parents[3]


def get_user_config_dir() -> Path:
    """Return the default MineOps user config folder."""

    local_app_data = os.environ.get("LOCALAPPDATA")
    if local_app_data:
        return Path(local_app_data) / "MineOps"

    return Path.home() / ".mineops"


def default_config_data() -> dict:
    """Build the default MineOps configuration."""

    return {
        "mineops": {
            "server_id": "default",
            "default_include_inactive": False,
        },
        "paths": {
            "data_root": "D:\\MineOps",
        },
        "minecraft": {
            "drive_letter": "Z",
            "servers_root": "Z:\\",
            "default_server_id": "gravestone_26_1_2",
            "servers": {
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
        },
    }


def write_default_config(config_path: Path) -> None:
    """Write the default MineOps configuration file."""

    config_path.parent.mkdir(parents=True, exist_ok=True)

    if config_path.exists():
        return

    config_path.write_text(
        yaml.safe_dump(default_config_data(), sort_keys=False),
        encoding="utf-8",
    )


def _candidate_config_files(folder: Path) -> list[Path]:
    """Return config file candidates for a folder."""

    return [folder / name for name in CONFIG_FILE_NAMES]


def find_config_file() -> tuple[Path, str, bool]:
    """Find the MineOps config file or create the default one."""

    env_config_file = os.environ.get("MINEOPS_CONFIG_FILE")
    if env_config_file:
        path = Path(env_config_file).expanduser().resolve()
        if path.exists():
            return path, "MINEOPS_CONFIG_FILE", False
        raise ConfigError(f"MINEOPS_CONFIG_FILE does not exist: {path}")

    env_config_dir = os.environ.get("MINEOPS_CONFIG_DIR")
    if env_config_dir:
        folder = Path(env_config_dir).expanduser().resolve()

        for candidate in _candidate_config_files(folder):
            if candidate.exists():
                return candidate, "MINEOPS_CONFIG_DIR", False

    runtime_dir = get_runtime_dir()
    runtime_source = "exe folder" if is_frozen_app() else "dev project folder"

    for candidate in _candidate_config_files(runtime_dir):
        if candidate.exists():
            return candidate, runtime_source, False

    user_config_path = get_user_config_dir() / "config.yaml"

    defaults_created = not user_config_path.exists()

    if defaults_created:
        write_default_config(user_config_path)

    return user_config_path, "default user config", defaults_created


def load_config_file(config_path: Path) -> dict:
    """Load a YAML MineOps config file."""

    try:
        data = yaml.safe_load(config_path.read_text(encoding="utf-8"))
    except OSError as exc:
        raise ConfigError(f"Unable to read config file: {config_path}") from exc
    except yaml.YAMLError as exc:
        raise ConfigError(f"Invalid YAML config file: {config_path}") from exc

    if not isinstance(data, dict):
        raise ConfigError(f"Config file must contain a YAML object: {config_path}")

    return data


def _resolve_path(data_root: Path, value: str) -> Path:
    """Resolve config paths relative to data_root."""

    path = Path(value).expanduser()

    if path.is_absolute():
        return path

    return data_root / path


def load_settings() -> Settings:
    """Load MineOps configuration settings."""

    config_path, config_source, defaults_created = find_config_file()
    data = load_config_file(config_path)

    mineops = data.get("mineops", {})
    paths = data.get("paths", {})
    minecraft = data.get("minecraft", {})

    server_id = str(mineops.get("server_id", "default"))

    data_root = Path(str(paths.get("data_root", "D:/MineOps"))).expanduser()
    metadata_root = _resolve_path(data_root, str(paths.get("metadata_root", "metadata")))
    backups_root = _resolve_path(data_root, str(paths.get("backups_root", "backups")))

    app_logs_root = _resolve_path(data_root, str(paths.get("app_logs_root", "logs")))

    minecraft_settings = MinecraftSettings(
        drive_letter=str(minecraft.get("drive_letter", "Z")),
        servers_root=Path(str(minecraft.get("servers_root", "Z:\\"))).expanduser(),
        default_server_id=str(
            minecraft.get("default_server_id", "gravestone_26_1_2")
        ),
        servers=dict(minecraft.get("servers", {})),
    )

    metadata = SettingsMetadata(
        config_path=config_path,
        config_source=config_source,
        defaults_created=defaults_created,
    )

    return Settings(
        server_id=server_id,
        data_root=data_root,
        metadata_root=metadata_root,
        backups_root=backups_root,
        logs_root=app_logs_root,
        minecraft = minecraft_settings,
        metadata=metadata,
        )
