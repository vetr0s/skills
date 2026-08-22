---
name: writing-for-agents
description: How to write a document an agent will execute. Use when creating or editing a skill in this repo, editing CLAUDE.md or AGENTS.md, or writing any file whose reader is an agent rather than a person. Covers frontmatter, descriptions that actually trigger, what to inline versus push behind a pointer, and how to prune.
---

# Writing for agents

A skill, a `CLAUDE.md`, and a reference file reached by a pointer are the same
kind of document. The packaging differs. The writing does not.

The goal is not a good-looking document. It is **low variance**: the agent takes
the same path through the work on every run.

## Mechanics

Every skill in this repo is `<name>/SKILL.md` with YAML frontmatter:

```yaml
---
name: kebab-case-name          # must match the directory name
description: <trigger text>    # the only thing loaded until the skill fires
---
```

Supporting files go in `<name>/assets/` for things the document hands to the
user, and `<name>/references/` for things the agent reads on demand. Reference
them by relative path so the skill still works when it is symlinked.

Run `install.sh` after adding a skill. It links every directory containing a
`SKILL.md` into `~/.claude/skills/`. Skills load at session start, so a new one
needs a fresh session.

## The description is the whole trigger

The body of a skill is invisible until it fires. The description is the only
thing the agent sees when deciding. A perfect body behind a vague description is
a skill that never runs.

A description does two jobs. It says what the material is, and it lists the
**branches** that should reach it. A branch is a distinct case the document
handles.

- **Front-load the first clause.** That is where the triggering happens.
- **One trigger per branch.** Synonyms that rename a single case are one branch
  written twice. Collapse them.
- **Quote the words the user will actually type.** `"why is this broken"` beats
  "diagnostic scenarios".
- **Cut identity the body already carries.** The description is not a summary.

When a skill fails to fire, fix the description before touching the body. That
is where the bug almost always is.

## Two budgets

Every document spends one of two things.

**Context load** is what always-loaded material costs the agent. A skill
description, a line in `CLAUDE.md`. It is paid every turn whether or not it
fires.

**Cognitive load** is what it costs me. Knowing which document exists and when
to reach for it. This one is not a cost to minimise. It is the price of keeping
judgment on my side, so spend it where my judgment matters and remove it where
it does not.

Material behind a pointer escapes context load and pays only for the pointer's
line.

## What goes where

A document holds two content types. **Steps** are the ordered actions.
**Reference** is the definitions and rules consulted on demand. They mix freely.

Rank each piece by how immediately the agent needs it:

1. **In-file step.** What the agent does, in order. The primary tier.
2. **In-file reference.** Consulted on demand. A flat set of peers is a fine
   arrangement, not a smell.
3. **Disclosed reference.** Pushed into a separate file and reached by a
   pointer, loaded only when the pointer fires.

The cleanest test is branching. Inline what every branch needs. Push behind a
pointer what only some branches reach.

Keep a concept's definition, rules, and caveats under one heading. Scattering
one meaning across a document is worse than saying it once in the wrong place.

**Sprawl** is the failure mode. A document too long even when every line is
true and unique. Attention thins across the excess. The cure is to disclose
reference behind pointers and split by branch.

## Completion criteria

Every step ends on the condition that says the work is done. Two things make
that condition a lever.

**Can the agent tell done from not-done?** A vague bound invites stopping early.
"Understanding reached" is not checkable. "You can name one command you have
already run, and paste its output" is.

**How much does it demand?** "Every modified file accounted for" forces real
work where "produce a change list" does not. The demand drives the digging that
never appears as its own step.

The strongest criteria are checkable and exhaustive at once.

If you notice the agent rushing a step because it can see easy steps waiting
behind it, sharpen the bound first. Only split the document if the bound is
genuinely fuzzy and the rushing is real.

## Leading words

A **leading word** is a compact idea the model already holds, reused as a token
rather than respelled as a sentence. *Tight*, *red*, *seam*, *lever*, *blast
radius*. Repeat the word and it accumulates meaning across the document and
anchors a whole region of behaviour cheaply.

Look for a triad spelled out at three different places, or a sentence that
gestures at one idea. Each is begging to collapse.

- "fast, deterministic, low-overhead" becomes *tight*.
- "a check you believe in" becomes *red*, which turns a fuzzy gate into a
  binary observable.

Prefer a word the model already knows. Coining your own works only if you define
it, and you pay in definition tokens what an existing word gives free.

## Prompt the positive

Steering by prohibition drags the forbidden thing into context and makes it
*more* available. Say "write one-line comments" rather than "do not write long
comments", so the banned behaviour is never named.

A prohibition earns its place only as a hard guardrail you cannot phrase
positively. The commit attribution rule in `CLAUDE.md` is one. Even then, pair
it with the positive target.

## Pruning

- **One source of truth per meaning.** The same rule in two places costs
  maintenance, costs tokens, and inflates that rule's apparent importance.
- **The environment is a source of truth too.** A Makefile target, a directory
  layout, `--help` output. A document that restates them is a cache, and it
  earns its keep only when the lookup is expensive. Cache the unwritten
  convention and the reason behind a choice. Leave the one-command lookups
  alone, where they cannot go stale.
- **Hunt no-ops.** An instruction the model already follows by default pays
  tokens to say nothing. The test is whether the line changes behaviour against
  the default, which you settle by running the document, not by arguing. When a
  sentence fails, delete the sentence. Do not trim words out of it.
- The same test grades leading words. A word too weak to beat the default is a
  no-op, and the fix is a stronger word, not a different technique.

Without pruning the default outcome is sediment. Stale layers settle because
adding feels safe and removing feels risky.

## House style

These documents follow `CLAUDE.md` like everything else. Short declarative
sentences, no em dashes, no mid-sentence commentary, sentence case headings, no
emoji. Run `unslop` over a skill before calling it done.

## Before you call it done

- The description names every branch and quotes real trigger phrases.
- Every step has a completion criterion you could check.
- Nothing in the body restates something the environment already says.
- No section duplicates a rule that lives in `CLAUDE.md`. Point at it instead.
- You reread it as an agent seeing it cold, mid-task, with no other context.
