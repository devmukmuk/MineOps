# tools/dev-docs/DESIGNIT.md

1. **Purpose**
   <pre lang="markdown">
   DesignIt is the standardized feature planning and architecture workflow.

   When the user says:
   "DesignIt"

   the assistant should:
   - analyze the requested feature/module
   - ask discovery questions if needed
   - break work into small implementation units
   - organize development into phases
   - estimate simplified story points
   - generate implementation roadmaps
   - document architecture considerations
   </pre>

1. **Design Goals**
   <pre lang="markdown">
   The DesignIt workflow should produce:

   - small incremental implementation phases
   - low-risk development steps
   - testable deliverables
   - clear workflow architecture
   - provider/service boundaries
   - future scalability planning
   - implementation-oriented planning documents
   </pre>

1. **Story Point Rules**
   <pre lang="markdown">
   1 Story Point should represent:

   - a focused implementation task
   - a small coding session
   - a testable unit of work
   - a low-risk incremental change

   Examples:

   - add CLI option
   - add provider abstraction
   - add validation rule
   - add SQLite table
   - add report export
   - add unit tests
   - add workflow service
   </pre>

1. **Phase Rules**
   <pre lang="markdown">
   Prefer:

   2 story points ≈ 1 phase

   Phases should remain:

   - small
   - reviewable
   - PR-friendly
   - independently testable
   - incrementally deployable
   </pre>

1. **Discovery Questions**
   <pre lang="markdown">
   The assistant should explore:

   Feature Purpose
   - What problem is solved?
   - Who uses it?
   - What is success?

   Inputs and Outputs
   - What data enters?
   - What data is produced?
   - Are reports required?

   CLI and UX
   - CLI commands/options?
   - Config-driven defaults?
   - Preview/repair modes?

   Architecture
   - New module or enhancement?
   - Related services/providers?
   - SQLite integration?
   - Sidecar compatibility?

   Validation and Safety
   - Dangerous operations?
   - Recovery requirements?
   - Logging/reporting expectations?

   Testing
   - Important edge cases?
   - Unit vs integration tests?
   </pre>

1. **Canonical Output Structure**
   <pre lang="markdown">
   # ==================================================
   # Feature Name
   # ==================================================

   Estimated Story Points:
   Estimated Phases:

   # --------------------------------------------------
   # Phase 1
   # --------------------------------------------------
   - Story 1a
   - Story 1b

   # --------------------------------------------------
   # Phase 2
   # --------------------------------------------------
   - Story 2a
   - Story 2b

   # ==================================================
   # Architecture Notes
   # ==================================================

   # ==================================================
   # Testing Strategy
   # ==================================================

   # ==================================================
   # Risks / Considerations
   # ==================================================

   # ==================================================
   # Future Enhancements
   # ==================================================
   </pre>

1. **Output Rules**
   <pre lang="markdown">
   The assistant should:

   - produce ONE single markdown block
   - avoid fragmented responses
   - avoid conversational commentary
   - make output copy/paste ready
   - prefer concise implementation wording
   - focus on architecture and execution

   Output should work well for:
   - GitHub planning
   - roadmap discussions
   - implementation tracking
   - project architecture notes
   - developer planning sessions
   </pre>

1. **Recommended Documentation Structure**
   <pre lang="markdown">
   docs/<module>-docs/
   ├── README.md
   ├── overview.md
   ├── architecture.md
   ├── workflows.md
   ├── cli-reference.md
   ├── testing.md
   ├── roadmap.md
   └── diagrams/

   Prefer Mermaid diagrams for:
   - workflow pipelines
   - provider architecture
   - repair execution flow
   - sidecar lifecycle
   - service orchestration
   </pre>

<br>Author: Mike Mattinson/Chat  
<br>Updated: May/20/2026