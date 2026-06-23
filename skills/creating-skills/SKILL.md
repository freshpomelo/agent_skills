---
name: creating-skills
description: Use when creating, scaffolding, or installing a new skill on this machine, or writing a new SKILL.md, so it lands in the agent_skills repo and stays discoverable by Claude Code.
---

# Creating Skills (local placement convention)

## Overview

On this machine, a skill's **real files live in the `agent_skills` git repo**, and `~/.claude/skills/` holds only a **symlink** to them. This keeps every skill version-controlled and pushable (`git@github.com:freshpomelo/agent_skills.git`) while still being discoverable by Claude Code.

**Core rule:** Never write a new skill directly into `~/.claude/skills/`. Write it in the repo, then symlink.

**REQUIRED SUB-SKILL:** Use superpowers:writing-skills for the authoring methodology — TDD baseline, the `name`/`description` rules ("Use when…", no workflow summary), structure, and testing. This skill only adds *where the files go and how they are linked*.

## When to Use

- "Create / make / scaffold / build a new skill"
- Writing a new `SKILL.md`
- Installing a skill so `/skill-name` works on this machine

**Not for:** editing an already-installed skill (edit the real file in the repo directly — the symlink already points there), or gstack/plugin skills (those have their own grouping under `agent_skills/gstack/`).

## The Layout

```
real:    /Users/wuyoumin/PycharmProjects/agent_skills/skills/<skill-name>/SKILL.md
symlink: ~/.claude/skills/<skill-name>  ->  .../agent_skills/skills/<skill-name>
```

The symlink points at the skill **directory** (not `SKILL.md`), using an **absolute** path. This matches every existing personal skill (`browser-use`, `fireworks`, `confluencewiki`, …).

## Steps

```bash
SKILL=<skill-name>     # letters, numbers, hyphens only — no spaces/parens
REPO=/Users/wuyoumin/PycharmProjects/agent_skills/skills

# 1. Create the real skill dir IN THE REPO (never in ~/.claude/skills)
mkdir -p "$REPO/$SKILL"

# 2. Author "$REPO/$SKILL/SKILL.md" following superpowers:writing-skills
#    (+ supporting files in the same dir only if genuinely needed)

# 3. Symlink the DIRECTORY into ~/.claude/skills using the ABSOLUTE path
ln -s "$REPO/$SKILL" "$HOME/.claude/skills/$SKILL"

# 4. Verify the link resolves and the skill is loadable
ls -la "$HOME/.claude/skills/$SKILL"
test -f "$HOME/.claude/skills/$SKILL/SKILL.md" && echo "OK: discoverable"

# 5. Commit to the repo so it's backed up
git -C "$REPO/.." add "skills/$SKILL"
git -C "$REPO/.." commit -m "feat(skill): add $SKILL"
```

## Quick Reference

| Step | Command / Check |
|------|-----------------|
| Real file location | `agent_skills/skills/<name>/SKILL.md` |
| Symlink | `ln -s <abs-repo-dir> ~/.claude/skills/<name>` |
| Link target | the **directory**, **absolute** path |
| Verify | `ls -la ~/.claude/skills/<name>` shows `->` |
| Persist | `git add` + `commit` in the repo |

## Common Mistakes

- **Writing the skill into `~/.claude/skills/` directly** — then it isn't in git and gets lost on cleanup/reinstall. The real file goes in the repo.
- **Symlinking `SKILL.md` instead of the directory** — breaks supporting files and the expected layout. Link the dir.
- **Relative symlink path** — use the absolute repo path so the link resolves from anywhere.
- **Forgetting to commit** — the skill isn't backed up until committed and pushed to `agent_skills`.
