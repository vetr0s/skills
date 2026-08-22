---
name: standard-html
description: Write plans, code and directory state summaries, audit reports, design docs, and decision records as plain HTML documents in a fixed house style instead of Markdown. Use whenever the user asks for a plan, an explanation of how something works, a comparison, a state-of-the-code summary, or any document holding complex structure such as tables, decisions, status, or phased work. Also use when the user says "make a doc", "write this up", "standard html", or references the house style.
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
identical. This is deliberate. It makes these documents instantly recognizable
as notes-about-the-work rather than part-of-the-work, and the reader's eye never
has to re-learn the layout.

The house style is `assets/style.css` in this skill directory. Read it and paste
it verbatim into a `<style>` tag in the document's `<head>`. Never `<link>` to
it. The file must survive being moved, emailed, or opened from disk.

Do not add design flourishes on top of it. No gradients, no shadows, no cards,
no icon fonts, no animations, no web fonts, no color beyond the variables the
stylesheet already defines. It is a plain document on a plain background,
readable in light and dark mode.

If a document seems to need a new component, prefer prose. If it genuinely needs
one, add it to `assets/style.css` **and** demonstrate it in `assets/template.html`
**and** list it under Components below. A component that exists in only one of
those three places is drift, and the next document either misses it or reinvents
it.

## The house rules apply to the document too

`CLAUDE.md` governs the prose inside these files exactly as it governs
everything else. The failure mode is copying a violation out of the assets, so
check for these before saving:

- **No em dashes.** Not in the title, not in a `<dd>`, not in a caption.
- **No attribution to Claude or any AI tool**, in the footer or anywhere else.
  The footer records what the document was built from, not who typed it.
- Sentence case headings, no emoji, short declarative sentences.

Run `unslop` over the body before you save.

## When to use HTML and when not to

Use it for: implementation plans, audit and review reports, architecture and
state-of-the-codebase summaries, option comparisons and decision records,
migration and phased-work trackers, anything with a table or a status column.

Stay in prose or Markdown for: a two-sentence answer, a chat reply, a commit
message, a PR body, a README, or any file whose consumer is a tool rather than
a person. Do not convert a project's existing Markdown docs to HTML unless
asked.

## Building the document

Start from `assets/template.html`. It shows every component in the stylesheet.
Delete what you do not use. The structure is always:

1. `<h1>` with the document's title.
2. `<p class="meta">` with a byline of date, repo and commit, and document kind.
3. **A bottom-line paragraph.** One paragraph, in plain sentences, giving the
   conclusion or proposal. A reader who stops after it still knows the answer.
   Never open with "Overview" boilerplate.
4. Optionally a `<nav class="toc">`. It goes **after** the bottom line, never
   before it, and only earns its place past roughly six `<h2>` sections. A short
   document does not get one.
5. The body, in `<h2>` sections.
6. Optionally `<p class="footer">` recording what the document was built from:
   files read, commands run, sources.

### Components

| Component | Markup |
| --- | --- |
| Callouts | `<div class="note">` / `.warn` / `.ok`, each with a `<span class="note-label">` |
| Decisions, key/value facts | `<dl>` with `<dt>` and `<dd>` |
| Plan steps | `<ul class="tasks">` with `data-state="done\|wip\|todo"` |
| Findings, comparisons | `<table>` wrapped in `<div class="scroll">` |
| Status | `<span class="tag tag-good\|tag-warn\|tag-bad">` |
| File paths | `<span class="path">` |
| Code | `<pre><code>`, escaping `<`, `>`, and `&` |
| Contents | `<nav class="toc">` around a nested `<ol>`, with `id` on each heading |
| Back to contents | `<a class="backtotoc">` at the foot of a long section |

Write the body the way you would write prose: full sentences, the point first.
Tables are for short enumerable facts. Put the reasoning in the paragraph around
the table, not crammed into its cells.

## Where the file goes

Default to `docs/` in the current project if it exists, otherwise `notes/`,
creating it if needed. Name the file after the subject in kebab-case, for
example `docs/auth-migration-plan.html`. If the work is throwaway, use the
session scratchpad instead. When the user wants it in a browser, `open <file>`
on macOS.

If the user asks to **share** the document, publish it with the Artifact tool
instead. Same content and same `<style>` block, but drop the `<!doctype>`,
`<html>`, `<head>`, and `<body>` wrapper, because the artifact host supplies
them. Keep the `<title>` tag; it names the artifact.

## After writing

Tell the user the path in one line and give them the bottom line in the chat
too. Do not paste the document's contents back into the conversation.
