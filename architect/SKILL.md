---
name: architect
description: Design the shape of a change before writing it. Sketch the caller's usage, the types, and the signatures first, compare competing shapes, then implement against the chosen one. Use for "plan this", "design this", "architect this", "how should I structure X", "what's the plan for", and any non-trivial work where jumping into code would lock in the wrong shape.
---

# Architect

Decide the shape before filling it in. The output of the design phase is a
sketch: the caller's usage, the types, and the signatures, with bodies left as
`not implemented`.

The purpose is not ceremony. It is that the shape of a change is the expensive
decision, and it is cheapest to change while it is still a page of signatures.

## Track the phases

Open a todo list with one entry per phase before starting. Long design work
loses phases silently otherwise.

1. Ground
2. Sketch
3. Choose
4. Implement
5. Scrap

## Phase 1: Ground

Build a real model of every part of the system the new code touches. Run the
`how` skill over those subsystems. Use critique mode when the existing structure
is the constraint, or when the design will have to push back on it.

Naming a file is not grounding. You need the traced flow that `how` produces.

Skip this phase only when the work is genuinely greenfield with nothing around
it to integrate.

## Phase 2: Sketch

**Write the caller's usage first.** Before any type, write the code that will
call this thing, as you wish it read. Everything else derives from that. A
design that starts from the implementation and works outward produces an
interface shaped like its own internals.

Then produce, for each candidate:

- **The types.** Structs, enums, and their fields. What owns what. What lives
  how long.
- **The signatures.** Every public function, with bodies left as `not
  implemented` or a line of pseudocode.
- **The file map.** What lives where, and what includes what.
- **The rationale.** A paragraph on why this shape, and what it gives up.

Generate **two or three genuinely different shapes**, not one shape with
variations. Dispatch them as parallel agents with the same task and the phase 1
grounding, so they do not converge by watching each other.

Different means different. A struct-of-arrays layout against an array-of-structs
layout. A callback against a polled queue. One module against a seam splitting
two. If the candidates differ only in naming, you have not explored anything.

### What to judge them on

**Depth.** How much behaviour sits behind how much interface? A deep module hides
a lot behind a little. A shallow one has an interface nearly as complicated as
its implementation, and earns nothing.

Apply the deletion test: imagine the module gone. If complexity vanishes, it was
a pass-through and should not exist. If complexity reappears spread across every
caller, it is doing real work.

**Ownership.** Who allocates, who frees, who may hold a reference and for how
long. In C and Odin this decides more bugs than anything else on this list.

**The interface is the test surface.** Callers and tests cross the same seam. If
you want to test past the interface, the module is the wrong shape.

**Seams that are real.** One implementation behind an interface is a
hypothetical seam. Two is a real one. Do not add a seam until something actually
varies across it.

**Reader load.** How many layers does a reader cross to answer "what happens
when I call this"?

Then synthesize. Pick the strongest base and graft the good parts of the others
into it. Say which candidate you started from and what you took from where.

## Phase 3: Choose

Default is to keep going. Present the synthesized sketch and start implementing.

Stop for sign-off only when the user asked for a checkpoint, or when the design
commits to something expensive to undo: a file format, a public API, a data
layout that other code will grow into.

If the sketch is big enough to want sections, a comparison table, or a decision
record, write it with `standard-html` and hand over the path.

The sketch can land as its own commit. Later commits then read as filling in
bodies against a stable contract.

## Phase 4: Implement against the sketch

Replace `not implemented` with code. The sketch is the contract.

**Deviations are signal, not friction.** When a function needs a parameter the
sketch did not anticipate, say so. Ask whether the sketch was wrong, the
requirement was missed, or the implementation is overreaching. Do not silently
bolt it on.

## Phase 5: Scrap when the shape is wrong

If implementation keeps producing friction the sketch cannot absorb, throw the
sketch out. Do not bolt fixes onto a wrong design.

The signal is a **pattern**, not one hard case. Tells:

- The same shape of workaround appearing in unrelated places.
- Several unrelated edge cases that each need a special-case branch.
- Types that need escape hatches to compile. A `void *`, a cast, a field that is
  optional but always set in practice.
- Reaching for a lock when the sketch said the state was not shared.
- Callers having to know the module's internal rules to use it correctly.
- Two or more independent phase 4 deviations of the same shape.

Use judgment. A few edge cases do not condemn a design, and complexity in the
problem is not complexity in the design.

When you scrap:

1. Rerun `how` over what was actually built. The implementation lessons go into
   the next design as inputs.
2. Redesign as if the new constraints had been there on day one, rather than
   patching the old shape to accommodate them.
3. Subtract before adding. The new sketch should start smaller than the old one.
4. Return to phase 2.

## Done when

The caller's usage is written, the types and signatures exist, every public
function has a signature or a stated reason it does not, and you can say which
of the competing shapes you chose and what it gives up.
