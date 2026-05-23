# ==================================================
# Settings.py Config Discovery + Default Build
# ==================================================

MineOps settings.py - redesign config loading to auto-create defaults when missing and discover config near the .exe in dist or near the CLI during dev.

Estimated Story Points: 4
Estimated Phases: 2

# --------------------------------------------------
# Phase 1 - Config discovery and default creation
# --------------------------------------------------
- Story 1a - Add config discovery order for explicit path, environment variable, .exe/dist folder, CLI/dev folder, then user config folder.
- Story 1b - Add default config creation when no config file exists, including parent folder creation and safe first-run behavior.

# --------------------------------------------------
# Phase 2 - Tests and CLI visibility
# --------------------------------------------------
- Story 2a - Add tests for dev discovery, dist discovery, missing config creation, and override precedence.
- Story 2b - Update about command output to show config path, config source, and whether defaults were created.

# ==================================================
# Architecture Notes
# ==================================================

Recommended discovery order:

1. CLI provided config path, if supported later.
2. MINEOPS_CONFIG_FILE environment variable.
3. MINEOPS_CONFIG_DIR environment variable.
4. Collocated with frozen .exe:
   - Path(sys.executable).parent / "config.yaml"
   - Path(sys.executable).parent / "config.ini"
5. Near dev CLI/package:
   - project root / "config.yaml"
   - project root / "config.ini"
   - src/mineops/config.yaml
   - src/mineops/config.ini
6. User fallback config folder:
   - %LOCALAPPDATA%/MineOps/config.yaml

Recommended settings.py helpers:

- is_frozen_app()
- get_executable_dir()
- get_project_root_candidates()
- get_user_config_dir()
- find_config_file()
- write_default_config()
- load_settings()

Default behavior:

- If a config file is found, load it.
- If no config file is found, create default config at the user fallback location.
- Do not silently overwrite an existing config.
- Return both settings and config metadata:
  - config_path
  - config_source
  - defaults_created

# ==================================================
# Testing Strategy
# ==================================================

Add pytest coverage for:

- Missing config creates default config.
- Existing config is loaded without overwrite.
- Environment variable path wins over discovered files.
- Frozen/exe-style path is preferred for dist simulation.
- Dev/project config is discovered during local development.
- Invalid config raises a clear ConfigError.
- about command displays resolved config metadata.

# ==================================================
# Risks / Considerations
# ==================================================

- Avoid writing config files into src/ or dist unless explicitly requested.
- Dist/.exe collocated config should be read-first, not created-first.
- Default creation should happen only in the safe user config folder.
- Keep path handling Windows-friendly.
- Keep config metadata visible for troubleshooting.

# ==================================================
# Future Enhancements
# ==================================================

- Support --config-file CLI option.
- Support --config-dir CLI option.
- Add config init command.
- Add config validate command.
- Add profile support later if MineOps grows like MindIt.