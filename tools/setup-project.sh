#!/usr/bin/env bash

set -e

PROJECT_ROOT="$(pwd)"

echo "================================================="
echo "Creating MineOps scaffold..."
echo "Root: $PROJECT_ROOT"
echo "================================================="

# =================================================

# FOLDERS

# =================================================

mkdir -p config/servers
mkdir -p config/schemas

mkdir -p data/exports
mkdir -p data/logs
mkdir -p data/temp
mkdir -p data/backups

mkdir -p scripts

mkdir -p src/mineops/commands
mkdir -p src/mineops/services
mkdir -p src/mineops/models
mkdir -p src/mineops/providers
mkdir -p src/mineops/utils

mkdir -p tests/commands
mkdir -p tests/services
mkdir -p tests/providers

mkdir -p tools

mkdir -p docs/architecture
mkdir -p docs/workflows
mkdir -p docs/examples

mkdir -p build
mkdir -p dist

# =================================================

# README

# =================================================

cat > README.md << 'README_EOF'

# MineOps

Minecraft utility and automation toolkit written in Python.

## Features

* Server automation
* World backups
* RCON tools
* Player utilities
* Map exports
* Mod synchronization
* Interactive CLI

## Development

```bash
python -m venv .venv
source .venv/Scripts/activate
pip install -r requirements.txt
```

## Run

```bash
python -m mineops about
```

## Test

```bash
pytest
```

README_EOF

# =================================================

# .gitignore

# =================================================

cat > .gitignore << 'GITIGNORE_EOF'

# Python

**pycache**/
*.pyc
*.pyo
*.pyd

# Virtual Environment

.venv/
venv/

# Pytest

.pytest_cache/

# Build

build/
dist/
*.spec

# IDE

.vscode/
.idea/

# Logs

*.log

# Local Config

.env

# OS

Thumbs.db
.DS_Store
GITIGNORE_EOF

# =================================================

# requirements.txt

# =================================================

cat > requirements.txt << 'REQ_EOF'
typer[all]
rich
pyyaml
pytest
pyinstaller
pydantic
mcrcon
REQ_EOF

# =================================================

# pytest.ini

# =================================================

cat > pytest.ini << 'PYTEST_EOF'
[pytest]
testpaths = tests
pythonpath = src
PYTEST_EOF

# =================================================

# pyproject.toml

# =================================================

cat > pyproject.toml << 'PYPROJECT_EOF'
[build-system]
requires = ["setuptools>=61.0"]
build-backend = "setuptools.build_meta"

[project]
name = "mineops"
version = "0.1.0"
description = "Minecraft utility and automation toolkit"
authors = [
{name = "Mike"}
]
requires-python = ">=3.12"

[tool.pytest.ini_options]
pythonpath = ["src"]
PYPROJECT_EOF

# =================================================

# CONFIG

# =================================================

cat > config/config.yaml << 'CONFIG_EOF'
app:
name: MineOps
environment: dev

paths:
minecraft_drive: M:
backup_drive: B:
exports_root: D:/MineOps/exports
logs_root: D:/MineOps/logs

defaults:
server: survival

servers:
survival:
server_id: survival
world_path: M:/Servers/Survival/world
backup_path: B:/MinecraftBackups/Survival
rcon_host: 192.168.1.50
rcon_port: 25575
rcon_password: change-me
CONFIG_EOF

# =================================================

# PYTHON SOURCE FILES

# =================================================

cat > src/mineops/**init**.py << 'INIT_EOF'
**version** = "0.1.0"
INIT_EOF

cat > src/mineops/**main**.py << 'MAIN_EOF'
from mineops.cli import main

main()
MAIN_EOF

cat > src/mineops/cli.py << 'CLI_EOF'
import typer
from rich import print

app = typer.Typer(
help="MineOps - Minecraft utility toolkit"
)

@app.command()
def about() -> None:
print("[green]MineOps[/green]")
print("Minecraft utility toolkit")

def main() -> None:
app()

if **name** == "**main**":
main()
CLI_EOF

cat > src/mineops/settings.py << 'SETTINGS_EOF'
from pathlib import Path
from typing import Any

import yaml

DEFAULT_CONFIG_PATH = Path("config/config.yaml")

def load_settings(
config_path: Path = DEFAULT_CONFIG_PATH,
) -> dict[str, Any]:

```
if not config_path.exists():
    raise FileNotFoundError(
        f"Config file not found: {config_path}"
    )

with config_path.open(
    "r",
    encoding="utf-8",
) as file:
    data = yaml.safe_load(file)

return data or {}
```

SETTINGS_EOF

cat > src/mineops/constants.py << 'CONSTANTS_EOF'
APP_NAME = "MineOps"
VERSION = "0.1.0"
CONSTANTS_EOF

# =================================================

# COMMAND FILES

# =================================================

touch src/mineops/commands/**init**.py
touch src/mineops/commands/backup.py
touch src/mineops/commands/server.py
touch src/mineops/commands/players.py
touch src/mineops/commands/maps.py
touch src/mineops/commands/mods.py

# =================================================

# SERVICE FILES

# =================================================

touch src/mineops/services/**init**.py
touch src/mineops/services/backup_service.py
touch src/mineops/services/server_service.py
touch src/mineops/services/rcon_service.py
touch src/mineops/services/world_service.py

# =================================================

# MODEL FILES

# =================================================

touch src/mineops/models/**init**.py
touch src/mineops/models/server_ref.py
touch src/mineops/models/backup_result.py

# =================================================

# PROVIDER FILES

# =================================================

touch src/mineops/providers/**init**.py
touch src/mineops/providers/filesystem_provider.py
touch src/mineops/providers/minecraft_provider.py

# =================================================

# UTILITY FILES

# =================================================

touch src/mineops/utils/**init**.py
touch src/mineops/utils/paths.py
touch src/mineops/utils/logging.py
touch src/mineops/utils/hashing.py

# =================================================

# TEST FILES

# =================================================

touch tests/**init**.py

touch tests/commands/**init**.py
touch tests/services/**init**.py
touch tests/providers/**init**.py

cat > tests/test_settings.py << 'TEST_EOF'
from mineops.settings import load_settings

def test_load_settings() -> None:
settings = load_settings()

```
assert "app" in settings
```

TEST_EOF

# =================================================

# TOOL FILES

# =================================================

touch tools/build.py
touch tools/release.py
touch tools/dev-reset.py

# =================================================

# SCRIPT FILES

# =================================================

touch scripts/backup-world.py
touch scripts/sync-mods.py
touch scripts/export-map.py
touch scripts/player-report.py

# =================================================

# GIT INIT

# =================================================

git init

echo ""
echo "================================================="
echo "MineOps scaffold created successfully!"
echo "================================================="
echo ""
echo "Next steps:"
echo ""
echo "python -m venv .venv"
echo "source .venv/Scripts/activate"
echo ""
echo "pip install -r requirements.txt"
echo ""
echo "python -m mineops about"
echo ""
echo "================================================="
