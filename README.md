# skills

Personal agent skills kept in one repo. The installer links each skill into
Claude Code and Codex so the same files work in both agents.

The skills use the open agent skills layout. Each skill is a directory with a
`SKILL.md` file and optional scripts, references, and assets.

`CLAUDE.md` is the single source of truth for global instructions. `AGENTS.md`
is a symlink to it. The installer links that shared file into each agent's
global instruction location.

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

`install.sh` creates these links:

| Agent | Skills | Global instructions |
| --- | --- | --- |
| Claude Code | `~/.claude/skills/` | `~/.claude/CLAUDE.md` |
| Codex | `~/.agents/skills/` | `~/.codex/AGENTS.md` |

The installer is idempotent. It leaves any non-symlinked file or directory
already living at a destination alone.

## Adding a skill

Read [`writing-for-agents`](writing-for-agents/). Then create `<name>/SKILL.md`
with YAML frontmatter: a `name` matching the directory, and a `description` that
spells out the trigger phrases, since the description is the only thing the agent
sees when deciding whether the skill is relevant. Supporting files go in
`<name>/assets/` for things handed to the user and `<name>/references/` for
things the agent reads on demand. Then re-run `install.sh`.

Restart the agent when a new skill does not appear.

## Credits

Six of these are adapted from MIT-licensed work by Lauren Tan, Matt Pocock, and
Cursor. See [`NOTICE.md`](NOTICE.md).
