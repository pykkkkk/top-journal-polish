#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Detector-facing risk scanner for academic prose (English).

Companion to the top-journal-polish skill, Step 8 (AI-Trace Reflection).

WHY THIS EXISTS
---------------
`scan_ai_traces.py` measures the structural traces that coincide with real
writing defects (dashes, pegs, templates, long sentences, rhythm). This script
measures a different thing: the handful of *statistical proxies that commercial
AI detectors actually score*, so that a false-positive risk can be seen and
reduced in a document that a human wrote or polished.

The proxies are the published ones, not invented ones:

  P1  low perplexity        -> proxied here by FORMULAIC density and
                               SELF-REPETITION (see the honesty note below)
  P2  low burstiness        -> sentence-length coefficient of variation
  P3  high formulaic lang.  -> multiword formula + AI-typical lexicon density
  P4  consistent formality  -> NOT scored; see the honesty note
  P5  low lexical diversity -> MTLD (length-robust) + MSTTR-50
  extra, from vendor docs   -> hedge density and paragraph-shape uniformity

HONESTY NOTES (read before acting on any number)
------------------------------------------------
1. This is NOT a detector and does not predict a detector's score. Commercial
   detectors are neural classifiers; the same text commonly scores differently
   across them (published false-positive rates for human text span 0-100%
   across 13 detectors). Treat every number here as a *direction*, not a grade.
2. Real perplexity needs a language model; this script has no model and no
   network. Word-frequency rarity is NOT used as a proxy, because in this
   register it inverts: technical terms are globally rare but locally
   predictable, so a frequency proxy would call dense academic prose
   "high perplexity" while a real model calls it low. Formulaicity and
   self-repetition are used instead, because those *are* predictability.
3. Proxy P4 (consistent formality) is deliberately NOT scored. Formal academic
   English is uniformly formal by construction, so the proxy carries no
   variance in this register and can only mislead.
4. Short text is unstable. Detector accuracy is itself unreliable below roughly
   250 words; below 100 words MTLD is suppressed. The script says so.
5. Reducing these proxies is only legitimate for text you wrote or text whose
   language you are legitimately polishing. This is a false-positive-risk
   diagnostic, not a bypass tool. Authoring rules and disclosure rules are
   unaffected by anything printed here.

Usage
-----
    python scan_detectability.py DRAFT.md                  # one report
    python scan_detectability.py BEFORE.md AFTER.md        # report + delta
    python scan_detectability.py DRAFT.md --json > p.json
    python scan_detectability.py --text "..."              # analyse a string
    python scan_detectability.py selftest                  # assertions

Scope: English only (the proxy lexicons are English). For structural traces in
Chinese, use `scan_ai_traces.py --lang zh`.
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

# ---------------------------------------------------------------------------
# 1. Text loading (prose only, paragraph boundaries preserved)
# ---------------------------------------------------------------------------

TEX_DROP_ENV = (r"(?:equation\*?|align\*?|gather\*?|multline\*?|eqnarray\*?|"
                r"table\*?|threeparttable|longtable|tabular\*?|tabular|"
                r"figure\*?|tikzpicture|verbatim|lstlisting)")


def _strip_tex_inline(body):
    """Remove maths, citations, cross-references, commands and comments.

    Newlines are preserved so that paragraph boundaries survive.
    """
    body = re.sub(r"\\begin\{" + TEX_DROP_ENV + r"\}.*?\\end\{" + TEX_DROP_ENV + r"\}",
                  "\n\n", body, flags=re.S)
    body = re.sub(r"\\\[.*?\\\]", " MATH ", body, flags=re.S)
    body = re.sub(r"\$\$.*?\$\$", " MATH ", body, flags=re.S)
    body = re.sub(r"\$[^$]*\$", " MATH ", body)
    body = re.sub(r"\\cite[a-zA-Z]*\*?(?:\[[^\]]*\])?\{[^{}]*\}", " CITE ", body)
    body = re.sub(r"\\(?:eqref|autoref|ref|pageref)\{[^{}]*\}", " N ", body)
    body = re.sub(r"\\label\{[^{}]*\}", " ", body)
    body = re.sub(r"\\(?:emph|textit|textbf|texttt|textsc|url|footnote|text)"
                  r"\{([^{}]*)\}", r"\1", body)
    body = re.sub(r"(?m)^\s*%.*$", " ", body)
    body = re.sub(r"\\[a-zA-Z@]+\*?(\[[^\]]*\])?(\{[^{}]*\})?", " ", body)
    body = re.sub(r"\\([%&_#{}])", r"\1", body)
    body = body.replace("~", " ").replace("{", " ").replace("}", " ")
    return body


