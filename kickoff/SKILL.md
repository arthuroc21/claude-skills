---
name: kickoff
description: Run the day-zero setup when a new project, repository, or build effort begins. Use this skill whenever the user starts something new — "let's build X", "I'm starting a new project", "new repo", "set up a project", "kick off", "let's get started on…" — or opens a fresh codebase with no scaffolding yet. It interviews for a few high-leverage details (including a name for the effort), sets up GitHub (linking an existing repo or creating a new private one, and committing on every change), and initialises HANDOFF.md plus a project CLAUDE.md — deferring the HANDOFF.md format to the handoff skill. Works across Chat, Cowork, Code, and Design, adapting per surface.
---

# Kickoff

## What this is for

This is the **day-zero** skill: it runs once, when a project or codebase is first being set up. Its job is to turn a vague "let's build X" into a project that is properly scaffolded — understood, version-controlled, and self-documenting — before real work begins.

It is the companion to the `handoff` skill: **kickoff sets the project up; handoff keeps it up to date from there.** Kickoff deliberately does **not** re-implement the HANDOFF.md format — the `handoff` skill owns that, and remains the single source of truth so the two never drift apart.

**Always a fresh start.** Treat the current conversation as the beginning of a *new* effort — even when it runs inside an existing project (a Cowork or Code workspace that already has files). Read that surrounding context, to ask sharper questions and to avoid clashing with what is already there, but still scaffold this as a new, **named** initiative with its own state rather than assuming you are continuing prior work. (Genuinely resuming earlier work is the one exception — handled in Step 3, when the user already has a `HANDOFF.md` to adopt.)

## Adapting to the surface

This runs on all four surfaces — Chat, Cowork, Code, and Design. Steps 1 (questions) and 3 (state files) work everywhere; what changes per surface is **how version control happens and where the files live**:

- **Claude Code** — full flow: `git`/`gh` in a terminal, files in the repo, committed on every change.
- **Cowork** — files live in the project folder, wherever it is synced (Google Drive, OneDrive, Dropbox, or local disk). One Cowork project often hosts several efforts, so first settle *which* folder this effort uses — a new named subfolder for this chat, an existing subfolder, or the project's main folder (see Step 1) — and create the state files there. If a terminal with `gh` is available, do the GitHub steps directly; if not, treat it like the no-terminal surfaces below.
- **Chat (claude.ai)** — no terminal, and no persistent filesystem between conversations. Produce the state files as downloadable artifacts (and suggest storing them in a Project so they persist), and do the GitHub part by giving the user the exact commands to run themselves.
- **Claude Design** — canvas- and session-oriented. Keep state inline and hand the user the files to store and version elsewhere.

## Step 1 — Understand what we're building

Open with a short, high-leverage set of questions — not a questionnaire. This is the kickoff of a **new** effort (see *Always a fresh start*): infer everything you can from the surrounding context first, and ask only what you genuinely cannot infer. Cover at most:

- **A name for this new effort** — used as the title of the conversation/session, the default name for the GitHub repo, and the `HANDOFF.md` title. On surfaces where you cannot set the conversation title yourself, suggest the user set it (e.g. `/rename <name>` in Claude Code).
- **What we're building and the end goal** — the North Star.
- **Stack / platform / language**, and where it will run or deploy.
- **Existing materials to build on** — any files, designs, docs, or code already in the project (or elsewhere) that this new effort should start from or reuse. Especially relevant when kickoff runs inside a workspace that already has content.
- **(Cowork only) Which folder this effort uses** — when running inside a Cowork project, ask where this effort's files should live: **(a)** a **new subfolder** for this chat, with a name the user chooses, created inside the project folder; **(b)** an **existing subfolder** to connect to and continue in; or **(c)** the project's **main folder**, as-is. This sets where `HANDOFF.md`, `CLAUDE.md`, and everything else for the effort are created. Lean toward a new named subfolder when the project folder already holds other work, so each effort stays self-contained — and create the folder once the user picks the name.
- **Whether a GitHub repo already exists** — this drives Step 2.
- **Whether they already have a HANDOFF.md to start from** — this drives Step 3.
- **Hard constraints** — deadline, required tools or services, things to avoid.

Ask them together, keep it tight, and start as soon as you have enough. Do not block the project on perfect answers — note anything still open as `(TBC)` and proceed.

## Step 2 — GitHub: link or create

How this step runs depends on the surface (see *Adapting to the surface*). Where a terminal with `git` and the GitHub CLI (`gh`) is available — Claude Code, and Cowork if it has one — do it directly, as below. Where there is no terminal — Chat, Design — instead produce the repo files and give the user the exact commands to run themselves; never claim to have pushed.

First, on a terminal-capable surface, **check the tooling**: confirm `gh` is installed and authenticated (`gh auth status`). If it is not authenticated, stop and ask the user to run `gh auth login` — never handle credentials yourself.

Then, based on Step 1:

- **Repo already exists** → link it. Verify the working directory is the right clone, or set the remote (`git remote add origin <url>`, or `git remote set-url origin <url>`), and confirm with `git remote -v`.
- **No repo yet** → create one, **private by default**, defaulting the repo name to the name from Step 1. If the directory is not a git repo yet, `git init`, add a `.gitignore`, and make an initial commit first, then create and push: `gh repo create <name> --private --source=. --remote=origin --push`. Make it public only if the user explicitly asks.

Add a sensible `.gitignore` for the stack before the first commit (dependencies, build output, env files, secrets). From then on, **commit and push after every significant change** — the same trigger the `handoff` skill uses. Write clear commit messages. Never commit secrets, keys, or `.env` files; never force-push a shared branch. On surfaces without a terminal, hand the user these commands and the same commit-on-change habit to run themselves.

## Step 3 — Initialise project state

Create two files at the project root (the repo root in Code; in Cowork, the effort folder chosen in Step 1 — a new subfolder, an existing one, or the project's main folder; downloadable/Project files in Chat; handed to the user in Design):

1. **HANDOFF.md** — the project's living state file. Based on the Step 1 answer about an existing HANDOFF.md:
   - **If they already have one** → wait for them to provide it (upload it, or point to its path), adopt it as the project's state file, and resume from its current state instead of starting blank. Read it, confirm where things stand in 2–3 lines, and let the `handoff` skill take over ongoing updates.
   - **If they do not** → create a new one, populated with what Step 1 established (name, summary, stack, current state, next steps).
   - Either way, defer to the `handoff` skill for the structure and all ongoing updates — do not re-specify the format here; it is the single source of truth.
2. **CLAUDE.md** — the project's standing conventions, so the continuous behaviours survive even when this skill is not re-triggered mid-project. Start from `assets/CLAUDE_md_core.md`, fill in the project overview and stack from Step 1, and write it as **project facts, not commands** (e.g. "This project commits on every change", not "You must commit") — imperative system-style phrasing can trip prompt-injection defences.

## What this establishes for the project

- A **private** GitHub repo (unless made public on request), updated on every significant change.
- A **HANDOFF.md** kept current by the `handoff` skill.
- A **CLAUDE.md** so "commit on change" and "keep HANDOFF.md current" are *always-on* for the project — not dependent on a skill re-firing. This is the on-demand-skill + always-on-CLAUDE.md pairing working together.
