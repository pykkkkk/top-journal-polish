#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Word-level register scanner for academic manuscripts.

Companion to the top-journal-polish skill, Steps 5 and 8.

Police non-technical diction against the three governing rules of
`references/word_choice.md`: disciplinary priority, neutral register, and
intensity-matched substitution. The scanner separates two kinds of findings:

  DEFECT      a trace that should be removed or replaced
  CONTEXT     legitimate in some positions (e.g. "sharply" for a real
              magnitude change, "rather than" for a real contrast, "several"
              for a real count). Report, then judge in context.

Reporting legitimate-but-repeated items is the point: density, not mere
presence, is the signal.

Usage
-----
    python scan_register.py <file> [--lang en|zh] [--limit 6] [--json]

Read-only: opens no sockets, spawns no subprocess, writes no files.
Standard library only.
"""

import argparse
import json
import os
import re
import sys
from collections import Counter

# --------------------------------------------------------------------------
# Bands:  (label, severity, regex)
#   severity: "defect"  -> should be fixed
#             "context" -> report density; judge each instance in context
# --------------------------------------------------------------------------

EN_BANDS = [
    ("hype / journalistic", "defect",
     r"skyrocket\w*|plummet\w*|soar\w*|plunge\w*|shocking\w*|explosive\w*|"
     r"game-chang\w*|revolutioniz\w*|unprecedented\w*|viral\w*"),

    ("ornate / literary", "defect",
     r"delve|delv\w+|myriad|plethora|burgeon\w*|tapestry|realm|beacon|"
     r"cornerstone|bedrock|poised to|usher\w*|herald\w*|paradigm shift|"
     r"rich tapestry|landscape of\w*"),

    ("assertive filler", "defect",
     r"[Ii]t is important to note|[Ii]t should be noted|[Ii]t is worth noting|"
     r"suffice it to say|needless to say|[Aa]s (?:we|is) all know"),

    ("over-assertive verb", "defect",
     r"\b(?:proves?|disproves?|demonstrates? (?:conclusively|clearly)|"
     r"undoubtedly|definitively|incontrovertibly|indisputably)\b"),

    ("AI emphasis adverb", "defect",
     r"(?:^|\. )(?:Importantly|Critically|Crucially|Strikingly|Notably),|"
     r"(?:^|\. )(?:Essentially|Ultimately|Arguably),"),

    ("wordy nominalization", "defect",
     r"in order to|due to the fact that|for the purpose of|in the event that|"
     r"with respect to|on the part of|in terms of"),

    ("self-narration", "context",
     r"[Ww]e note that|[Ww]e read the evidence|[Aa]s we (?:document|show|argue) "
     r"(?:below|above)|[Ii]n this (?:paper|section|subsection), we"),

    ("vague intensifier", "context",
     r"\b(?:very|quite|fairly|extremely|severely|greatly|substantially|"
     r"considerably|remarkably|particularly|especially|really|truly)\b"),

    ("precision claim", "context",
     r"\b(?:precisely|exactly|perfectly|materially|markedly)\b"),

    ("vague quantifier", "context",
     r"\b(?:various|numerous|several|many|some|a range of|a wide range of|"
     r"a battery of|a host of)\b"),

    ("repeated contrast frame", "context",
     r"\brather than\b"),
]

ZH_BANDS = [
    ("新闻腔", "defect", r"飙升|暴跌|井喷|爆发式|史无前例|颠覆性|空前|震撼|引爆"),

    ("华丽/文学化", "defect",
     r"深入探讨|诸多|纷繁|蓝图|里程碑|基石|标杆|谱系|铺陈|勾勒|绽放"),

    ("断言填充", "defect", r"众所周知|不言而喻|毋庸置疑|显而易见|不言自明"),

    ("过度断言动词", "defect", r"充分证明|无可辩驳|确凿无疑|彻底颠覆"),

    ("AI 提示语气", "defect", r"需要注意的是|值得注意的是|需要强调的是|值得一提的是"),

    ("机械列举", "defect", r"第[一二三四五六]，"),

    ("自我叙述", "context", r"本文认为|笔者认为|我们认为|我们注意到|本文试图"),

    ("冗余名词化", "context",
     r"进行[^，。]{0,6}的(?:分析|研究|讨论|考察)|作出[^，。]{0,6}的判断|"
     r"起到[^，。]{0,6}的作用|对[^，。]{0,8}进行[^，。]{0,6}"),

    ("空洞强化/模糊量词", "context",
     r"非常|十分|极其|相当|大大|一些|许多|大量|各种|若干|部分"),
]


# --------------------------------------------------------------------------
# Line extraction (skip maths, tables, code)
# --------------------------------------------------------------------------

def lines_of(path):
    if path == "-":
        raw = sys.stdin.read()
        kind = "txt"
    else:
        with open(path, encoding="utf-8", errors="replace") as fh:
            raw = fh.read()
        kind = os.path.splitext(path)[1].lower().lstrip(".")
    skip_env = ("table", "threeparttable", "longtable", "tabular", "equation",
                "align", "gather", "multline", "tikzpicture", "verbatim",
                "lstlisting")
    out, depth = [], None
    for i, ln in enumerate(raw.splitlines(), 1):
        s = ln.strip()
        if kind == "tex":
            m = re.search(r"\\begin\{(" + "|".join(skip_env) + r")\*?\}", s)
            if m:
                depth = m.group(1)
            if depth:
                if re.search(r"\\end\{" + depth + r"\*?\}", s):
                    depth = None
                continue
            if not s or s.startswith("%") or s.startswith("\\"):
                continue
            s = re.sub(r"\$[^$]*\$", " MATH ", s)
        elif kind in ("md", "markdown"):
            if not s or s.startswith("#") or s.startswith("|") or s.startswith("```"):
                continue
            s = re.sub(r"`[^`]*`", " ", s)
        else:
            if not s:
                continue
        out.append((i, s))
    return out


# --------------------------------------------------------------------------
# Scan
# --------------------------------------------------------------------------

def scan(pairs, lang="en", limit=6):
    bands = EN_BANDS if lang == "en" else ZH_BANDS
    findings = []
    for label, severity, pat in bands:
        rx = re.compile(pat)
        hits = [(i, s) for i, s in pairs if rx.search(s)]
        if not hits:
            continue
        tokens = Counter(m.group(0).lower() for _, s in hits for m in rx.finditer(s))
        findings.append({
            "band": label,
            "severity": severity,
            "lines": len(hits),
            "tokens": dict(tokens.most_common()),
            "examples": [{"line": i, "text": s[:180]} for i, s in hits[:limit]],
        })
    return findings


def render(pairs, findings):
    w = print
    w("=" * 74)
    w("WORD-LEVEL REGISTER SCAN")
    w("=" * 74)
    w("prose lines scanned: %d" % len(pairs))
    if not findings:
        w("\nno band matched")
        return
    defects = [f for f in findings if f["severity"] == "defect"]
    context = [f for f in findings if f["severity"] == "context"]
    for title, group in (("DEFECT -- fix these", defects),
                         ("CONTEXT -- judge density, do not auto-flag", context)):
        if not group:
            continue
        w("\n" + title)
        w("-" * 74)
        for f in group:
            w("\n  %s   (%d lines)" % (f["band"], f["lines"]))
            w("    tokens: %s" % f["tokens"])
            for ex in f["examples"]:
                w("    L%-5d %s" % (ex["line"], ex["text"]))
            if f["lines"] > len(f["examples"]):
                w("    (%d more lines)" % (f["lines"] - len(f["examples"])))
    w("")


def main():
    ap = argparse.ArgumentParser(description="Word-level register scanner.")
    ap.add_argument("file", help="manuscript path (.tex/.md/.txt) or '-' for stdin")
    ap.add_argument("--lang", choices=["en", "zh"], default="en")
    ap.add_argument("--limit", type=int, default=6, help="examples per band (default 6)")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    try:
        pairs = lines_of(a.file)
    except OSError as exc:
        sys.stderr.write("error: cannot read '%s' (%s)\n"
                         % (a.file, getattr(exc, "strerror", None) or exc))
        return 2
    findings = scan(pairs, a.lang, a.limit)
    if a.json:
        print(json.dumps({"lines": len(pairs), "findings": findings},
                         ensure_ascii=False, indent=2))
    else:
        render(pairs, findings)
    return 0


if __name__ == "__main__":
    sys.exit(main())
