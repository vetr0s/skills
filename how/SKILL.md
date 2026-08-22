---
name: how
description: Explain how a subsystem works, at the level of an engineer being onboarded onto it. Use for "how does X work", "walk me through X", "explain this subsystem", a code walkthrough before changing something, and placement questions like "where should this live" or "which layer owns this". Can also critique the architecture on request. Use `audit` for whole-project health and `blast-radius` for what a change breaks.
---

# How

Build a working mental model of a subsystem and hand it over. The target is what
a good engineer would say while onboarding someone onto the code. Not annotated
source.

Two modes. **Explain** is the default. **Critique** adds an architectural
teardown on top, and only fires when the user asks for problems rather than
understanding.

## 1. Read the question

Work out what is actually being asked:

- A subsystem. "How does the renderer work?"
- A flow. "What happens between keypress and pixel?"
- A structure. "How is the asset pipeline laid out?"
- A placement question. "Where should input remapping live?"

If it is ambiguous, state your best reading in one line and go. Do not ask.
The user will redirect if you are off.

## 2. Decide how much machinery it needs

**Narrow** means one file or one function. Explore and explain in a single pass
yourself. Skip to step 4.

**Wide** means a subsystem crossing several files, or a flow that touches
multiple layers. Fan out first.

When in doubt, go narrow. You can always fan out after hitting a wall.

## 3. Fan out

Split the question into two to four **non-overlapping slices** and dispatch one
`Explore` agent per slice, all in a single message. The slices are the whole
design decision here. For "how does the renderer work":

- Resource lifetime and ownership.
- The per-frame path from update to draw call.
- Shader and pipeline setup.

Give every agent the same instructions:

- Start broad, then follow one thread. From an entry point, trace the call
  chain, the data flow, and the type definitions.
- Read the code. Do not infer behaviour from a file name or a function name.
- Stop when you can describe the path from input to output with no step
  hand-waved.
- Return `file:line` for every claim.
- Note what is surprising, and what a newcomer would get wrong.

Overlap between agents is fine. You reconcile it.

## 4. Write the explanation

Prose, not pseudocode. Reference `file:line` so the reader can go look, and quote
code only when the shape of the code is itself the point.

Structure, adapted to the question. Not every section fires every time.

**What it is.** One or two paragraphs. What it does and why it exists. Enough
for the reader to decide whether to keep going.

**The pieces.** The types, structs, and functions that carry the design. Brief
definition of each. Only the ones needed to follow the rest.

**How it works.** The core. What triggers it, what happens in order, where the
data goes, where the decisions are made. This is most of the document.

**Where things live.** A short map of the relevant files. Not every file. The
ones you would open first.

**Gotchas.** The non-obvious parts. The thing that looks wrong but is load
bearing. The historical reason something is shaped strangely. The sharp edge
that will bite.

If the explanation runs long enough to want a table, a status column, or more
than four sections, write it with `standard-html` instead of dumping it into
chat.

## 5. Critique mode

Only when the user asked for problems, not understanding.

Explain first. You cannot critique architecture you have not traced.

Then dispatch two to four agents against the explanation and the real files,
each with a different lens:

- **Coupling.** What knows about what, and what should not.
- **Ownership and lifetime.** Who allocates, who frees, who may hold a pointer,
  and for how long. In C and Odin this is where the real bugs live.
- **Depth.** Is a lot of behaviour sitting behind a small interface, or is the
  interface nearly as complicated as the thing it wraps? A module whose deletion
  would make complexity vanish was a pass-through.
- **Change cost.** Pick the two changes most likely to be asked for next. How
  many files does each touch?

Then judge the results yourself. You are the lead, not an aggregator. Sort every
finding into:

- **Act on.** Real, worth fixing now.
- **Consider.** Real, but the cost is unclear.
- **Noted.** True and low priority.
- **Dismissed.** Wrong, missing context, or taste.

Say why for each dismissal. An agent finding you cannot confirm in the file is
not a finding.

Present the explanation first, then the critique below it. Someone who only
wanted to understand the system should not have to wade through the teardown.

## Done when

Every step of the flow is traced, no step is hand-waved, and every claim about
the code points at a `file:line` you actually opened.
