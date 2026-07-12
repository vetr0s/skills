---
name: audit
description: Holistic read-only review of a project's current state — architecture, code health, correctness risks, tests, documentation drift, and tooling — using parallel exploration agents, reported as an HTML document. Use when the user says "audit the code", "audit this", "what's the state of this project", "review the whole codebase", or asks for a holistic/overall review rather than a review of a specific diff.
---

# Audit

A whole-project health check: what this codebase is, what shape it's in, and
what should be dealt with first. This is **not** a diff review — for the working
diff or a PR use `/code-review`. This looks at the project as it stands.

## Ground rules

**The audit is read-only.** Do not edit, refactor, format, or "quickly fix"
anything while auditing, however trivial. The deliverable is the report; the
user decides what gets acted on. If something is on fire, say so loudly in the
report and offer to fix it after.

**Every finding names a file and a line.** A claim you cannot point at is not a
finding, it is a vibe. Cut it.

**Rank by consequence, not by how easy it was to spot.** A silent data-loss path
outranks a hundred lint nits. If the codebase is fundamentally fine, the report
should say that plainly rather than manufacturing problems to look thorough.

## 1. Scope it first

Before spawning anything, spend a couple of minutes yourself: read the README
and any `CLAUDE.md`, look at the directory layout, the build/package manifest,
and the recent git log. You need enough of a map to write good agent prompts and
to tell what the project is *trying* to be. If the user pointed at a subdirectory
or a subsystem, audit that and treat the rest as context only.

## 2. Explore in parallel

Dispatch `Explore` agents concurrently — one per dimension, in a single message.
Use four to six; scale down for a small project, and split a dimension in two if
the codebase is large. Standard dimensions:

- **Architecture & structure.** What are the entry points, the layers, the data
  flow? Where does the actual work happen? What abstractions exist and do they
  earn their keep?
- **Correctness & risk.** Error handling, edge cases, concurrency, unchecked
  input, resource lifecycles, anything that loses data or fails silently.
- **Code health.** Duplication, dead code, inconsistent idioms across the
  codebase, complexity hotspots, TODOs that have outlived their author.
- **Tests & verification.** What exists, does it run, what's actually covered
  versus what merely has a test file, what is critical and untested.
- **Documentation drift.** README, `CLAUDE.md`, comments, and API docs against
  what the code really does. Instructions that no longer work are worse than
  missing ones.
- **Dependencies & tooling.** Build scripts, CI, pinning, unused or outdated
  deps, whether a newcomer could actually get this running.

Give each agent the map from step 1, tell it the audit is read-only, and require
that it return findings as `file:line` plus a one-sentence statement of the
problem and its consequence. Ask each for its honest read of what's *good* too —
the report needs to say what not to touch.

## 3. Verify before you believe

Agent findings are leads, not conclusions. Before anything reaches the report,
open the cited file and confirm it says what the agent claimed. Findings that
turn on runtime behavior deserve better than reading: run the test, run the
command, check the actual output. Drop anything that does not survive this, and
do not soften it into a "potential concern" — silently dropping a false positive
is the whole point of the step.

Where two agents surfaced the same underlying problem from different angles,
merge them into one finding.

## 4. Report

Write the report with the **standard-html** skill — read that skill and follow
it. Save to `docs/audit-YYYY-MM-DD.html`. Structure:

1. **Bottom line.** One paragraph: the state of this project in plain sentences,
   and the single most important thing to do about it.
2. **What's solid.** Briefly. Real, so the user knows what has been checked and
   found good.
3. **Findings**, ordered by consequence. Each one: what's wrong, where
   (`file:line`), what it costs, and what fixing it would take. Use the status
   tags for severity.
4. **Documentation drift**, called out separately — it is the finding type the
   user is least likely to notice unaided.
5. **Recommended order of work.** A short task list, not a backlog dump.

Close in the chat with the bottom line and the file path. Then stop — do not
start fixing things unless the user asks.
