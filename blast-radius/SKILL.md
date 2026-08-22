---
name: blast-radius
description: Work out what a change breaks somewhere else, before it ships, and prove the one fact it is safe because of by running code. Use for "blast radius", "what could this break", "is this safe to change", changes to a header or a public struct, and small diffs you do not trust. Use `how` to understand a subsystem and `debug` once something is already broken.
---

# Blast radius

Find what a change breaks somewhere other than where you made it.

Listing the callers is not the job. Grep does that in a second. The job is the
breakage grep will not show you.

## Do not trust your own writeup

A blast-radius writeup that sounds right is worthless. It reads as convincing
whether or not it is true, and that is the trap. So do not hand over the
writeup. Find the one or two facts the whole thing rests on and prove them by
running code.

### How sure are you

For each fact the change's safety depends on, get as far down this list as is
cheap, and say where you stopped.

1. **You said so.** Worth nothing on its own.
2. **You pointed at the line.** A real `file:line`, or the dependency's own
   source.
3. **You showed the bad case cannot happen.** You walked the failing path step
   by step and it does not reach.
4. **You ran it.** A program that calls the real code and fails loudly if you
   are wrong.
5. **You reproduced it in the running app.**

Any safety fact you cannot get to step 4, say so out loud. Do not write it up as
settled. Step 4 is usually one small file that includes the same header the
project ships and calls the exact function you are worried about.

## Steps

### 1. Read the change

The diff, the symbols it adds, changes, and removes, and what now behaves
differently. Include the part the diff does not spell out: a struct that grew, a
default that moved, an enum that gained a case, an allocation that changed
owner.

### 2. Find the one fact it is safe because of

Most changes that look frightening are safe because of a single fact. "This only
ever runs on entries already marked dead." "Nothing outside this file holds that
pointer past the frame." Find that fact. If it holds, the whole list of scary
cases dies at once.

Spend your time here, not on a long list of maybes.

### 3. Look where grep stops

This is the part that earns the skill. Grep finds callers of a symbol. It does
not find:

- **Layout changes.** A field added or reordered in a struct that something else
  memcpys, serializes, casts, or writes to disk. Anything that reads those bytes
  without going through the type is invisible to a symbol search.
- **Header ripple.** A macro whose expansion changed. An inline function whose
  body changed but whose callers were built earlier. A single-header library
  where the consumer defines the implementation macro in exactly one
  translation unit.
- **Stale artifacts.** Whether the build actually rebuilds every dependent
  object file when that header changes, or whether a stale `.o` will link
  cleanly and crash at runtime.
- **Ownership and lifetime.** Who frees this now, and did that move? Is a
  pointer kept across a resize that can reallocate?
- **Cross-language and on-disk readers.** A save file, a config format, a
  shader's expected uniform layout, a script binding, a test fixture checked in
  months ago.
- **Ordering.** Init order, teardown order, whether this now runs before or
  after something it used to follow.
- **Vendored copies.** Search the whole tree, not just `src/`. A vendored or
  duplicated copy of the same file will not be caught by a build.

### 4. Be honest about each risk

Give each one a real likelihood and a real cost. Keep the ones you confirmed.
List the ones you checked and cleared separately, because knowing what was
examined is half the value.

Cite a real `file:line`. A search that finds nothing is a legitimate answer, so
say so and give the search. Never invent a caller or an API.

### 5. Prove the one fact

Write the program, run it, paste what happened. For a native project this is
usually a twenty-line `main()` compiled against the real headers, or a run under
`-fsanitize=address,undefined` that would trip on the failure mode you are
worried about.

If you cannot prove it cheaply, mark it unproven. Do not round up.

## What to hand back

- **What changed.** Including the part that is not obvious from the diff.
- **The one fact it is safe because of.** State it, say which rung you reached,
  and show the proof. If you could not prove it, write "unproven".
- **Risks.** Only the real ones. Each names how it breaks, the `file:line`, how
  likely, how bad, and how to check.
- **Cleared.** What you looked at and why it is fine.
- **Before you merge.** The cheapest check that would catch the real bug,
  including the program you wrote.

Run it through `unslop` before handing it over.
