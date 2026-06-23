# claude-skills — HANDOFF

**Last updated:** 2026-06-23 · **Phase:** **published & wired** — repo live and public on GitHub; both skills installed locally; `SessionStart` handoff-reload hook installed · **Surface(s):** now developed in Claude Code (local clone in Google Drive); originally authored in claude.ai chat; skills target all four surfaces (Chat, Cowork, Code, Design)

## 1. Summary / North Star

A public GitHub repo holding two complementary Claude Agent Skills — `kickoff` (day-zero project setup) and `handoff` (living `HANDOFF.md` maintenance) — so long-running projects stay resumable across Claude sessions. End goal: publish them publicly, installable in Claude Code and via claude.ai settings, working on every surface. The repo also serves as the ongoing workspace for any further skills.

## 2. Current state

Both skills are written, validated, unified, and cross-surface. **The repo is published** — live and public at **https://github.com/arthuroc21/claude-skills** (MIT, default branch `main`). The local clone / repo root is `G:\My Drive\Claude\Discovering Claude\Skills` (a cloud-synced folder — see caveat in §8). The LICENSE copyright holder is `arthuroc21`, and a project `CLAUDE.md` at the root makes "commit + push every skill change", "keep all copies in sync", and "keep HANDOFF.md current" standing conventions. Both skills are installed locally at `~/.claude/skills/{kickoff,handoff}`, kept identical to the repo. A `SessionStart` hook (clear + compact, `shell: bash`) is installed in `~/.claude/settings.json` to re-inject HANDOFF.md after a reset. This repo is the ongoing workspace for creating/editing/updating skills: every skill change here is committed/pushed to `claude-skills` and re-synced to the local install.

## 3. Map

> Paths below are relative to the repo root (`G:\My Drive\Claude\Discovering Claude\Skills`, published as `arthuroc21/claude-skills`).

| Name | Where | What it does |
|------|-------|--------------|
| HANDOFF.md | repo root | This living state file (committed; read at session start / after compaction) |
| CLAUDE.md | repo root | Standing project conventions: commit + push every change, sync all copies, keep HANDOFF.md current, public repo |
| README.md | repo root | Repo readme: what the skills do, install steps, optional compaction hook, cross-surface note |
| LICENSE | repo root | MIT licence; copyright holder `arthuroc21` |
| .gitignore | repo root | Ignores `*.skill`, `*.zip`, OS/editor cruft |
| handoff/SKILL.md | handoff/ | The handoff skill (cross-surface) |
| handoff/assets/HANDOFF_template.md | handoff/assets/ | 8-section state-file skeleton (genericised) |
| kickoff/SKILL.md | kickoff/ | The kickoff skill (cross-surface; resumes from an existing HANDOFF.md) |
| kickoff/assets/CLAUDE_md_core.md | kickoff/assets/ | Standing-conventions block for a project CLAUDE.md |
| local install | `~/.claude/skills/{kickoff,handoff}` | The active Claude Code copy; kept identical to the repo |
| claude-skills.zip / *.skill | `~/Downloads` (build outputs, gitignored) | The original packaged artifacts the repo was seeded from; superseded by the live repo |
| SessionStart hook (clear + compact) | `~/.claude/settings.json` (not in repo) | Re-injects `HANDOFF.md` into context after `/clear` or compaction; installed (shell=bash) |

## 4. Conventions and glossary

*Standing conventions for this work:*

