#!/usr/bin/env python3
"""Build the 'claude-skills' Cowork plugin bundle from every skill in this repo and
drop it into the sibling 'Cowork Skills Library' folder, ready to install in Cowork.

A "skill" is any top-level directory containing a SKILL.md. New skills are picked up
automatically; deleted ones simply stop being bundled.

Run manually:   python scripts/build_cowork_plugin.py
Runs automatically after each commit via .git/hooks/post-commit.
"""
import json
import os
import subprocess
import sys
import zipfile
from datetime import datetime

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LIBRARY = os.path.normpath(os.path.join(REPO, "..", "Cowork Skills Library"))
PLUGIN_NAME = "claude-skills"


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


def main():
    skills = find_skills()
    if not skills:
        print("[build-plugin] No skills (no */SKILL.md) found — nothing to build.")
        return 0

    count = git("rev-list", "--count", "HEAD", default="0")
    sha = git("rev-parse", "--short", "HEAD", default="local")
    version = "0.1.%s" % count if count.isdigit() else "0.1.0"
    built = datetime.now().strftime("%Y-%m-%d %H:%M")

    plugin_json = {
        "name": PLUGIN_NAME,
        "version": version,
        "description": "Custom Agent Skills by arthuroc21 — " + ", ".join(skills) + ".",
        "author": {"name": "arthuroc21"},
        "homepage": "https://github.com/arthuroc21/claude-skills",
        "repository": "https://github.com/arthuroc21/claude-skills",
        "license": "MIT",
        "keywords": skills,
    }

    plugin_readme = (
        "# %s\n\n" % PLUGIN_NAME
        + "Custom Agent Skills bundled for Claude Cowork. "
        + "Version %s (built %s, commit %s).\n\n" % (version, built, sha)
        + "Skills in this bundle:\n\n"
        + "".join("- `%s:%s`\n" % (PLUGIN_NAME, s) for s in skills)
        + "\nSource of truth: https://github.com/arthuroc21/claude-skills\n"
    )

    os.makedirs(LIBRARY, exist_ok=True)
    out_plugin = os.path.join(LIBRARY, PLUGIN_NAME + ".plugin")
    tmp = out_plugin + ".tmp"
    with zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr(".claude-plugin/plugin.json", json.dumps(plugin_json, indent=2) + "\n")
        z.writestr("README.md", plugin_readme)
        for s in skills:
            for root, _dirs, files in os.walk(os.path.join(REPO, s)):
                for f in files:
                    full = os.path.join(root, f)
                    rel = os.path.relpath(full, REPO).replace("\\", "/")
                    z.write(full, "skills/" + rel)
    os.replace(tmp, out_plugin)

    index = (
        "# Cowork Skills Library\n\n"
        "Installable bundle of our custom Claude skills, rebuilt automatically from the\n"
        "`claude-skills` repo on every commit. Reference this folder from Cowork and\n"
        "install the bundle to get every skill at once.\n\n"
        "## `%s.plugin`  (v%s, built %s)\n\n" % (PLUGIN_NAME, version, built)
        + "Bundles %d skill(s): " % len(skills)
        + ", ".join("`%s:%s`" % (PLUGIN_NAME, s) for s in skills) + ".\n\n"
        "### Install in Cowork\n"
        "1. Open a Cowork chat and attach `%s.plugin` from this folder.\n" % PLUGIN_NAME
        + "2. Press **Install / Accept** on the preview.\n"
        "3. Type `/` — the skills appear as `%s:<name>`.\n\n" % PLUGIN_NAME
        + "Updating: the file here refreshes automatically, but Cowork does **not**\n"
        "auto-pull — reinstall the latest `.plugin` from this folder to apply changes\n"
        "(or to drop a skill that was deleted).\n\n"
        "Source: https://github.com/arthuroc21/claude-skills\n"
    )
    with open(os.path.join(LIBRARY, "README.md"), "w", encoding="utf-8") as fh:
        fh.write(index)

    size = os.path.getsize(out_plugin)
    print("[build-plugin] Wrote %s (v%s, %d skills, %d bytes)"
          % (out_plugin, version, len(skills), size))
    print("[build-plugin] Library: %s" % LIBRARY)
    return 0


if __name__ == "__main__":
    sys.exit(main())
