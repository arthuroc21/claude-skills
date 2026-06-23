# claude-skills — HANDOFF

**Last updated:** 2026-06-23 · **Phase:** both skills complete and cross-surface; pending GitHub publish + `SessionStart` hook install · **Surface(s):** authored in claude.ai chat; skills target all four surfaces (Chat, Cowork, Code, Design)

## 1. Summary / North Star

A public GitHub repo holding two complementary Claude Agent Skills — `kickoff` (day-zero project setup) and `handoff` (living `HANDOFF.md` maintenance) — so long-running projects stay resumable across Claude sessions. End goal: publish them publicly, installable in Claude Code and via claude.ai settings, working on every surface.

## 2. Current state

Both skills are written, validated, and packaged, and have since been **made cross-surface** and unified. `kickoff` now also **asks whether a HANDOFF.md already exists and resumes from it** instead of always starting blank. The repo `claude-skills/` is assembled and zipped (`claude-skills.zip`), with both skills updated inside it. **Not yet pushed to GitHub.** The user is at the context-window limit in Claude Code; they have detailed instructions for two pending tasks: (a) publishing the repo (via `gh` or the GitHub website), and (b) installing a `SessionStart` hook scoped to `clear` + `compact` that re-injects `HANDOFF.md` after a reset.

## 3. Map

| Name | Where | What it does |
|------|-------|--------------|
| README.md | claude-skills/ | Repo readme: what the skills do, install steps, optional compaction hook, cross-surface note |
| LICENSE | claude-skills/ | MIT licence; copyright holder still a placeholder |
| .gitignore | claude-skills/ | Ignores `*.skill`, `*.zip`, OS/editor cruft |
| handoff/SKILL.md | claude-skills/handoff/ | The handoff skill (now explicitly cross-surface) |
| handoff/assets/HANDOFF_template.md | claude-skills/handoff/assets/ | 8-section state-file skeleton (example row genericised everywhere) |
| kickoff/SKILL.md | claude-skills/kickoff/ | The kickoff skill (cross-surface; resumes from an existing HANDOFF.md) |
| kickoff/assets/CLAUDE_md_core.md | claude-skills/kickoff/assets/ | Standing-conventions block for a project CLAUDE.md |
| claude-skills.zip | delivered artifact | The repo, zipped for publishing |
| handoff.skill / kickoff.skill | delivered artifacts | Packaged skills for install / claude.ai upload |
| SessionStart hook (clear + compact) | user's `~/.claude/settings.json` (not in repo) | Re-injects `HANDOFF.md` into context after `/clear` or compaction; install pending |

## 4. Conventions and glossary

*Standing conventions for this work:*

- The `HANDOFF.md` format is owned **solely** by the `handoff` skill; `kickoff` defers to it and does not duplicate the template (single source of truth).
- `kickoff` = day 0 (setup); `handoff` = day 1 onward (maintenance). On a new project both fire — one sets up, the other maintains.
- Both skills work across **Chat, Cowork, Code, and Design**, adapting per surface; `kickoff`'s GitHub step is direct where a terminal exists and guided (commands handed to the user) where it does not.
- Australian English, ISO dates (`YYYY-MM-DD`).
- Skill install paths: `~/.claude/skills/` (global, Code), `<repo>/.claude/skills/` (per-project, committed), or claude.ai Settings upload. Skills do **not** sync across surfaces.
- `kickoff` creates repos **private by default**; this `claude-skills` repo is public by explicit user choice.
- The `SessionStart` hook's stdout is injected into context as a message (deterministic), which is what makes the post-reset handoff reload reliable — stronger than relying on the skill alone.

## 5. Decision log

*Append only — newest at the bottom.*

