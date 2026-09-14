# top-journal-polish

### Publication-grade academic translation & writing polish for economics, management, and quantitative social science

> Bilingual (中文 ↔ English) translation and English-only revision aligned with the editorial
> conventions of **AER, QJE, JPE, Econometrica, Management Science, JFE, JEEA, REStud, JRS**
> and comparable SSCI outlets. Built for empirical economists, applied econometricians, and
> quantitative social scientists who want their prose to read like it already cleared desk review.

---

![Journals](https://img.shields.io/badge/journals-10%20top%20SSCI-blue)
![Terminology](https://img.shields.io/badge/terminology-12%20categories%20%C2%B7%20150%2B%20terms-9c27b0)
![Languages](https://img.shields.io/badge/languages-中文%20%C2%B7%20English-brightgreen)
![Workflow](https://img.shields.io/badge/workflow-7--step%20pipeline-orange)
![License](https://img.shields.io/badge/license-MIT-green)

---

## What it does

`top-journal-polish` turns rough drafts, Chinglish, and literal translations into disciplinary,
journal-ready prose. It does **not** simply paraphrase. It enforces a strict pipeline that:

1. **Classifies the text segment** (abstract, introduction, identification, results, robustness,
   mechanism, conclusion, …) and applies segment-specific rules.
2. **Fact-checks causal-inference claims** against canonical textbooks before touching wording —
   a translation that is fluent but wrong is worse than one that is clumsy but correct.
3. **Normalizes terminology** to the internationally standardized forms (e.g. *parallel trends
   assumption*, not *parallel trend hypothesis*; *instrumental variables (IV) estimation*, not
   *instrumental variable method*).
4. **Adapts to a named target journal** (AER voice ≠ QJE voice ≠ Econometrica voice).
5. **Strips AI-generated tells** — em-dash overuse, "It is worth noting that", "In particular,"
   every paragraph, mechanical parallelism — so the output does not read like a model wrote it.

The skill ships with two reference files: a **150+ term bilingual terminology dictionary** and a
**per-journal style guide** covering ten outlets.

---

## Why this skill exists

Most "polish" tools and prompts do one of two things badly:

- They **translate literally**, producing textbook-idiosyncratic or China-domestic-journal variants
  ("鉴别方法" → *identification method* instead of *identification strategy*; "工具变量法" →
  *instrumental variable method* instead of *instrumental variables (IV) estimation*).
- They **smooth prose without checking substance**, leaving factually incorrect causal claims
  (calling a collider a mediator, asserting SUTVA holds under clear interference) intact and polished.

This skill treats terminology as a correctness problem, not a style problem, and treats causal
claims as something to verify before rewriting. The result is text a referee is less likely to flag
on first read.

---

## Features

| Feature | What you get |
|---------|--------------|
| **Three task modes** | `TR-ZH2EN` (中文→英文), `TR-EN2ZH` (英文→中文技术回译), `PO-EN` (英文-only polish) |
| **Segment-aware rules** | Abstract, Introduction, Literature, Theory, Empirical/Identification, Results, Robustness, Mechanism, Conclusion each get their own conventions |
| **Causal-inference fact-check** | Claims cross-referenced against *Causal Inference: What If*, *The Mixtape*, Imbens & Rubin, Angrist & Pischke, Wooldridge before revision |
| **Canonical terminology** | 12 categories, 150+ EN↔ZH pairs with explicit *avoid* columns |
| **Journal-specific voice** | 10 outlets with signature tone, abstract length, hedge hierarchy, and prohibited patterns |
| **AI-trace reflection** | A dedicated pass that removes LLM-typical constructions in both English and Chinese |
| **Transparent revisions** | Every change is logged with a rationale (terminology / logic / journal convention / causal language) |
| **Equation & citation safety** | Mathematical content never altered; missing citations flagged with `[CITE?]` |

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
| `[JRS]` | Journal of Rural Studies | Interdisciplinary, China-context friendly, accessible prose |
| `—` | General top-journal standard | Applied when no journal is named |

---

## Terminology coverage

The bundled `references/terminology.md` is the backbone of correctness. It covers:

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

Each entry gives the **canonical English**, the **规范中文译法**, and an explicit **禁止使用 / Avoid**
column — so the assistant knows what *not* to write.

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

---

## How it works

The skill runs a fixed pipeline:

1. **Identify task type** — `TR-ZH2EN` / `TR-EN2ZH` / `PO-EN`; load journal rules if a target is named.
2. **Classify the segment** — abstract, introduction, results, etc., to pick the right conventions.
3. **Fact-check causal claims** — verify mediators/confounders/colliders, identifying assumptions,
   and SUTVA against authoritative sources; flag errors in the revision notes.
4. **Apply terminology rules** — resolve ambiguous words to their discipline-specific equivalent
   (e.g. in a DAG context, "部分" → *nodes*, "路径" → *paths*).
5. **Produce output** — always two blocks: **Block A (clean final text)** + **Block B (revision table)**.
6. **Journal-specific adaptation** — layer outlet style on top of general standards.
7. **AI-trace reflection** — scan and remove LLM-typical patterns before delivery.

---

## Installation (WorkBuddy)

This is a [WorkBuddy](https://www.workbuddy.cn) skill. Place the folder so the agent can load it:

**User-level** (available in every project):

```bash
git clone https://github.com/<your-org>/top-journal-polish.git \
  ~/.workbuddy/skills/top-journal-polish
```

**Project-level** (shared with a team via the repo):

```bash
cp -r top-journal-polish <your-project>/.workbuddy/skills/
```

Or install it from the WorkBuddy skill marketplace if published there. After install, the skill
activates automatically when you paste text and ask for translation, polish, or rewriting, or when
you name a target journal.

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
├── SKILL.md                      # Workflow, quality standards, anti-patterns
├── references/
│   ├── terminology.md           # 12-category EN↔ZH canonical dictionary
│   └── journal_styles.md        # Per-journal voice, structure, prohibited patterns
└── README.md
```

---

## Customization

- **Add a journal**: append a `[XXX]` section to `references/journal_styles.md` following the
  existing template (signature features → stylistic markers → sentence structure → prohibited patterns).
- **Extend terminology**: add rows to the relevant category in `references/terminology.md`; always
  fill the *avoid* column so the assistant knows deprecated variants.
- **Tighten the AI-trace pass**: edit the English / Chinese checklists in `SKILL.md` Step 7 to match
  your own writing voice.

---

## Quality standards enforced

- **Zero Chinglish** — no SVO inversion, over-nominalization, or literal conjunction translation.
- **Calibrated hedging** — *consistent with* / *suggests* / *provides evidence that* / *establishes*,
  matched to evidence strength.
- **Identification language** — descriptive ("is associated with") vs causal ("increases") is never
  confused; causal language appears only when the design supports it.
- **Significance ≠ importance** — statistical significance is separated from economic magnitude.

---

## Disclaimer

This skill improves writing and terminology; it does **not** constitute methodological advice and
does not guarantee acceptance at any journal. The author remains responsible for the substance,
identification strategy, and correctness of their work.

---

## License

Released under the [MIT License](LICENSE). Free to use, modify, and redistribute.

---

*If this skill saved you a round of reviewer comments, consider giving it a star — and open an issue
or PR to extend the terminology table or add your target journal.*