def load_paragraphs(path):
    """Return (paragraphs, kind). Each paragraph is a prose-only string."""
    if path == "-":
        raw = sys.stdin.read()
        kind = "txt"
    else:
        with open(path, encoding="utf-8", errors="replace") as fh:
            raw = fh.read()
        kind = os.path.splitext(path)[1].lower().lstrip(".") or "txt"

    if kind == "tex":
        m = re.search(r"\\begin\{document\}(.*?)(\\end\{document\}|\\appendix|\Z)",
                      raw, re.S)
        body = m.group(1) if m else raw
        body = _strip_tex_inline(body)
        blocks = re.split(r"\n\s*\n+", body)
        return [re.sub(r"\s+", " ", b).strip() for b in blocks if b.strip()], kind

    # markdown / plain text: walk lines so that blank lines delimit paragraphs
    if kind == "md":
        raw = re.sub(r"```.*?```", "\n\n", raw, flags=re.S)
    paras, buf = [], []
    for ln in raw.splitlines():
        s = ln.strip()
        if not s:
            if buf:
                paras.append(" ".join(buf))
                buf = []
            continue
        if kind == "md":
            if s.startswith("#") or s.startswith("|") or s.startswith("```"):
                continue
            if re.match(r"^[-*+]\s+\S", s) and len(s) < 60:
                continue
            s = re.sub(r"`[^`]*`", " ", s)
            s = re.sub(r"!?\[([^\]]*)\]\([^)]*\)", r"\1", s)
            s = re.sub(r"[*_>]+", " ", s)
        buf.append(s)
    if buf:
        paras.append(" ".join(buf))
    return [re.sub(r"\s+", " ", p).strip() for p in paras if p.strip()], kind


# ---------------------------------------------------------------------------
# 2. Segmentation and tokenisation
# ---------------------------------------------------------------------------

ABBREV = {
    "al", "e.g", "i.e", "cf", "vs", "etc", "fig", "figs", "eq", "eqs", "no",
    "nos", "vol", "pp", "ed", "eds", "ca", "approx", "resp", "sect", "ch",
    "dr", "prof", "mr", "ms", "mrs", "st", "inc", "ltd", "jr", "sr", "u.s",
    "u.k", "i.v", "min", "max",
}

SENT_SPLIT = r"(?<=[.!?])\s+(?=[\"\'(\[]?[A-Z0-9])"

PLACEHOLDER = {"MATH", "CITE", "N"}


def segment(text):
    text = re.sub(r"\s+", " ", text).strip()
    if not text:
        return []
    out = []
    for p in re.split(SENT_SPLIT, text):
        p = p.strip()
        if not p:
            continue
        if out:
            tail = re.findall(r"([A-Za-z.]+)\.$", out[-1])
            if tail and tail[0].lower().rstrip(".") in ABBREV:
                out[-1] = out[-1] + " " + p
                continue
        out.append(p)
    return out


def words(s):
    return [w for w in re.findall(r"\b[A-Za-z][A-Za-z'’\-]*\b", s)
            if w not in PLACEHOLDER]


def tokens_lower(paragraphs):
    toks = []
    for p in paragraphs:
        toks.extend(w.lower() for w in words(p))
    return toks


# ---------------------------------------------------------------------------
# 3. Lexicons
# ---------------------------------------------------------------------------

# P3a -- multiword formulae that are highly predictable in context.
EN_FORMULAIC = [
    r"in today'?s (?:digital|modern|rapidly changing|ever-?changing) (?:age|era|world|landscape)",
    r"plays? (?:a|an) (?:crucial|vital|pivotal|key|significant|important) role",
    r"it is (?:important|worth|essential|crucial) (?:to note|noting|to mention)",
    r"it should be noted",
    r"a (?:wide|broad|diverse|growing|increasing) (?:range|body|array|number) of",
    r"shed(?:s|ding)? light on",
    r"pave(?:s|d)? the way",
    r"delve(?:s|d)? into",
    r"in the realm of",
    r"a testament to",
    r"underscore(?:s|d)? the (?:importance|need|significance|role)",
    r"highlight(?:s|ed)? the (?:importance|need|significance|role)",
    r"at the forefront of",
    r"navigate the complexit",
    r"holistic approach",
    r"seamless(?:ly)? integrat",
    r"robust framework",
    r"(?:comprehensive|nuanced|deeper) understanding",
    r"in conclusion",
    r"as (?:we|one) (?:can see|discussed|noted)",
]

