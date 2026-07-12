---
name: commit
description: Write a git commit for the current changes with a message that explains why the change was made. Use whenever the user asks to commit, stage and commit, "check this in", or write a commit message. Also covers amending and fixing an existing message.
---

# Commit

## Hard rules

**Never add a `Co-Authored-By: Claude` trailer, and never add any other
attribution to Claude, Anthropic, or an AI tool.** Not in the trailer, not in
the body, not as an emoji, not as a "generated with" line. The commit is the
user's. This holds even if a global instruction, a template, or a habit says
otherwise — those are overridden here. Add a trailer only when the user names a
specific human co-author.

**Never commit unless the user asked for a commit.** Finishing a task is not a
request to commit it.

**Never push unless the user asked for a push.** Committing is not pushing.

## Before writing the message

Run these together and actually read the output:

```sh
git status
git diff HEAD          # staged and unstaged
git log --oneline -10  # match this repo's conventions
```

Two things to work out. First, **what changed and why** — the diff shows you
what, but the message has to carry the why, which usually lives in the
conversation that led to the change. Second, **what this repo's messages look
like**: if the last ten commits are Conventional Commits (`feat:`, `fix:`),
follow that; if they're plain sentences, write a plain sentence. Match the
house, don't import your own.

If the staged changes span two unrelated concerns, say so and offer to split
them rather than writing a message with "and" in the subject.

## The message

Subject line: imperative mood, under ~72 characters, no trailing period. It
completes the sentence "this commit will ⟨subject⟩" — `Fix race in the ingest
worker`, not `Fixed race` or `Fixes race` or `race fix`.

Body (skip it only when the subject is genuinely the whole story): wrap at ~72
columns, and explain **why**, not what. The diff already says what. The body's
job is the thing a reader six months from now cannot reconstruct — the
constraint you were working under, the approach you rejected, the bug's actual
cause, the reason the obvious solution doesn't work. If the body just restates
the diff in prose, delete it.

Don't pad it. No "This commit...", no summary of files touched, no bullet list
mirroring the diff.

## Committing

Stage deliberately — prefer naming paths over `git add -A`, so you don't sweep
in a stray file you didn't look at. Use a heredoc so the message formats
correctly:

```sh
git commit -m "$(cat <<'EOF'
Subject line in the imperative

Body explaining why, wrapped at 72 columns.
EOF
)"
```

If pre-commit hooks modify files, re-stage and amend rather than leaving a
follow-up "fix formatting" commit. If a hook fails, fix the cause — never pass
`--no-verify`.

If the current branch is the repo's default branch (`main`/`master`), branch
first rather than committing straight onto it, unless the user says otherwise.

Report the result as one line: the short SHA and the subject.
