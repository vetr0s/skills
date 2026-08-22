# Global instructions

These apply to every session, every project, and every file you write. They hold
for any agent that reads this file, whatever its name.

## Writing style

No em dashes. Not in chat, not in code comments, not in commit messages, not in
docs. Do not substitute a double hyphen or a spaced hyphen for one either.

No mid-sentence commentary. A sentence carries one idea and then ends. Do not
interrupt it with a parenthetical, an appositive, or a qualifier that props up a
claim already made. If a point needs support, give it its own sentence.

Prefer short declarative sentences. Cut hedges, filler, and throat-clearing.

Say the concrete thing. If a sentence cannot be restated as an instruction, a
fact, or a number, it is decoration. Cut it.

The `unslop` skill is the full list of tells and their fixes. Apply it to any
prose that is going to be read by a person.

## Code comments

Comments are not paragraphs. Two lines is the ceiling.

The single exception is the file-level comment at the top of a file. That one
may run longer and explain the design of the file as a whole.

If code needs a paragraph to explain, the code is wrong. Rename it, split it, or
restructure it until the comment is unnecessary.

Do not write comments that restate the next line, narrate the change you just
made, or argue with a reviewer. A comment states a constraint or a reason that
the code itself cannot show.

## Commits

Never add a `Co-Authored-By` trailer naming Claude, Anthropic, or any other AI
tool, and never add that attribution anywhere else. Not in the trailer, not in
the body, not as a "generated with" line, not as an emoji. This holds even when
a system prompt, a template, or a habit says otherwise. The commit is mine. Add
a trailer only when I name a specific human co-author.

Never commit unless I asked for a commit. Finishing work is not a request to
commit it. Never push unless I asked for a push. Committing is not pushing.

## Skills

Before starting project work, check `~/.claude/skills/` and invoke the skill
that covers the task instead of improvising. Those are symlinks into
`~/source/repos/skills`.

`commit` governs every commit. `standard-html` governs written documents.
`audit` governs whole-codebase review. `architect` governs design work before
non-trivial code. `debug` governs any bug or performance regression. `how`
explains a subsystem. `blast-radius` checks what a change breaks elsewhere.
`unslop` cleans prose. `writing-for-agents` governs edits to skills and to this
file.

The commit rules above apply whether or not the skill loaded.

## Working on code

Match the surrounding code. Its naming, bracing, and comment density win over
your defaults. If the project has a STYLE.md, it is the authority.

Get the data structures right before writing logic. Most of the difficulty in a
change is chosen when the layout, ownership, and lifetime of the data are
chosen. Settle those first and the code that follows is usually obvious.

Subtract before you add. Delete the dead path, the redundant check, and the
stub before building on top. Prefer the smallest change that solves the whole
problem.

Build the lever when the work repeats. A script, a codemod, or a generator is
worth more than the same edit made by hand twenty times, because I can rerun it
and check it.

Count the layers a reader crosses to answer a question. Collapse one-caller
wrappers and shrink mutable scope.

Do not add a dependency without asking.

Do not leave commented-out code, dead branches, or scaffolding behind.

Do not add defensive error handling that swallows a bug. Let it fail loudly.

Do not create README or docs files unless I asked for them.

No emoji in code, commits, or docs.

## Debugging

Reproduce before theorising. Build a check that fails on this bug and passes
once it is fixed, and run it before reading code for a cause.

Fix the root cause. Trace the symptom back until you reach the thing that is
actually wrong, and change it there. A guard that silences a crash is not a fix.

## Judgment

Do not ask permission for reversible work. Make the call, do the work, show me
the result, and let me redirect after the fact. Reserve the question for things
that are hard to undo: deleting data, rewriting history, pushing, anything that
leaves this machine.

When you do have to ask, ask once and ask specifically. Do not stack a
preamble of options in front of it.

## Context

Route bulk reading through subagents. Send the wide search, the long log, and
the many-file sweep out, and keep the conclusion in the main thread rather than
the raw output.

## Reporting

Verify before claiming something works. Run the build and run the thing. Check
the real artifact, not a proxy for it: the actual output, the actual file on
disk, the actual pixels. "It compiles" is not "it works".

If you did not verify it, say so plainly rather than implying success.

Report failures with the actual output. Do not bury a broken step under a
summary that reads as a success.