# P3b -- single tokens that detectors weight (vendor "first-layer" vocabulary).
EN_AI_LEXICON = [
    "crucial", "pivotal", "holistic", "seamless", "multifaceted", "myriad",
    "paramount", "intricate", "meticulous", "meticulously", "realm",
    "landscape", "underscores", "fosters", "delve", "leverage", "nuanced",
    "comprehensive", "robust",
]

# Softeners that are reducible rather than domain-necessary.
EN_HEDGES = [
    r"arguably", r"seemingly", r"apparently", r"presumably", r"plausibly",
    r"it seems", r"to some extent", r"in some cases", r"somewhat",
    r"relatively", r"broadly speaking", r"generally speaking",
    r"it could be argued", r"one might argue", r"\btends? to\b", r"\btend to\b",
]

# Reported for information only -- modal verbs are domain-essential in
# economics and are NOT scored.
EN_MODALS = r"\b(?:may|might|could|would|can|shall|should)\b"

# Function words excluded before counting repeated 4-grams, so that the probe
# captures self-repetition of *content frames* rather than of "of the".
STOPWORDS = {
    "the", "a", "an", "of", "to", "in", "on", "at", "by", "for", "and", "or",
    "but", "is", "are", "was", "were", "be", "been", "being", "as", "that",
    "this", "these", "those", "it", "its", "with", "from", "than", "then",
    "so", "into", "we", "our", "they", "their", "he", "she", "his", "her",
    "i", "you", "your", "not", "no", "do", "does", "did", "has", "have",
    "had", "will", "would", "can", "could", "may", "might", "must", "shall",
    "should", "there", "here", "which", "who", "whom", "whose", "when",
    "where", "why", "how", "if", "while", "because", "about", "above",
    "below", "between", "during", "after", "before", "over", "under",
    "again", "more", "most", "some", "such", "only", "own", "same", "too",
    "very", "both", "each", "few", "other", "also", "one", "two", "three",
}


# ---------------------------------------------------------------------------
# 4. Metrics
# ---------------------------------------------------------------------------

def _cv(vals):
    if len(vals) < 2:
        return 0.0
    m = statistics.fmean(vals)
    if not m:
        return 0.0
    return 100.0 * statistics.pstdev(vals) / m


def mtld(tokens, threshold=0.72):
    """Measure of Textual Lexical Diversity (McCarthy & Jarvis 2010).

    Length-robust, unlike type-token ratio. Returned value has no universal
    cut-off; read it relatively (across your own drafts)."""

    def one_pass(seq):
        factors = 0.0
        types = set()
        count = 0
        for w in seq:
            types.add(w)
            count += 1
            if len(types) / count < threshold:
                factors += 1
                types = set()
                count = 0
        if count:
            ttr = len(types) / count
            factors += (1.0 - ttr) / (1.0 - threshold)
        if factors <= 1e-12:
            # No factor ever closed, i.e. the type-token ratio never fell
            # through the threshold. Diversity saturated, so MTLD is at least
            # the text length; returning 0 here would invert the scale.
            return float(len(seq))
        return len(seq) / factors

    if len(tokens) < 50:
        return 0.0
    return (one_pass(tokens) + one_pass(list(reversed(tokens)))) / 2.0


def msttr(tokens, window=50):
    if len(tokens) < window:
        return 0.0
    vals = []
    for i in range(0, len(tokens) - window + 1, window):
        chunk = tokens[i:i + window]
        vals.append(len(set(chunk)) / window)
    return 100.0 * statistics.fmean(vals) if vals else 0.0


def repeated_ngram_share(tokens, n=4):
    """Share of content tokens that sit inside a repeated n-gram."""
    seq = [w for w in tokens if w not in STOPWORDS]
    if len(seq) < n * 2:
        return 0.0, {}
    grams = Counter(tuple(seq[i:i + n]) for i in range(len(seq) - n + 1))
    repeated = {g: c for g, c in grams.items() if c > 1}
    covered = 0
    for g, c in repeated.items():
        covered += (c - 1) * n           # count repeats, not the first sighting
    share = 100.0 * covered / max(1, len(seq))
    top = {" ".join(g): c for g, c in
           sorted(repeated.items(), key=lambda x: -x[1])[:5]}
    return share, top


def density(count, n_words):
    return 100.0 * count / max(1, n_words)


def _count_patterns(pats, text):
    n = 0
    hits = Counter()
    for p_ in pats:
        rx = re.compile(p_, re.I)
        for m in rx.finditer(text):
            n += 1
            hits[m.group(0).lower()] += 1
    return n, dict(hits)


