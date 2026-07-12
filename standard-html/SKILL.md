---
name: standard-html
description: Write plans, code/directory state summaries, audit reports, design docs, and decision records as plain HTML documents in a fixed house style instead of Markdown. Use whenever the user asks for a plan, an explanation of how something works, a comparison, a state-of-the-code summary, or any document holding complex structure (tables, decisions, status, phased work). Also use when the user says "make a doc", "write this up", "standard html", or references the house style.
---

# Standard HTML documents

Markdown collapses under real structure. A plan with phases, owners, status, and
tradeoffs becomes an unreadable wall of asterisks. This skill writes those
documents as plain HTML instead, in one house style that is the same in every
project.

## The rule about styling

**The document's look never adapts to the project it lives in.** Not the
project's fonts, not its brand colors, not its design tokens, not its Tailwind
config. A plan for a neon-themed game and a plan for a bank's backend look
identical. This is deliberate: it makes these documents instantly recognizable
as notes-about-the-work rather than part-of-the-work, and it means the reader's
eye never has to re-learn the layout.

The house style is `assets/style.css` in this skill directory. Read it and paste
it verbatim into a `<style>` tag in the document's `<head>`. Never `<link>` to
it — the file must survive being moved, emailed, or opened from disk.

Do not add design flourishes on top of it: no gradients, no shadows, no cards,
no icon fonts, no animations, no web fonts, no color beyond the variables the
stylesheet already defines. It is a plain document on a plain background,
readable in light and dark mode. If a document seems to need a new component,
prefer prose; if it genuinely needs one, add it to `assets/style.css` so every
future document gets it too, rather than inlining a one-off style.

## When to use HTML and when not to

Use it for: implementation plans, audit and review reports, architecture and
state-of-the-codebase summaries, option comparisons and decision records,
migration and phased-work trackers, anything with a table or a status column.

Stay in prose or Markdown for: a two-sentence answer, a chat reply, a commit
message, a PR body, a README, or any file whose consumer is a tool rather than
a person. Do not convert a project's existing Markdown docs to HTML unless
asked.

## Building the document

Start from `assets/template.html`. It shows every component in the stylesheet;
delete what you do not use. The structure is always:

1. `<h1>` with the document's title.
2. `<p class="meta">` — a byline of date, repo/commit, and document kind.
3. **A bottom-line paragraph.** One paragraph, in plain sentences, giving the
   conclusion or proposal. A reader who stops after it still knows the answer.
   Never open with "Overview" boilerplate or a table of contents.
4. The body, in `<h2>` sections.
5. Optionally `<p class="footer">` recording what the document was built from
   (files read, commands run, sources).

Components available: `.note` / `.warn` / `.ok` callouts, `<dl>` for decisions
and key/value facts, `<ul class="tasks">` with `data-state="done|wip|todo"` for
plan steps, `<table>` (wrap in `<div class="scroll">`) for findings,
`<span class="tag tag-good|tag-warn|tag-bad">` for status, `<span class="path">`
for file paths, `<pre><code>` for code.

Write the body the way you would write prose: full sentences, the point first.
Tables are for short enumerable facts — put the reasoning in the paragraph
around the table, not crammed into its cells. Escape `<`, `>`, and `&` inside
code blocks.

## Where the file goes

Default to `docs/` in the current project if it exists, otherwise `notes/`,
creating it if needed. Name the file after the subject in kebab-case, e.g.
`docs/auth-migration-plan.html`. If the work is throwaway, use the session
scratchpad instead. When the user wants it in a browser, `open <file>` on macOS.

If the user asks to *share* the document, publish it with the Artifact tool
instead: same content and same `<style>` block, but drop the `<!doctype>`,
`<html>`, `<head>`, and `<body>` wrapper — the artifact host supplies them.

## After writing

Tell the user the path in one line and give them the bottom line in the chat
too. Do not paste the document's contents back into the conversation.
