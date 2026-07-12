# skills

Personal [Claude Code](https://claude.com/claude-code) skills, kept in one repo and
symlinked into `~/.claude/skills/` so they version with git and follow me between
machines.

| Skill | What it does |
| --- | --- |
| [`audit`](audit/) | Read-only holistic review of a project — architecture, correctness, code health, tests, doc drift, tooling — via parallel exploration agents, reported as HTML. |
| [`commit`](commit/) | Writes commit messages that explain *why*. Never attributes the commit to Claude. |
| [`standard-html`](standard-html/) | Writes plans, audits, and design docs as plain HTML in a fixed house style instead of Markdown. |

## Install

```sh
git clone git@github.com:vetr0s/skills.git ~/sources/repos/skills
~/sources/repos/skills/install.sh
```

`install.sh` symlinks every skill directory into `~/.claude/skills/`. It is
idempotent, and it leaves any non-symlinked skills already living there alone.

## Adding a skill

Create `<name>/SKILL.md` with YAML frontmatter — `name` and a `description` that
spells out the trigger phrases, since the description is the only thing Claude sees
when deciding whether a skill is relevant. Supporting files (stylesheets,
templates, examples) go in `<name>/assets/`. Then re-run `install.sh`.

Skills are loaded at session start, so a new one needs a fresh session to show up.