# ---------------------------------------------------------------------------
# 5. Risk model
# ---------------------------------------------------------------------------
# CALIBRATION. The ramps and bands below were set from a 9-paper top-5
# econ/management corpus, NOT from informal-text conventions. The corpus is
# ERA-STRATIFIED at the user's instruction (papers published after generative AI
# may themselves be AI-influenced, so a pre-2020 clean-human baseline anchors
# the bands): OLD = 4 pre-2020 papers (Autor-Dorn 2013 AER, Chetty 2014 QJE,
# MTO ~2007/2012, QJE qjz042 ~2015/2019); NEW = 5 papers 2021+ (Tertiarization
# 2022, China Financial System 2022, Intrachoice 2023, Putting Teams 2023,
# Marx-Hsu 2021). Observed medians (min-max) are statistically indistinguishable
# across eras -- the 2021+ papers show NO contamination signature:
#                       OLD (pre-2020)        NEW (2021+)
#     burstiness CV %      55.6 (50.6-73.5)    63.4 (55.6-89.6)
#     formulaic /100w       0.06 (0.00-0.09)    0.07 (0.03-0.12)
#     self-repeat %        15.2  (8.0-39.8)    29.8  (6.1-40.9)
#     MTLD                 71.9 (66.4-72.9)    88.3 (64.4-105.9)
#     hedge /100w           0.07 (0.05-0.14)    0.07 (0.04-0.11)
#     risk_index            1.6  (0.0-5.2)      0.0  (0.0-0.7)
# Every real paper scores LOW (0-5.2) on risk_index; no paper is RED on any
# proxy. That is the design target: legitimate prose must not be flagged.
# Anything stricter than these floors would flag every legitimate paper, which
# is exactly the failure mode this tool exists to avoid. Two consequences:
# (a) real academic prose is naturally formulaic-poor but self-repetitive, so
# the self-repetition floor is high; (b) burstiness in published work is far
# above the detector convention for informal text, so the informal 0.30/0.60
# thresholds are NOT used directly.
#
# para_word_cv caveat: this proxy measures paragraph-shape dispersion, but PDF
# extraction flattens paragraph boundaries, so it could not be corpus-validated
# here. It retains a heuristic band and is only scored when a draft supplies real
# paragraph structure (e.g. a markdown file); for flattened prose it is None and
# excluded from risk_index. Its weight (0.15) is the smallest that still lets it
# register in a graded draft.
#
# Each proxy maps to ai_likeness in [0,1] by a linear ramp between a value that
# is fully human-typical (0) and one that is fully AI-typical (1).

RAMPS = {
    # key: (one_at, zero_at) for the raw value; direction handled below
    "burstiness_cv": (30.0, 55.0),      # higher CV = more human
    "formulaic_per100": (0.15, 1.5),
    "self_repeat_pct": (45.0, 60.0),
    "mtld": (50.0, 65.0),               # higher MTLD = more human
    "hedging_per100": (0.3, 1.5),
    "para_word_cv": (18.0, 35.0),       # higher dispersion = more human
}

WEIGHTS = {
    "burstiness_cv": 0.25,
    "formulaic_per100": 0.20,
    "self_repeat_pct": 0.15,
    "mtld": 0.15,
    "hedging_per100": 0.10,
    "para_word_cv": 0.15,
}

# Reporting bands: (ok_side, warn_band, red_band) as plain thresholds.
BANDS = {
    "burstiness_cv":      ("human-like >= 50%", "35-50%", "< 35%"),
    "formulaic_per100":   ("<= 0.5", "0.5-1.5", "> 1.5"),
    "self_repeat_pct":    ("<= 45", "45-60", "> 60"),
    "mtld":               (">= 60", "45-60", "< 45"),
    "hedging_per100":     ("<= 0.5", "0.5-1.5", "> 1.5"),
    "para_word_cv":       (">= 35%", "22-35%", "< 22%"),
}


def _lin(v, one_at, zero_at):
    if one_at == zero_at:
        return 0.0
    return max(0.0, min(1.0, (v - one_at) / (zero_at - one_at)))


def ai_likeness(key, v):
    one_at, zero_at = RAMPS[key]
    raw = _lin(v, one_at, zero_at)
    if key in ("burstiness_cv", "mtld", "para_word_cv"):
        return 1.0 - raw               # high value is the human direction
    return raw


def status(key, v):
    """Status against the corpus-calibrated bands (see the CALIBRATION note)."""
    if key == "burstiness_cv":
        return "OK" if v >= 50 else ("RED" if v < 35 else "WARN")
    if key == "formulaic_per100":
        return "OK" if v <= 0.5 else ("RED" if v > 1.5 else "WARN")
    if key == "self_repeat_pct":
        return "OK" if v <= 45 else ("RED" if v > 60 else "WARN")
    if key == "mtld":
        return "OK" if v >= 60 else ("RED" if v < 45 else "WARN")
    if key == "hedging_per100":
        return "OK" if v <= 0.5 else ("RED" if v > 1.5 else "WARN")
    if key == "para_word_cv":
        return "OK" if v >= 35 else ("RED" if v < 22 else "WARN")
    return "OK"


