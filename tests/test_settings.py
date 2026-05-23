"""Tests for MineOps settings."""

from mineops.config import load_settings


def test_load_settings() -> None:
    """Load default MineOps settings."""

    settings = load_settings()

    assert settings.server_id == "default"
