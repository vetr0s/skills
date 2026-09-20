---
name: bash
description: Write, edit, or review Bash scripts using Dave Eddy's YSAP Bash Style Guide. Use for .sh files, Bash shebangs, shell automation, "write a bash script", and "review this shell script". Do not apply Bash-only rules to scripts that deliberately target POSIX sh.
---

# Bash

Write safe Bash in the style defined by the
[YSAP Bash Style Guide](https://style.ysap.sh). Preserve behavior when editing
an existing script.

## Choose Bash deliberately

Use `#!/usr/bin/env bash` unless the target environment requires a fixed path.
Keep a POSIX `sh` script portable when Bash features add no value.

Prefer Bash builtins and keywords over external commands. Use parameter
expansion for string edits, arrays for lists, globs for files, arithmetic
contexts for integers, and `read -r` for structured input. Stream line-based
data through `while read -r` instead of storing it for a `for` loop.

## Format

- Indent with tabs and keep lines within 80 columns.
- Leave at most one blank line in a row.
- Put `then` beside `if` and `do` beside its loop.
- Use semicolons only where block syntax requires them.
- Write functions as `name()`. Make every function variable `local`.
- Preserve comments unless their meaning changes.

## Expansions and tests

Use `[[ ... ]]` for tests. Use `((...))` and `$((...))` for integer work. Use
`$(...)` for command substitution.

Use single quotes for literal strings. Use double quotes when the string needs
expansion. Quote every expansion that can undergo word splitting. Add braces
only when they separate a variable name from adjacent text.

Use lowercase variable names. Reserve uppercase names for constants and
exported environment variables. Use `declare` only for associative arrays.

## External commands

Pass file names directly when a command accepts them. Avoid useless `cat`
pipelines. Do not parse `ls`. Prefer portable options over GNU-only options.

Avoid executable-location tricks when the caller can pass a path or run from a
documented directory. Use `BASH_SOURCE` only when locating adjacent files is
part of the script's job.

## Failures

Check fallible operations at the point where later commands depend on them.
Write `cd "$dir" || exit` before commands that require the new directory.
Return failures from helper functions when callers can recover.

Do not enable `errexit`. Handle expected failure explicitly. Never use `eval`.
Use arrays or indirect expansion instead.

## Verify

Run `bash -n` on every changed script. Run ShellCheck when it is already
available. Execute the real script or its smallest safe behavior check. The
work is done when syntax, style, and the observed behavior all pass.
