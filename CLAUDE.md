# claude-skills

## Project overview

`claude-skills` is a workspace and public GitHub repo for creating, editing, and maintaining [Claude Agent Skills](https://code.claude.com/docs/en/skills). It currently holds two complementary skills — `kickoff` (day-zero project setup) and `handoff` (living `HANDOFF.md` maintenance) — and is the home for any further skills built here. Skills are authored as plain-Markdown `SKILL.md` files (plus optional `assets/`) and target all four Claude surfaces: Chat, Cowork, Code, and Design. There is no build or runtime — the source files are the deliverable.

## Working conventions

This project uses GitHub (`claude-skills`) for version control. Changes are committed and pushed after every significant change — a skill created or edited, a decision made or reversed, a file added or removed, a fix landed — rather than batched up. Whenever a skill changes here, every copy is kept in sync: it is committed and pushed to the `claude-skills` GitHub repo, and the local install at `~/.claude/skills/<skill>` is refreshed — so no copy drifts. Commit messages are clear and specific. Secrets, API keys, and `.env` files are never committed; `.gitignore` keeps them — and packaged `*.skill`/`*.zip` build outputs — out of the repo. This repo is intentionally **public**.

Project state lives in `HANDOFF.md` at the repo root, maintained per the `handoff` skill: it is read at the start of a session and after any context compaction, and updated on every significant change, so the project can always be resumed from that one file. The `HANDOFF.md` format is owned solely by the `handoff` skill — `kickoff` and everything else defer to it (single source of truth).

## Stack and commands

Markdown-based Agent Skills; no language toolchain, build step, or tests. A skill is a folder containing a `SKILL.md` (with YAML frontmatter: `name`, `description`) and optional `assets/`.

- **Install / sync (Claude Code):** `cp -r <skill> ~/.claude/skills/` (global) or `<repo>/.claude/skills/` (per-project). Re-copy after every edit so the local install matches the repo.
- **Package (claude.ai upload):** `cd <skill> && zip -r ../<skill>.zip . && cd ..`
- **Conventions:** Australian English, ISO dates (`YYYY-MM-DD`). Skills do not sync across surfaces — install separately per surface.
