# Canonical Terminology Reference
# Top-Journal Economics & Management — Causal Inference / Econometrics

This reference provides the authoritative English ↔ Chinese mappings for terms appearing in
AER, QJE, JPE, Econometrica, MS, JFE, JEEA, REStud, and comparable SSCI outlets.
When translating or polishing, always use these forms. Never substitute textbook variants,
domestic-journal variants, or colloquial renderings.

---

## 1. Research Design & Identification Strategy

| English (Canonical) | Chinese (规范译法) | 禁止使用 / Avoid |
|---|---|---|
| identification strategy | 识别策略 | 鉴别方法 |
| causal identification | 因果识别 | 因果鉴定 |
| natural experiment | 自然实验 | 天然实验 |
| quasi-experiment | 准实验 | 半实验 |
| exogenous variation | 外生变异 / 外生变动 | 外部变化 |
| endogeneity | 内生性 | 内部性 |
| selection bias | 选择性偏误 | 选择偏差（统计语境可用） |
| confounding variable / confounder | 混杂变量 / 混杂因子 | 干扰变量、干扰因素 |
| omitted variable bias (OVB) | 遗漏变量偏误 | 遗漏变量问题 |
| reverse causality | 反向因果 | 逆向因果 |
| simultaneity bias | 联立性偏误 | 同时性偏差 |
| local average treatment effect (LATE) | 局部平均处理效应 | 局部平均处理效果 |
| average treatment effect (ATE) | 平均处理效应 | 平均处理效果 |
| average treatment effect on the treated (ATT) | 受处理者平均处理效应 | — |
| intent-to-treat (ITT) | 意向性处理效应 | — |
| complier average causal effect (CACE) | 顺从者平均因果效应 | — |

---

## 2. Difference-in-Differences (DID / DiD)

| English (Canonical) | Chinese (规范译法) | 禁止使用 / Avoid |
|---|---|---|
| difference-in-differences (DID / DiD) | 双重差分（法） | 差中差、二重差分 |
| parallel trends assumption | 平行趋势假设 | 平行趋势假设（注意：assumption，非 hypothesis） |
| staggered adoption DID | 交错采用双重差分 | 分阶段DID |
| two-way fixed effects (TWFE) | 双向固定效应 | 双固定效应 |
| event-study design | 事件研究设计 | 事件窗设计 |
| pre-trend test | 预趋势检验 | 预期趋势检验 |
| dynamic treatment effect | 动态处理效应 | 动态处置效应 |
| Callaway–Sant'Anna estimator | Callaway–Sant'Anna 估计量 | — |
| Sun–Abraham estimator | Sun–Abraham 估计量 | — |
| Bacon decomposition | Bacon 分解 | — |
| heterogeneous treatment effects | 异质性处理效应 | 异质处理效果 |

---

## 3. Regression Discontinuity Design (RDD)

| English (Canonical) | Chinese (规范译法) | 禁止使用 / Avoid |
|---|---|---|
| regression discontinuity design (RDD) | 断点回归设计 | 回归不连续设计 |
| sharp RDD | 精确断点回归 | 尖锐RDD |
| fuzzy RDD | 模糊断点回归 | — |
| running variable / forcing variable | 运行变量 | 驱动变量（可接受）、跑动变量（避免） |
| bandwidth selection | 带宽选择 | — |
| local linear regression | 局部线性回归 | — |
| continuity assumption | 连续性假设 | — |
| McCrary density test | McCrary 密度检验 | — |
| Imbens–Kalyanaraman (IK) bandwidth | IK 最优带宽 | — |

---

## 4. Instrumental Variables (IV)

| English (Canonical) | Chinese (规范译法) | 禁止使用 / Avoid |
|---|---|---|
| instrumental variables (IV) | 工具变量（法）| 工具变数法 |
| two-stage least squares (2SLS) | 两阶段最小二乘法 | 二阶段最小二乘 |
| first stage | 第一阶段 | — |
| second stage | 第二阶段 | — |
| relevance condition | 相关性条件 | 相关条件 |
| exclusion restriction | 排除性约束 | 外生性约束（不同含义，避免混用） |
| instrument validity | 工具变量有效性 | — |
| weak instrument | 弱工具变量 | 弱工具 |
| F-statistic (first-stage) | 第一阶段 F 统计量 | — |
| over-identification test / Sargan–Hansen test | 过度识别检验 | — |
| endogenous regressor | 内生解释变量 | 内生变量（可接受，需上下文明确） |

---

## 5. Propensity Score Methods (PSM / IPW)

| English (Canonical) | Chinese (规范译法) | 禁止使用 / Avoid |
|---|---|---|
| propensity score matching (PSM) | 倾向得分匹配 | 倾向分数匹配 |
| inverse probability weighting (IPW) | 逆概率加权 | 逆倾向加权 |
| common support assumption | 共同支撑假设 | 公共支持假设 |
| covariate balance | 协变量平衡 | 控制变量均衡 |
| average treatment effect on the treated (ATT) | 受处理者平均处理效应 | — |
| doubly robust estimator | 双重稳健估计量 | — |
| kernel matching | 核匹配 | — |
| nearest-neighbor matching | 最近邻匹配 | — |
| caliper matching | 卡钳匹配 | — |

---

## 6. Causal Graph / Structural Causal Model

