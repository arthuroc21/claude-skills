#!/usr/bin/env python3
"""Build one Cowork plugin per skill in this repo, into the sibling
'Cowork Skills Library' folder, so each skill can be installed individually in Cowork.

A "skill" is any top-level directory containing a SKILL.md. Each skill becomes its own
<skill>.plugin (plugin name = skill name, so it shows in Cowork as <skill>:<skill>).
New skills are picked up automatically; deleted skills have their stale .plugin removed.

Run manually:   python scripts/build_cowork_plugin.py
"""
import json
import os
import re
import subprocess
import sys
import zipfile
from datetime import datetime

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LIBRARY = os.path.normpath(os.path.join(REPO, "..", "Cowork Skills Library"))


def git(*args, default=""):
    try:
        return subprocess.check_output(
            ["git", "-C", REPO, *args], stderr=subprocess.DEVNULL
        ).decode().strip()
    except Exception:
        return default


def find_skills():
    skills = []
    for name in sorted(os.listdir(REPO)):
        if name.startswith("."):
            continue
        d = os.path.join(REPO, name)
        if os.path.isdir(d) and os.path.isfile(os.path.join(d, "SKILL.md")):
            skills.append(name)
    return skills


def skill_description(skill):
    """Pull the frontmatter `description:` from the skill's SKILL.md (capped)."""
    try:
        text = open(os.path.join(REPO, skill, "SKILL.md"), encoding="utf-8").read()
        fm = re.search(r"^---\s*$(.*?)^---\s*$", text, re.S | re.M)
        if fm:
            dm = re.search(r"^description:\s*(.+)$", fm.group(1), re.M)
            if dm:
                desc = dm.group(1).strip().strip('"').strip("'")
                return (desc[:280] + "…") if len(desc) > 280 else desc
    except Exception:
        pass
    return "Custom Agent Skill: %s." % skill


def build_one(skill, version, built, sha):
    plugin_json = {
        "name": skill,
        "version": version,
        "description": skill_description(skill),
        "author": {"name": "arthuroc21"},
        "homepage": "https://github.com/arthuroc21/claude-skills",
        "repository": "https://github.com/arthuroc21/claude-skills",
        "license": "MIT",
    }
    readme = (
        "# %s\n\n" % skill
        + "Custom Agent Skill for Claude Cowork. "
        + "Version %s (built %s, commit %s).\n\n" % (version, built, sha)
        + "Install this `.plugin` in Cowork, then run it from the `/` menu as "
        + "`%s:%s`.\n\nSource: https://github.com/arthuroc21/claude-skills\n" % (skill, skill)
    )
    out = os.path.join(LIBRARY, skill + ".plugin")
    tmp = out + ".tmp"
    with zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr(".claude-plugin/plugin.json", json.dumps(plugin_json, indent=2) + "\n")
        z.writestr("README.md", readme)
        for root, _dirs, files in os.walk(os.path.join(REPO, skill)):
            for f in files:
                full = os.path.join(root, f)
                rel = os.path.relpath(full, REPO).replace("\\", "/")  # e.g. kickoff/SKILL.md
                z.write(full, "skills/" + rel)
    os.replace(tmp, out)


def main():
    skills = find_skills()
    os.makedirs(LIBRARY, exist_ok=True)

    count = git("rev-list", "--count", "HEAD", default="0")
    sha = git("rev-parse", "--short", "HEAD", default="local")
    version = "0.1.%s" % count if count.isdigit() else "0.1.0"
    built = datetime.now().strftime("%Y-%m-%d %H:%M")

    expected = set()
    for s in skills:
        build_one(s, version, built, sha)
        expected.add(s + ".plugin")
        print("[build-plugin] %s.plugin (v%s)" % (s, version))

    # Remove stale .plugin files (deleted skills, or the old combined bundle)
    for f in os.listdir(LIBRARY):
        if f.endswith(".plugin") and f not in expected:
            os.remove(os.path.join(LIBRARY, f))
            print("[build-plugin] removed stale %s" % f)

    lines = [
        "# Cowork Skills Library\n",
        "Individual, installable Cowork plugins — **one per skill** — rebuilt "
        "automatically from the `claude-skills` repo. Install only the ones you need.\n",
        "| Skill | File | In Cowork |",
        "|-------|------|-----------|",
    ]
    for s in skills:
        lines.append("| `%s` | `%s.plugin` | `%s:%s` |" % (s, s, s, s))
    lines += [
        "",
        "## Install in Cowork",
        "1. Open a Cowork chat and attach the `<skill>.plugin` you want.",
        "2. Press **Install / Accept** on the preview.",
        "3. Type `/` — the skill appears as `<skill>:<skill>`.",
        "",
        "Updating: files here refresh automatically, but Cowork does not auto-pull — "
        "reinstall a `.plugin` to apply its changes (or to drop a deleted skill).",
        "",
        "Built %s · v%s · Source: https://github.com/arthuroc21/claude-skills" % (built, version),
    ]
    with open(os.path.join(LIBRARY, "README.md"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")

    print("[build-plugin] %d plugin(s) in %s" % (len(skills), LIBRARY))
    return 0


if __name__ == "__main__":
    sys.exit(main())
