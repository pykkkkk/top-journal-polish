# Canonical Causal-Inference Facts
# Self-contained reference for the Step 3 fact-check

This file lists well-established causal-inference facts used to verify the substantive
correctness of claims in the user's text. It is **fully self-contained**: it replaces any
external textbook, connector, or private knowledge base. When Step 3 finds a claim that
contradicts an entry below, it is flagged in Block B as a Substantive Check correction,
citing the relevant section (e.g. `causal_facts.md §2`).

Entries reflect the consensus of the standard literature (Rubin, Pearl, Hernán & Robins,
Imbens & Angrist, Cunningham, Wooldridge). They state what is *correct*; the error patterns
in §6 tell you what to flag.

---

## 1. Potential Outcomes & Treatment Effects

- **Potential outcomes**: For unit *i*, `Y_i(1)` and `Y_i(0)` are the outcomes under treatment
  and control. The unit-level effect is `Y_i(1) − Y_i(0)`; only one is ever observed (the
  fundamental problem of causal inference).
- **ATE** — Average Treatment Effect: `E[Y(1) − Y(0)]` over the whole population.
- **ATT** — effect on the treated: `E[Y(1) − Y(0) | T = 1]`.
- **ATU / ATC** — effect on the untreated/controls: `E[Y(1) − Y(0) | T = 0]`.
- **ITT** — Intention-to-Treat: effect of *assignment* to treatment, not of treatment received.
  With imperfect compliance, ITT ≠ effect of the treatment itself; the gap is explained by compliance.
- **LATE / CACE** — Local Average Treatment Effect = Complier Average Causal Effect (Angrist–Imbens):
  the effect for **compliers** (units whose treatment status responds to the instrument). It is
  **not** the ATE and does not generalize to never-takers or always-takers.
- **SUTVA** — Stable Unit Treatment Value Assumption: (i) no **interference** between units (one
  unit's treatment does not affect another's outcome); (ii) no **multiple versions** of treatment.
  SUTVA is **violated** under spillovers, network effects, general equilibrium effects, or when
  the treatment intensity assigned to one unit depends on others' assignments.

---

## 2. Causal Graph Primitives (DAGs)

- **Confounder** — a common cause of both treatment `T` and outcome `Y`. It opens a backdoor path
  `T ← X → Y` and **must** be adjusted for to identify the effect.
- **Mediator** — lies *on* the causal path `T → M → Y`. Controlling for a mediator when estimating
  the **total** effect blocks part of the effect (you recover only the direct effect). Control for
  it only in a deliberate mechanism/mediation analysis, never when the goal is the total effect.
