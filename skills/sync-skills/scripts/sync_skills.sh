#!/usr/bin/env bash
set -euo pipefail

# Configuration
SKILLS_SRC="${HOME}/.claude/skills"
PLUGINS_CACHE="${HOME}/.claude/plugins/cache"
REPO_DIR="${1:-.}"
SKILLS_DEST="${REPO_DIR}/skills"
COMMIT_MSG="${2:-Sync all installed skills}"

# Validate repo
if ! git -C "$REPO_DIR" rev-parse --is-inside-work-tree &>/dev/null; then
  echo "Error: $REPO_DIR is not a git repository" >&2
  exit 1
fi

# 1. Sync custom skills from ~/.claude/skills/
if [ -d "$SKILLS_SRC" ]; then
  echo "==> Syncing custom skills from $SKILLS_SRC ..."
  rsync -av \
    --exclude='.system' \
    --exclude='*.skill' \
    --exclude='__pycache__' \
    --exclude='sync-skills' \
    "$SKILLS_SRC/" "$SKILLS_DEST/"
fi

# 2. Sync plugin skills from ~/.claude/plugins/cache/
#    For each plugin, find the latest version and sync its skills/
if [ -d "$PLUGINS_CACHE" ]; then
  echo "==> Syncing plugin skills from $PLUGINS_CACHE ..."
  find "$PLUGINS_CACHE" -mindepth 2 -maxdepth 2 -type d | while read -r plugin_dir; do
    plugin_name=$(basename "$(dirname "$plugin_dir")")
    version=$(basename "$plugin_dir")

    # Find the skills/ subdirectory (may be at skills/ or under a hash dir)
    skills_dir=""
    if [ -d "$plugin_dir/skills" ]; then
      skills_dir="$plugin_dir/skills"
    else
      # Look one level deeper (e.g. document-skills/<hash>/skills/)
      for sub in "$plugin_dir"/*/skills; do
        if [ -d "$sub" ]; then
          skills_dir="$sub"
          break
        fi
      done
    fi

    if [ -z "$skills_dir" ]; then
      continue
    fi

    # Check if this is the latest version for this plugin
    latest_version=$(ls -v "$(dirname "$plugin_dir")" | tail -1)
    if [ "$version" != "$latest_version" ]; then
      continue
    fi

    echo "    Plugin: $plugin_name ($version)"
    dest="${SKILLS_DEST}/${plugin_name}"
    mkdir -p "$dest"
    rsync -av \
      --exclude='__pycache__' \
      --exclude='sync-skills' \
      "$skills_dir/" "$dest/"
  done
fi

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
