# top-journal-polish

### Publication-grade academic translation & writing polish for economics, management, and quantitative social science

> Bilingual (中文 ↔ English) translation and English-only revision aligned with the editorial
> conventions of **eight top outlets** — AER, QJE, JPE, Econometrica, Management Science, JFE,
> JEEA, and REStud — plus a general top-journal fallback. Built for empirical economists, applied
> econometricians, and quantitative social scientists who want their prose to read like it already
> cleared desk review.

---

![Journal styles](https://img.shields.io/badge/journal%20styles-8-blue)
![Terminology](https://img.shields.io/badge/terminology-12%20categories%20%C2%B7%20135%20pairs-9c27b0)
![Languages](https://img.shields.io/badge/languages-中文%20%C2%B7%20English-brightgreen)
![Workflow](https://img.shields.io/badge/workflow-9--step%20pipeline-orange)
![Scripts](https://img.shields.io/badge/scripts-4%20%C2%B7%20stdlib%20only-lightgrey)
![License](https://img.shields.io/badge/license-MIT-green)

---

## What it does

`top-journal-polish` turns rough drafts, Chinglish, and literal translations into disciplinary,
journal-ready prose. It does **not** simply paraphrase. It runs a strict nine-step pipeline that:

1. **Identifies the task type** — `TR-ZH2EN`, `TR-EN2ZH`, or `PO-EN`.
2. **Classifies the text segment** (abstract, introduction, identification, results, robustness,
   mechanism, conclusion, …) and applies segment-specific rules.
3. **Fact-checks causal-inference claims** against a bundled, self-contained causal-facts reference
   *before* touching wording — a translation that is fluent but wrong is worse than one that is
   clumsy but correct.
4. **Normalizes terminology** to the internationally standardized forms (e.g. *parallel trends
   assumption*, not *parallel trend hypothesis*; *instrumental variables (IV) estimation*, not
   *instrumental variable method*).
5. **Enforces a neutral academic register** — strips literary ornament and journalistic hype, and
   offers intensity-matched alternatives (with reasons) so tone stays neutral, never dramatic.
6. **Produces two blocks** — Block A (clean final text) and Block B (revision table with a stated
   rationale for every change).
7. **Adapts to a named target journal** (AER voice ≠ QJE voice ≠ Econometrica voice).
8. **Strips AI-generated tells** in a *measured loop*: baseline scan → triage → rewrite → re-measure,
   with a before/after delta table.
9. **Runs a prosody gate** on the finished English prose: rhythm and density metrics with red-line
   markers, iterated until nothing RED remains.

The skill ships with **six reference files** and **four standard-library scripts** — see
[Project structure](#project-structure).

---

## Why this skill exists

Most "polish" tools and prompts do one of two things badly:

- They **translate literally**, producing textbook-idiosyncratic or China-domestic-journal variants
  ("鉴别方法" → *identification method* instead of *identification strategy*; "工具变量法" →
  *instrumental variable method* instead of *instrumental variables (IV) estimation*).
- They **smooth prose without checking substance**, leaving factually incorrect causal claims
  (calling a collider a mediator, asserting SUTVA holds under clear interference) intact and polished.

This skill treats terminology as a **correctness** problem, not a style problem, and treats causal
claims as something to verify before rewriting. The result is text a referee is less likely to flag
on first read.

A third failure mode is what the last two steps target: prose that is *correct and idiomatic but
reads like a model wrote it*, or that is rhythmically flat enough to be uncomfortable to read. Steps 8
and 9 measure both, and Step 8 re-measures after editing rather than trusting a read-through.

---

## Features

| Feature | What you get |
|---------|--------------|
| **Three task modes** | `TR-ZH2EN` (中文→英文), `TR-EN2ZH` (英文→中文技术回译), `PO-EN` (英文-only polish) |
| **Segment-aware rules** | Abstract, Introduction, Literature, Theory, Empirical/Identification, Results, Robustness, Mechanism, Conclusion each get their own conventions |
| **Causal-inference fact-check** | Claims checked against a bundled causal-facts reference (SUTVA, backdoor, collider/mediator, DID/RDD/IV assumptions) — no external textbook or connector dependency |
| **Canonical terminology** | 12 categories, 135 EN↔ZH pairs with explicit *avoid* columns |
| **Strict word choice** | Three-band register control (literary / neutral / hype) plus intensity spectra for common words, with intensity-matched alternatives and reasons |
| **Journal-specific voice** | 8 outlets with signature tone, abstract length, hedge hierarchy, and prohibited patterns |
| **Measured AI-trace audit** | Step 8 is a measured loop with **three** bundled scanners: take a baseline, rewrite, re-measure, verify rhythm did not flatten. Ships with threshold bands, a trace-to-fix mapping, and a before/after delta table |
| **Detector-risk diagnostic** | A third scanner measures the six statistical proxies that commercial AI detectors score, and reports a `risk_index` — explicitly a *false-positive-risk diagnostic, never a target* |
| **Prosody gate (Step 9)** | Quantitative rhythm-and-density gate: nPVI, %stressed syllables, stress alternation, inter-stress CV, syllables/word, sentence-length statistics, and parallelism density — with five red-line markers |
| **Transparent revisions** | Every change is logged with a rationale (terminology / word choice / logic / journal convention / causal language) |
| **Equation & citation safety** | Mathematical content never altered; missing citations flagged with `[CITE?]`; inconsistent notation flagged inline |

---

## Supported journals

The skill adapts its voice and structure to the target outlet. Activate a journal by naming it
(e.g. *"polish this for QJE"*) or by its tag.

| Tag | Journal | Signature |
|-----|---------|-----------|
| `[AER]` | American Economic Review | Authoritative, economical; every sentence earns its place |
| `[QJE]` | Quarterly Journal of Economics | Confident, big-picture; strong empirical claims when well-identified |
| `[JPE]` | Journal of Political Economy | Intellectual gravitas; theory–empirics integration |
| `[ECTA]` | Econometrica | Strictly formal; numbered assumptions, labeled proofs |
| `[MS]` | Management Science | Rigorous but accessible; managerial implications required |
| `[JFE]` | Journal of Financial Economics | Asset pricing / corporate finance; economic magnitudes mandatory |
| `[JEEA]` | Journal of the European Economic Association | Clean ID + policy relevance; distributional analysis valued |
| `[REStud]` | Review of Economic Studies | Theory + structural-empirical integration |
| `—` | General top-journal standard | Applied when no journal is named |

> **Coverage of the bundled style file.** `references/journal_styles.md` carries a section for each
> of the eight outlets above, plus a general top-journal section that applies when no journal is
> named. Naming an outlet that has no section falls back to those general principles — see
> [Customization](#customization) for how to add one.

---

## Terminology coverage

The bundled `references/terminology.md` is the backbone of correctness: **12 categories, 135
canonical EN↔ZH pairs**, each row carrying the canonical English, the 规范中文译法, and an explicit
**禁止使用 / Avoid** column — so the assistant knows what *not* to write.

1. Research design & identification strategy
2. Difference-in-Differences (DID / DiD)
3. Regression Discontinuity Design (RDD)
4. Instrumental Variables (IV)
5. Propensity score methods (PSM / IPW)
6. Causal graphs / Structural Causal Models (DAG, SCM)
7. Panel data & fixed effects
8. Standard errors & inference
9. Robustness & placebo
10. Mechanism & heterogeneity
11. Common statistics & model-output terms
12. Paper structure terms

---

## Quick example

**Input (typical literal draft):**

> 本文研究了教育竞争对家庭教育负担的影响。我们使用DID方法来研究这个问题。结果显示教育竞争对家庭负担有显著的正向影响。值得注意的是，这个效应在城镇家庭更明显。

**Block A — Polished version (`TR-ZH2EN`):**

> This paper examines how educational competition affects household educational expenditure. We
> exploit plausibly exogenous variation in a difference-in-differences framework to identify the
> causal effect. A one-standard-deviation increase in educational competition is associated with a
> β-unit increase in household burden (p < 0.01). The effect is concentrated among urban households.

**Block B — Revision notes (excerpt):**

| # | Original | Revised | Rationale |
|---|----------|---------|-----------|
| 1 | 我们使用DID方法来研究这个问题 | We exploit … in a difference-in-differences framework | Journal convention: name the *identification strategy / exogenous variation*, not the "method" |
| 2 | 显著的正向影响 | a β-unit increase … (p < 0.01) | Quantify magnitude; "显著" → statistically significant, reported with coefficient |
| 3 | 值得注意的是 | *(deleted)* | AI-trace: sentence-opening hedge removed; factual content stands alone |
| 4 | 城镇家庭 | urban households | Standard demographic term; "城镇" → *urban* in household-context prose |

**Word choice — intensity-matched alternatives (`word_choice.md §3`):**

| Original | Same-intensity neutral | Lower intensity | Higher intensity (hype — avoid) | Reason |
|----------|------------------------|-----------------|--------------------------------|--------|
| 大幅上升 | rose substantially | rose slightly | skyrocketed | "skyrocketed" adds news drama; "rose substantially" keeps the magnitude without the hype |
| 显著下降 | declined substantially | dipped | plummeted | neutral verb + magnitude word; "plummeted" is rhetorical |

---

## How it works

The skill runs a fixed nine-step pipeline.

| Step | Action | Guard |
|------|--------|-------|
| **1** | Identify task type (`TR-ZH2EN` / `TR-EN2ZH` / `PO-EN`) | — |
| **2** | Classify the segment to pick the right conventions | — |
| **3** | Fact-check causal claims against `causal_facts.md` | Never alters intended meaning; writes a *Substantive Check* row |
| **4** | Apply terminology rules from `terminology.md` | Context-dependent sense resolution (DAG "部分" → *nodes*) |
| **5** | Enforce register & word choice from `word_choice.md` | Offer intensity-matched alternatives with reasons |
| **6** | Produce **Block A** (clean text) + **Block B** (revision table) | Fixed two-block output |
| **7** | Layer journal style from `journal_styles.md` (if named) | — |
| **8** | **AI-trace reflection** as a measured loop | Baseline → rewrite → re-measure; deliver a before/after delta table |
| **9** | **Prosody polish** — final rhythm-and-density gate | Paragraph-level or longer only; English prose only |

### Step 8 — measured, not eyeballed

```bash
python scripts/scan_ai_traces.py manuscript.tex           # structure: punctuation, pegs, templates, long sentences, rhythm
python scripts/scan_register.py manuscript.tex --limit 8  # diction: defect bands and context probes
python scripts/scan_detectability.py manuscript.tex       # detector-facing proxies → risk_index
```

Three rules govern the loop:

1. **Density is the signal, not presence.** `respectively`, `rather than`, and a colon introducing a
   list are legitimate journal prose. Never zero out a probe to make a number look clean.
2. **A falling sentence-length stdev is not by itself success.** Deleting outliers and flattening the
   prose both lower it. Verify rhythm instead: healthy prose keeps *adjacent pairs within ±2 words*
   low and the *≥2× length ratio* high.
3. **The pass is a style pass.** Numbers, equations, citations, and exhibits are out of scope. Apply
   rewrites as exact-match replacements with a `count == 1` check so partial application cannot pass
   silently.

`scan_detectability.py` deserves a caveat that the code itself states: it measures the statistical
proxies commercial AI detectors actually score (burstiness / sentence-length CV%, formulaic density,
self-repetition %, MTLD, hedge density, paragraph-shape CV%) and reports a `risk_index`. It is a
**false-positive-risk diagnostic, not a detector, and is never optimised as a target.** Bands are
era-stratified against a pre-2020 vs 2021+ corpus, which the calibration found statistically
indistinguishable.

### Step 9 — the prosody gate

```bash
python scripts/prosody_check.py BLOCK_A.md
python scripts/prosody_check.py BLOCK_A.md --json > prosody.json
```

**Scope.** Runs only when Block A contains **two or more sentences** after body-prose cleaning, and
only on English prose — so it applies to `PO-EN` and `TR-ZH2EN`, and is skipped for single-sentence
requests and for `TR-EN2ZH` (whose output is Chinese, which an English-phonology checker cannot
measure).

**Exit gate.** No RED-line marker — **SLURRY / POUNDING / ROBOTIC / DENSE / FLAT** — and WARN items
either resolved or explicitly waived with a stated reason (e.g. "one 45-word sentence kept: it
carries a single complex identification argument").

> **A counter-intuitive band, worth knowing.** `cv_words_per_sentence` originally flagged high
> variation as a defect and failed every real top-journal paper (CV 55–88%). The band is flipped:
> variation is now the target (**OK ≥ 50%, RED < 35%**) because it is the same quantity detectors
> call "burstiness" — high variance reads as human on both gates. Related adjustments:
> `p95_words_per_sentence` is RED only above **95**, and `mean_words_per_sentence` sits at **22–35**.
> The exact thresholds are authoritative in `scripts/prosody_check.py`, not in the prose.

---

## Installation

This is a plain `SKILL.md` bundle: a directory containing `SKILL.md` plus `references/` and
`scripts/`. Any agent that discovers skills from a directory tree can use it.

**DeepSeek Harness (DSH)** — user level, available in every workspace:

```powershell
# copy the bundle to the DSH user skill root
Copy-Item -Recurse top-journal-polish "$env:USERPROFILE\.dsh\skills\"
```

Project level: place it under `<project>/.dsh/skills/`.

Verify the bundle registered by checking that `SKILL.md` sits one level below the scan root:

```powershell
Test-Path "$env:USERPROFILE\.dsh\skills\top-journal-polish\SKILL.md"   # → True
```

**Other agents** use the same layout under their own root: `~/.claude/skills/` (Claude Code),
`~/.agents/skills/` (Codex), `~/.workbuddy/skills/` (WorkBuddy), and so on.

The skill activates when you paste text and ask for translation, polish, or rewriting, or when you
name a target journal.

---

## Usage

Trigger the skill with natural language:

- *"把这段摘要翻译成 AER 风格英文"*
- *"Polish this introduction for QJE"*
- *"润色这段实证结果，去掉 AI 痕迹"*
- *"Translate this paragraph back to Chinese for review"*

Common trigger phrases: `翻译`, `润色`, `polish`, `translate`, `顶刊写作`, `改写`, `学术英语`,
`摘要修改`, `引言润色`, plus any named journal (AER / QJE / MS / JFE / …).

---

## Project structure

```
top-journal-polish/
├── SKILL.md                      # 9-step workflow, quality standards, anti-patterns, checklists
├── README.md                     # this file
├── CHANGELOG.md                  # Keep-a-Changelog history, incl. design notes and caveats
├── LICENSE                       # MIT
├── references/
│   ├── terminology.md            # 12-category, 135-pair EN↔ZH canonical dictionary
│   ├── causal_facts.md           # Self-contained causal-inference fact reference
│   ├── word_choice.md            # Register control + intensity-spectrum synonym ladders
│   ├── journal_styles.md         # Per-journal voice, structure, prohibited patterns (8 outlets)
│   ├── anti_ai_trace_audit.md    # Step 8 method: measured loop, thresholds, proxies, pitfalls
│   └── prosody_target_card.md    # Step 9 method: bands, red-line markers, adjust-and-re-run loop
└── scripts/
    ├── scan_ai_traces.py         # Structure probes: punctuation, pegs, templates, rhythm
    ├── scan_register.py          # Diction probes: defect bands + context bands
    ├── scan_detectability.py     # Detector-facing proxy diagnostic → risk_index
    └── prosody_check.py          # Step 9 rhythm-and-density gate
```

### Script reference

All four scripts are **standard library only**, read-only, with no network access and no
subprocess. Input accepts `.tex` (preamble, floats, tables and display maths stripped), `.md` (code
fences and tables stripped), and plain text; `-` reads stdin. `--json` emits machine-readable output.

| Script | Signature | What it reports |
|--------|-----------|-----------------|
| `scan_ai_traces.py` | `<file> [--lang en\|zh] [--long 45] [--json]` | Punctuation traces, transition-peg density, repeated syntactic templates, long-sentence load, sentence-length rhythm |
| `scan_register.py` | `<file> [--lang en\|zh] [--limit 6] [--json]` | *Defect* bands (hype, ornate, assertive filler, over-assertive verbs, AI emphasis adverbs, wordy nominalisation) and *context* bands (self-narration, vague intensifier, precision claim, vague quantifier, repeated contrast frame) |
| `scan_detectability.py` | `<file> [--json] [--text "..."] [selftest]` | Burstiness (sentence-length CV%), formulaic density, self-repetition %, MTLD, hedge density, paragraph-shape CV%, `risk_index` |
| `prosody_check.py` | `<file> [--json] [--text "..."] [selftest]` | nPVI, %stressed, alternation rate, inter-stress CV, syllables/word, sentence-length stats, parallelism density, red-line markers |

Both `scan_detectability.py` and `prosody_check.py` ship calibration-lock self-tests (30 and 24
assertions respectively) so a threshold edit cannot drift silently:

```bash
python scripts/scan_detectability.py selftest
python scripts/prosody_check.py selftest
```

**Language handling.** English is measured in words; Chinese is measured in characters (CJK
ideographs plus Latin tokens), and the long-sentence default rises from 45 words to 60 characters,
because word-counting a CJK sentence counts clauses rather than length. Citation commands are
replaced by a capitalised placeholder before sentence segmentation — unwrapping them to bare author
keys leaves a lower-case token at a sentence start, which defeats the splitter and manufactures
phantom long sentences.

**Known limitation.** Display equations and float bodies are stripped before segmentation, so a
sentence ending immediately before a display and the one beginning immediately after it can be
measured as a single sentence. Boundary artefacts must be discounted by hand.

---

## Customization

- **Add a journal**: append a `[XXX]` section to `references/journal_styles.md` following the
  existing template (signature features → stylistic markers → sentence structure → prohibited
  patterns). Step 7 picks up a section added this way automatically.
- **Extend terminology**: add rows to the relevant category in `references/terminology.md`; always
  fill the *avoid* column so the assistant knows the deprecated variants.
- **Extend word choice**: add words or spectra to `references/word_choice.md` §2–§3; keep the neutral
  band as the middle column and preserve the low→high intensity order.
- **Retune the gates**: edit the band tables in `scripts/prosody_check.py` and
  `scripts/scan_detectability.py`, then update the matching self-test assertions — the self-tests are
  what make a retune deliberate rather than accidental.
- **Tighten the AI-trace pass**: edit the English / Chinese checklists in `SKILL.md` Step 8 to match
  your own writing voice.

---

## Quality standards enforced

- **Zero Chinglish** — no SVO inversion, over-nominalization, or literal conjunction translation.
- **Calibrated hedging** — *consistent with* / *suggests* / *provides evidence that* / *establishes*,
  matched to evidence strength.
- **Identification language** — descriptive ("is associated with") vs causal ("increases") is never
  confused; causal language appears only when the design supports it.
- **Significance ≠ importance** — statistical significance is separated from economic magnitude.
- **Neutral register** — no literary ornament and no journalistic hype; substitutions stay within the
  same intensity band.
- **Readable rhythm** — no RED-line prosody marker survives delivery.

---

## Disclaimer

This skill improves writing and terminology; it does **not** constitute methodological advice and
does not guarantee acceptance at any journal. The detector-facing metrics in Step 8 are a diagnostic
of *false-positive risk*, not evidence that text is or is not machine-written, and they must not be
optimised as a target. The author remains responsible for the substance, identification strategy, and
correctness of their work.

---

## License

Released under the [MIT License](LICENSE). Free to use, modify, and redistribute.
