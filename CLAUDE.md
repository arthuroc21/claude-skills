# claude-skills

## Project overview

`claude-skills` is a workspace and public GitHub repo for creating, editing, and maintaining [Claude Agent Skills](https://code.claude.com/docs/en/skills). It currently holds two complementary skills — `kickoff` (day-zero project setup) and `handoff` (living `HANDOFF.md` maintenance) — and is the home for any further skills built here. Skills are authored as plain-Markdown `SKILL.md` files (plus optional `assets/`) and target all four Claude surfaces: Chat, Cowork, Code, and Design. The `SKILL.md` sources are the deliverable; lightweight scripts package them for distribution without changing them — the repo doubles as a **Claude Code plugin marketplace** (`.claude-plugin/marketplace.json` + a per-skill `plugin.json`), and each skill is also built into its own Cowork plugin.

## Working conventions

This project uses GitHub (`claude-skills`) for version control. Changes are committed and pushed after every significant change — a skill created or edited, a decision made or reversed, a file added or removed, a fix landed — rather than batched up. Whenever a skill changes here, every copy is kept in sync: it is committed and pushed to the `claude-skills` GitHub repo, the local Claude Code install at `~/.claude/skills/<skill>` is refreshed, the in-repo Claude Code **plugin-marketplace** files (`.claude-plugin/marketplace.json` + each `<skill>/.claude-plugin/plugin.json`) are regenerated via `scripts/build_marketplace.py`, and one Cowork plugin per skill is rebuilt into the sibling `Skills Library/` folder (`<skill>.plugin`, via `scripts/build_cowork_plugin.py`) — so no copy drifts. Commit messages are clear and specific. Secrets, API keys, and `.env` files are never committed; `.gitignore` keeps them — and packaged `*.skill`/`*.zip`/`*.plugin` build outputs — out of the repo. This repo is intentionally **public**.

Project state lives in `HANDOFF.md` at the repo root, maintained per the `handoff` skill: it is read at the start of a session and after any context compaction, and updated on every significant change, so the project can always be resumed from that one file. The `HANDOFF.md` format is owned solely by the `handoff` skill — `kickoff` and everything else defer to it (single source of truth).

## Stack and commands

Markdown-based Agent Skills; no language toolchain, build step, or tests. A skill is a folder containing a `SKILL.md` (with YAML frontmatter: `name`, `description`) and optional `assets/`.

- **Install / sync (Claude Code):** `cp -r <skill> ~/.claude/skills/` (global) or `<repo>/.claude/skills/` (per-project). Re-copy after every edit so the local install matches the repo.
- **Package (claude.ai upload):** `cd <skill> && zip -r ../<skill>.zip . && cd ..`
- **Build marketplace files (Claude Code):** `python scripts/build_marketplace.py` → regenerates `.claude-plugin/marketplace.json` and each `<skill>/.claude-plugin/plugin.json` from the skills, so the repo installs as a marketplace: `/plugin marketplace add arthuroc21/claude-skills` → `/plugin install <skill>@claude-skills`. These are **tracked** files, so run it **before committing** when a skill is added/removed or its description changes — deliberately *not* in the post-commit hook, which would dirty the tree. Each skill is a skills-only plugin whose `SKILL.md` sits at the plugin root; `version` is omitted so installs track the commit SHA and auto-update.
- **Build Cowork plugins:** `python scripts/build_cowork_plugin.py` → packages **each skill into its own `<skill>.plugin`** in the sibling `Skills Library/` folder, for installing individually in Cowork (each shows as `<skill>:<skill>`). New skills are auto-included; deleted ones have their stale `.plugin` removed. Run on every skill change. A git `post-commit` hook auto-rebuilds these (only — not the tracked marketplace files) on every commit — reinstall it after cloning with `sh scripts/install-hooks.sh`.
- **Conventions:** Australian English, ISO dates (`YYYY-MM-DD`). Skills do not sync across surfaces — install separately per surface.
