# Anti-AI-Trace Audit — Programmatic Method

Companion to **Step 8 (AI-Trace Reflection)** of `SKILL.md`, and to Steps 5 and 6.

This file turns the anti-AI pass from an impressionistic read into a measured
loop: **baseline → triage → rewrite → re-measure → verify rhythm**, with two
scripts in `scripts/` doing the measuring.

---

## 1. Why the pass is programmatic

Three reasons, in order of importance.

1. **Manual judgement is not reproducible.** A reader who has just noticed one
   pattern tends to notice it everywhere. Two readers rarely produce the same
   list, and neither can say whether a rewrite helped.
2. **Density is the signal, not presence.** `respectively`, `rather than`, and a
   colon introducing a list are all correct academic English. What reads as
   machine-written is a *texture*: every third sentence opening with a
   transition peg, consecutive sentences of near-identical length, a single
   consequence frame (`, so Y`) doing all the work. Texture is a count, not an
   impression.
3. **A claim of improvement needs evidence.** "I removed the AI traces" is not
   falsifiable. A before/after table is.

**State the objective honestly.** The purpose is not to evade AI detectors,
which are unreliable and are not the standard a referee applies. The purpose is
to remove the stylistic fingerprints that coincide with *real* writing
weaknesses: mechanised transitions, uniform sentence rhythm, clause-stacked
sentences, and restatement that adds no content. Every rewrite rule below is
justified by the writing defect it fixes, not by its effect on a detector.

---

## 2. The five stages

### S1 — Baseline
Run both scanners on the current manuscript and **record** the numbers. Do not
begin editing first; without a baseline the pass cannot be reported.

```bash
python scripts/scan_ai_traces.py manuscript.tex          # structure
python scripts/scan_register.py manuscript.tex --limit 8 # diction
python scripts/scan_detectability.py manuscript.tex      # detector-facing proxies
python scripts/scan_ai_traces.py manuscript.tex --json > baseline.json
```

`scan_detectability.py` measures the handful of *statistical proxies that
commercial AI detectors actually score* (see §3b). It is a **false-positive-risk
diagnostic**, not a detector, and is never optimised as a target (§3b honesty
boundary).

### S2 — Triage
Sort every finding into **defect** or **probe** using the bands in §3. Defects
are fixed. Probes are read in context and only reduced when the density itself
is the problem. Never zero out a probe to make a number look clean.

### S3 — Rewrite
Apply §4's mapping. Batch the edits as exact string replacements and verify
each target occurs exactly once (see pitfall 6).

### S4 — Re-measure
Re-run S1 on the revised file and build the delta table. Report it with the
deliverable. A rewrite that does not move the numbers should be reported as not
having done so.

### S5 — Rhythm verification
Re-run the `[E] RHYTHM` block and confirm the rewrite did not flatten the prose.
This stage exists because the most likely way to *fail* an anti-AI pass is to
over-succeed at stage S4 — see pitfall 1.

---

## 3. Thresholds and target bands

| Probe | Defect when | Target | Reading |
|---|---|---|---|
| `---` or U+2014 em dash | any | `0` | A mid-sentence explanatory dash is the single most reliable trace |
| Explanatory colon | — | probe | Context-dependent; see §5.3 |
| Transition-peg density | `> 10%` of sentences | `<= 5%` | Pegs are `However`, `Moreover`, `Importantly`, `In particular`, `Thus`, `Therefore`, `Specifically`, `Notably`, … |
| `N purposes / assumptions / features` + `First, Second, Third` | `>= 3` occurrences | `<= 2` | The template is `N X. First, … Second, … Third, …` |
| Sentences `> 45` words (EN) or `> 60` characters (ZH) | `> 10%` | `<= 5%` | Clause stacking |
| Sentences `> 60` words (EN) or `> 90` characters (ZH) | any | `0` | Treat as a defect regardless of share |
| Adjacent sentences within `±2` words | `> 25%` | `<= 25%` | Reads as recited rhythm |
| Longest run of same-length sentences | `>= 4` | `<= 3` | A sustained monotone passage |
| Hype / ornate / assertive filler / over-assertive verbs / wordy nominalisation | any | `0` | No legitimate use in an empirical manuscript |
| Vague intensifier, precision claim, vague quantifier, `rather than` | — | probe | Density judgement; these are frequency signals |

