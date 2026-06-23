# Claude Skills — `kickoff` & `handoff`

Two complementary [Agent Skills](https://code.claude.com/docs/en/skills) for keeping long-running projects coherent across Claude sessions — so a fresh Claude instance (or a new teammate) can always pick up where the last one left off.

- **`kickoff`** — the *day-zero* skill. When a new project or repo begins, it asks a short set of high-leverage questions, sets up GitHub (links an existing repo or creates a new private one, then commits on every significant change), and initialises the project's state files.
- **`handoff`** — the *day-one-onward* skill. It maintains a living `HANDOFF.md` that captures the project's full state — summary, current status, file map, decision log, change log, next steps, and blockers — updated automatically on every significant change.

## How they fit together

`kickoff` sets a project up; `handoff` keeps it up to date from there. `kickoff` does **not** re-implement the `HANDOFF.md` format — `handoff` owns that, so the two never drift apart. On a new project, both fire: one does the setup, the other takes over maintenance.

The guiding idea behind both is the **cold-start test**: write things down so that a fresh instance with zero memory of the conversation could resume the work by reading one file alone.

## What's inside

```
.
├── handoff/
│   ├── SKILL.md
│   └── assets/
│       └── HANDOFF_template.md      # the 8-section state-file skeleton
└── kickoff/
    ├── SKILL.md
    └── assets/
        └── CLAUDE_md_core.md        # standing-conventions block for a project's CLAUDE.md
```

## Install

### Claude Code

Drop the skill folders into a skills directory — Claude Code discovers them automatically.

```bash
# Global — available in every project
cp -r handoff kickoff ~/.claude/skills/

# …or per-project, committed to the repo so teammates inherit it
cp -r handoff kickoff <your-repo>/.claude/skills/
```

A new skill is picked up on the next session; if the skills directory already existed when the session started, it takes effect within the session.

### claude.ai

Zip a single skill folder and upload it in **Settings → Capabilities/Skills**:

```bash
cd handoff && zip -r ../handoff.zip . && cd ..
```

> Note: skills do **not** sync across surfaces — install separately in Claude Code and in claude.ai.

### Optional — keep the handoff alive through context compaction (Claude Code)

When Claude Code auto-compacts a long conversation, this `SessionStart` hook re-feeds `HANDOFF.md` so the session resumes from the real state rather than a lossy summary. Add it to `~/.claude/settings.json`:

```json
{
  "hooks": {
    "SessionStart": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "f=\"$CLAUDE_PROJECT_DIR/HANDOFF.md\"; test -f \"$f\" && { echo '=== HANDOFF.md (current project state — read before continuing) ==='; cat \"$f\"; } || true"
          }
        ]
      }
    ]
  }
}
```

## Conventions

The `HANDOFF.md` template defaults to **Australian English** and **ISO dates** (`YYYY-MM-DD`, for sortability) — change to taste. Both skills work across **Chat, Cowork, Code, and Design**, adapting per surface: where a terminal with `git` and the [GitHub CLI (`gh`)](https://cli.github.com/) is available, `kickoff` does the GitHub setup directly; where there is none, it runs the questions, initialises the files, and hands you the commands to run yourself.

## License

MIT — see [`LICENSE`](LICENSE).
