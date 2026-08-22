# skills

Personal [Claude Code](https://claude.com/claude-code) skills, kept in one repo
and symlinked into `~/.claude/skills/` so they version with git and follow me
between machines.

`CLAUDE.md` is the single source of truth for global instructions. `AGENTS.md`
is a symlink to it, so an agent that looks for that name finds the same rules.

## Skills

| Skill | What it does |
| --- | --- |
| [`architect`](architect/) | Designs the shape of a change before writing it. Caller usage first, then types and signatures, with competing shapes compared before one is picked. |
| [`audit`](audit/) | Read-only whole-project review: architecture, correctness, code health, tests, doc drift, tooling. Parallel agents, reported as HTML. |
| [`blast-radius`](blast-radius/) | Works out what a change breaks somewhere else, and proves the one fact it is safe because of by running code. |
| [`commit`](commit/) | Writes commit messages that explain *why*. Never attributes the commit to an AI tool. Covers amending and splitting. |
| [`debug`](debug/) | Diagnosis loop built around a fast check that goes red on the bug. Covers native crashes, memory errors, and frame-time regressions. |
| [`how`](how/) | Explains how a subsystem works, at onboarding depth. Can also critique the architecture. |
| [`standard-html`](standard-html/) | Writes plans, audits, and design docs as plain HTML in a fixed house style instead of Markdown. |
| [`unslop`](unslop/) | Strips AI tells out of prose. A catalogue of the patterns with their fixes. |
| [`writing-for-agents`](writing-for-agents/) | How to write a document an agent will execute. Governs edits to the skills in this repo and to `CLAUDE.md`. |

## Install

```sh
git clone git@github.com:vetr0s/skills.git ~/source/repos/skills
~/source/repos/skills/install.sh
```

`install.sh` symlinks every skill directory into `~/.claude/skills/`, and
`CLAUDE.md` into `~/.claude/`. It is idempotent, and it leaves any non-symlinked
file already living there alone.

## Adding a skill

Read [`writing-for-agents`](writing-for-agents/). Then create `<name>/SKILL.md`
with YAML frontmatter: a `name` matching the directory, and a `description` that
spells out the trigger phrases, since the description is the only thing the agent
sees when deciding whether the skill is relevant. Supporting files go in
`<name>/assets/` for things handed to the user and `<name>/references/` for
things the agent reads on demand. Then re-run `install.sh`.

Skills load at session start, so a new one needs a fresh session to show up.

## Credits

Six of these are adapted from MIT-licensed work by Lauren Tan, Matt Pocock, and
Cursor. See [`NOTICE.md`](NOTICE.md).
