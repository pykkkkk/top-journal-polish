# Prosody Target Card — the final rhythm-and-density gate for top-journal prose

This card defines the **target rhythm-and-density bands** that the final prosody check
(`scripts/prosody_check.py`) measures a draft against. It is the quantitative gate that runs
**as Step 9 of the polish workflow**, after the AI-trace reflection (Step 8) and before delivery.
Its job is to catch low reading comfort from rhythm and density that the terminology, register, and
AI-trace passes cannot see.

> The bands below are **not** a "native-speaker accent." They describe the shared, copy-edited
> register of leading econ / management journals, estimated from a 7-paper top-5 corpus study and
> **re-validated on a 9-paper era-stratified corpus** (4 pre-2020 + 5 papers 2021+; statistically indistinguishable)
> (4 China-led + 3 native-led papers; empirical shared intervals). Editorial copy-editing
> flattens most author-level rhythm fingerprints, so the actionable target is *alignment with
> the shared top-journal register*, not imitation of any one group.

## How the metrics are computed

Text only, no audio. Syllable stress is estimated with a small lexicon + first-syllable heuristic
(accurate stress needs CMUdict or acoustic data — see caveats). Metrics rest on speech-rhythm
theory:

- **nPVI** — normalised pairwise variability index of stressed/unstressed durations
  (Grabe & Low 2002). Higher = stronger stress-timed contrast.
- **% stressed** — share of stressed syllables (Ramus 1999 vowel-share analogy; natural English ≈ 35–45%).
- **alternation rate** — share of adjacent 0/1 flips in the stress sequence (~50% natural; >78% mechanical).
- **inter-stress CV** — coefficient of variation of gaps between stressed syllables (Dellwo 2006 Varco).
- **syllables / word, and its CV** — lexical weight and lexical-variation proxies.
- **mean / p95 / CV of words per sentence** — syntactic density and rhythm variation.
- **parallel per 100 words** — density of `and/but/or/;` (parallel-structure load).

## The target card

| Dimension | Comfort target band | Red line (triggers marker) | Why it matters |
|---|---|---|---|
| nPVI (stress contrast) | **35–45** | `< 15` → FLAT | monotone feel when too low |
| % stressed syllables | 36–42% | — | balance of content vs function load |
| alternation rate | 50–65% | `> 78%` → ROBOTIC | mechanical beat when too regular |
| inter-stress CV | 45–70% | — | varied spacing reads less monotonous |
| mean syllables / word | 1.6–1.9 | `> 2.0` → over-Latinate | heavy words tire the reader |
| **mean words / sentence** | **22–35** | `> 45` → DENSE | working-memory load; top journals run ≈ 30–35 |
| p95 words / sentence | ≤ 75 | `> 95` | one long sentence is fine; only an extreme 95th percentile is bloat |
| CV of words / sentence | **≥ 50% (higher is better)** | `< 35%` → monotone | visible length variation aids parsing AND is what detectors read as human; same quantity detectors call "burstiness" — reward variation, not uniformity |
| parallelism per 100 words | 2.5–4.5 | `> 6` → gunfire | thin out chained connectives |

The `scripts/prosody_check.py` `TARGET_CARD` dictionary holds the exact numeric thresholds; treat
that file as authoritative if this table and the code ever drift.

## Red-line markers (sentence-level)

These are computed from the stress run-lengths, not just the aggregate bands, and they **name the
offending sentence** so the author can fix it:

1. **SLURRY** — a sentence with a run of ≥ 8 unstressed syllables (typically `of/for/in/the` +
   relative clauses stacked). *Fix:* split the sentence or switch to active voice.
2. **POUNDING** — a run of ≥ 5 stressed syllables (piled monosyllabic content words, e.g.
   "firm bank loan risk drop"). *Fix:* insert a weak syllable or a connective.
3. **ROBOTIC** — alternation > 78% *and* inter-stress CV < 35% (a metronomic beat). *Fix:* break the
   pattern with one longer or parallel sentence.
4. **DENSE** — mean sentence length > 40 words. *Fix:* split the longest sentences.
5. **FLAT** — nPVI < 15. *Fix:* mix short and long stressed/unstressed units; avoid monotone listing.

## Using the card in the workflow (Step 9)

1. Run `python scripts/prosody_check.py BLOCK_A.md` (or `--json` for machine-readable output). For a
   `.tex` source, extract the body prose first or paste Block A into a `.md` / `.txt` file; the checker
   strips headings, tables, citations `(Author, Year)`, equations, and code fences.
2. Read the verdict: each metric shows its value against the band (OK / WARN / RED); any triggered
   marker names the sentence that caused it.
3. **Adjust, then re-run.** This is a loop, not a one-shot: split the flagged sentence, insert a short
   one to break a monotone run, vary opener rhythm to break ROBOTIC alternation, or swap a Latinate
   noun for a shorter word. Re-run until no RED marker remains and WARN count is low.
4. Only then deliver Block A and Block B, and note in the Revision Notes that the prosody gate was run.

## Caveats (carried from the corpus study)

- **Heuristic stress.** The lexicon + first-syllable rule mis-estimates multi-syllable and Latinate
  words; a production tool should use CMUdict (nltk) or acoustic data.
- **"Comfort" is not yet calibrated.** These metrics measure rhythm contrast / regularity — one facet
  of reading comfort, not a validated psychometric. Do not maximise a single number; act on the
  diagnostic signals.
- **Sample.** The shared bands were first estimated from a 7-paper top-5 corpus (4 China-led + 3
  native-led) and **re-validated on a 9-paper era-stratified corpus** (4 pre-2020 + 5 papers 2021+;
  see `scan_detectability.py`'s calibration note). The two eras are statistically indistinguishable on
  every metric, which anchors the bands against the worry that 2021+ literature is AI-contaminated.
  Treat the bands as a strong prior, not a fixed law; widen the sample before trusting fine thresholds.
- **`cv_words_per_sentence` was corrected to reward variation, not uniformity.** It measures the *same
  quantity* detectors call "burstiness" — high CV = varied sentence length = human-like; low CV =
  flat, templated rhythm that is both hard to read and what AI detectors flag. Real top-journal prose
  spans ~55–88%; the band is OK ≥ 50%, RED < 35%. A draft that drops CV toward uniformity to "look
  tidy" would *raise* its detector false-positive risk.
