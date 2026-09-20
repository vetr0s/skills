#!/usr/bin/env bash
# Symlink every skill into each supported agent's user skill directory.
# Link the shared global instructions into each agent's config directory.
# Idempotent. Refuses to clobber a real file or directory that isn't ours.

repo=${BASH_SOURCE[0]%/*}
repo=$(cd "$repo" && pwd) || exit
install_home="${SKILLS_INSTALL_HOME:-$HOME}"
skill_dests=(
	"$install_home/.claude/skills"
	"$install_home/.agents/skills"
)

for dest in "${skill_dests[@]}"; do
	mkdir -p "$dest" || exit
done

link() {
	local target=$1
	local link=$2
	if [[ -e $link && ! -L $link ]]; then
		printf 'skip %s: exists and is not a symlink\n' \
			"${link/#$HOME/\~}" >&2
		return
	fi
	ln -sfn "$target" "$link" || return
	printf 'linked %s\n' "${link/#$HOME/\~}"
}

for skill in "$repo"/*/; do
	name=${skill%/}
	name=${name##*/}
	[[ -f $skill/SKILL.md ]] || continue
	for dest in "${skill_dests[@]}"; do
		link "$skill" "$dest/$name" || exit
	done
done

mkdir -p "$install_home/.claude" "$install_home/.codex" || exit
link "$repo/CLAUDE.md" "$install_home/.claude/CLAUDE.md" || exit
link "$repo/AGENTS.md" "$install_home/.codex/AGENTS.md" || exit
