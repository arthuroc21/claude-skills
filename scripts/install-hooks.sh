#!/bin/sh
# Install this project's git hooks into .git/hooks.
# Git hooks are NOT version-controlled, so run this once after cloning:
#   sh scripts/install-hooks.sh
set -e
root="$(git rev-parse --show-toplevel)"
hook="$root/.git/hooks/post-commit"
cat > "$hook" <<'HOOK'
#!/bin/sh
# Auto-rebuild the per-skill Cowork plugins into "../Skills Library" after each
# commit. Installed by scripts/install-hooks.sh. Failures never block the commit.
root="$(git rev-parse --show-toplevel)"
python "$root/scripts/build_cowork_plugin.py" || true
HOOK
chmod +x "$hook"
echo "Installed post-commit hook -> $hook"