- The `HANDOFF.md` format is owned **solely** by the `handoff` skill; `kickoff` defers to it and does not duplicate the template (single source of truth).
- `kickoff` = day 0 (setup); `handoff` = day 1 onward (maintenance). On a new project both fire — one sets up, the other maintains.
- Both skills work across **Chat, Cowork, Code, and Design**, adapting per surface; `kickoff`'s GitHub step is direct where a terminal exists and guided (commands handed to the user) where it does not.
- **Skills are platform-agnostic:** Cowork guidance covers any synced or local folder (Google Drive, OneDrive, Dropbox, local disk), not just Google Drive.
- **Sync every copy on change:** a skill edited here is committed/pushed to GitHub *and* re-copied to `~/.claude/skills/` so no copy drifts (encoded in `CLAUDE.md`).
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
- **2026-06-23** — Repo named `claude_skills` (underscore), superseding the tentative `claude-skills`. Why: explicit user instruction at kickoff in Claude Code. The local folder name (`Skills`) and README are unaffected; only the GitHub repo name changed.
- **2026-06-23** — LICENSE copyright holder set to `arthuroc21` (the user's GitHub identity). Why: user choice at kickoff; resolves the prior placeholder.
- **2026-06-23** — Published the repo **public** from Claude Code via `gh repo create` (not the website flow), seeded from `claude-skills.zip`. Why: a terminal with authenticated `gh` was available, so the direct path applied. Confirmed public visibility before pushing.
- **2026-06-23** — The repo doubles as the ongoing **workspace** for all future skills, not just the home of `kickoff`/`handoff`. Why: user wants every skill created here committed/pushed to `claude_skills`; encoded in `CLAUDE.md`.
- **2026-06-23** — Repo **renamed back to `claude-skills`** (hyphen), reversing the `claude_skills` choice two entries above. Why: explicit user instruction; the hyphenated name was the original suggestion and is preferred. Done via `gh repo rename` (GitHub auto-redirects the old URL) + `git remote set-url`. The earlier underscore entries are left as-is (append-only record of what was true at the time).
- **2026-06-23** — Generalised the skills' Cowork wording from "Google Drive" to any synced/local folder (Google Drive, OneDrive, Dropbox, local disk), and broadened handoff's write-failure note to cover OneDrive Files On-Demand / Dropbox online-only placeholders. Why: the skills must be platform-agnostic, not Google-Drive-specific.
- **2026-06-23** — Standing convention added: every skill change is propagated to **all** copies — pushed to GitHub *and* re-synced to `~/.claude/skills/`. The two skills were installed there (they had not been in `~/.claude/skills/` before; the session's `anthropic-skills` plugin provided byte-identical copies, but that path is session-scoped). Why: user wants local and remote kept in lockstep.
- **2026-06-23** — `SessionStart` hook installed in `~/.claude/settings.json` with `shell: "bash"` and matcher `clear|compact`. Why: the user is on Windows but has Git Bash, so a POSIX command with an explicit bash shell is the most reliable; pipe-tested positive (prints HANDOFF.md) and negative (silent when absent) before writing.
- **2026-06-23** — Updated the `kickoff` skill's Step 1: it now (a) treats every session as the start of a **new, named effort** even inside an existing Cowork/Code workspace — reading ambient context to sharpen questions but not assuming continuation ("Always a fresh start"); (b) asks for a **name** for the new effort (conversation/session title, default repo name, HANDOFF.md title); and (c) adds an "existing materials to build on" question. Why: user request. Other proposed additions (definition-of-done, scope/non-goals, audience) were offered but the user chose to keep the question set tight.

## 6. Change log

*Append only — newest at the top.*

- **2026-06-23** — `kickoff/SKILL.md`: added the "Always a fresh start / new named effort" framing, a **name** question, and an **existing-materials** question to Step 1 (and a note that the repo name defaults to the Step 1 name); updated the description. Synced to `~/.claude/skills/kickoff` and pushed.
- **2026-06-23** — Renamed the repo to `claude-skills`; generalised both skills' cloud-folder wording (any synced/local platform); installed both skills to `~/.claude/skills/` and added a sync-everywhere convention to `CLAUDE.md`; installed the `SessionStart` handoff-reload hook (clear+compact, shell=bash) in `~/.claude/settings.json`; committed + pushed.
- **2026-06-23** — **Ran `kickoff` in Claude Code and published the repo.** Seeded the working dir from `claude-skills.zip`, adopted the uploaded `HANDOFF.md` as the root state file, filled the LICENSE holder (`arthuroc21`), added a project `CLAUDE.md`, then `git init` → initial commit → `gh repo create claude_skills --public --push`. Live at https://github.com/arthuroc21/claude_skills (9 files, `main`).
- **2026-06-23** — Provided detailed steps to install the `SessionStart` hook scoped to `clear` + `compact` in `~/.claude/settings.json`, with JSON-merge and validation guidance.
- **2026-06-23** — Provided detailed GitHub publishing steps via the website (no CLI): create empty public repo, drag-and-drop the unzipped contents, commit.
- **2026-06-23** — Made both skills cross-surface; added kickoff's existing-HANDOFF.md resume branch; unified/genericised the template; repackaged both `.skill` files and re-zipped the repo; updated the README's surface note.
- **2026-06-23** — Assembled the `claude-skills` repo (README, LICENSE, .gitignore, both skills), genericised the handoff template example, zipped it for publishing.
- **2026-06-23** — Built the `kickoff` skill; validated and packaged.
- **2026-06-23** — Updated the `handoff` skill: added post-compaction re-read + state-check to behaviour 3; repackaged.
- **2026-06-23** — Built the `handoff` skill from the user's `handoff-global-default.md`; validated, packaged, installed globally in Code; documented a `SessionStart` hook for compaction resilience.

## 7. Next steps

*Editable — keep current.*

- [x] Fill the LICENSE copyright holder (`arthuroc21`). — done
- [x] Publish the repo. — done → https://github.com/arthuroc21/claude-skills
- [x] Install the `SessionStart` hook (clear + compact) in `~/.claude/settings.json`. — done (shell=bash); may need `/hooks` opened once or a restart to load in the current session.
- [x] Install `kickoff` + `handoff` into `~/.claude/skills/`. — done; kept in sync with the repo.
- [ ] (Optional) Build the `/handoff-out` slash command for the manual "update handoff → ready to compact" flow.
- [ ] (Optional) Test both skills on a real new project.

## 8. Open questions / blockers

*Editable.*

- ~~LICENSE copyright holder~~ — resolved: `arthuroc21`.
- ~~Final repo name~~ — resolved: `claude-skills`.
- Licence choice not final (MIT in place; Apache-2.0 raised as an alternative — low priority now that it's published).
- **Caveat:** the repo lives in a cloud-synced folder (currently Google Drive, `G:\My Drive\...`; the same risk applies to OneDrive, Dropbox, etc.). The sync client can race on `.git` internals (lock files, packed objects) and occasionally corrupt the local repo. GitHub is the source of truth, so any local corruption is recoverable by re-cloning. Consider excluding this folder from sync, or keeping the working clone on a non-synced local path.
