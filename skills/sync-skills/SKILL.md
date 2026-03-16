---
name: sync-skills
description: Sync installed Claude skills from ~/.claude/skills/ to a GitHub repo, then commit and push. No local clone required. Use when the user asks to "同步skill"、"备份skill"、"sync skills"、"push skills to git", or wants to back up their installed skills to a git repository.
---

# Sync Skills

Sync all custom skills from `~/.claude/skills/` to a GitHub repo via temporary shallow clone. No pre-existing local clone needed.

## What Gets Synced

- All custom skill directories (each containing SKILL.md and resources)
- Excludes: `.system/` (built-in skills), `*.skill` (package files), `__pycache__`, and the `sync-skills` skill itself

## Usage

```bash
bash scripts/sync_skills.sh <github-repo-url> [commit-message] [branch]
```

- `github-repo-url` (required): e.g. `git@github.com:user/repo.git` or `https://github.com/user/repo.git`
- `commit-message`: Optional (defaults to "Sync skills from ~/.claude/skills")
- `branch`: Optional (defaults to `main`)

## Workflow

1. Shallow clone the target repo to a temp directory
2. Rsync skills into `skills/` (with `--delete` to mirror removals)
3. Commit and push if changes exist
4. Auto-cleanup temp directory on exit

## Prerequisites

- `git` with push access to the target repo (SSH key or HTTPS credentials)
- `rsync` installed
