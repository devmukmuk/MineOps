# ==================================================
# MineOps Gravestone Log Report Command
# ==================================================

Source script reviewed: :contentReference[oaicite:0]{index=0}

Estimated Story Points: 8
Estimated Phases: 4

# --------------------------------------------------
# Phase 1 - Add Gravestone Service Core
# --------------------------------------------------
- Story 1a - Move log parsing logic into `src/mineops/services/gravestones/gravestone_service.py`
- Story 1b - Add dataclasses for placed graves, found graves, scan results, and report summary

# --------------------------------------------------
# Phase 2 - Add CLI Command
# --------------------------------------------------
- Story 2a - Add `mineops gravestones scan` command
- Story 2b - Support options: `log_folder`, `--player`, `--not-found-only`

# --------------------------------------------------
# Phase 3 - Config Integration
# --------------------------------------------------
- Story 3a - Add optional config key for default Minecraft log folder
- Story 3b - Allow CLI to use config default when `log_folder` is omitted

# --------------------------------------------------
# Phase 4 - Tests and Reports
# --------------------------------------------------
- Story 4a - Add pytest coverage for `.log`, `.log.gz`, player filtering, found/not-found matching
- Story 4b - Add optional JSON report output for future automation

# ==================================================
# Proposed Command UX
# ==================================================

mineops gravestones scan P:/minecraft/server/logs

mineops gravestones scan P:/minecraft/server/logs --player MohawkBoy6

mineops gravestones scan --player MohawkBoy6 --not-found-only

mineops gravestones scan --write-report

# ==================================================
# Architecture Notes
# ==================================================

Recommended module structure:

src/mineops/
├── commands/
│   └── gravestones/
│       ├── __init__.py
│       └── cli.py
├── services/
│   └── gravestones/
│       ├── __init__.py
│       ├── models.py
│       └── gravestone_service.py

The current script should be converted from argparse to Typer-style MineOps CLI integration.

The regex parsing should remain in the service layer.

The CLI should only handle:
- user options
- config fallback
- display formatting
- optional report writing

# ==================================================
# Testing Strategy
# ==================================================

Test cases:
- placed gravestone is detected
- found gravestone is detected
- found event only counts after placed event
- player filter is case-insensitive
- all players shown when no player is provided
- `.gz` logs are readable
- unreadable files are skipped safely
- `--not-found-only` hides found results

# ==================================================
# Risks / Considerations
# ==================================================

- Minecraft/mod log text may vary by version
- player names with spaces or special characters may need careful regex handling
- found grave logs do not currently include dimension, so matching uses player + coordinates
- report order depends on file sorting and event order

# ==================================================
# Future Enhancements
# ==================================================

- Add JSON/CSV export
- Add Rich table output
- Add config-driven default log folder
- Add date filtering
- Add dimension-aware matching if found log lines include dimension later
- Add command alias such as `mineops graves scan`