FIXES = {
    "burstiness_cv":
        "Break the uniform cadence: put one short sentence (<=9 words) next to "
        "a long one so sentence length varies visibly.",
    "formulaic_per100":
        "Replace a stock phrase with the specific claim it is standing in for "
        "(name the mechanism, the actor, or the number).",
    "self_repeat_pct":
        "Vary how the same concept is introduced; repeated 4-word frames are "
        "the clearest self-similarity signal.",
    "mtld":
        "Use the precise verb or noun you mean instead of repeating a generic "
        "one (does not mean rarer vocabulary for its own sake).",
    "hedging_per100":
        "Delete reducible softeners; where a hedge is honest, keep it and say "
        "what the uncertainty is.",
    "para_word_cv":
        "Let paragraph length differ; a page of equal-length paragraphs reads "
        "as templated.",
}


# ---------------------------------------------------------------------------
# 6. Scan
# ---------------------------------------------------------------------------

def scan(paragraphs):
    text = " ".join(paragraphs)
    sents = segment(text)
    toks = tokens_lower(paragraphs)
    lens = [len(words(s)) for s in sents]
    lens = [x for x in lens if x > 0] or [0]

    n_words = len(toks)
    rep = {"corpus": {
        "paragraphs": len(paragraphs),
        "sentences": len(sents),
        "words": n_words,
        "mean_sent_len": round(statistics.fmean(lens), 1) if lens else 0.0,
    }}

    # length reliability
    if n_words < 100:
        rep["corpus"]["reliability"] = (
            "TOO SHORT (<100 words): MTLD suppressed, all proxies unstable")
    elif n_words < 250:
        rep["corpus"]["reliability"] = (
            "SHORT (<250 words): detectors themselves are unreliable here; "
            "read as a direction only")
    else:
        rep["corpus"]["reliability"] = "adequate (>=250 words)"

    # P2 burstiness
    cv = _cv(lens)
    short = sum(1 for x in lens if x <= 9)
    pairs = list(zip(lens, lens[1:]))
    near = sum(1 for a, b in pairs if abs(a - b) <= 2) if pairs else 0
    ratio = sum(1 for a, b in pairs if max(a, b) >= 2 * max(1, min(a, b))) if pairs else 0
    rep["proxies"] = {}
    rep["proxies"]["burstiness_cv"] = {
        "value": round(cv, 1),
        "detail": {
            "stdev_sent_len": round(statistics.pstdev(lens), 1) if len(lens) > 1 else 0.0,
            "pct_sentences_le9_words": round(100.0 * short / max(1, len(lens)), 1),
            "pct_adjacent_within_2_words": round(100.0 * near / max(1, len(pairs)), 1),
            "pct_adjacent_2x_ratio": round(100.0 * ratio / max(1, len(pairs)), 1),
        },
    }

    # P3a/P3b formulaic language
    nf, fhits = _count_patterns(EN_FORMULAIC, text)
    lex = re.compile(r"(?<![\w])(" + "|".join(EN_AI_LEXICON) + r")(?![\w])", re.I)
    lhits = Counter(m.group(0).lower() for m in lex.finditer(text))
    nlex = sum(lhits.values())
    rep["proxies"]["formulaic_per100"] = {
        "value": round(density(nf + nlex, n_words), 2),
        "detail": {"multiword_phrases": nf, "ai_lexicon_tokens": nlex,
                   "multiword_hits": fhits, "lexicon_hits": dict(lhits.most_common(8))},
    }

    # self-repetition
    share, top = repeated_ngram_share(toks)
    rep["proxies"]["self_repeat_pct"] = {
        "value": round(share, 1),
        "detail": {"top_repeated_4grams": top},
    }

    # P5 lexical diversity (suppressed rather than zeroed when too short:
    # a suppressed metric must never be scored as if it were maximally AI)
    m = mtld(toks) if n_words >= 100 else None
    rep["proxies"]["mtld"] = {
        "value": None if m is None else round(m, 1),
        "detail": {"msttr_50": round(msttr(toks), 1),
                   "type_token_ratio": round(100.0 * len(set(toks)) / max(1, n_words), 1),
                   "distinct_types": len(set(toks)),
                   "note": ("MTLD suppressed: fewer than 100 words"
                            if m is None else None)},
    }

    # hedging
    nh, hhits = _count_patterns(EN_HEDGES, text)
    rep["proxies"]["hedging_per100"] = {
        "value": round(density(nh, n_words), 2),
        "detail": {"hits": hhits,
                   "modal_per100_info_only":
                       round(density(len(re.findall(EN_MODALS, text, re.I)), n_words), 2)},
    }

    # paragraph-shape uniformity
    pwords = [len(words(p)) for p in paragraphs]
    pwords = [x for x in pwords if x > 3]
    rep["proxies"]["para_word_cv"] = {
        "value": round(_cv(pwords), 1) if len(pwords) >= 3 else None,
        "detail": {"paragraphs_counted": len(pwords),
                   "words_per_paragraph": pwords[:20],
                   "note": None if len(pwords) >= 3
                           else "fewer than 3 usable paragraphs: not scored"},
    }

    # ---- risk index -------------------------------------------------------
    scored, total_w = 0.0, 0.0
    rows = []
    excluded = []
    for key in WEIGHTS:
        v = rep["proxies"][key]["value"]
        if v is None:
            excluded.append(key)
            continue
        a = ai_likeness(key, v)
        scored += WEIGHTS[key] * a
        total_w += WEIGHTS[key]
        rows.append({"proxy": key, "value": v, "status": status(key, v),
                     "ai_likeness": round(a, 2),
                     "band": "OK %s | WARN %s | RED %s" % BANDS[key],
                     "fix": FIXES[key] if status(key, v) != "OK" else ""})
    idx = round(100.0 * scored / total_w, 1) if total_w else None
    aizone = sum(1 for r in rows if r["ai_likeness"] >= 0.6)
    if idx is None:
        base = "UNDEFINED"
    elif idx < 25:
        base = "LOW"
    elif idx < 45:
        base = "MODERATE"
    elif idx < 65:
        base = "ELEVATED"
    else:
        base = "HIGH"
    # Length gate: the index is always reported for transparency, but it is
    # not graded below the length at which detectors themselves are reliable.
    if n_words < 100:
        tier = "INSUFFICIENT (n<100)"
    elif n_words < 250:
        tier = "LOW-CONFIDENCE " + base
    else:
        tier = base
    rep["risk"] = {
        "risk_index": idx,
        "tier": tier,
        "base_tier": base,
        "weights_used": round(total_w, 2),
        "proxies_excluded": excluded,
        "proxies_in_ai_like_zone": aizone,
        "cluster_flag": aizone >= 3,
        "rows": rows,
        "note": ("risk_index is an internal diagnostic built from published "
                 "proxies with fixed weights; it is NOT a detector prediction "
                 "and must not be optimised as a target."),
    }
    return rep


