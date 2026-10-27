#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Structural AI-trace scanner for academic manuscripts.

Companion to the top-journal-polish skill, Step 8 (AI-Trace Reflection).

Measures the *structural* signals that a manual read tends to judge
impressionistically: punctuation traces, transition-peg density, repeated
syntactic templates, long-sentence load, and sentence-length rhythm.

The point is to obtain an auditable before/after baseline, so that an
"anti-AI pass" can be shown to have changed something rather than merely
asserted to have.

Usage
-----
    python scan_ai_traces.py <file> [--lang en|zh] [--long 45] [--json]

    <file>   path to a .tex, .md, or .txt manuscript; use "-" for stdin

Read-only: opens no sockets, spawns no subprocess, writes no files.
Standard library only.
"""

import argparse
import json
import os
import re
import statistics
import sys
from collections import Counter

# --------------------------------------------------------------------------
# Text extraction
# --------------------------------------------------------------------------

TEX_DROP_ENV = r"(?:equation\*?|align\*?|gather\*?|multline\*?|eqnarray\*?|" \
               r"table\*?|threeparttable|longtable|tabular\*?|tabular|" \
               r"figure\*?|tikzpicture|verbatim|lstlisting)"


def _strip_tex(text):
    """Return prose-only view of a LaTeX source."""
    # keep the body only
    m = re.search(r"\\begin\{document\}(.*?)(\\end\{document\}|\\appendix|\Z)",
                  text, re.S)
    body = m.group(1) if m else text
    # drop display-math and float/table environments (they carry no sentence rhythm)
    body = re.sub(r"\\begin\{" + TEX_DROP_ENV + r"\}.*?\\end\{" + TEX_DROP_ENV + r"\}",
                  " ", body, flags=re.S)
    body = re.sub(r"\\\[.*?\\\]", " ", body, flags=re.S)
    body = re.sub(r"\$\$.*?\$\$", " ", body, flags=re.S)
    # inline math -> placeholder so it does not inflate word counts
    body = re.sub(r"\$[^$]*\$", " MATH ", body)

    # Citations become a CAPITALISED placeholder. Unwrapping them to bare
    # author keys would leave a lower-case token at the start of a sentence
    # ("... (1992). smith1992 show that ..."), which defeats the sentence
    # splitter and manufactures phantom long sentences.
    body = re.sub(r"\\cite[a-zA-Z]*\*?(?:\[[^\]]*\])?\{[^{}]*\}", " CITE ", body)
    # Cross-references become a neutral number-like token.
    body = re.sub(r"\\(?:eqref|autoref|ref|pageref)\{[^{}]*\}", " N ", body)
    body = re.sub(r"\\label\{[^{}]*\}", " ", body)          # drop labels entirely
    # keep only the argument of plain text-formatting commands
    body = re.sub(r"\\(?:emph|textit|textbf|texttt|textsc|textsuperscript|"
                  r"url|footnote|text)\{([^{}]*)\}", r"\1", body)
    # comments and remaining commands
    body = re.sub(r"(?m)^\s*%.*$", " ", body)
    body = re.sub(r"\\[a-zA-Z@]+\*?(\[[^\]]*\])?(\{[^{}]*\})?", " ", body)
    # escaped punctuation, tie, and leftover braces
    body = re.sub(r"\\([%&_#{}])", r"\1", body)
    body = body.replace("~", " ")
    body = body.replace("{", " ").replace("}", " ")
    return body


def _strip_md(text):
    """Return prose-only view of a Markdown document."""
    text = re.sub(r"```.*?```", " ", text, flags=re.S)      # fenced code
    text = re.sub(r"`[^`]*`", " ", text)                    # inline code
    lines = []
    for ln in text.splitlines():
        s = ln.strip()
        if not s or s.startswith("#") or s.startswith("|") or s.startswith("```"):
            continue
        if re.match(r"^[-*+]\s+\S", s) and len(s) < 60:      # terse bullets
            continue
        lines.append(s)
    text = " ".join(lines)
    text = re.sub(r"!?\[([^\]]*)\]\([^)]*\)", r"\1", text)  # links/images
    text = re.sub(r"[*_>]+", " ", text)
    return text


def extract(path, lang="en"):
    if path == "-":
        raw = sys.stdin.read()
        kind = "txt"
    else:
        with open(path, encoding="utf-8", errors="replace") as fh:
            raw = fh.read()
        kind = os.path.splitext(path)[1].lower().lstrip(".") or "txt"
    if kind == "tex":
        return _strip_tex(raw)
    if kind in ("md", "markdown"):
        return _strip_md(raw)
    return raw


# --------------------------------------------------------------------------
# Sentence segmentation
# --------------------------------------------------------------------------

ABBREV = {
    "al", "e.g", "i.e", "cf", "vs", "etc", "fig", "figs", "eq", "eqs", "no",
    "nos", "vol", "pp", "ed", "eds", "ca", "approx", "resp", "sect", "ch",
    "dr", "prof", "mr", "ms", "mrs", "st", "inc", "ltd", "jr", "sr", "u.s",
    "u.k", "i.v", "min", "max",
}


SENT_SPLIT = (r"(?:(?<=[.!?])\s+(?=[\"\'(\[]?[A-Z0-9])"
              r"|(?<=[\u3002\uff01\uff1f])\s*(?=[\"\'(\[\u201c\u300c]?"
              r"[A-Za-z0-9\u4e00-\u9fff]))")


def segment(text):
    """Split into sentences. Latin terminators require following whitespace, so
    decimals ("0.5") are never split; CJK terminators do not, since Chinese
    punctuation is not followed by a space."""
    text = re.sub(r"\s+", " ", text).strip()
    if not text:
        return []
    parts = re.split(SENT_SPLIT, text)
    out = []
    for p in parts:
        p = p.strip()
        if not p:
            continue
        # re-join a split caused by an abbreviation
        if out:
            tail = re.findall(r"([A-Za-z.]+)\.$", out[-1])
            if tail and tail[0].lower().rstrip(".") in ABBREV:
                out[-1] = out[-1] + " " + p
                continue
        out.append(p)
    return out


def words(s):
    """Latin word tokens; placeholders for maths and citations are excluded
    so that sentence-length statistics reflect the prose, not the notation."""
    return [w for w in re.findall(r"\b[\w'’\-]+\b", s)
            if w not in ("MATH", "CITE", "N")]


def sent_len(s, lang="en"):
    """Sentence length. Latin prose is measured in words. Chinese prose is
    measured in characters (CJK ideographs plus Latin word tokens), because
    word-counting a CJK sentence counts clauses rather than length."""
    if lang == "zh":
        cjk = len(re.findall(r"[\u3400-\u4dbf\u4e00-\u9fff]", s))
        latin = len([w for w in re.findall(r"[A-Za-z][A-Za-z'\-]*", s)
                     if w not in ("MATH", "CITE", "N")])
        return cjk + latin
    return len(words(s))


# --------------------------------------------------------------------------
# Probes
# --------------------------------------------------------------------------

EN_PEGS = (r"However|Moreover|Furthermore|Additionally|In addition|In particular|"
           r"Specifically|More broadly|Notably|Importantly|Critically|Indeed|"
           r"Overall|Thus|Hence|Therefore|Consequently|Meanwhile|Conversely|"
           r"By contrast|Similarly|Nonetheless|Taken together|Collectively|"
           r"In short|In sum|Ultimately|Essentially|Arguably")
ZH_PEGS = (r"需要注意的是|值得注意的是|与此同时|此外|综上所述|换言之|换句话说|"
           r"首先|其次|最后|总而言之|由此可见")

EN_TEMPLATES = {
    "X, so Y":                        r", so [a-z]",
    "X, which <verb>s":               r", which \w+s\b",
    "X, and therefore Y":             r", and therefore\b",
    "rather than":                    r"\brather than\b",
    "not only ... but also":          r"\bnot only\b[^.]{0,80}\bbut also\b",
    "thereby + gerund":               r"\bthereby \w+ing\b",
    "that is,":                       r"\bthat is,",
    "In other words":                 r"\bin other words\b",
    "Note that":                      r"\bNote that\b",
    "respectively":                   r"\brexpectively\b",
    "N purposes/assumptions/features": r"\b(?:three|four|five) (?:purposes|assumptions|"
                                       r"features|reasons|channels|mechanisms|takeaways)\b",
    "First/Second/Third/... opener":  r"(?:^|\. )(?:First|Second|Third|Fourth),",
    "It is <adj> that":               r"\bIt is \w+ (?:to|that)\b",
    "This <verb>s that":              r"\bThis \w+s that\b",
    "as can be seen":                 r"\bAs can be seen\b",
    "the extent to which":            r"\bthe extent to which\b",
    "plays a ... role":               r"\bplays? (?:a|an) \w+ role\b",
}

ZH_TEMPLATES = {
    "破折号 ——":        r"——",
    "解释性冒号":        r"[^\d]\s*：\s*[^\d]",
    "即（重述）":        r"[，。；]即[^\w]",
    "需要注意的是":      r"需要注意的是",
    "值得注意的是":      r"值得注意的是",
    "第一/第二/第三":    r"第[一二三四]，",
    "综上所述":          r"综上所述",
    "与此同时":          r"与此同时",
}


def scan(text, lang="en", long_threshold=None):
    # Chinese prose packs more content per token, so 45 characters is a far
    # lower bar than 45 English words; the default is raised accordingly.
    if long_threshold is None:
        long_threshold = 45 if lang == "en" else 60
    unit = "words" if lang == "en" else "characters"
    sents = segment(text)
    lens = [sent_len(s, lang) for s in sents] or [0]
    pegs = EN_PEGS if lang == "en" else ZH_PEGS
    templates = EN_TEMPLATES if lang == "en" else ZH_TEMPLATES

    rep = {}
    rep["corpus"] = {
        "unit": unit,
        "sentences": len(sents),
        "words": sum(lens),
        "mean_words": round(statistics.mean(lens), 1),
        "median_words": round(statistics.median(lens), 1),
        "stdev_words": round(statistics.pstdev(lens), 1),
    }

    # A. punctuation traces
    rep["punctuation"] = {
        "em_dash_triple (---)": len(re.findall(r"---", text)),
        "em_dash_unicode": len(re.findall(r"\u2014", text)),
        "explanatory_colon": len(re.findall(r"[a-z)]\s*[:：]\s+[a-zA-Z]", text)),
        "semicolon": len(re.findall(r";", text)),
    }

    # B. transition-peg density
    peg_sents = sum(1 for s in sents if re.search(r"(?<![\w])(" + pegs + r")(?![\w])", s))
    rep["transition_pegs"] = {
        "sentences_with_peg": peg_sents,
        "pct_of_sentences": round(100.0 * peg_sents / max(1, len(sents)), 1),
        "target_band": "<= 10% (lower is better; 0-5% is typical of human journal prose)",
        "tokens": dict(Counter(
            m.group(0) for s in sents
            for m in re.finditer(r"(?<![\w])(" + pegs + r")(?![\w])", s))),
    }

    # C. repeated templates
    rep["templates"] = {}
    for name, pat in templates.items():
        n = len(re.findall(pat, text, re.I))
        if n:
            rep["templates"][name] = n

    # D. long-sentence load
    over = [(i, sent_len(s, lang), s) for i, s in enumerate(sents, 1)
            if sent_len(s, lang) > long_threshold]
    rep["long_sentences"] = {
        "unit": unit,
        "threshold": long_threshold,
        "count": len(over),
        "pct": round(100.0 * len(over) / max(1, len(sents)), 1),
        "target_band": ("<= 5% above the threshold; treat 60+ English words "
                        "(or roughly 90+ Chinese characters) as a defect"),
        "over_60": sum(1 for _, n, _ in over if n > (60 if lang == "en" else 90)),
        "items": [{"index": i, "words": n, "text": s[:200]} for i, n, s in over],
    }

    # E. rhythm (the counter-check: do NOT let a rewrite flatten sentence length)
    pairs = list(zip(lens, lens[1:]))
    if pairs:
        near = sum(1 for a, b in pairs if abs(a - b) <= 2)
        ratio = sum(1 for a, b in pairs if max(a, b) >= 2 * max(1, min(a, b)))
        run = mx = 1
        for a, b in pairs:
            if abs(a - b) <= 2:
                run += 1
                mx = max(mx, run)
            else:
                run = 1
    else:
        near = ratio = 0
        mx = 0
    rep["rhythm"] = {
        "adjacent_pairs": len(pairs),
        "pct_within_2_words": round(100.0 * near / max(1, len(pairs)), 1),
        "pct_with_2x_ratio": round(100.0 * ratio / max(1, len(pairs)), 1),
        "longest_same_length_run": mx,
        "short_sentences_le9": sum(1 for x in lens if x <= 9),
        "pct_short": round(100.0 * sum(1 for x in lens if x <= 9) / max(1, len(lens)), 1),
        "target_band": ("pct_within_2_words <= 25% and pct_with_2x_ratio >= 25%: "
                        "only a low 'within +/-2 words' share shows real length variation. "
                        "A low stdev alone does not imply monotony, but a high "
                        "'within +/-2 words' share does."),
        "histogram_by_10_words": dict(sorted(Counter(
            min(x, 50) // 10 * 10 for x in lens).items())),
    }
    return rep


# --------------------------------------------------------------------------
# Report
# --------------------------------------------------------------------------

def render(rep):
    out = []
    w = out.append
    w("=" * 74)
    w("STRUCTURAL AI-TRACE SCAN")
    w("=" * 74)
    c = rep["corpus"]
    w("sentences %d | %s %d | mean %.1f | median %.1f | stdev %.1f"
      % (c["sentences"], c["unit"], c["words"], c["mean_words"],
         c["median_words"], c["stdev_words"]))

    w("\n[A] PUNCTUATION TRACES")
    for k, v in rep["punctuation"].items():
        w("    %-26s %d" % (k, v))
    w("    note: in LaTeX, '--' is an en dash and is legitimate in compound terms")
    w("          (e.g. treated--control) and numeric ranges; only '---' and")
    w("          mid-sentence explanatory dashes are traces.")
    w("          A colon is a trace only when it replaces a sentence to explain")
    w("          the preceding clause. Colons that introduce a genuine list, a")
    w("          displayed equation, or a stated assumption are legitimate, so")
    w("          treat this count as a probe, not a defect count.")

    w("\n[B] TRANSITION-PEG DENSITY")
    p = rep["transition_pegs"]
    w("    %d of %d sentences (%.1f%%)   target: %s"
      % (p["sentences_with_peg"], c["sentences"], p["pct_of_sentences"], p["target_band"]))
    if p["tokens"]:
        for k, v in sorted(p["tokens"].items(), key=lambda x: -x[1]):
            w("      %-18s %d" % (k, v))

    w("\n[C] REPEATED SYNTACTIC TEMPLATES")
    if rep["templates"]:
        for k, v in sorted(rep["templates"].items(), key=lambda x: -x[1]):
            w("    %-34s %d" % (k, v))
    else:
        w("    none")

    w("\n[D] LONG-SENTENCE LOAD")
    L = rep["long_sentences"]
    w("    >%d %s: %d (%.1f%%)   far over: %d"
      % (L["threshold"], L["unit"], L["count"], L["pct"], L["over_60"]))
    w("    target: %s" % L["target_band"])
    for it in L["items"]:
        w("      [%2dw] %s%s" % (it["words"], it["text"], "..." if len(it["text"]) >= 200 else ""))

    w("\n[E] RHYTHM (counter-check against over-flattening)")
    r = rep["rhythm"]
    u = c["unit"]
    w("    adjacent pairs                 %d" % r["adjacent_pairs"])
    w("    within +/-2 %-18s %.1f%%   <- lower is better" % (u, r["pct_within_2_words"]))
    w("    with >=2x length ratio         %.1f%%   <- higher is better" % r["pct_with_2x_ratio"])
    w("    longest same-length run        %d" % r["longest_same_length_run"])
    w("    sentences <=9 %-18s %d (%.1f%%)" % (u, r["short_sentences_le9"], r["pct_short"]))
    w("    %s" % r["target_band"])
    w("    histogram (%s // 10): %s" % (u, r["histogram_by_10_words"]))
    w("")
    return "\n".join(out)


def main():
    ap = argparse.ArgumentParser(description="Structural AI-trace scanner.")
    ap.add_argument("file", help="manuscript path (.tex/.md/.txt) or '-' for stdin")
    ap.add_argument("--lang", choices=["en", "zh"], default="en")
    ap.add_argument("--long", type=int, default=None,
                    help="long-sentence threshold (default: 45 English words / "
                         "60 Chinese characters)")
    ap.add_argument("--json", action="store_true", help="emit JSON instead of a report")
    a = ap.parse_args()
    try:
        text = extract(a.file, a.lang)
    except OSError as exc:
        sys.stderr.write("error: cannot read '%s' (%s)\n"
                         % (a.file, getattr(exc, "strerror", None) or exc))
        return 2
    rep = scan(text, a.lang, a.long)
    print(json.dumps(rep, ensure_ascii=False, indent=2) if a.json else render(rep))
    return 0


if __name__ == "__main__":
    sys.exit(main())