| English (Canonical) | Chinese (规范译法) | 禁止使用 / Avoid |
|---|---|---|
| directed acyclic graph (DAG) | 有向无环图 | 单向无环图 |
| causal DAG (CDAG) | 因果有向无环图 | — |
| structural causal model (SCM) | 结构因果模型 | — |
| potential outcomes framework | 潜在结果框架 | 可能结果框架 |
| counterfactual | 反事实 | 假设情境（通俗化，避免） |
| backdoor criterion | 后门准则 | 后门标准 |
| front-door criterion | 前门准则 | — |
| collider | 对撞节点 | 碰撞变量 |
| mediator | 中介变量 | 中间变量（可接受，需一致） |
| moderator | 调节变量 | 调节因子 |
| **部分（DAG语境）** → **nodes** | 节点 | — |
| **路径（DAG语境）** → **paths** | 路径 | — |

---

## 7. Panel Data & Fixed Effects

| English (Canonical) | Chinese (规范译法) | 禁止使用 / Avoid |
|---|---|---|
| fixed effects (FE) | 固定效应 | 固定效果 |
| random effects (RE) | 随机效应 | 随机效果 |
| Hausman test | Hausman 检验 | 豪斯曼检验 |
| within estimator | 组内估计量 | — |
| between estimator | 组间估计量 | — |
| entity fixed effects | 个体固定效应 | — |
| time fixed effects | 时间固定效应 | — |
| two-way fixed effects (TWFE) | 双向固定效应 | — |
| first differencing | 一阶差分 | — |
| Arellano–Bond estimator | Arellano–Bond 估计量 | — |
| Blundell–Bond estimator | Blundell–Bond 估计量 | — |

---

## 8. Standard Errors & Inference

| English (Canonical) | Chinese (规范译法) | 禁止使用 / Avoid |
|---|---|---|
| clustered standard errors | 聚类标准误 | 集群标准差 |
| heteroskedasticity-robust standard errors | 异方差稳健标准误 | 稳健标准差 |
| Driscoll–Kraay standard errors | Driscoll–Kraay 标准误 | — |
| wild cluster bootstrap | 野生聚类自助法 | — |
| randomization inference | 随机化推断 | — |
| multiple hypothesis testing | 多重假设检验 | 多重比较问题 |
| family-wise error rate (FWER) | 族错误率 | — |
| false discovery rate (FDR) | 错误发现率 | — |
| Bonferroni correction | Bonferroni 校正 | — |
| Holm–Bonferroni correction | Holm–Bonferroni 校正 | — |
| Anderson–Rubin confidence set | Anderson–Rubin 置信集 | — |

---

## 9. Robustness & Placebo

| English (Canonical) | Chinese (规范译法) | 禁止使用 / Avoid |
|---|---|---|
| robustness check | 稳健性检验 | 鲁棒性检验（可接受，但"稳健性"更规范） |
| placebo test | 安慰剂检验 | 伪检验 |
| falsification test | 伪造检验 | — |
| sensitivity analysis | 敏感性分析 | — |
| alternative specification | 替代性设定 | 其他设定 |
| sample restriction | 样本限制 | 样本筛选（视上下文） |

---

## 10. Mechanism & Heterogeneity

| English (Canonical) | Chinese (规范译法) | 禁止使用 / Avoid |
|---|---|---|
| mechanism analysis | 机制分析 | 机理分析（可接受） |
| causal channel | 因果渠道 / 因果机制 | 传导路径（通俗化） |
| mediation analysis | 中介分析 | — |
| subgroup analysis | 亚组分析 | 分组分析 |
| heterogeneity analysis | 异质性分析 | — |
| effect modification | 效应修饰 | — |
| spillover effect | 溢出效应 | 外溢效应 |
| general equilibrium effect | 一般均衡效应 | — |
| SUTVA (Stable Unit Treatment Value Assumption) | 稳定单元处理值假设 | — |

---

## 11. Common Statistics & Model Output Terms

| English (Canonical) | Chinese (规范译法) | Notes |
|---|---|---|
| coefficient | 系数 | — |
| standard error | 标准误 | 非"标准差" |
| t-statistic | t 统计量 | — |
| p-value | p 值 | — |
| confidence interval (CI) | 置信区间 | — |
| R-squared | R 方 / R² | — |
| adjusted R-squared | 调整 R 方 | — |
| log-likelihood | 对数似然 | — |
| AIC / BIC | AIC / BIC | 不译 |
| elasticity | 弹性 | — |
| semi-elasticity | 半弹性 | — |
| marginal effect | 边际效应 | — |
| interaction term | 交互项 | — |
| control variable | 控制变量 | — |
| dependent variable | 被解释变量 / 因变量 | 两者均可，同文中保持一致 |
| independent variable / regressor | 解释变量 / 回归量 | — |
| treatment variable | 处理变量 | — |
| binary variable / dummy variable | 虚拟变量 | 哑变量（可接受，但"虚拟变量"更规范） |

---

## 12. Paper Structure Terms

| English (Canonical) | Chinese (规范译法) |
|---|---|
| contribution | 研究贡献 |
| identification assumption | 识别假设 |
| data construction | 数据构建 |
| sample selection | 样本选取 |
| baseline specification | 基准设定 |
| baseline result | 基准结果 |
| main specification | 主要设定 |
| reduced-form estimate | 简约式估计 |
| structural estimate | 结构式估计 |
| back-of-the-envelope calculation | 粗略估算 |
| stylized fact | 文体化事实 / 典型事实 |
| takeaway | 主要结论 |
