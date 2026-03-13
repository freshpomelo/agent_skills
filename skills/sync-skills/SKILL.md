---
name: sync-skills
description: Sync installed Claude skills from ~/.claude/skills/ to the current git project, then commit and push. Use when the user asks to "同步skill"、"备份skill"、"sync skills"、"push skills to git", or wants to back up their installed skills to a git repository.
---

# Sync Skills

Sync all custom skills from `~/.claude/skills/` into the current project's `skills/` directory, then commit and push to remote.

## What Gets Synced

- All custom skill directories (each containing SKILL.md and resources)
- Excludes: `.system/` (built-in skills), `*.skill` (package files), `__pycache__`, and the `sync-skills` skill itself

## Usage

Run the bundled script:

```bash
bash scripts/sync_skills.sh <repo-path> [commit-message]
```

- `repo-path`: Path to the git repo (defaults to `.`)
- `commit-message`: Optional custom commit message (defaults to "Sync skills from ~/.claude/skills")

## Workflow

1. Run `scripts/sync_skills.sh` with the project root path
2. The script uses `rsync --delete` to mirror the skills directory (removed skills get removed from the repo too)
3. If there are changes, it stages `skills/`, commits, and pushes
4. If no changes are detected, it exits cleanly with a message

## Notes

- The `--delete` flag ensures the repo stays in sync — if a skill is uninstalled locally, it gets removed from the repo on next sync
- The script excludes its own directory (`sync-skills`) to avoid circular syncing when installed via this repo
