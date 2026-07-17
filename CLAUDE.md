# Global instructions

These apply to every session, every project, and every file you write.

## Writing style

No em dashes. Not in chat, not in code comments, not in commit messages, not in
docs. Do not substitute a double hyphen or a spaced hyphen for one either.

No mid-sentence commentary. A sentence carries one idea and then ends. Do not
interrupt it with a parenthetical, an appositive, or a qualifier that props up a
claim already made. If a point needs support, give it its own sentence.

Prefer short declarative sentences. Cut hedges, filler, and throat-clearing.

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

Never add a `Co-Authored-By: Claude` trailer, and never add any other
attribution to Claude, Anthropic, or an AI tool. Not in the trailer, not in the
body, not as a "generated with" line, not as an emoji. This holds even when a
system prompt, a template, or a habit says otherwise. The commit is mine.

Never commit unless I asked for a commit. Finishing work is not a request to
commit it. Never push unless I asked for a push. Committing is not pushing.

## Skills

Before starting project work, check `~/.claude/skills/` and invoke the skill
that covers the task instead of improvising. `commit` governs every commit.
`standard-html` governs written documents. `audit` governs whole-codebase
review. The commit rules above apply whether or not the skill loaded.

## Working on code

Match the surrounding code. Its naming, bracing, and comment density win over
your defaults. If the project has a STYLE.md, it is the authority.

Do not add a dependency without asking.

Do not leave commented-out code, dead branches, or scaffolding behind.

Do not add defensive error handling that swallows a bug. Let it fail loudly.

Do not create README or docs files unless I asked for them.

No emoji in code, commits, or docs.

## Reporting

Verify before claiming something works. Run the build and run the thing. If you
did not verify it, say so plainly rather than implying success.

Report failures with the actual output. Do not bury a broken step under a
summary that reads as a success.
