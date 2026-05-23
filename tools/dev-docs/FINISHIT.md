# ==================================================
# FINISHIT Workflow
# ==================================================

1. **Purpose**
   <pre lang="markdown">
   FinishIt is the standardized workflow for:
   - finalizing active feature work
   - committing completed implementation
   - pushing existing feature branches
   - creating pull requests

   When the user says:
   - "finishit"
   - "ready to commit and pr"

   the assistant should:
   - assume implementation is already complete
   - assume the user is already on the correct branch
   - prepare commit + PR workflow
   </pre>

1. **Expected Repository State**
   <pre lang="markdown">
   Expected:
   - existing GitHub issue already exists
   - branch already exists
   - implementation already completed
   - user already checked out to feature branch

   The assistant should:
   - verify current branch
   - verify git status
   - avoid creating duplicate branches/issues
   </pre>

1. **Critical Workflow Rules**
   <pre lang="markdown">
   NEVER during FinishIt workflow:
   - git checkout main
   - git pull origin main
   - git checkout -b ...
   - create duplicate issue

   These commands belong ONLY to ChangeIt workflows.

   FinishIt assumes:
   - active implementation branch already exists
   - work is already in progress or complete
   </pre>

1. **Command Output Rules**
   <pre lang="markdown">
   When generating terminal commands:

   - ALWAYS use plain fenced markdown code blocks
   - Prefer ```bash fenced blocks
   - NEVER use writing blocks for terminal commands
   - NEVER interleave commentary inside command blocks
   - Output must be directly copy/paste safe for Git Bash

   Example:

   ```bash
   git status
   pytest
   git add .

1. **Assistant Responsibilities**
   <pre lang="markdown">
   The assistant should:
   - generate commit messages
   - generate PR titles
   - generate PR descriptions
   - recommend pytest before commit
   - use current branch automatically
   - push current branch
   - create PR into main
   - avoid modifying branch topology
   </pre>

1. **Canonical Workflow Template**
   <pre lang="bash">
   CURRENT_BRANCH=$(git branch --show-current)

   git status

   git add .

   pytest || exit 1

   git commit -m ""

   git push -u origin "$CURRENT_BRANCH"

   gh pr create \
     --base main \
     --head "$CURRENT_BRANCH" \
     --title "" \
     --body "
   ## Why
   - ...

   ## What
   - ...

   ## Impact
   - ...

   Closes #...
   "
   </pre>

1. **Optional Lightweight PR Variant**
   <pre lang="bash">
   CURRENT_BRANCH=$(git branch --show-current)

   git status

   git add .

   pytest || exit 1

   git commit -m ""

   git push -u origin "$CURRENT_BRANCH"

   gh pr create \
     --base main \
     --head "$CURRENT_BRANCH" \
     --fill
   </pre>

1. **Post Merge Cleanup**
   <pre lang="bash">
   After the PR is merged, use POSTMERGE.md.
   </pre>

1. **Workflow Preferences**
   <pre lang="markdown">
   Prefer:
   - small focused commits
   - PR-friendly changes
   - passing tests before commit
   - clear Why/What/Impact PR descriptions
   - current branch safety checks

   Avoid:
   - committing directly to main
   - branch switching during finalize workflow
   - creating duplicate issues
   - rebasing during finalization unless requested
   </pre>

<br>Author: Mike Mattinson/Chat
<br>Updated: May/21/2026