### 3b. Detector-facing proxies (`scan_detectability.py`)

`scan_ai_traces.py` measures *structural* traces that coincide with real writing
defects. `scan_detectability.py` measures a different thing: the published
*statistical proxies that commercial AI detectors actually score*, so a
false-positive risk can be seen and reduced in a human-written or legitimately
polished manuscript. The proxies are the standard published ones, not invented:

| Proxy | What it proxies | Why it is a detector signal |
|---|---|---|
| **P2 burstiness** — sentence-length CV% | low burstiness (uniform sentences) | detector convention: flat rhythm ⇒ likely AI |
| **P3 formulaic density** — per 100 words | high formulaic language | stock phrases / AI-typical lexicon are predictable |
| **P4 self-repetition** — repeated 4-grams % | self-similarity | repeated frames are predictable |
| **P5 lexical diversity** — MTLD | low diversity | repetitive vocabulary is predictable |
| **hedge density** — per 100 words | hedging / formulaic connectors | vendors weight these |
| **paragraph-shape CV%** | uniform paragraphs | a page of equal blocks reads templated |

Honesty boundary (read before acting on any number):

1. **This is NOT a detector and does not predict a detector's score.** Commercial
   detectors are neural classifiers; the same text commonly scores differently
   across them. Treat every number here as a *direction*, not a grade.
2. **Real perplexity needs a language model**; this script has no model and no
   network. Word-frequency rarity is deliberately *not* used as a proxy — in this
   register it inverts (technical terms are globally rare but locally
   predictable). Formulaicity and self-repetition are used instead.
3. **Consistent formality (P4 in vendor lists) is deliberately NOT scored.** Formal
   academic English is uniformly formal by construction, so the proxy carries no
   variance here and can only mislead.
4. **Short text is unstable.** Below ~250 words detectors are themselves
   unreliable; below 100 words MTLD is suppressed (not zeroed). The tool says so.
5. **Reducing these proxies is legitimate only for text you wrote or legitimately
   polished.** This is a false-positive-risk diagnostic, not a bypass tool.
   Authoring and disclosure rules are unaffected.

Calibration — era-stratified, per the user's instruction that 2021+ literature may
itself be AI-influenced. The bands were anchored on a 9-paper top-5
econ/management corpus split into **OLD** (4 pre-2020 papers: Autor-Dorn 2013 AER,
Chetty 2014 QJE, MTO ~2007/2012, QJE qjz042 ~2015/2019) and **NEW** (5 papers
2021+: Tertiarization 2022, China Financial System 2022, Intrachoice 2023, Putting
Teams 2023, Marx-Hsu 2021). The two eras are **statistically indistinguishable**
on every proxy — the 2021+ papers show no contamination signature:

| Proxy | OLD median (min–max) | NEW median (min–max) |
|---|---|---|
| burstiness CV% | 55.6 (50.6–73.5) | 63.4 (55.6–89.6) |
| formulaic /100w | 0.06 (0.00–0.09) | 0.07 (0.03–0.12) |
| self-repeat % | 15.2 (8.0–39.8) | 29.8 (6.1–40.9) |
| MTLD | 71.9 (66.4–72.9) | 88.3 (64.4–105.9) |
| hedge /100w | 0.07 (0.05–0.14) | 0.07 (0.04–0.11) |
| risk_index | 1.6 (0.0–5.2) | 0.0 (0.0–0.7) |

Every real paper scores **LOW** (0–5.2) on `risk_index`; none is RED on any proxy.
That is the design target: legitimate prose must not be flagged. It also confirms
the conceptual point — these proxies measure a *stylistic fingerprint, not AI
authorship*, and a well-written 2023 paper is indistinguishable from a 2013 one on
them. (Caveat: paragraph-shape CV could not be corpus-validated because PDF
extraction flattens paragraph boundaries; it keeps a heuristic band and only
scores when a draft supplies real paragraphs.)

Two documented biases in the scanner, to keep in view when reading a report:

