#!/usr/bin/env bash
set -euo pipefail

# Configuration
SKILLS_SRC="${HOME}/.claude/skills"
REPO_URL="${1:?Usage: sync_skills.sh <github-repo-url> [commit-message]}"
COMMIT_MSG="${2:-Sync skills from ~/.claude/skills}"
BRANCH="${3:-main}"

# Validate source exists
if [ ! -d "$SKILLS_SRC" ]; then
  echo "Error: Skills source directory not found: $SKILLS_SRC" >&2
  exit 1
fi

# Create temp directory and ensure cleanup
TMPDIR=$(mktemp -d)
trap 'rm -rf "$TMPDIR"' EXIT

# Shallow clone
echo "Cloning $REPO_URL ..."
git clone --depth 1 --branch "$BRANCH" "$REPO_URL" "$TMPDIR/repo"

# Sync skills
SKILLS_DEST="$TMPDIR/repo/skills"
echo "Syncing skills from $SKILLS_SRC to $SKILLS_DEST ..."
rsync -av --delete \
  --exclude='.system' \
  --exclude='*.skill' \
  --exclude='__pycache__' \
  --exclude='sync-skills' \
  "$SKILLS_SRC/" "$SKILLS_DEST/"

# Check for changes
cd "$TMPDIR/repo"
if git diff --quiet && git diff --cached --quiet && [ -z "$(git ls-files --others --exclude-standard skills/)" ]; then
  echo "No changes to commit."
  exit 0
fi

# Stage, commit, push
git add skills/
git commit -m "$COMMIT_MSG"
echo "Pushing to $REPO_URL ..."
git push
echo "Done."
