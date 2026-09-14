---
name: top-journal-polish
description: >
  Top-journal academic translation and writing polish for economics, management,
  and quantitative social science. Targets AER, QJE, JPE, Econometrica, MS, JFE,
  RFS, JEEA, REStud and comparable SSCI outlets. Handles Chinese-to-English and
  English-to-Chinese translation with strict causal-inference / econometrics
  terminology, and polishes abstracts, introductions, empirical-results
  sections, robustness checks, mechanism analyses, and conclusions to match
  top-journal editorial conventions. Trigger phrases include: 翻译, 润色, polish,
  translate, AER/QJE/MS writing, 顶刊改写, 学术英语, 实证写作, 摘要修改, 引言润色, etc.
agent_created: true
---

# Top-Journal Academic Translation & Polish

## Purpose

Provide publication-grade translation and writing polish aligned with the editorial conventions of
AER, QJE, JPE, Econometrica, Management Science, JFE, RFS, JEEA, and REStud.
Covers Chinese ↔ English translation and English-only polish for empirical economics,
theoretical modeling, applied econometrics, and quantitative social-science manuscripts.

---

## Trigger Conditions

Load this skill when the user:
- Pastes Chinese or English text and asks for translation, polish, rewriting, or proofreading
- Mentions a target journal (AER, QJE, MS, JFE, etc.)
- Asks about academic phrasing, sentence structure, or terminology for economics / management papers
- Uses phrases such as 润色, 翻译, polish, translate, 顶刊写作, 改写, 学术英语

---

## Workflow

### Step 1 — Identify Task Type

Determine which of the three task types applies:

| Code | Task | Description |
|------|------|-------------|
| `TR-ZH2EN` | Chinese → English translation | Full translation with terminology alignment |
| `TR-EN2ZH` | English → Chinese translation | Technical back-translation for review purposes |
| `PO-EN` | English polish only | Style, logic, and terminology improvement |

If the user specifies a **target journal**, activate the journal-specific style rules in
`references/journal_styles.md` for that outlet.

---

### Step 2 — Classify Text Segment

Before polishing, classify the pasted segment:

- **Abstract** → dense, structured, 4–6 sentences: motivation / gap / method / main finding / implication
- **Introduction** → inverted-pyramid narrative; establish fact, identify gap, preview contribution, roadmap
- **Literature Review** → tight citation-linked comparisons; avoid long summaries
- **Theoretical Framework** → formal, compact; every assumption stated; notation consistent with standard field usage
- **Empirical Specification / Identification** → explicit identification strategy, data description, estimation equation
- **Results** → coefficient-centered; significance only when economically meaningful; avoid "significant at 5%"-only claims
- **Robustness / Placebo** → structured list of threats and responses; parallel construction
- **Mechanism / Heterogeneity** → causal channel logic; avoid "suggest" when evidence is direct
- **Conclusion** → mirror introduction; no new citations; policy implications scoped correctly
- **Other** → apply general top-journal prose standards

Load `references/terminology.md` for all task types.

---

### Step 3 — Fact-Check Claims Against Causal Inference Expertise

Before applying terminology rules, verify the substantive correctness of the text's causal-inference claims. A translation or polish that is terminologically accurate but factually incorrect can mislead readers and undermine credibility.

**Procedure:**

1. **Identify the causal claim(s)** — Extract the core causal statements from the user's text (e.g., "X causes Y", "Z is a mediator/confounder/collider", "the identifying assumption is ...", "SUTVA is violated because ...").