- Word counts exclude mathematics, citations, and cross-reference placeholders,
  so `mean_words` measures **prose** rhythm, not notional sentence length. A
  sentence containing a long inline expression will therefore look shorter here
  than it reads on the page.
- Display equations and float bodies are stripped before segmentation. A
  sentence that ends immediately before a display and the sentence that begins
  immediately after it can be measured as one. Discount `>45`-word hits whose
  text straddles a `:` or an equation boundary.

---

## 4. Trace → fix mapping

| Trace | Fix | Why |
|---|---|---|
| Explanatory colon | Sentence break, semicolon, or a `which` / `as` clause | The colon substitutes punctuation for structure |
| `N purposes. First, … Second, … Third, …` | Content-led transitions (`On design, …`; `The outcome, by contrast, …`) | Recitation replaces argument |
| Sentence `> 45` words | Split at the least dependent clause | Clause stacking is the strongest machine signature |
| `, so Y` repeated | Vary: `under which`, `which <verb>s`, `and X therefore <verb>`, sentence break | One consequence frame doing all the work |
| `rather than` dense | `not`, `as opposed to`, or recast the clause | Single contrast frame |
| Tautological double clause | Reduce to one clause | States the same content twice |
| Metadiscourse peg (`This is precisely why`, `This matters because`) | Delete; let the claim stand | Self-narration in place of content |
| Redundant restatement sentence (`It is the audit trail for the framework.`) | Delete | Adds no information |
| Comma splice or wrong punctuation before a display | Colon or full stop | Grammar — and a spliced clause also reads machine-made |
| Verbatim duplication across sections | Forward reference | Signals generated padding |
| Intensifier over a small effect (`strongly significant` at `p = 0.05`) | Plain `significant` | A **calibration defect**, not merely style: see §5.9 |
| Filler `robust` inside a causal claim (`no robust causal decline`) | Restate the claim precisely | Vague hedge standing in for the finding |
| `respectively` at the end of a paired statement | Two sentences, or restructure | Ambiguous pairing; a known over-use |

---

## 5. Pitfalls

**5.1 A falling sentence-length standard deviation is not success.**
This is the trap the pass is most likely to fall into. Removing 90-word
outliers lowers the stdev *and* improves readability; flattening the prose also
lowers the stdev and makes it worse. Only the rhythm block distinguishes the
two: healthy prose keeps `within ±2 words` low (≈10–20%) and `>= 2× ratio`
high (≈40%+). Run S5 before reporting any stdev movement.

**5.2 En dashes are legitimate.** In LaTeX, `--` renders as an en dash and is
correct in compound terms (`treated--control`) and numeric ranges (`ages 6--15`).
Only `---` or U+2014 used to insert an explanation is a trace. A naive count of
`--` produces false positives on any economics manuscript.

**5.3 Colons are usually legitimate.** A colon introducing a genuine list, a
displayed equation, or a stated assumption is standard journal prose. Treat the
count as a probe.

**5.4 Do not zero out a probe.** `respectively`, `rather than`, and `several` are
normal. The signal is density. Eliminating them entirely produces stilted prose
and is a worse outcome than the original.

**5.5 Never touch content.** An anti-AI pass is a style pass. Numbers,
coefficients, standard errors, equations, citations, cross-references, table and
figure content, and technical terminology are out of scope. A changed
coefficient is a different paper.

**5.6 Verify every replacement.** Apply rewrites as exact-match replacements
with a `count == 1` check, and print the failures. Silent partial application
is the main operational risk in a large batch: several edits can report success
while overwriting one another.

**5.7 Expect boundary artefacts.** See §3. Read the long-sentence list before
acting on it.

**5.8 Preserve non-ASCII byte-for-byte.** Manuscripts may contain CJK text,
typographic quotes, or mathematical symbols. Read and write UTF-8 without
normalisation, and confirm the file size change is attributable to the edits.

**5.9 Word choice is a calibration issue, not a cosmetic one.**
`strongly significant` for `p = 0.025`, `severely skewed` for an ordinary
right skew, and `materially tighter` with no comparison are not merely
AI-flavoured: they **overstate the evidence**. Register work at this level
belongs in the same pass as the sentence work, and each instance should be
logged with the rationale category *Word choice / Register*.

