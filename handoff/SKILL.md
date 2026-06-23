---
name: handoff
description: Maintain a living HANDOFF.md that captures a project's full state — summary, current status, file map, decision log, change log, next steps, and blockers — so a fresh Claude instance with no prior memory (or a new human teammate) can resume the work by reading that one file. Use this skill whenever starting a new project or repository; resuming or picking up an existing one ("where did we leave off", "continue the X project", "pick up where we stopped"); setting up cross-session continuity or persistent context; or when the user asks to create, read, or update a handoff / state snapshot / session-handoff document. Also use it proactively to keep HANDOFF.md current whenever a significant change happens — a decision made or reversed, a file or resource added or removed, a milestone hit, a blocker raised or cleared, a scope or approach change — without waiting to be asked.
---

# Handoff

## What this is for

Long projects span many sessions, and context evaporates between them: auto-memory is lossy, and a fresh instance of Claude starts blind. This skill keeps a single living file, `HANDOFF.md`, that holds enough of the project's state for the work to resume cleanly from it alone.

**The governing principle — the cold-start test.** Write `HANDOFF.md` so that a fresh instance of Claude, with zero memory of the conversation (or a new human teammate), could pick the project back up by reading this one file. If something essential lives only in the conversation, it is not captured yet. Every decision about what to include comes back to this test.

## The three behaviours

1. **At project start** — if `HANDOFF.md` does not already exist, create it from `assets/HANDOFF_template.md`.
2. **On every significant change** — update `HANDOFF.md` *without being asked*. This is a standing default, not a task to wait for. Do it quietly as part of the work — do not turn every edit into an announcement or stop to ask permission.
3. **At the start of a session, and after any context compaction** — treat it as a cold start: re-read `HANDOFF.md` first, summarise the current state and next steps in 2–3 lines, and do a quick state-check before continuing. A compaction replaces the live conversation with a lossy summary, so `HANDOFF.md` is what restores the real state and tells you where the reset conversation should resume. On surfaces with no persistent filesystem (Chat, Design), there is no automatic file to read, so look for one the user has provided — uploaded, pasted, or kept in a Project — before assuming there is none. If no `HANDOFF.md` is present and this is clearly an ongoing project, offer to start one.

A *significant change* is: a decision made or reversed; a file created, renamed, moved or deleted; a change of approach or stack; a milestone completed; a blocker raised or cleared; a change of scope; an external resource added; next steps altered. When in doubt, if a returning reader would want to know it, log it.

## Where HANDOFF.md lives

This skill applies on all four surfaces — Chat, Cowork, Code, and Design. The behaviours above are the same everywhere; only persistence differs, so put the file where it will actually survive on each:

- **Claude Code** — `HANDOFF.md` at the repository root. Edit the real file on each change, and commit it so teammates inherit it. It coexists with `CLAUDE.md`: that file holds standing rules and conventions, this one holds state and history.
- **Cowork** — `HANDOFF.md` in the project folder, wherever it is synced (Google Drive, OneDrive, Dropbox, or local disk). If it sits in a cloud-sync client that streams files on demand (Google Drive for Desktop, OneDrive Files On-Demand, Dropbox online-only) and writes fail, the file is likely an online-only placeholder — mark the file or folder "Available offline" / "Always keep on this device" to fix it.
- **Chat (claude.ai)** — there is no persistent file between conversations and no background process. Maintain `HANDOFF.md` within the session and hand it back as a file the user can save. To carry it across conversations it must live in a Project as a reference document, or be pasted/uploaded at the start of the next session. A Preferences line can make the *behaviour* default, but the *file* still has to be stored deliberately.
- **Claude Design** — canvas- and session-oriented, the least file-based surface. Keep the state inline and give the user the file to store elsewhere.

## Structure

Use `assets/HANDOFF_template.md` as the exact skeleton — copy it and fill it in rather than rebuilding the layout from memory, so the format stays identical across sessions. The italic convention notes under each section are meant to stay (they keep the file self-explaining); the `[bracketed]` bits are placeholders to replace with real content.

The sections and why each exists:

- **Header** — project name, last-updated timestamp, phase, surface(s). Orientation at a glance.
- **1. Summary / North Star** — what the project is and the end goal.
- **2. Current state** — where work left off, what is working, what is outstanding. The first thing a returning reader checks.
- **3. Map** — a table of files, repos, datasets, connectors and APIs (name · where · what it does), so nothing important is invisible.
- **4. Conventions and glossary** — naming, stack, terminology a newcomer would not know.
- **5. Decision log** — append only, newest at the bottom: date · decision · why · alternatives rejected. Stops settled choices being silently relitigated.
- **6. Change log** — append only, newest at the top: date · what changed. The running history.
- **7. Next steps** — editable; keep current.
- **8. Open questions / blockers** — editable.

## Discipline

These rules are what keep the file trustworthy:

- **Real facts, never placeholders.** If a detail does not exist yet, write `(TBC)` — never invent a plausible-sounding value, and strip every `[bracketed]` prompt from the template once filled. A handoff full of fiction is worse than no handoff.
- **Concise and factual.** It is a working document, not a narrative.
- **Sections 5 and 6 only grow.** They are the historical record — append, do not edit or delete.
- **Do not reopen logged decisions** unless the user asks.
- **Current instruction wins.** If what the user says now conflicts with the file, the new instruction takes precedence — follow it and update the file to match.
- **Australian English**, ISO dates (`YYYY-MM-DD`), so the file is sortable and matches the user's conventions.