2. **Cross-reference with authoritative sources** — Search the user's IMA knowledge base (`kb_id: "001a5fbec780168a"`, title: "ZephyrLiuX的知识库") using the `mcp__ima-mcp__search_knowledge` tool to verify the claim. When needed, fetch specific pages from the following textbooks in the knowledge base:

   | Textbook | File ID | Primary Use |
   |----------|---------|-------------|
   | Hernán & Robins — *Causal Inference: What If* (hernanrobins_WhatIf_26apr24.pdf) | pdf_d11a5947f51fe97cda47c5c9ed79bc19_a90214f7313c349a1949dae56b4ef976001a5fbec780168a | DAGs, identification, mediation, causal diagram, collider, SUTVA |
   | Cunningham — *Causal Inference: The Mixtape* (Causal_Inference_TheMixtape.pdf) | pdf_d11a5947f51fe97cda47c5c9ed79bc19_f6690e77e2805714d2a8ac533af85c07001a5fbec780168a | DID, RDD, IV, matching, causal intuition |
   | Imbens & Rubin — *Causal Inference for Statistics, Social, and Biomedical Sciences* (Guido W. Imbens, Donald B. Rubin - Causal Inference ... .pdf) | pdf_d11a5947f51fe97cda47c5c9ed79bc19_754c44f86abe25debd972883b2b2be17001a5fbec780168a | Potential outcomes framework, assignment mechanisms |
   | Angrist & Pischke — *基本无害的计量经济学：实证研究指南* (基本无害的计量经济学：实证研究指南.pdf) | pdf_d11a5947f51fe97cda47c5c9ed79bc19_6daefc3510fa44b965898b3977bbd5d8001a5fbec780168a | Quasi-experimental designs, identification strategies |
   | Wooldridge — *Econometric Analysis of Cross Section and Panel Data* (Wooldridge - Cross-section and Panel Data.pdf) | pdf_d11a5947f51fe97cda47c5c9ed79bc19_e18fb47da9efb82a373982cc38d58ee9001a5fbec780168a | Panel data methods, endogeneity, selection |

3. **Add a "Substantive Check" row to Block B** — If the user's text contains a factual error or a misleading causal claim, add a row to the Revision Notes table with the following format:

   ```
   # | 用户原文 | [Corrected text] | Substantive Check: [Textbook name] states that [correct claim]. The user's statement [what was wrong]. [Corrected to ...]. |
   ```

   If the claim is correct, include a brief verification note (e.g., "Substantive Check: Confirmed — consistent with [Textbook], Ch. [X]"). This demonstrates rigor and builds trust.

