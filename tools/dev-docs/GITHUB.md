# tools/dev-docs/GITHUB.md

# --------------------------------------------------
# 1. create / checkout branch
# --------------------------------------------------
git fetch origin
git checkout -b feat/photoit-chime-phase1 origin/main

# --------------------------------------------------
# 2. develop + commit

# --------------------------------------------------
git add .
git commit

ggdG     # clear everything
i        # enter insert mode
(paste)  # Shift+Insert
Esc
:wq

# commit format:
# <area>: <summary>
#
# Why:
# - ...
# What:
# - ...
# Impact:
# - ...

# --------------------------------------------------
# 3. push + create PR
# --------------------------------------------------
git push -u origin HEAD

gh pr create \
  --base main \
  --fill \
  --title "feat(photoit): chime feedback phase 1" \
  --body "Closes #94"


gh pr status
gh pr view


# --------------------------------------------------
# 4. validate PR
# --------------------------------------------------
gh pr checks
pytest

# optional manual checks
python -m mindit about
python -m mindit photoit --interactive


# --------------------------------------------------
# 5. merge PR
# --------------------------------------------------
gh pr merge --merge --delete-branch


# --------------------------------------------------
# 6. release build - 2 part new release flow
# --------------------------------------------------
python -m tools.release --autobuild --publish --os win

gh pr view 156
gh pr merge 156 --merge --delete-branch

git checkout main
git pull

python -m tools.release --tag-only --version 2026.4.49 --os win


# --------------------------------------------------
# 7. capture artifacts (optional but recommended)
# --------------------------------------------------
# store outputs for debugging / regression
# output/dev-runs/YYYY-MM-DD/<feature>/


Author: Mike Mattinson
Updated: Apr/29/2026
Updated: May/19/2026



BRANCH="fix-scanit-remove-empty-folders"
ISSUE_TITLE="Fix ScanIt remove-empty-folders command"
ISSUE_BODY="Track fix for ScanIt remove-empty-folders command."
COMMIT_MESSAGE="fix(scanit): repair remove empty folders command"

ISSUE_URL=$(gh issue create \
  --title "$ISSUE_TITLE" \
  --body "$ISSUE_BODY")

ISSUE_NUMBER=$(basename "$ISSUE_URL")

git checkout main
git pull origin main
git checkout -b "$BRANCH"

git add .
git status
pytest || exit 1

git commit -m "$COMMIT_MESSAGE"

git push -u origin "$BRANCH"

gh pr create \
  --base main \
  --head "$BRANCH" \
  --title "$ISSUE_TITLE" \
  --body "
## Why
- Fix the ScanIt remove-empty-folders command so the CLI loads and runs correctly.

## What
- Repairs the command definition/import issue.
- Keeps the command available under scanit.
- Supports dry-run behavior.

## Impact
- Restores ScanIt cleanup workflow.
- Reduces manual cleanup after duplicate/move operations.

Closes #$ISSUE_NUMBER
"
 --fill

gh pr create --base main --head "$BRANCH" --fill


# go to github and manually process the pr, then after:
# ---- review / merge PR manually on GitHub ----

git checkout main
git pull origin main
git branch -d "$BRANCH"
git fetch --prune