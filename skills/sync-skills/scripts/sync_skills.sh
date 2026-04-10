#!/usr/bin/env bash
set -euo pipefail

# Default repo (SSH) — override with first argument
DEFAULT_REPO="git@github.com:freshpomelo/agent_skills.git"

# Configuration
SKILLS_SRC="${HOME}/.claude/skills"
REPO_URL="${1:-$DEFAULT_REPO}"
COMMIT_MSG="${2:-Sync skills from ~/.claude/skills}"
BRANCH="${3:-main}"

# Auto-convert HTTPS to SSH to avoid interactive auth prompts
if [[ "$REPO_URL" =~ ^https://github\.com/(.+)$ ]]; then
  REPO_URL="git@github.com:${BASH_REMATCH[1]}"
  # Ensure .git suffix
  [[ "$REPO_URL" != *.git ]] && REPO_URL="${REPO_URL}.git"
fi

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
  --exclude='.DS_Store' \
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
