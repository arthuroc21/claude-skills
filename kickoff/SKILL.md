---
name: kickoff
description: Run the day-zero setup when a new project, repository, or build effort begins. Use this skill whenever the user starts something new — "let's build X", "I'm starting a new project", "new repo", "set up a project", "kick off", "let's get started on…" — or opens a fresh codebase with no scaffolding yet. It does three things, in order — (1) asks a short set of high-leverage questions about what is being built and its constraints; (2) sets up GitHub — links an existing repo or creates a new private one, then commits and pushes on every significant change; (3) initialises HANDOFF.md and a project CLAUDE.md so the project has durable state and standing conventions from the start. Defers to the handoff skill for the HANDOFF.md structure and its ongoing maintenance — it does not duplicate that format. Works across Chat, Cowork, Code, and Design, adapting per surface — doing the GitHub setup directly where a terminal exists, and guiding the user through it where it does not.
---

# Kickoff

## What this is for

This is the **day-zero** skill: it runs once, when a project or codebase is first being set up. Its job is to turn a vague "let's build X" into a project that is properly scaffolded — understood, version-controlled, and self-documenting — before real work begins.

It is the companion to the `handoff` skill: **kickoff sets the project up; handoff keeps it up to date from there.** Kickoff deliberately does **not** re-implement the HANDOFF.md format — the `handoff` skill owns that, and remains the single source of truth so the two never drift apart.

## Adapting to the surface

This runs on all four surfaces — Chat, Cowork, Code, and Design. Steps 1 (questions) and 3 (state files) work everywhere; what changes per surface is **how version control happens and where the files live**:

- **Claude Code** — full flow: `git`/`gh` in a terminal, files in the repo, committed on every change.
- **Cowork** — files live in the project folder (Google Drive or local). If a terminal with `gh` is available, do the GitHub steps directly; if not, treat it like the no-terminal surfaces below.
- **Chat (claude.ai)** — no terminal, and no persistent filesystem between conversations. Produce the state files as downloadable artifacts (and suggest storing them in a Project so they persist), and do the GitHub part by giving the user the exact commands to run themselves.
- **Claude Design** — canvas- and session-oriented. Keep state inline and hand the user the files to store and version elsewhere.

## Step 1 — Understand what we're building

Open with a short, high-leverage set of questions — not a questionnaire. Infer everything you can from the context first, and ask only what you genuinely cannot infer. Cover at most:

- **What we're building and the end goal** — the North Star.
- **Stack / platform / language**, and where it will run or deploy.
- **Whether a GitHub repo already exists** — this drives Step 2.
- **Whether they already have a HANDOFF.md to start from** — this drives Step 3.
- **Hard constraints** — deadline, required tools or services, things to avoid.

Ask them together, keep it tight, and start as soon as you have enough. Do not block the project on perfect answers — note anything still open as `(TBC)` and proceed.

## Step 2 — GitHub: link or create

How this step runs depends on the surface (see *Adapting to the surface*). Where a terminal with `git` and the GitHub CLI (`gh`) is available — Claude Code, and Cowork if it has one — do it directly, as below. Where there is no terminal — Chat, Design — instead produce the repo files and give the user the exact commands to run themselves; never claim to have pushed.

First, on a terminal-capable surface, **check the tooling**: confirm `gh` is installed and authenticated (`gh auth status`). If it is not authenticated, stop and ask the user to run `gh auth login` — never handle credentials yourself.

Then, based on Step 1:

- **Repo already exists** → link it. Verify the working directory is the right clone, or set the remote (`git remote add origin <url>`, or `git remote set-url origin <url>`), and confirm with `git remote -v`.
- **No repo yet** → create one, **private by default**. If the directory is not a git repo yet, `git init`, add a `.gitignore`, and make an initial commit first, then create and push: `gh repo create <name> --private --source=. --remote=origin --push`. Make it public only if the user explicitly asks.

Add a sensible `.gitignore` for the stack before the first commit (dependencies, build output, env files, secrets). From then on, **commit and push after every significant change** — the same trigger the `handoff` skill uses. Write clear commit messages. Never commit secrets, keys, or `.env` files; never force-push a shared branch. On surfaces without a terminal, hand the user these commands and the same commit-on-change habit to run themselves.

## Step 3 — Initialise project state

Create two files at the project root (the repo root in Code; the project folder in Cowork; downloadable/Project files in Chat; handed to the user in Design):

1. **HANDOFF.md** — the project's living state file. Based on the Step 1 answer about an existing HANDOFF.md:
   - **If they already have one** → wait for them to provide it (upload it, or point to its path), adopt it as the project's state file, and resume from its current state instead of starting blank. Read it, confirm where things stand in 2–3 lines, and let the `handoff` skill take over ongoing updates.
   - **If they do not** → create a new one, populated with what Step 1 established (summary, stack, current state, next steps).
   - Either way, defer to the `handoff` skill for the structure and all ongoing updates — do not re-specify the format here; it is the single source of truth.
2. **CLAUDE.md** — the project's standing conventions, so the continuous behaviours survive even when this skill is not re-triggered mid-project. Start from `assets/CLAUDE_md_core.md`, fill in the project overview and stack from Step 1, and write it as **project facts, not commands** (e.g. "This project commits on every change", not "You must commit") — imperative system-style phrasing can trip prompt-injection defences.

## What this establishes for the project

- A **private** GitHub repo (unless made public on request), updated on every significant change.
- A **HANDOFF.md** kept current by the `handoff` skill.
- A **CLAUDE.md** so "commit on change" and "keep HANDOFF.md current" are *always-on* for the project — not dependent on a skill re-firing. This is the on-demand-skill + always-on-CLAUDE.md pairing working together.
