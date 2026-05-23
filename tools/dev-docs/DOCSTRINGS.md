# tools/dev-docs/DOCSTRINGS.md

1. **Purpose**
   <pre lang="markdown">
   DocStrings is the standardized documentation workflow for:
   - module docstrings
   - class docstrings
   - function docstrings
   - method docstrings
   - CLI command docstrings
   - pylint-friendly documentation

   When the user says:
   "docstrings"

   the assistant should:
   - review missing docstrings
   - improve weak docstrings
   - generate short standard docstrings
   - help reduce pylint warnings
   - preserve clean readable code
   </pre>

1. **Assistant Responsibilities**
   <pre lang="markdown">
   The assistant should:

   - Add module docstrings
   - Add class docstrings
   - Add function docstrings
   - Add method docstrings
   - Keep wording short and consistent
   - Prefer one-line docstrings
   - Avoid unnecessary verbosity
   - Preserve existing code behavior
   - Follow pylint-friendly standards
   - Show complete updated methods/files when requested
   </pre>

1. **Docstring Rules**
   <pre lang="markdown">
   Standard docstring rules:

   - Use triple double-quotes
   - Start with a capital letter
   - End with a period
   - Keep most docstrings to one sentence
   - Explain what the code does
   - Avoid explaining implementation details
   - Avoid obvious/redundant wording
   - Prefer concise wording
   - Prefer improving code clarity over long explanations

   Prefer:

   """Load configuration settings."""

   Avoid:

   """This function loads the configuration settings
   from the configuration file and returns them."""
   </pre>

1. **Coverage Expectations**
   <pre lang="markdown">
   Prefer docstrings for:

   - packages
   - modules
   - public classes
   - public functions
   - public methods
   - Typer CLI commands
   - reusable helpers

   Usually avoid docstrings for:

   - tiny private helpers
   - obvious property accessors
   - trivial test-only setup code
   </pre>

1. **Pylint Goals**
   <pre lang="markdown">
   The goal is to reduce common pylint warnings early:

   - missing-module-docstring
   - missing-class-docstring
   - missing-function-docstring

   The assistant should proactively include docstrings
   during scaffolding and implementation.
   </pre>

1. **MineOps Style Preferences**
   <pre lang="markdown">
   For MineOps projects:

   - Keep wording practical
   - Keep wording simple
   - Prefer operational terminology
   - Avoid academic-style documentation
   - Avoid excessive parameter sections
   - Prefer readability over completeness

   Examples:

   """MineOps project package."""

   """Run the MineOps command-line interface."""

   """Load MineOps configuration settings."""

   """Print project environment details."""

   """Validate Minecraft server backups."""
   </pre>

1. **Code Style Examples**
   <pre lang="python">
   """MineOps project package."""
   </pre>

   <pre lang="python">
   def load_config(config_path: Path) -> Config:
       """Load the MineOps configuration file."""
   </pre>

   <pre lang="python">
   class ConfigError(Exception):
       """Raised when configuration is invalid."""
   </pre>

   <pre lang="python">
   @app.command()
   def about() -> None:
       """Print project and environment details."""
   </pre>

1. **Workflow Preferences**
   <pre lang="markdown">
   Prefer:
   - short docstrings
   - consistent wording
   - pylint-friendly formatting
   - incremental cleanup
   - readable code

   Avoid:
   - multi-paragraph docstrings
   - noisy documentation
   - fake/generated wording
   - implementation-heavy explanations
   - excessive parameter documentation
   </pre>

<br>Author: Mike Mattinson/Chat
<br>Updated: May/23/2026