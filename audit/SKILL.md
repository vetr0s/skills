---
name: audit
description: Whole-project read-only review of a project's current state, covering architecture, code health, correctness risks, tests, documentation drift, and tooling, using parallel exploration agents and reported as an HTML document. Use when the user says "audit the code", "audit this", "what's the state of this project", "review the whole codebase", or asks for a holistic or overall review rather than a review of a specific diff.
---

# Audit

A whole-project health check: what this codebase is, what shape it is in, and
what to deal with first.

This is **not** a diff review. For the working diff or a PR use `/code-review`.
For what one change might break elsewhere use `blast-radius`. For understanding
one subsystem rather than judging the whole project use `how`. This looks at the
project as it stands.

## Ground rules

**The audit is read-only.** Do not edit, refactor, format, or quickly fix
anything while auditing, however trivial. The deliverable is the report. The
user decides what gets acted on. If something is on fire, say so loudly in the
report and offer to fix it after.

**Every finding names a file and a line.** A claim you cannot point at is not a
finding, it is a vibe. Cut it.

**Rank by consequence, not by how easy it was to spot.** A silent data-loss path
outranks a hundred lint nits. If the codebase is fundamentally fine, the report
should say that plainly rather than manufacturing problems to look thorough.

## 1. Scope it first

Before spawning anything, spend a few minutes yourself. Read the README, any
`CLAUDE.md` or `AGENTS.md`, and any `STYLE.md`. Look at the directory layout,
the build manifest, and the recent git log. You need enough of a map to write
good agent prompts and to tell what the project is *trying* to be.

**Establish what is out of scope and say so in the report.** Do not audit
`vendor/`, `third_party/`, `node_modules/`, `build/`, generated files, or
anything the project did not write. Findings there are noise, and grepping them
drowns the real signal. Check `.gitignore` and the build script for what is
generated.

If the user pointed at a subdirectory or a subsystem, audit that and treat the
rest as context only.

Scale the audit to the project. A four-file library gets two agents and a short
report. Manufacturing six dimensions for a small project produces padding.

## 2. Explore in parallel

Dispatch `Explore` agents concurrently, one per dimension, in a single message.
Use four to six, and split a dimension in two if the codebase is large.

- **Architecture and structure.** Entry points, layers, data flow. Where the
  actual work happens. What abstractions exist and whether they earn their keep.
- **Correctness and risk.** Error handling, edge cases, concurrency, unchecked
  input, resource lifecycles, anything that loses data or fails silently. In C
  and Odin, add ownership and lifetime: who allocates, who frees, what holds a
  pointer across a resize.
- **Code health.** See the sharper standard below.
- **Tests and verification.** What exists, whether it runs, what is actually
  covered versus what merely has a test file, what is critical and untested.
- **Documentation drift.** README, `CLAUDE.md`, comments, and API docs against
  what the code really does. Instructions that no longer work are worse than
  missing ones.
- **Dependencies and tooling.** Build scripts, CI, pinning, unused or outdated
  deps, whether a newcomer could actually get this running.

Give each agent the map from step 1, the out-of-scope list, and the instruction
that the audit is read-only. Require findings as `file:line` plus a one-sentence
statement of the problem and its consequence. Ask each for its honest read of
what is **good** too. The report needs to say what not to touch.

### The code health standard

Generic "this could be cleaner" findings are worthless. Have that agent look for
specific, countable things:

- **Files that outgrew their name.** A file whose name no longer predicts its
  contents. Give the line count and say what the second thing inside it is.
- **Functions that grew a second job.** Look for a function whose name contains
  "and", or whose body has two clearly separated halves.
- **Condition growth.** A branch chain that has been extended repeatedly, each
  time by one more case, until nobody can say what the default behaviour is.
  Count the branches and the distinct variables tested.
- **Shallow abstractions.** A wrapper whose interface is nearly as complicated
  as the thing it wraps. Apply the deletion test: if deleting it makes
  complexity vanish, it is a pass-through and it costs more than it gives.
- **Copy-and-diverge.** The same logic in several places where the copies have
  since drifted apart. The drift is the finding, not the duplication.
- **Idiom inconsistency.** Two different ways of doing the same thing in one
  codebase, especially error handling and allocation.
- **TODOs that outlived their author.** `git blame` them and give the date. A
  TODO from two years ago is a decision, not a plan.
- **Dead code.** Unreferenced functions, unreachable branches, flags never set.

## 3. Verify before you believe

Agent findings are leads, not conclusions. Before anything reaches the report,
open the cited file and confirm it says what the agent claimed.

Findings that turn on runtime behavior deserve better than reading. Run the
test, run the build, check the actual output. A performance claim without a
measurement is not a finding.

Drop anything that does not survive this. Do not soften a false positive into a
"potential concern". Silently dropping it is the whole point of the step.

Where two agents surfaced the same underlying problem from different angles,
merge them into one finding.

## 4. Severity

Use one scale so the tags mean the same thing every time.

| Tag | Meaning |
| --- | --- |
| `tag-bad` | Loses data, corrupts state, crashes, or leaks something secret. Fix before shipping anything else. |
| `tag-warn` | Real defect or real drag on the work, but nothing is currently on fire. |
| `tag-good` | Checked and sound. Say so explicitly. |

Anything that fits none of the three is a nit. Nits do not get a row in the
table. Collect them in one sentence or drop them.

## 5. Report

Write the report with the **standard-html** skill. Read that skill and follow
it. Save to `docs/audit-YYYY-MM-DD.html`. Structure:

1. **Bottom line.** One paragraph: the state of this project in plain sentences,
   and the single most important thing to do about it.
2. **Scope.** What was audited and what was excluded, so the reader knows what
   the silence covers.
3. **What's solid.** Briefly, and real, so the user knows what has been checked
   and found good.
4. **Findings**, ordered by consequence. Each one: what is wrong, where
   (`file:line`), what it costs, and what fixing it would take.
5. **Documentation drift**, called out separately. It is the finding type the
   user is least likely to notice unaided.
6. **Recommended order of work.** A short task list, not a backlog dump.

Close in the chat with the bottom line and the file path. Then stop. Do not
start fixing things unless the user asks.
