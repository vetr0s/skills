#!/usr/bin/env python3
# Flags the patterns catalogued in the `unslop` skill. Line-oriented and
# deliberately noisy at the margins: a hit is a place to look, not a verdict.
import re, sys, pathlib, collections

RULES = [
    # (severity, label, compiled pattern)
    ("HIGH", "em dash",                r"—"),
    ("HIGH", "AI attribution",         r"(?i)\b(generated (by|with) (claude|ai|chatgpt|copilot)|co-authored-by:\s*(claude|codex))"),
    ("HIGH", "curly quote",            r"[‘’“”]"),
    ("HIGH", "not just X but Y",       r"(?i)\bnot (just|only) [^.,;]{2,40}[,;]? (but|it'?s|they'?re)\b"),
    ("HIGH", "chatbot phrase",         r"(?i)\b(i hope this helps|let me know if|feel free to reach out|great question|you'?re absolutely right|certainly!|of course!)"),

    ("MED",  "AI vocabulary",          r"(?i)\b(delve|leverag(e|ing|es)|utiliz(e|ing|es)|seamless(ly)?|robust|pivotal|crucial|tapestry|testament|underscore[sd]?|garner(ed|s)?|intricate|interplay|showcas(e|es|ing)|foster(s|ing)?|myriad|plethora|vibrant|holistic|paradigm)\b"),
    ("MED",  "promotional",            r"(?i)\b(blazingly fast|lightning[- ]fast|cutting[- ]edge|state[- ]of[- ]the[- ]art|groundbreaking|game[- ]chang(er|ing)|powerful(ly)?|elegant(ly)?|effortless(ly)?|beautiful(ly)? (simple|crafted)|battle[- ]tested)\b"),
    ("MED",  "significance inflation", r"(?i)\b(evolving landscape|the landscape of|sets? the stage|indelible|deeply rooted|at its core|in today'?s world|more than just)\b"),
    ("MED",  "copula avoidance",       r"(?i)\b(serves as|stands as|boasts|acts as a bridge)\b"),
    ("MED",  "filler",                 r"(?i)\b(in order to|due to the fact that|it (is|'s) (important|worth) (to note|noting)|it should be noted|needless to say|at the end of the day|when it comes to)\b"),
    ("MED",  "stacked hedge",          r"(?i)\b(could potentially|may possibly|might potentially|somewhat of a|a bit of a bit)\b"),
    ("MED",  "superficial -ing tail",  r",\s+(highlighting|ensuring|showcasing|reflecting|fostering|underscoring|emphasizing|allowing for|enabling)\b"),
    ("MED",  "generic closer",         r"(?i)(the future (looks|is) bright|much to (consider|explore)|the possibilities are endless|happy (coding|hacking)!)"),

    ("LOW",  "abstract metaphor noun", r"(?i)\b(substrate|the wedge|a vector for|locus|nexus|bedrock|scaffolding for|modality|api surface)\b"),
    ("LOW",  "bold-colon header",      r"^\s*[-*]?\s*\*\*[^*]{2,40}:\*\*"),
    ("LOW",  "emoji",                  r"[\U0001F300-\U0001FAFF✀-➿⬀-⯿️]"),
    ("LOW",  "rule of three",          r"(?i)\b\w+, \w+,? and \w+ (are|is|make|makes|provide|provides)\b"),
]
RULES = [(s, l, re.compile(p)) for s, l, p in RULES]

TITLE_CASE = re.compile(r"^#{1,6}\s+(?:[A-Z][a-z]+\s+){2,}[A-Z][a-z]+\s*$")
SKIP_WORDS = {"A", "An", "The", "And", "Or", "But", "For", "To", "In", "On", "Of", "With"}

IGNORE_FILE = re.compile(r"slop-detector:\s*ignore-file")
IGNORE_LINE = re.compile(r"slop-detector:\s*ignore")

def scan(path):
    try:
        text = path.read_text(errors="replace")
    except Exception:
        return []
    # A document that catalogues the patterns opts out, or every run is noise.
    if IGNORE_FILE.search(text[:2000]):
        return []
    hits, fenced = [], False
    for i, line in enumerate(text.splitlines(), 1):
        if line.lstrip().startswith("```"):
            fenced = not fenced
            continue
        if fenced or IGNORE_LINE.search(line):
            continue
        for sev, label, pat in RULES:
            m = pat.search(line)
            if m:
                hits.append((sev, label, i, m.group(0)[:40], line.strip()[:90]))
        if TITLE_CASE.match(line):
            words = line.split()[1:]
            if sum(1 for w in words if w not in SKIP_WORDS and w[:1].isupper()) >= 3:
                hits.append(("LOW", "title case heading", i, line.strip()[:40], line.strip()[:90]))
    return hits

def main(paths):
    per_file, per_label = {}, collections.Counter()
    for p in paths:
        h = scan(pathlib.Path(p))
        if h:
            per_file[p] = h
            for sev, label, *_ in h:
                per_label[(sev, label)] += 1
    order = {"HIGH": 0, "MED": 1, "LOW": 2}
    for p, h in sorted(per_file.items(), key=lambda kv: -sum(3 - order[s] for s, *_ in kv[1])):
        score = sum(3 - order[s] for s, *_ in h)
        print(f"\n=== {p}  (score {score}, {len(h)} hits)")
        for sev, label, ln, frag, ctx in sorted(h, key=lambda x: (order[x[0]], x[2])):
            print(f"  {sev:4} {label:24} :{ln:<4} {frag!r}")
    print("\n" + "=" * 60 + "\nTOTALS BY PATTERN")
    for (sev, label), n in sorted(per_label.items(), key=lambda kv: (order[kv[0][0]], -kv[1])):
        print(f"  {sev:4} {label:24} {n}")
    print(f"\n{len(per_file)} files with hits out of {len(paths)} scanned")

if __name__ == "__main__":
    main(sys.argv[1:])
