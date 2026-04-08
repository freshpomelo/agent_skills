---
name: dev-tracker
description: Use when a bug is discovered, diagnosed, or fixed during conversation - whether found by Claude or reported by the user. Also use BEFORE each git commit to record all code changes made since the last commit. Triggers on "记个bug"、"log this bug"、"记录变更"、"log changes", or when Claude identifies and resolves unexpected behavior, errors, or defects in the codebase.
---

# Dev Change Tracker

Record bugs and code changes to `DEV_TRACKER.md` (project root, beside CLAUDE.md) for future reference.

## When to Use

- You or the user discover a bug during the conversation
- A bug is diagnosed and/or fixed
- **Before each git commit** — summarize all code changes made since the last commit
- The user explicitly asks to log a bug or record changes

## Format

`DEV_TRACKER.md` uses compact plain text — no markdown bold/italic, no backtick fences, no bullet markers. This minimizes token cost when AI reads the file.

### Bug Log entry

```
[BUG-NNN] Short title
branch: branch-name | module: path/to/file.py | commit: abc1234
symptom: What went wrong (1 sentence)
cause: Root cause (1 sentence)
fix: How it was resolved, or "pending" (1 sentence)
```

### Change Log entry

```
[CHG-NNN] Short title (YYYY-MM-DD)
branch: branch-name | commit: abc1234
files: file1.py, file2.js, file3.html
what: What was changed (2-3 sentences)
how: Key implementation decisions (1-2 sentences)
result: Outcome and verification (1 sentence)
```

## Rules

1. **Read `DEV_TRACKER.md` first** to get the latest BUG/CHG number, then increment
2. If `DEV_TRACKER.md` doesn't exist, create it with headers `# Dev Tracker`, `## Bug Log`, `## Change Log`
3. Keep each field concise but enough to recall the context months later
4. **Module/Files** should be the most specific paths possible (file > directory > component)
5. For bugs: **Symptom** describes observable behavior, **Cause** explains root cause
6. For changes: **What** covers the user's intent, **How** covers your approach, **Result** covers verification
7. If not yet committed, set Commit to "pending" and update later
8. **Branch**: get via `git branch --show-current`
9. **Commit**: get via `git log --oneline -1` after committing
10. Do NOT duplicate — check existing entries before adding
11. For changes: group related modifications into one CHG entry (e.g. "sidebar refactoring" not one entry per file)
12. For changes: get the date via `date +%Y-%m-%d`
13. **Bugs only go to Bug Log** — do NOT create a Change Log entry for bug fixes. Change Log is reserved for feature work, refactoring, and other non-bug changes