# ---------------------------------------------------------------------------
# 7. Report
# ---------------------------------------------------------------------------

LABELS = {
    "burstiness_cv": "Burstiness (sentence-length CV %)",
    "formulaic_per100": "Formulaic density (per 100 words)",
    "self_repeat_pct": "Self-repetition (repeated 4-grams %)",
    "mtld": "Lexical diversity (MTLD)",
    "hedging_per100": "Hedge density (per 100 words)",
    "para_word_cv": "Paragraph-shape dispersion (words CV %)",
}


def render(rep):
    o = []
    w = o.append
    c = rep["corpus"]
    w("=" * 74)
    w("DETECTOR-FACING RISK SCAN  (false-positive risk, English prose)")
    w("=" * 74)
    w("paragraphs %d | sentences %d | words %d | mean sentence %.1f words"
      % (c["paragraphs"], c["sentences"], c["words"], c["mean_sent_len"]))
    w("reliability: %s" % c["reliability"])
    w("")
    w("%-42s %9s %6s" % ("PROXY", "VALUE", "STATUS"))
    w("-" * 74)
    for r in rep["risk"]["rows"]:
        w("%-42s %9.2f %6s" % (LABELS[r["proxy"]][:42], r["value"], r["status"]))
    w("-" * 74)
    if rep["risk"]["risk_index"] is None:
        w("risk_index n/a (no scorable proxy)")
    else:
        w("risk_index %.1f / 100   tier %s   proxies in AI-like zone %d%s"
          % (rep["risk"]["risk_index"], rep["risk"]["tier"],
             rep["risk"]["proxies_in_ai_like_zone"],
             "   [CLUSTER]" if rep["risk"]["cluster_flag"] else ""))
    if rep["risk"]["proxies_excluded"]:
        w("not scored (length/insufficient data): %s"
          % ", ".join(rep["risk"]["proxies_excluded"]))
    w("weights used %.2f of 1.00" % rep["risk"]["weights_used"])
    w("")
    for r in rep["risk"]["rows"]:
        if r["fix"]:
            w("  -> %s: %s" % (LABELS[r["proxy"]], r["fix"]))
            w("     band  %s" % r["band"])
    w("")
    w("note: %s" % rep["risk"]["note"])
    w("")
    # detail blocks
    d = rep["proxies"]
    w("[detail] burstiness: %s" % d["burstiness_cv"]["detail"])
    w("[detail] formulaic : %s" % d["formulaic_per100"]["detail"])
    w("[detail] self-rep  : %s" % d["self_repeat_pct"]["detail"])
    w("[detail] diversity : %s" % d["mtld"]["detail"])
    w("[detail] hedging   : %s" % d["hedging_per100"]["detail"])
    w("[detail] paragraphs: %s" % d["para_word_cv"]["detail"])
    w("")
    w("Bands (provisional; anchored on published detector conventions):")
    for k, b in BANDS.items():
        w("  %-42s OK %s | WARN %s | RED %s"
          % (LABELS[k][:42], b[0], b[1], b[2]))
    w("")
    return "\n".join(o)