- **2026-06-23** — handoff relies on a continuously-maintained file rather than detecting the context limit. Why: the model can't reliably sense its own token budget. Rejected: auto-trigger an update at the limit (not feasible).
- **2026-06-23** — kickoff defers the `HANDOFF.md` format to the handoff skill instead of bundling its own copy. Why: single source of truth, avoid drift. Rejected: duplicating the template inside kickoff.
- **2026-06-23** — kickoff creates GitHub repos private by default. Why: avoid accidentally publishing code. Rejected: public default.
- **2026-06-23** — kickoff also writes a project `CLAUDE.md`. Why: make "commit on change" and "keep HANDOFF.md current" always-on, surviving the skill not re-firing mid-project.
- **2026-06-23** — "compact right after each handoff" was NOT added to the skill. Why: `/compact` is a built-in not exposed to programmatic (Skill-tool) invocation, and compacting per-update would be counterproductive. Rejected: skill-triggered compaction.
- **2026-06-23** — claude-skills licensed MIT and published public. Why: common permissive default for shareable tooling. Alternative noted: Apache-2.0.
- **2026-06-23** — Both skills made cross-surface (Chat, Cowork, Code, Design); kickoff's GitHub step adapts (direct on terminal surfaces, guided elsewhere). Why: the user wants the skills usable on every surface, not Code-only.
- **2026-06-23** — kickoff asks up front whether a HANDOFF.md already exists; if so, it waits for the file and resumes from it. Why: support picking up existing projects, not only greenfield ones.
- **2026-06-23** — Skill versions unified: the genericised example replaces the project-specific one everywhere, so the installed copy and the public copy are identical. Why: avoid divergence between personal and public.
- **2026-06-23** — The `SessionStart` hook is scoped to the `clear` and `compact` matchers (not no-matcher/all-sources). Why: the handoff should reload specifically on those resets, and those are the well-supported sources. Rejected: firing on every source including `startup` (which had reliability reports).

## 6. Change log

*Append only — newest at the top.*

- **2026-06-23** — Provided detailed steps to install the `SessionStart` hook scoped to `clear` + `compact` in `~/.claude/settings.json`, with JSON-merge and validation guidance.
- **2026-06-23** — Provided detailed GitHub publishing steps via the website (no CLI): create empty public repo, drag-and-drop the unzipped contents, commit.
- **2026-06-23** — Made both skills cross-surface; added kickoff's existing-HANDOFF.md resume branch; unified/genericised the template; repackaged both `.skill` files and re-zipped the repo; updated the README's surface note.
- **2026-06-23** — Assembled the `claude-skills` repo (README, LICENSE, .gitignore, both skills), genericised the handoff template example, zipped it for publishing.
- **2026-06-23** — Built the `kickoff` skill; validated and packaged.
- **2026-06-23** — Updated the `handoff` skill: added post-compaction re-read + state-check to behaviour 3; repackaged.
- **2026-06-23** — Built the `handoff` skill from the user's `handoff-global-default.md`; validated, packaged, installed globally in Code; documented a `SessionStart` hook for compaction resilience.

## 7. Next steps

*Editable — keep current.*

- [ ] Fill `[YOUR NAME OR ORG]` in `claude-skills/LICENSE`.
- [ ] Publish the repo — either `gh repo create claude-skills --public --source=. --remote=origin --push`, or the GitHub website drag-and-drop flow.
- [ ] Install the `SessionStart` hook (clear + compact) in `~/.claude/settings.json`; validate with `python3 -m json.tool` and `/hooks`.
- [ ] Re-install the updated `handoff` and install `kickoff` into `~/.claude/skills/` (`unzip -o`).
- [ ] (Optional) Build the `/handoff-out` slash command for the manual "update handoff → ready to compact" flow.
- [ ] (Optional) Test both skills on a real new project.

## 8. Open questions / blockers

*Editable.*

- LICENSE copyright holder not yet chosen (TBC — placeholder in file).
- Final repo name not locked (defaulted to `claude-skills`; user may rename).
- Licence choice not final (MIT in place; Apache-2.0 raised as an alternative).
