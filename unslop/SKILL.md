---
name: unslop
description: Strip AI tells out of prose. A catalogue of the patterns that make writing read as machine-generated, each with its fix. Use before shipping any README, doc, comment, commit body, blog post, or report, and when the user says "unslop this", "this reads like AI", "de-slop", or complains about em dashes, filler, or LLM voice.
---

<!-- slop-detector: ignore-file -->

# Unslop

Edit text so it does not read as generated. Preserve the meaning. Keep the
intended tone.

## Process

1. Read the whole thing once for meaning.
2. Run `scripts/slop.py <files>` for the mechanical tells.
3. Scan against the catalogue below for the ones a regex cannot see.
4. Rewrite. Do not annotate, do not leave a change log in the text.
5. Rerun the script and ask what still marks this as machine-written.

The script finds surface patterns: em dashes, curly quotes, the vocabulary
list, filler, chatbot phrases. It cannot see a vague claim, a passive
construction, or a paragraph that says nothing, which is most of what matters.
Treat a clean run as the start of the read, not the end of it. Hits are places
to look, not verdicts, and it over-flags bold lead-ins that are doing real work.

A document that quotes the patterns on purpose opts out with a
`slop-detector: ignore-file` comment near the top, or one line at a time with
`slop-detector: ignore`.

## House rules come first

`CLAUDE.md` governs. These three are the ones that get violated most and they
outrank everything else in the catalogue.

1. **No em dashes.** Not one. Do not substitute an en dash, a double hyphen, a
   spaced hyphen, or a parenthesis. Trading an em dash for a parenthesis swaps
   one tell for another. End the sentence, or use a comma.
2. **No mid-sentence commentary.** One idea per sentence, then stop. An
   appositive or a parenthetical that props up a claim already made is the
   single loudest tell in technical writing. If the point needs support, give it
   its own sentence.
3. **Short declarative sentences.** Cut hedges, filler, and throat-clearing.

## What replaces the slop

Removing patterns is half the job. Sterile, voiceless text is just as obviously
generated as flowery text.

- **Have a view.** React to the facts instead of listing pros and cons neutrally.
- **Be specific.** Not "performance improved" but "frame time dropped from 18ms
  to 4ms".
- **Name the mechanism.** Not "the API stays out of your way" but "every call
  returns a value; nothing mutates the argument".

Do not reach for the usual advice about varying rhythm or letting some mess in.
The house style is short and declarative, and it does not read as generated when
the sentences carry real content.

## Catalogue

### Content

1. **Significance inflation.** "pivotal moment", "testament to", "evolving
   landscape", "sets the stage for", "deeply rooted". Cut the puffery. State
   what happened.
2. **Superficial -ing tails.** "...highlighting the need for", "...ensuring
   consistency", "...showcasing the power of". Delete, or replace with the
   actual consequence.
3. **Promotional language.** "seamless", "robust", "powerful", "elegant",
   "groundbreaking", "blazingly fast". Describe the behaviour or give the number.
4. **Vague attribution.** "Experts believe", "It is widely considered". Name the
   source or delete the claim.
5. **Formulaic tension.** "Despite these challenges, X continues to thrive."
   Replace with the specific facts.

### Vocabulary

6. **The list.** additionally, crucial, delve, leverage, enhance, facilitate,
   foster, garner, interplay, intricate, landscape (abstract), pivotal,
   showcase, tapestry, testament, underscore, utilize, vibrant, robust, seamless.
   Use the plain word.
7. **Copula avoidance.** "serves as", "stands as", "boasts", "features". Say
   "is" or "has".
8. **Negative parallelism.** "It's not just X, it's Y." State the point.
9. **Rule of three.** Forcing ideas into groups of three. Use the real number.
10. **Synonym cycling.** The function, the routine, the procedure, the call, all
    in one paragraph. Pick one word and repeat it.
11. **False ranges.** "from parsing to rendering" where the two ends are not on
    a scale. List the things.

### Punctuation and shape

12. **Colon as connector.** Fine before a list or an example. Not as a
    mid-sentence hinge. Rewrite so the point stands without it.
13. **Boldface spray.** Do not bold every proper noun, acronym, or term of art.
14. **Inline-header lists.** The tell is a bold label whose colon restates the
    line: "**Performance:** Performance improved". Convert to prose. A bold
    lead-in that names a thing and is followed by genuinely new detail is fine.
15. **Title Case Headings.** Sentence case.
16. **Decorative emoji.** Remove.
17. **Curly quotes and ellipsis characters.** Straight quotes, three periods.

### Chat artifacts

18. **Assistant phrases.** "I hope this helps", "Let me know if", "Of course",
    "Certainly", "Great question", "You're absolutely right". Remove.
19. **Cutoff disclaimers.** "While specific details are limited". Find the
    detail or drop the sentence.
20. **Announcing the finding.** "Found it!", "The smoking gun!", "Interesting!".
    State what you found.

### Filler

21. **Filler phrases.** "in order to" becomes "to". "due to the fact that"
    becomes "because". "it is important to note that" gets deleted whole.
22. **Stacked hedges.** "could potentially possibly" becomes "may", or becomes
    nothing.
23. **Generic closers.** "The future looks bright." "There is much to consider."
    End on the last real sentence.

### Jargon

24. **Abstract metaphor nouns.** substrate, wedge, vector, locus, nexus,
    primitive (as a noun), surface (as in "API surface"), bedrock, scaffolding
    (as metaphor), paradigm, modality. Each has a plainer concrete word.
    "Substrate" is "base". "Wedge in" is "add". "Vector" is "way".
25. **Feeling instead of function.** "the database stays close at hand", "types
    that follow your schema". These name a sensation. The fix names the
    mechanism or a number. "`.to_sql()` returns the exact string sent to the
    database." "Renaming a column fails the build."

### Sentence mechanics

26. **Dense sentences.** If the reader has to back up to parse it, split it.
27. **Passive voice.** Catch "is/are/was/were" plus a past participle and name
    the actor. "Queries are validated" becomes "the compiler validates queries".
    Passive is fine only when the actor is unknown or genuinely irrelevant.
28. **Adverbs propping up weak verbs.** "runs quickly" becomes "is fast" or the
    measured number. "significantly improves" becomes the delta. An adverb
    holding up a verb means the verb is wrong.

## In code and commits

The same rules apply, plus:

- A comment that restates the next line is slop. Delete it.
- A commit body that narrates the diff is slop. The body carries the why.
- A docstring listing every parameter with its own type restated from the
  signature is slop. Say what the function is for.
- Defensive checks added "just in case" are the code form of hedging. See
  `CLAUDE.md`.

## Done when

You can read the piece aloud and no sentence makes you wince. Then check the top
three house rules one final time by searching for them literally: em dash, open
parenthesis mid-sentence, and any sentence over about thirty words.
