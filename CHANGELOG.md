# Changelog

All notable changes to this skill are recorded here.
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

### Added
- `references/anti_ai_trace_audit.md` — the Step 8 method as a **measured loop**
  (baseline → triage → rewrite → re-measure → verify rhythm). Includes the
  threshold and target-band table, the trace-to-fix mapping, an eight-point
  pitfall list, the delta-table deliverable format, and a generic worked
  example.
- `scripts/scan_ai_traces.py` — structural probes: punctuation traces,
  transition-peg density, repeated syntactic templates, long-sentence load
  (`>45`/`>60` English words), and sentence-length rhythm (`within ±2 words`,
  `≥2× length ratio`, longest same-length run, length histogram).
- `scripts/scan_register.py` — diction probes split into **defect** bands
  (hype/journalistic, ornate/literary, assertive filler, over-assertive verbs,
  AI emphasis adverbs, wordy nominalisation) and **context** bands
  (self-narration, vague intensifier, precision claim, vague quantifier,
  repeated contrast frame).
- `scripts/prosody_check.py` — Step 9 rhythm-and-density gate: nPVI, %stressed,
  alternation rate, inter-stress CV, syllables/word, sentence-length stats, and
  parallelism density, plus sentence-level red-line markers
  (SLURRY / POUNDING / ROBOTIC / DENSE / FLAT). Standard library only.
- `references/prosody_target_card.md` — Step 9 method: the rhythm-and-density
  target card (bands, red-line markers, the adjust-and-re-run loop) and its
  caveats. Thresholds **re-validated on a 9-paper era-stratified corpus** (4
  pre-2020 + 5 papers 2021+; the two eras are statistically indistinguishable on
  every metric).
- `scripts/scan_detectability.py` — **new** Step 8 detector-facing false-positive-risk
  scanner. Measures six published statistical proxies that commercial AI detectors
  actually score (burstiness / sentence-length CV%, formulaic density,
  self-repetition %, MTLD, hedge density, paragraph-shape CV%) and reports a
  `risk_index`. Bands are era-stratified (pre-2020 vs 2021+ corpus). The script
  carries an explicit **honesty boundary: a diagnostic, not a detector; never
  optimised as a target**. 30 self-test assertions.

### Changed
- Step 8 now opens with the programmatic pre-scan: run both scanners, take a
  baseline **before** editing, re-measure afterwards, and deliver a
  before/after delta table. Three governing rules added: density is the signal
  rather than presence; a falling sentence-length stdev is not by itself
  success; the pass is a style pass and must not touch content.
- `### Reference Files` now lists `references/anti_ai_trace_audit.md`, and a new
  `## Scripts` section documents all three tools.
- `references/anti_ai_trace_audit.md` gains **§3b Detector-facing proxies** with the
  proxy table, the five-point honesty boundary, and the era-stratified calibration
  table (OLD vs NEW medians). The Step 8 baseline now runs all three scanners and
  the §6 delta table adds the detector-proxy rows.
- **Prosody card correction (Step 9):** `cv_words_per_sentence` was rewarding
  uniformity and flagging every real top-journal paper (CV 55–88%) as WARN. The
  band is flipped to reward variation (**OK ≥ 50%, RED < 35%**) — it is the same
  quantity detectors call "burstiness", so high CV is now the human-like target on
  both gates. `p95_words_per_sentence` loosened (RED only > 95, was > 60) and
  `mean_words_per_sentence` widened to 22–35. Calibration-lock assertions added to
  `prosody_check.py` (24/24) and `scan_detectability.py` (30/30) selftests.
- README: Features table gains a *Measured anti-AI audit* row; Project structure
  updated.
- New **Step 9 — Prosody Polish**: runs after Step 8 (AI-trace reflection) and
  before delivery as the final quantitative rhythm-and-density gate. Scoped to
  **paragraph-level or longer** tasks only (skipped for single-sentence requests
  and for `TR-EN2ZH`, since the checker measures English phonology).

### Design notes
- Both scripts are standard library only, read-only, with no network access and
  no subprocess. Input accepts `.tex` (preamble, floats, tables, and display
  maths stripped), `.md` (code fences and tables stripped), and plain text;
  `-` reads stdin. `--json` emits machine-readable output.
- English and Chinese are both supported. Latin prose is measured in words;
  Chinese prose is measured in characters (CJK ideographs plus Latin tokens),
  and the long-sentence default rises from 45 words to 60 characters, because
  word-counting a CJK sentence counts clauses rather than length.
- Citation commands are replaced by a **capitalised** placeholder before
  sentence segmentation. Unwrapping them to bare author keys leaves a
  lower-case token at the start of a sentence, which defeats the splitter and
  manufactures phantom long sentences.
- Known limitation, documented in the reference: display equations and float
  bodies are stripped before segmentation, so a sentence ending immediately
  before a display and the one beginning immediately after it can be measured
  as a single sentence. Boundary artefacts must be discounted by hand.
