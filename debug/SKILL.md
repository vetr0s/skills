---
name: debug
description: Diagnosis loop for a bug or a performance regression, built around a fast reproducible check that goes red on the bug. Use when the user says "debug this", "diagnose", "why is this broken", or reports something crashing, hanging, corrupting, leaking, giving wrong output, or running slow. Covers native crashes, memory errors, and frame-time regressions.
---

# Debug

A discipline for bugs that did not fall out after five minutes of reading. Work
the phases in order. Skip one only by saying out loud why.

## The one rule

**Build the check before you build the theory.** A command that goes red on this
bug and green once it is fixed is the whole skill. Every other technique
(bisection, instrumentation, hypothesis testing) is just something that consumes
that command. Without one you are reading code and guessing, and you will
"fix" something that was never broken.

If you catch yourself explaining a cause before the red command exists, stop and
go back to phase 1.

## Phase 1: Build the check

Spend disproportionate effort here. Be stubborn about it.

Pick the cheapest thing on this list that can actually reach the bug.

1. **Failing test** at whatever seam reaches it.
2. **Direct invocation** with a fixture input, diffing stdout against known-good
   output. `./build/thing < fixture.txt | diff - expected.txt`.
3. **Sanitizer build.** For anything native, this is usually the fastest path
   from "weird" to "exact line". Rebuild with `-fsanitize=address,undefined
   -fno-omit-frame-pointer -g` and run the normal workload. ASan turns a
   corruption that manifests 200ms later into a stack trace at the write.
   Odin: `-sanitize:address`, and `-debug` for line info.
4. **Debugger script.** `lldb -b -o run -o bt -o 'frame variable' -- ./build/thing args`
   is a non-interactive repro you can rerun and diff.
5. **Replay a captured trace.** Dump the real input (event log, input frames,
   network payload, file) to disk once, then replay it through the code path in
   isolation. This is how you make an interactive bug non-interactive.
6. **Throwaway harness.** A `main()` that calls the one suspect function with the
   one suspect input. For a single-header library this is a twenty-line file.
7. **Fuzz or property loop.** For "sometimes wrong output", run a few thousand
   random inputs and look for the failure mode.
8. **Differential run.** Same input through the old binary and the new one, diff
   the outputs. Works when you know it used to be right.
9. **Bisection harness.** If it appeared between two known commits, automate
   "build, run, check, exit 0 or 1" and hand it to `git bisect run`.
10. **Driven session.** For a TUI or an editor, drive it under `tmux send-keys`
    and `tmux capture-pane` so the run is scripted and the output is captured.

### Tighten it

Once you have a check, treat it as the product and sharpen it:

- **Faster.** Cache the setup, skip unrelated init, narrow the scope. A
  two-second check is a different tool from a thirty-second one.
- **Sharper.** Assert on the exact symptom, not "did not crash".
- **Deterministic.** Seed the RNG, pin the clock, fix the frame delta, isolate
  the working directory.

### Intermittent bugs

The goal is not a clean repro. It is a **higher hit rate**. Loop the trigger a
few hundred times, run copies in parallel, add load, narrow the timing window,
inject sleeps at the suspect point. A bug that fires half the time is
debuggable. One that fires one time in a hundred is not, so keep raising the
rate until it is.

### Done when

You can name **one command** you have **already run at least once**, and paste
its output, that is:

- **Red-capable.** It drives the real code path and asserts the user's exact
  symptom. Not "runs clean". It must be able to catch *this* bug.
- **Deterministic**, or pinned to a high enough hit rate.
- **Fast.** Seconds.
- **Runnable unattended.**

### When you genuinely cannot build one

Say so explicitly and list what you tried. Then ask for one of: access to the
environment that reproduces it, a captured artifact (core dump, log, input
recording, screen capture with timestamps), or permission to add temporary
instrumentation to the real run. Do not proceed to hypothesise without a check.

## Phase 2: Reproduce and minimise

Run the check. Watch it go red.

Confirm it is producing the failure the **user** described and not a different
one nearby. Wrong bug means wrong fix.

Then shrink the repro to the smallest scenario that still goes red. Cut inputs,
callers, config, and steps one at a time, rerunning after each cut. Keep only
what is load-bearing.

A minimal repro shrinks the hypothesis space in phase 3 and becomes the
regression test in phase 5. Done when removing any remaining element turns it
green.

## Phase 3: Hypothesise

Write **three to five ranked hypotheses before testing any of them.** Generating
one at a time anchors you on the first plausible idea, which is the most common
way a debugging session goes wrong.

Each must be falsifiable. State the prediction:

> If X is the cause, then changing Y makes the bug disappear, and changing Z
> makes it worse.

A hypothesis with no prediction is a vibe. Sharpen it or drop it.

Show the ranked list before testing. The user often re-ranks it instantly
because they know what changed last week. Do not block on the answer.

## Phase 4: Instrument

Each probe maps to a specific prediction from phase 3. **Change one variable at
a time.**

In order of preference:

1. **Debugger.** One breakpoint and a `frame variable` beats ten prints. For
   memory bugs, a watchpoint on the address that gets clobbered ends the search
   immediately.
2. **Targeted prints** at the boundary that separates two hypotheses.
3. Never "log everything and grep".

**Tag every temporary print** with a unique marker, `[DBG-a4f2]`. Cleanup is
then one grep instead of a careful reread.

### Performance branch

For a regression in frame time or throughput, prints are usually wrong and
measurement is right.

1. **Establish a baseline number** before touching anything. Frames per second
   is too coarse. Measure the actual span in nanoseconds around the suspect
   region and print a distribution, not a mean. The tail is where the stutter
   lives.
2. **Sample the real run.** `sample <pid>` or Instruments on macOS. Look at
   where time actually goes before deciding where it goes.
3. **Bisect the frame.** Stub out subsystems one at a time until the number
   comes back. That tells you the region; the profiler tells you the line.
4. Measure first, fix second, then measure again against the baseline you wrote
   down. A perf fix with no before-and-after number is not a finding.

## Phase 5: Fix and lock it down

Write the regression test **before** the fix, if there is a correct seam for it.

A correct seam exercises the real bug pattern as it occurs at the call site. If
the only reachable seam is too shallow (a unit test that cannot replicate the
chain that triggered it), a test there gives false confidence.

**If no correct seam exists, that is itself the finding.** Say so. The structure
of the code is preventing the bug from being pinned down.

If a seam exists:

1. Turn the minimised repro into a failing test there.
2. Watch it fail.
3. Apply the fix, at the root cause. A guard that silences the symptom is not a
   fix, and neither is a null check added where the null should never have come
   from.
4. Watch it pass.
5. Rerun the phase 1 check against the original, un-minimised scenario.

## Phase 6: Clean up

Before declaring done:

- Original repro no longer reproduces. Rerun the phase 1 command and paste it.
- Regression test passes, or the absence of a seam is written down.
- Every `[DBG-...]` print removed. Grep the marker to prove it.
- Throwaway harnesses and fixtures deleted, or moved somewhere clearly marked.
- Sanitizer flags reverted if they were added to the normal build.

State the hypothesis that turned out to be right in the commit body, per the
`commit` skill. That is exactly the "why" a future reader cannot reconstruct.