def delta(rep_a, rep_b, na="BEFORE", nb="AFTER"):
    o = []
    w = o.append
    w("=" * 74)
    w("DELTA  (same instrument, before -> after)")
    w("=" * 74)
    w("%-42s %10s %10s %10s" % ("PROXY", na, nb, "CHANGE"))
    w("-" * 74)
    ma = {r["proxy"]: r for r in rep_a["risk"]["rows"]}
    mb = {r["proxy"]: r for r in rep_b["risk"]["rows"]}
    for k in WEIGHTS:
        if k not in ma or k not in mb:
            continue
        va, vb = ma[k]["value"], mb[k]["value"]
        if va is None or vb is None:
            continue
        d_ = vb - va
        flag = ""
        # direction of improvement depends on the proxy
        if k in ("burstiness_cv", "mtld", "para_word_cv"):
            flag = "better" if d_ > 0 else ("worse" if d_ < 0 else "")
        else:
            flag = "better" if d_ < 0 else ("worse" if d_ > 0 else "")
        w("%-42s %10.2f %10.2f %10s %s"
          % (LABELS[k][:42], va, vb, "%+.2f" % d_, flag))
    w("-" * 74)
    ia, ib = rep_a["risk"]["risk_index"], rep_b["risk"]["risk_index"]
    if ia is not None and ib is not None:
        w("%-42s %10.1f %10.1f %10s"
          % ("risk_index", ia, ib, "%+.1f" % (ib - ia)))
    else:
        w("%-42s %10s %10s" % ("risk_index", ia, ib))
    w("tier: %s -> %s" % (rep_a["risk"]["tier"], rep_b["risk"]["tier"]))
    if rep_a["corpus"]["words"] < 250 or rep_b["corpus"]["words"] < 250:
        w("WARNING: at least one side is under 250 words; the delta is not "
          "gradable. Compare full sections, not fragments.")
    w("")
    return "\n".join(o)


# ---------------------------------------------------------------------------
# 8. Selftest
# ---------------------------------------------------------------------------