4. **Fallback** — If the IMA MCP connector is unavailable or the knowledge base search returns no relevant results, use general causal-inference expertise (the agent's built-in knowledge) to assess correctness. Note in Block B: "Substantive Check: No IMA source found; verified against general causal-inference knowledge."

5. **Boundary rule** — Do NOT alter the user's original intended meaning or add content the user did not write. The fact-check step only flags *factual inaccuracies* in the text's causal claims (e.g., mistaking a collider for a mediator, claiming SUTVA holds when interference is clearly present, misstating an identifying assumption). It does not introduce new arguments.

---

### Step 4 — Apply Terminology Rules

Critical terminology rules (override any common-language translations):

- Always consult `references/terminology.md` for the canonical English ↔ Chinese mapping
- Never introduce colloquial, textbook-idiosyncratic, or Chinese-domestic-journal variants
- For causal-inference terms (DID, PSM, RDD, IV, CDAG, counterfactual, treatment effect,
  confounder, parallel trends, exclusion restriction, LATE, ATT, ATE), use only the
  internationally standardized forms documented in the terminology reference
- **Context-dependent translation**: Words that are ambiguous in general Chinese must be
  resolved to their discipline-specific English counterpart. For example, in a DAG/causal-graph
  context, "部分" must be translated as "nodes" (not "parts"), and "路径" as "paths"
  (not "routes" or "ways"). Always identify the operative domain and select the
  terminologically correct equivalent.

---

### Step 5 — Produce Output

Always output **two clearly labeled blocks**:

#### Block A — 【润色定稿版 / Polished Version】

Deliver the final polished or translated text with no inline annotations.
- For `TR-ZH2EN`: produce fluent, native-level academic English
- For `TR-EN2ZH`: produce precise, natural Chinese that retains technical accuracy
- For `PO-EN`: produce a clean revised version ready for submission

#### Block B — 【修改备注 / Revision Notes】

Provide a structured comment table with the following columns:

| # | 原文片段 / Original | 修改后 / Revised | 修改依据 / Rationale |
|---|---------------------|-----------------|---------------------|

Rationale entries must specify:
- **Terminology**: why a specific term was chosen over alternatives
- **Sentence logic**: restructuring reason (passive → active, nominalization removed, etc.)
- **Journal convention**: citation to journal-specific convention where applicable
- **Causal language**: any upgrade from correlation language to identification language

---

### Step 6 — Journal-Specific Adaptation (if requested)

When the user names a target journal, apply the additional style rules from `references/journal_styles.md`.

Activate the relevant journal section:
- `[AER]` — American Economic Review
- `[QJE]` — Quarterly Journal of Economics
- `[JPE]` — Journal of Political Economy
- `[ECTA]` — Econometrica
- `[MS]` — Management Science
- `[JFE]` — Journal of Financial Economics
- `[JEEA]` — Journal of the European Economic Association
- `[REStud]` — Review of Economic Studies
- `[JRS]` — Journal of Rural Studies
- `[RFS]` — Review of Financial Studies

---

### Step 7 — AI-Trace Reflection (反查 AI 痕迹)

After producing both blocks (Block A + Block B) in Step 5, scan the entire output for the following AI-typical patterns and remove or replace them before delivering to the user.

#### English AI-Trace Checklist

| Pattern | Why It Looks AI-Generated | Replacement |
|---------|---------------------------|-------------|
| Em dash `—` or colon `:` used to insert an explanatory clause mid-sentence | Overuse of both em dashes and colons for explanation is a hallmark of LLM output | Rethink: does the clause need to be an appositive? If so, use parentheses or a comma-restricted relative clause. If contrast or explanation is needed, use a sentence break instead. |
| "that is" as a clause-level connector | "that is" is AI's default restatement device; human writers prefer "i.e.," "namely," or rewrite without the restatement | Either use "i.e.," (followed by a comma, then the restatement) or eliminate the restatement and merge the content directly into the preceding text |
| "In other words" | Same as "that is" — restatement marker that real academic writing uses sparingly | Delete the phrase and integrate the clarification directly; if the restatement is truly necessary, use "that is," |
| "Note that" at sentence start | This is AI's go-to attention-drawing device; genuine academic prose uses "Note that" only in technical asides | If the sentence is a normal argumentative step, remove "Note that" and let the sentence stand on its own. If it is a genuine caution (e.g., about a data limitation), keep it. |
| "It is worth noting that" | Wordy, hedge-stacking, AI-preferred | Delete entirely and start with the factual content. |
| "respectively" at the end of a paired statement | Overused by AI to pair items; humans usually restructure to make the pairing clearer through parallel sentence construction | Either delete "respectively" and rewrite as two short sentences, or keep only when the pairing would be genuinely ambiguous without it |
| "In particular," / "Specifically," / "More broadly," at sentence start | AI overuses these as generic transition pegs. They create a mechanical paragraph texture when used in more than one out of every four sentences. | Vary transitions or use a content-carrying transition (e.g., "The indirect effect tells a different story: ..." instead of "In particular, the indirect effect...") |
| Overly symmetrical parallel structures | AI tends to produce clauses of equal length and identical grammar in successive sentences, producing a "recited" rhythm | Break the rhythm: vary sentence length, swap clause order, or use a short interrupting sentence |
| "Importantly," / "Critically," / "Notably," as sentence-opening adverbs | These adverbs are AI's shortcut for emphasis without evidence | Either incorporate the emphasis into the content ("The key result is that X increases Y by Z%") or remove the adverb entirely |
| Parenthetical hedge stacks: "potentially, ... may ... possibly" | AI stacks multiple hedging devices in a single clause | Keep at most one hedge per clause. Choose the strongest one justified by the evidence. |
| "thereby" + gerund clause | "thereby doing" is AI's preferred way to express result | Replace with "and thus VERB" (finite verb) or separate into a new sentence. Only keep "thereby + -ing" when it genuinely improves readability (rarely). |

#### Chinese AI-Trace Checklist

| Pattern | Why It Looks AI-Generated | Replacement |
|---------|---------------------------|-------------|
| 破折号 `——` 或冒号 `：` 连接解释性插入语 | AI 过量使用破折号和冒号代替括号或重述句 | 改用括号、逗号从句，或拆分句子。若为解释性内容，直接融入上下文。 |
| 引号 `「」` 或 `""` 标记术语或特殊用法 | AI 倾向于用引号标记每一个非日常词汇 | 只有初次定义的术语或用反讽义时使用引号。常规专业术语直接使用不加引号。 |
| "即"（that is）做句间重述 | 在中文学术写作中，AI 过量使用 "即" 重述上一句的内容 | 要么删除重述句合并内容，要么将 "即" 改为 "换言之"（更书面的中文），或直接使用标点（冒号或分号）引导重述。 |
| "需要注意的是" / "值得注意的是" | 典型 AI 提示语气，在中文顶刊中极少出现 | 直接删除，内容保持不变。 |
| "换言之" / "换句话说" 作为段内转接 | AI 在中文中仿照 "in other words" 直译 | 删除，将解释内容直接融入上下文。 |
| 连续的"第一，第二，第三，第四" | AI 偏好机械列举 | 改用实质性过渡（如 "在理论层面，……；在实证层面，……"），或调整段落结构减少列举层级。 |
| "与此同时" / "此外" 在每段段首 | AI 生成的段落过渡模板 | 根据逻辑关系替换为 "相对而言""相比之下""进一步说" 等更具体的连接语，或直接省略。 |
| "综上所述" 开头的结论段 | 大量中式英文论文的 AI 改写痕迹 | 直接陈述核心结论，不需要 "综上所述" 做过渡标记。 |

**Post-reflection action:** If the reflection reveals any of these patterns, revise the offending passage before delivering. Do not mention the revision in the output — the revision notes (Block B) should only document intentional changes, not self-corrections.

---

## Quality Standards

### Language Quality
- Zero Chinglish constructions (subject-verb-object inversion, over-nominalization, literal conjunction translation)
- Consistent tense usage within sections (results in past tense; general claims in present tense)
- Hedging calibrated to evidence strength: "consistent with" / "suggests" / "provides evidence that" / "establishes"
- Avoid vague intensifiers: "very," "quite," "relatively," "obviously"

### Identification Language
- Distinguish between descriptive patterns ("is associated with") and causal claims ("increases," "reduces")
- Only use causal language when the identification strategy supports it
- State identification assumptions explicitly in empirical sections

### Citation and Reference Style
- Do not alter citations; flag missing citation information with `[CITE?]`
- Journal acronym usage: spell out on first mention, abbreviate thereafter

### Equations and Notation
- Do not alter mathematical content
- Flag inconsistent notation with inline comment `[NOTATION: suggest unifying with ...]`

---

## Anti-Patterns to Fix

The following patterns must be corrected on sight:

| Anti-pattern | Correction |
|---|---|
| "This paper studies..." | "This paper examines / investigates / estimates..." |
| "significant effect" (without magnitude) | Add coefficient size or elasticity |
| "As can be seen from Table X..." | "Table X reports..." or restructure to lead with finding |
| "In order to solve this problem..." | "To address this limitation..." |
| "The results show that A has a positive impact on B" | "A 1 SD increase in A is associated with a β-unit increase in B (p < 0.01)" |
| 混淆 "显著" 与 "重要" | 统计显著 → statistically significant; 经济重要 → economically meaningful |
| "We use DID method to study..." | "We exploit [exogenous variation / natural experiment] in a difference-in-differences framework..." |
| 直译 "平行趋势假设" → "parallel trend hypothesis" | → "parallel trends assumption" |
| 直译 "工具变量" → "instrumental variable method" | → "instrumental variables (IV) estimation" / "2SLS" |
| Em dash `—` or colon `:` for inline explanation | Replace with parentheses, comma-restricted clause, or sentence break |
| "that is" as clause-level restatement | Use "i.e.," or rewrite without restatement |
| "Note that" / "It is worth noting that" at sentence start | Delete, let the factual content stand alone |
| "In particular," / "Specifically," every paragraph | Vary transitions or lead with content |
| "Importantly," / "Critically," as sentence opener | Incorporate emphasis into content rather than using adverbial crutch |
| "respectively" at end of paired statement | If ambiguous, restructure as two sentences; otherwise delete |
| "thereby" + gerund clause | Replace with finite verb or separate sentence |
| 破折号 `——` 插入解释 | 改用括号或拆分句子 |
| 引号标记常规专业术语 | 删除引号，首次使用时用粗体或直接书写 |
| "即" 做段内重述 | 删除重述或改用冒号 |
| "需要注意的是" / "值得注意的是" | 直接删除 |
| "综上所述" 开篇结论句 | 直接进入核心结论 |
| **"……的问题" 直译为 "the problem of ..."** | **删除 "the problem of"，直接陈述事实。中文"……的问题"为冗余口语表达，英译时删除不影响语义。例：**"资源错误分配的问题" → "misallocation of resources"（非 "the problem of misallocation of resources"）** |

---

## Reference Files

- `references/terminology.md` — Canonical causal-inference and econometrics terminology (EN ↔ ZH)
- `references/journal_styles.md` — Journal-specific style rules for AER, QJE, JPE, ECTA, MS, JFE, JEEA, REStud