- **Collider** — a common *effect* of two variables (e.g. `T → C ← Y`). Conditioning on a collider
  **opens** a non-causal association between its parents (collider bias / Berkson's paradox).
  **Do not control for colliders.** Mistaking a collider for a mediator (or vice versa) is a common error.
- **Backdoor criterion** — a set `Z` satisfies it if (a) no node in `Z` is a descendant of `T`, and
  (b) `Z` blocks every path between `T` and `Y` that contains an arrow into `T`. Adjusting for such a
  `Z` identifies the effect under unconfoundedness.
- **Front-door criterion** — usable when an unobserved confounder blocks `T → Y` but a mediator `M`
  intercepts all directed paths from `T` to `Y`: requires (i) `M` intercepts all directed paths
  `T → Y`; (ii) no unblocked backdoor from `T` to `M`; (iii) all backdoor paths from `M` to `Y`
  blocked by `T`.
- **d-separation** — two nodes are d-separated by a set `Z` if all paths are blocked; d-separated
  nodes are conditionally independent given `Z`.

---

## 3. Identification Strategies — Core Assumptions

### Difference-in-Differences (DID / DiD)
- **Parallel trends assumption** (not a "hypothesis"): in the absence of treatment, the outcome
  difference between treated and control would have remained constant over time. It is an
  *assumption*, not directly testable; **pre-trends** are supporting evidence, not the assumption itself.
- Requires: no **anticipation** of treatment; no **concurrent** policies affecting one group; stable
  composition. In **staggered adoption**, naive TWFE can produce **negative weights** and be biased
  under heterogeneous effects — prefer Callaway–Sant'Anna, Sun–Abraham, or de Chaisemartin–D'Haultfœuille.

### Regression Discontinuity (RDD)
- **Continuity**: the conditional expectation of the potential outcomes is continuous in the running
  variable at the cutoff. The jump in the observed outcome is the treatment effect.
- **No manipulation** of the running variable (test via McCrary density test); the cutoff must not be
  manipulable. The estimate is **local** to the cutoff (sharp RDD) or local intent (fuzzy RDD).
- Fuzzy RDD requires the instrument-like relevance of the cutoff for treatment receipt.

### Instrumental Variables (IV / 2SLS)
- **Relevance**: the instrument affects the treatment (strong first stage; rule-of-thumb F > 10).
  Weak instruments bias 2SLS toward the OLS / reduced-form and inflate Type I error.
- **Exclusion restriction**: the instrument affects the outcome **only** through the treatment.
  (Distinct from "relevance"; confounding the two is a frequent error.)
- **Monotonicity**: the instrument increases treatment probability for everyone (or no one) — required
  to interpret the estimate as a LATE for compliers.
- 2SLS recovers LATE under these; overidentification tests (Sargan–Hansen) check instrument validity.

### Matching / PSM / IPW
- Requires **conditional independence** (ignorability) given observed `X`, and **common support**.
- PSM / nearest-neighbor / kernel matching estimate **ATT**, not ATE, unless properly generalized.
- Balance on covariates is a *requirement*, not a guarantee of identification (unobserved confounders remain).

### Panel FE / TWFE
- Fixed effects absorb **time-invariant** confounders; identification comes from **within** variation.
- Valid only if the within variation is **exogenous** (no time-varying confounders, no feedback).
- Staggered adoption needs the heterogeneous-effects-robust estimators noted under DID.

---

## 4. Effect Interpretation & Language

- Report the **effect type** actually identified (ATE vs ATT vs LATE vs ITT). Do not present a LATE as
  if it were the ATE.
- **Statistical significance ≠ economic magnitude.** A "significant" coefficient with no reported size
  is incomplete; always pair significance with a coefficient / elasticity / SD-change.
- Use **causal language** ("increases", "reduces") only when an identification strategy supports it.
  Otherwise use **descriptive** language ("is associated with", "predicts").
- Heterogeneous / subgroup effects describe *where* the effect differs; they are not a mechanism unless
  a channel is explicitly established.

---

## 5. Inference Caveats

- **Clustered standard errors** when observations are correlated within groups (individuals over time,
  firms within industry, regions).
- **Heteroskedasticity-robust** SEs unless homoskedasticity is justified.
- **Multiple testing**: control the false discovery rate (FDR / Benjamini–Hochberg) or family-wise error
  rate (FWER / Bonferroni, Holm) when testing many hypotheses.
- **Placebo / falsification**: under a valid identification strategy, a placebo outcome (or fake
  treatment timing) should show **no** effect. A non-null placebo is evidence against identification.

---

## 6. Common Factual Errors to Flag

Flag a claim in Block B when it commits any of the following:

| # | Error | Correct principle (see §) |
|---|-------|----------------------------|
| 1 | Calling a **collider** a mediator, or controlling for a collider | §2 |
| 2 | Controlling for a **mediator** when the total effect is intended | §2 |
| 3 | Asserting **SUTVA holds** when interference / spillovers are clearly present | §1 |
| 4 | "**Parallel trend hypothesis**" — should be *parallel trends assumption*; pre-trends are not the assumption | §3 DID |
| 5 | Appealing to an **IV** whose exclusion restriction is implausible, or confusing exclusion with relevance | §3 IV |
| 6 | Reporting a **LATE** as if it were the ATE | §1, §4 |
| 7 | Using **causal verbs** ("causes / increases") without an identification strategy | §4 |
| 8 | Treating a **significant** coefficient as informative without magnitude | §4 |
| 9 | Ignoring **reverse causality / omitted-variable / selection bias** in an observational claim | §2, §3 |
| 10 | Asserting RDD validity without addressing **running-variable manipulation** | §3 RDD |
| 11 | Equating **correlation with causation** in the absence of a design | §2, §4 |
| 12 | Conflating **ITT** with the effect of treatment received under imperfect compliance | §1 |