def selftest():
    n = [0]

    def ok(name, cond):
        n[0] += 1
        print("  %s %s" % ("PASS" if cond else "FAIL", name))
        if not cond:
            raise SystemExit("selftest failed: %s" % name)

    ok("segment splits", len(segment("One two. Three four.")) == 2)
    ok("segment keeps decimal", len(segment("The rate is 0.5 in 2020.")) == 1)
    ok("mtld monotone in variety",
       mtld([("w%d" % i) for i in range(200)]) >
       mtld(list("ab") * 100))
    ok("cv of constant is 0", abs(_cv([10, 10, 10])) < 1e-9)
    ok("cv of varied is positive", _cv([4, 20, 7]) > 0)
    ok("ai_likeness burstiness direction",
       ai_likeness("burstiness_cv", 20) > ai_likeness("burstiness_cv", 60))
    ok("ai_likeness mtld direction",
       ai_likeness("mtld", 40) > ai_likeness("mtld", 90))
    ok("ai_likeness cliche direction",
       ai_likeness("formulaic_per100", 8) > ai_likeness("formulaic_per100", 0.5))
    ok("status burstiness red", status("burstiness_cv", 22) == "RED")
    ok("status burstiness ok", status("burstiness_cv", 50) == "OK")
    ok("status mtld red", status("mtld", 40) == "RED")
    ok("repeated ngram finds repetition",
       repeated_ngram_share("alpha beta gamma delta alpha beta gamma delta".split())[0] > 0)
    ok("repeated ngram empty on short",
       repeated_ngram_share(["a", "b"])[0] == 0.0)

    cliche = ("It is important to note that this plays a crucial role in "
              "today's digital age. Delve into the multifaceted landscape. "
              "It is important to note that this plays a crucial role again.")
    plain = ("The reform cut fees by nine percent. Enrollment rose in the "
             "next year. Rural households gained the most, and urban ones "
             "gained little.")
    r_c = scan([cliche])
    r_p = scan([plain])
    ok("cliche text scores higher formulaic",
       r_c["proxies"]["formulaic_per100"]["value"] >
       r_p["proxies"]["formulaic_per100"]["value"])
    ok("cliche text scores higher risk",
       r_c["risk"]["risk_index"] > r_p["risk"]["risk_index"])
    flat = ["The rate is one. " * 12]
    varied = ["The rate is one. " * 2 + "A much longer sentence that keeps "
              "going and going and going and going and going adds words. "
              + "Short one. " * 2]
    ok("flat text scores lower burstiness",
       scan(flat)["proxies"]["burstiness_cv"]["value"] <
       scan(varied)["proxies"]["burstiness_cv"]["value"])
    ok("short text flagged unreliable",
       "TOO SHORT" in scan(["one two three"])["corpus"]["reliability"])

    # markdown cleaning must drop headings, tables and code but keep prose
    import tempfile
    md = ("# Title\n\nWe estimate the effect on rural households.\n\n"
          "| a | b |\n|---|---|\n| 1 | 2 |\n\n"
          "```\ncode_block()\n```\n\nA second prose paragraph follows here.\n")
    with tempfile.NamedTemporaryFile("w", suffix=".md", delete=False,
                                     encoding="utf-8") as fh:
        fh.write(md)
        tmp = fh.name
    try:
        paras, _ = load_paragraphs(tmp)
        joined = " ".join(paras)
        ok("md keeps prose paragraphs", len(paras) == 2)
        ok("md drops heading", "# Title" not in joined)
        ok("md drops table", "| a | b |" not in joined)
        ok("md drops code", "code_block" not in joined)
    finally:
        os.remove(tmp)

    # values typical of real top-journal prose must NOT be flagged: these
    # assertions lock the corpus calibration into the test suite
    ok("calibration: burstiness 59 OK", status("burstiness_cv", 59.3) == "OK")
    ok("calibration: self-repeat 30 OK", status("self_repeat_pct", 29.8) == "OK")
    ok("calibration: formulaic 0.07 OK", status("formulaic_per100", 0.07) == "OK")
    ok("calibration: mtld 79 OK", status("mtld", 79.0) == "OK")
    ok("calibration: mtld 64.4 OK (corpus floor)",
       status("mtld", 64.4) == "OK")
    ok("calibration: hedge 0.07 OK", status("hedging_per100", 0.07) == "OK")

    # a suppressed proxy is excluded, and a short text is not graded
    short = ["The rate is one and the effect is small. " * 8]
    r_s = scan(short)
    ok("mtld excluded when <100 words", "mtld" in r_s["risk"]["proxies_excluded"])
    ok("short text not graded", r_s["risk"]["tier"].startswith("INSUFFICIENT"))
    ok("risk_index still reported for transparency",
       r_s["risk"]["risk_index"] is not None)

    print("selftest: %d assertions passed" % n[0])
    return 0


# ---------------------------------------------------------------------------
# 9. CLI
# ---------------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser(
        description="Detector-facing false-positive-risk scanner (English).")
    ap.add_argument("files", nargs="*", help="up to two manuscript paths; '=' for stdin")
    ap.add_argument("--text", help="analyse this string instead of a file")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()

    if a.files and a.files[0] == "selftest":
        return selftest()

    if not a.files and a.text is None:
        ap.print_help()
        return 1

    if a.text is not None:
        reps = [scan([a.text])]
    else:
        if len(a.files) > 2:
            sys.stderr.write("error: at most two files\n")
            return 2
        reps = []
        for f in a.files:
            try:
                paras, _ = load_paragraphs(f)
            except OSError as exc:
                sys.stderr.write("error: cannot read '%s' (%s)\n"
                                 % (f, getattr(exc, "strerror", None) or exc))
                return 2
            if not paras:
                sys.stderr.write("error: no prose found in '%s'\n" % f)
                return 2
            reps.append(scan(paras))

    if a.json:
        print(json.dumps(reps[0] if len(reps) == 1 else reps,
                         ensure_ascii=False, indent=2))
        return 0
    for i, r in enumerate(reps):
        if len(reps) == 2:
            print("===== %s =====" % ("BEFORE" if i == 0 else "AFTER"))
        print(render(r))
    if len(reps) == 2:
        print(delta(reps[0], reps[1]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