---

## 6. Deliverable format

1. **Block A** — the polished text, produced per Step 6.
2. **Block B** — the revision-notes table, with every entry tagged
   *Sentence logic* or *Word choice / Register*.
3. **The delta table** — a third block, without which the first two are
   unverifiable:

| Probe | Before | After |
|---|---|---|
| `---` em dash | | |
| transition-peg density | | |
| sentences `> 45` words | | |
| sentences `> 60` words | | |
| mean sentence length | | |
| adjacent pairs within `±2` words | | |
| adjacent pairs with `≥2×` ratio | | |
| longest same-length run | | |
| defect-band token counts | | |
| detector risk_index (scan_detectability) | | |
| burstiness CV% | | |
| formulaic density /100w | | |
| self-repetition % | | |
| MTLD | | |
| hedge density /100w | | |

Do not claim an improvement the delta table does not show, and state plainly
which probes were left deliberately unchanged and why.

---

## 7. Worked example (generic)

**Before**

> The specification is estimated in two forms. It serves two purposes. It
> isolates the post-period contrast, and it absorbs the compositional drift
> that would otherwise contaminate the estimate: the treated share rises from
> 0.32 to 0.58 across waves, so a pooled coefficient would attribute this drift
> to the reform. This is precisely why we report the saturated form.

Findings: `N purposes` + recited triad; explanatory colon; `, so Y`;
`This is precisely why`; one sentence of 46 words.

**After**

> The specification is estimated in two forms. The saturated form isolates the
> post-period contrast, and it absorbs the compositional drift that would
> otherwise contaminate the estimate. The treated share rises from 0.32 to 0.58
> across waves, so a pooled coefficient would attribute this drift to the
> reform. We therefore report the saturated form.

Changes: the `It serves two purposes` + triad collapsed into one clause chain;
the colon became a sentence break; the metadiscourse peg replaced by the
content-carrying `We therefore report …`. Sentence lengths moved from
`5 / 4 / 46` to `5 / 27 / 22 / 7`, which is what the rhythm block rewards.

---

## 8. Tool reference

```
scripts/scan_ai_traces.py <file> [--lang en|zh] [--long 45] [--json]
    [A] punctuation traces
    [B] transition-peg density
    [C] repeated syntactic templates
    [D] long-sentence load (list + counts, >45 and >60 words)
    [E] rhythm: within ±2 words, ≥2× ratio, longest same-length run, histogram

scripts/scan_register.py <file> [--lang en|zh] [--limit 6] [--json]
    DEFECT bands:  hype/journalistic, ornate/literary, assertive filler,
                   over-assertive verbs, AI emphasis adverbs,
                   wordy nominalisation
    CONTEXT bands: self-narration, vague intensifier, precision claim,
                   vague quantifier, repeated contrast frame

scripts/scan_detectability.py <file> [--json] [--text "…"] [selftest]
    burstiness (sentence-length CV%), formulaic density, self-repetition %,
    MTLD, hedge density, paragraph-shape CV%  ->  risk_index + per-proxy bands
    Honesty boundary: a false-positive-risk diagnostic, NOT a detector; never
    optimised as a target. Bands are era-stratified (pre-2020 vs 2021+ corpus).

Both scripts: standard library only, read-only, no network, no subprocess.
Input: .tex (preamble, floats, tables, and display maths stripped),
       .md (code fences and tables stripped), or plain text; `-` reads stdin.
`--lang zh` switches the probes to Chinese trace patterns (破折号, 解释性冒号,
"需要注意的是", 机械列举, …).
```

An excerpt of a full report, for orientation:

```
[B] TRANSITION-PEG DENSITY
    1 of 311 sentences (0.3%)   target: <= 10%

[D] LONG-SENTENCE LOAD
    >45 words: 4 (1.3%)   over 60 words: 0

[E] RHYTHM (counter-check against over-flattening)
    within +/-2 words              13.2%   <- lower is better
    with >=2x length ratio         41.9%   <- higher is better
    longest same-length run        4
```
