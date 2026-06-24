#!/usr/bin/env python3
"""Generate the Claude Code plugin-marketplace files from the skills in this repo.

Writes, IN-REPO (these are tracked files, unlike the external Cowork plugins):
  - .claude-plugin/marketplace.json      lists every skill as an installable plugin
  - <skill>/.claude-plugin/plugin.json   per-skill plugin manifest

A "skill" is any top-level dir containing a SKILL.md. Each becomes a skills-only plugin
whose single SKILL.md sits at the plugin root — supported by Claude Code: "If a plugin has
no skills/ directory and no skills manifest field, a SKILL.md at the plugin root is loaded
as a single skill" (the frontmatter `name` fixes the invocation name). New skills are
picked up automatically; a deleted skill drops out of marketplace.json on the next run
(its folder, with its plugin.json, is already gone).

Users then:  /plugin marketplace add arthuroc21/claude-skills
             /plugin install <skill>@claude-skills

Run on skill add / remove / description change, BEFORE committing (the files are tracked):
    python scripts/build_marketplace.py

Deliberately NOT wired into the post-commit hook: it writes tracked files, so running it
post-commit would leave the working tree dirty after every commit. (The Cowork build, which
writes OUTSIDE the repo, is the post-commit one.) Version is intentionally omitted so each
plugin tracks the git commit SHA and users receive updates automatically as commits land.
"""
import json
import os
import re
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OWNER = "arthuroc21"
REPO_URL = "https://github.com/arthuroc21/claude-skills"
MARKET_NAME = "claude-skills"


def find_skills():
    out = []
    for name in sorted(os.listdir(REPO)):
        if name.startswith("."):
            continue
        if os.path.isfile(os.path.join(REPO, name, "SKILL.md")):
            out.append(name)
    return out


def frontmatter_description(skill):
    try:
        text = open(os.path.join(REPO, skill, "SKILL.md"), encoding="utf-8").read()
        fm = re.search(r"^---\s*$(.*?)^---\s*$", text, re.S | re.M)
        if fm:
            m = re.search(r"^description:\s*(.+)$", fm.group(1), re.M)
            if m:
                return m.group(1).strip().strip('"').strip("'")
    except Exception:
        pass
    return ""


def short_desc(full, cap=300):
    """First sentence of the (long) SKILL.md description, for the marketplace listing."""
    full = " ".join(full.split())
    if not full:
        return ""
    m = re.search(r"^(.{40,}?[.!?])\s", full + " ")
    s = m.group(1) if m else full
    if len(s) > cap:
        head = s[:cap]
        sp = head.rfind(" ")
        s = (head[:sp] if sp >= 80 else head).rstrip() + "…"
    return s


def write_json(path, obj):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=2, ensure_ascii=False)
        f.write("\n")


def main():
    skills = find_skills()
    plugins = []
    for s in skills:
        desc = short_desc(frontmatter_description(s)) or ("Custom Agent Skill: %s." % s)
        write_json(
            os.path.join(REPO, s, ".claude-plugin", "plugin.json"),
            {
                "name": s,
                "description": desc,
                "author": {"name": OWNER},
                "homepage": "%s/tree/main/%s" % (REPO_URL, s),
                "repository": REPO_URL,
                "license": "MIT",
            },
        )
        plugins.append({
            "name": s,
            "source": "./%s" % s,
            "description": desc,
            "category": "productivity",
            "license": "MIT",
        })
        print("[build-marketplace] %s/.claude-plugin/plugin.json" % s)

    write_json(
        os.path.join(REPO, ".claude-plugin", "marketplace.json"),
        {
            "name": MARKET_NAME,
            "owner": {"name": OWNER},
            "description": "Public marketplace of Claude Agent Skills for project "
                           "setup and cross-session continuity.",
            "plugins": plugins,
        },
    )
    print("[build-marketplace] .claude-plugin/marketplace.json (%d plugin(s))" % len(plugins))
    return 0


if __name__ == "__main__":
    sys.exit(main())
