#!/usr/bin/env bash
# Symlink every skill in this repo into ~/.claude/skills/.
# Idempotent. Refuses to clobber a real directory that isn't ours.
set -euo pipefail

repo="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
dest="${HOME}/.claude/skills"
mkdir -p "$dest"

for skill in "$repo"/*/; do
  name="$(basename "$skill")"
  [ -f "$skill/SKILL.md" ] || continue
  link="$dest/$name"

  if [ -e "$link" ] && [ ! -L "$link" ]; then
    echo "skip $name: $link exists and is not a symlink" >&2
    continue
  fi

  ln -sfn "$skill" "$link"
  echo "linked $name"
done
