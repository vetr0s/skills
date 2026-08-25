#!/usr/bin/env bash
# Symlink every skill into each supported agent's user skill directory.
# Link the shared global instructions into each agent's config directory.
# Idempotent. Refuses to clobber a real file or directory that isn't ours.
set -euo pipefail

repo="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
install_home="${SKILLS_INSTALL_HOME:-$HOME}"
skill_dests=(
  "$install_home/.claude/skills"
  "$install_home/.agents/skills"
)

for dest in "${skill_dests[@]}"; do
  mkdir -p "$dest"
done

link() {
  local target="$1" link="$2"
  if [ -e "$link" ] && [ ! -L "$link" ]; then
    echo "skip ${link/#$HOME/\~}: exists and is not a symlink" >&2
    return
  fi
  ln -sfn "$target" "$link"
  echo "linked ${link/#$HOME/\~}"
}

for skill in "$repo"/*/; do
  name="$(basename "$skill")"
  [ -f "$skill/SKILL.md" ] || continue
  for dest in "${skill_dests[@]}"; do
    link "$skill" "$dest/$name"
  done
done

mkdir -p "$install_home/.claude" "$install_home/.codex"
link "$repo/CLAUDE.md" "$install_home/.claude/CLAUDE.md"
link "$repo/AGENTS.md" "$install_home/.codex/AGENTS.md"
