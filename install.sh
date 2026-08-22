#!/usr/bin/env bash
# Symlink every skill in this repo into ~/.claude/skills/, and the global
# CLAUDE.md into ~/.claude/.
# Idempotent. Refuses to clobber a real file or directory that isn't ours.
set -euo pipefail

repo="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
dest="${HOME}/.claude/skills"
mkdir -p "$dest"

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
  link "$skill" "$dest/$name"
done

link "$repo/CLAUDE.md" "${HOME}/.claude/CLAUDE.md"
