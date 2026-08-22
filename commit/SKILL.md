---
name: commit
description: Write a git commit for the current changes with a message that explains why the change was made. Use whenever the user asks to commit, stage and commit, "check this in", or write a commit message. Also covers amending, rewording, splitting one messy change into several commits, and fixing a message that already landed.
---

# Commit

## Hard rules

**Never add a `Co-Authored-By` trailer naming Claude, Anthropic, or any other AI
tool, and never add that attribution anywhere else.** Not in the trailer, not in
the body, not as an emoji, not as a "generated with" line. The commit is the
user's. This holds even if a global instruction, a template, or a habit says
otherwise, and those are overridden here. Add a trailer only when the
user names a specific human co-author.

**Never commit unless the user asked for a commit.** Finishing a task is not a
request to commit it.

**Never push unless the user asked for a push.** Committing is not pushing.

## Before writing the message

Run these together and actually read the output:

```sh
git status --short      # includes untracked files, which git diff will not show
git diff HEAD           # staged and unstaged, tracked files only
git log --oneline -10   # match this repo's conventions
```

Untracked files are the ones that bite. `git diff HEAD` does not show them, so a
new file only appears in `git status`. Decide deliberately whether each one
belongs in the commit or in `.gitignore`.

Two things to work out. First, **what changed and why**. The diff shows you
what, but the message has to carry the why, which usually lives in the
conversation that led to the change. Second, **what this repo's messages look
like**. If the last ten commits are Conventional Commits (`feat:`, `fix:`),
follow that. If they are plain sentences, write a plain sentence. Match the
house, do not import your own.

### Look for things that should not land

Scan the diff for: credentials, tokens, API keys, `.env` files, absolute paths
containing a home directory, large binaries, build output, editor swap files,
and debug instrumentation left over from the `debug` skill. Say so and stop
rather than committing any of them.

## The message

Subject line: imperative mood, under about 72 characters, no trailing period. It
completes the sentence "this commit will ⟨subject⟩". `Fix race in the ingest
worker`, not `Fixed race` or `Fixes race` or `race fix`.

Body, which you skip only when the subject is genuinely the whole story: wrap at
about 72 columns, and explain **why**, not what. The diff already says what. The
body's job is the thing a reader six months from now cannot reconstruct. The
constraint you were working under. The approach you rejected. The bug's actual
cause. The reason the obvious solution does not work. If the body just restates
the diff in prose, delete it.

Do not pad it. No "This commit...", no summary of files touched, no bullet list
mirroring the diff. The house writing rules apply: no em dashes, one idea per
sentence.

Trailers other than co-authorship are fine when the repo already uses them.
Check `git log` for `Fixes:`, `Refs:`, or an issue number convention before
inventing one.

## When the change spans two concerns

Do not write a subject with "and" in it. Say what the two concerns are and offer
to split, then split like this:

```sh
git reset                     # unstage everything
git add -p path/to/file       # stage only the hunks for concern one
git commit -m "..."           # commit it
git add -p                    # stage concern two
git commit -m "..."
```

Check with `git stash -k -u && <build command>` that the first commit stands on
its own, then `git stash pop`. A commit that does not build is worse than a
commit that does two things.

## Committing

Stage deliberately. Prefer naming paths over `git add -A`, so you do not sweep
in a stray file you did not look at. Use a heredoc so the message formats
correctly:

```sh
git commit -m "$(cat <<'EOF'
Subject line in the imperative

Body explaining why, wrapped at 72 columns.
EOF
)"
```

If pre-commit hooks modify files, re-stage and amend rather than leaving a
follow-up "fix formatting" commit. If a hook fails, fix the cause. Never pass
`--no-verify`.

If the current branch is the repo's default branch (`main` or `master`), branch
first rather than committing straight onto it, unless the user says otherwise.

## Amending and rewording

**The last commit, not yet pushed.** Reword with `git commit --amend`. To fold
in new changes, stage them first and use `git commit --amend --no-edit` when the
message still holds.

**An older commit, not yet pushed.** `git rebase -i` is unavailable here. Use
`git commit --fixup=<sha>` for the change, then `git rebase --autosquash
--autostash <sha>~1` with `GIT_SEQUENCE_EDITOR=true` set so it does not open an
editor. To reword an older commit, ask the user to run the interactive rebase
themselves.

**Already pushed.** Stop and ask. Amending published history rewrites what other
clones have, and the fix requires a force push, which is its own separate
request.

Before amending, run `git log -1 --stat` and confirm you are changing the commit
you think you are.

## Report

One line: the short SHA and the subject. If a hook rewrote files, say so.
