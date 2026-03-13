#!/usr/bin/env bash
set -euo pipefail

# Configuration
SKILLS_SRC="${HOME}/.claude/skills"
REPO_DIR="${1:-.}"
SKILLS_DEST="${REPO_DIR}/skills"
COMMIT_MSG="${2:-Sync skills from ~/.claude/skills}"

# Validate source exists
if [ ! -d "$SKILLS_SRC" ]; then
  echo "Error: Skills source directory not found: $SKILLS_SRC" >&2
  exit 1
fi

# Validate repo
if ! git -C "$REPO_DIR" rev-parse --is-inside-work-tree &>/dev/null; then
  echo "Error: $REPO_DIR is not a git repository" >&2
  exit 1
fi

# Sync skills, excluding system skills, .skill packages, and __pycache__
echo "Syncing skills from $SKILLS_SRC to $SKILLS_DEST ..."
rsync -av --delete \
  --exclude='.system' \
  --exclude='*.skill' \
  --exclude='__pycache__' \
  --exclude='sync-skills' \
  "$SKILLS_SRC/" "$SKILLS_DEST/"

# Check for changes
cd "$REPO_DIR"
if git diff --quiet && git diff --cached --quiet && [ -z "$(git ls-files --others --exclude-standard skills/)" ]; then
  echo "No changes to commit."
  exit 0
fi

# Stage, commit, push
git add skills/
git commit -m "$COMMIT_MSG"
echo "Pushing to remote..."
git push
echo "Done."
