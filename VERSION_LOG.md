# Version Log: InfoFlow Simulator

---

## v0.1 — Original Concept (Jul 7, 2026)

**Title:** Playtesting with Data: A Telemetry Dashboard for Game Analytics and Cognitive Bottleneck Evaluation

**Domain:** Game HCI / playtesting / cognitive load

**Team:** 2 members, recruiting

**Core question:** Cognitive bottleneck in puzzle-like level structures

**Key metrics:** Stuck rates, dropout points, cognitive load patterns

**Output:** Interactive dashboard with game-console-inspired UI

---

## v0.2 — Capstone Proposal (Jul 9, 2026)

**Title:** InfoFlow Simulator: A Telemetry Dashboard for Information Engagement Analytics

**Domain:** Journalism & communication / audience analytics

**Team:** 4 members, fulfilled

**Core question:** How does information complexity affect attention retention and dropout?

**Key metrics:** Dwell time, dropout points, engagement patterns

**Output:** 3-tab Streamlit dashboard (Cognitive Heatmap, Dropout Alert, Future Research Blueprint) deployed on Render

---

## v0.3 — Schema-Adaptive Architecture (Jul 14, 2026)

**Title:** InfoFlow Simulator: Schema-Adaptive Telemetry Engine with Predictive Modeling

**Domain:** Cross-domain behavioral analytics / schema-adaptive dashboard

**Team:** 4 members — Yicheng Jiang (Lead), Shuoyang Jin, Jiaxin Wang, Quanquan Lu

**Core question:** Can a single dashboard auto-detect data semantics and generate targeted analysis from *any* behavioral CSV without manual configuration?

**Key metrics:** Column auto-detection accuracy, adaptive chart coverage, baseline model performance

**Output:** 4-tab schema-adaptive Streamlit dashboard with stress-test validation (5 heterogeneous datasets)

---

### New Features by Team Member

#### Yicheng Jiang (Yicheng Jiang) — Team Lead / Architecture / Integration

- **`config.yaml`** — 仿真引擎全部参数外部化，改参不改码
- **`data/program.py` 重构** — 封装 `run_simulation(**kwargs)` 可调用函数 + CLI 入口（`--seed`, `--logs`, `--users`, `--stages`），参数优先级：显式传参 > config.yaml > 硬编码默认值
- **`data/generate_stress_tests.py`** — 一键生成 5 组形态各异的承压测试 CSV：
  | 数据集 | 日志数 | 用户数 | 特征 |
  |--------|--------|--------|------|
  | `stress_1_default` | 2000 | 130 | 基线配置 |
  | `stress_2_small_sample` | 300 | 30 | 小样本边缘测试 |
  | `stress_3_high_difficulty` | 1500 | 100 | 全阶段高难度 |
  | `stress_4_low_familiarity` | 2000 | 130 | 用户熟悉度偏低 |
  | `stress_5_extra_wide` | 3000 | 200 | 大规模压力测试 |
- **Pipeline 打通** — 确保 "上传任意 CSV → 自动识别 schema → 自适应图表 + 模型" 全链路跑通
- **`app_old_backup.py`** — 已删除（死代码清理）

#### Jiaxin Wang (Jiaxin Wang) — Dashboard / Frontend

- **`infer_schema()` 模糊列名映射引擎** — 不要求用户 CSV 列名精确匹配。8 类语义关键词字典覆盖 50+ 常见别名：
  | 语义角色 | 识别关键词（示例） |
  |----------|-------------------|
  | `user_id` | `UserID, player, participant, subject, reader` |
  | `level_id` | `Stage, block, section, page, node, step` |
  | `dwell_time` | `Duration, time_spent, reading_time, rt, elapsed` |
  | `dropout_flag` | `Churn, abandon, exit_flag, bounce, attrition` |
  | `information_density` | `Complexity, difficulty, cognitive_load, clutter` |
  | `user_familiarity` | `Familiarity, expertise, proficiency, skill_level` |
- **📋 Data Overview 标签页** — 列质量审计（缺失值%、dtype、唯一值数） + 数值列分布直方图 + box plot + 原始数据预览
- **📊 Behavioral Analysis 标签页（自适应）** — 6 种图表根据检测到的列**条件渲染**：
  1. `level_id + dwell_time` → 注意力热力图
  2. `level_id + dropout_flag` → 留存率曲线 + 高风险阶段标注
  3. `information_density + dropout_flag` → 信息密度 vs 放弃率散点图（含 OLS 趋势线）
  4. `user_familiarity + dropout_flag` → 熟悉度 vs 放弃率柱状图
  5. `action_type` → 行为类型饼图
  6. 多数值列 → 相关性矩阵热力图
- **UI 升级** — 从 3 tab → 4 tab，sidebar 显示检测到的列映射关系

#### Shuoyang Jin (Shuoyang Jin) — Data Analysis / Predictive Modeling

- **🤖 Predictive Model 标签页** — 自动检测 `dropout_flag` 列后：
  - 自动选择数值特征（排除 ID、时间戳等）
  - 70/30 分层抽样 split + StandardScaler 标准化
  - LogisticRegression 训练（`class_weight='balanced'`）
  - 输出：Accuracy / Precision / Recall 四宫格指标卡
  - 混淆矩阵热力图
  - 系数排序特征重要性条形图（标注正负方向含义）
- **自适应特征工程** — 关键词过滤（排除 `dropout`, `user_id`, `timestamp` 等）确保模型不会 leak target 信息

#### Quanquan Lu (Quanquan Lu) — Narrative / Communication / Theory

- **`FINAL_REPORT.qmd` 完整报告** — 从仅有章节标题的空模板扩展为 8 章完整学术报告：
  1. Introduction（含创新点陈述）
  2. Related Work（Information Foraging → Cognitive Load → Dwell Time → Dashboard Design）
  3. Method（Simulation Engine + Schema-Adaptive Dashboard + Predictive Modeling + Stress Testing Protocol）
  4. Results（Simulation Output + Dashboard Demo + Model Performance）
  5. Limitations & Future Work（含到 CHI 2027 的实证路线图）
  6. Team Collaboration
  7. Conclusion
  8. AI Usage Disclosure
- **`references.bib`** — 从 1 条占位符扩展到 13 条真实学术文献：
  - Information Foraging Theory (Pirolli & Card, 1999; Pirolli, 2007)
  - Cognitive Load Theory (Sweller, 1988; Paas et al., 2003)
  - Dwell Time as Engagement Signal (Liu et al., 2014; Yi et al., 2014)
  - Dashboard Design & Sensemaking (Few, 2006; Saraiya et al., 2005)
  - Survival Analysis (Cox, 1972; Kaplan & Meier, 1958)
  - Usability Evaluation (Brooke, 1996)
  - ML Interpretability (Agarwal et al., 2019)
  - Information Complexity & Attention (Khot et al., 2018)
- **创新点陈述** — 提炼三层创新（范式创新 "Schema-Adaptive" + 方法创新 "Simulation-to-Deployment" + 跨领域可迁移性）
- **`README.md`** — 重写，加入快速上手、schema 映射表、研究路线图

---

### Architecture Changes (v0.2 → v0.3)

```
v0.2 (Jul 9)                          v0.3 (Jul 14)
─────────────                         ─────────────
app.py (3 tabs, 固定图表)     →       app.py (4 tabs, schema-adaptive)
  - 2 slider                             - infer_schema() fuzzy matcher
  - 2 硬编码图表                          - 6 种条件渲染图表
  - 严格列名匹配                          - 自适应特征工程
                                         - LogisticRegression + 混淆矩阵 + 特征重要性

data/program.py (脚本)        →       data/program.py (可调用函数 + CLI)
  - 硬编码参数                           - config.yaml 外部化
  - 只能 python program.py               - run_simulation(**kwargs) API
                                         - generate_stress_tests.py × 5 数据集

requirements.txt (198行)      →       requirements.txt (5行)
  - conda freeze dump                    - 精简核心依赖

references.bib (1条占位符)    →       references.bib (13条真实文献)

FINAL_REPORT.qmd (空模板)     →       FINAL_REPORT.qmd (8章完整报告)

README.md                     →       加入创新点陈述 + 路线图

新增:
  config.yaml                    ← 仿真参数外部化
  data/generate_stress_tests.py  ← 承压测试生成器
  data/stress_test_output/       ← 5 组测试数据集
```

---

### What We Kept (Core DNA)

| Element | Retention |
| :--- | :--- |
| **Synthetic data generation** | ✅ Parameterized via `config.yaml` — no code change needed for new configs |
| **Telemetry logging & SQL storage** | ✅ SQLite + structured queries retained |
| **Dropout as key metric** | ✅ Now auto-detected from any column name via fuzzy matching |
| **Interactive dashboard UI** | ✅ Upgraded from 3 to 4 tabs; charts adapt to data shape |
| **Reproducibility commitment** | ✅ GitHub + clean `requirements.txt` + `config.yaml` + stress test datasets |
| **Publication ambition** | ✅ CHI 2027 roadmap documented in FINAL_REPORT.qmd and README.md |
| **AI usage disclosure** | ✅ Transparent AI-assisted development |

---

### What Shifted (Directional Change)

| Aspect | v0.2 (Jul 9) | v0.3 (Jul 14) |
| :--- | :--- | :--- |
| **Core capability** | Single-dataset dashboard | Schema-adaptive engine: any CSV → auto analysis |
| **Validation** | None | 5 stress-test datasets with heterogeneous configs |
| **Predictive model** | Mentioned but not implemented | LogisticRegression with auto feature selection + importance |
| **Chart generation** | 2 hardcoded charts | 6 adaptive charts (conditional on detected columns) |
| **Config management** | Hardcoded in code | Externalized to `config.yaml` |
| **Dependencies** | 198-line conda dump | 5 clean entries |
| **Literature** | 1 placeholder | 13 real references across 4 research streams |

---

### Rationale for v0.3

1. **"任何数据都能跑" — 承压验证优先。** v0.2 只能处理列名精确匹配 `user_id, level_id, action_type, dwell_time, dropout_flag` 的 CSV。v0.3 的 `infer_schema()` 让任意 CSV 进来都能自动识别并生成分析，这是从"demo"到"工具"的关键跨越。

2. **预测建模从 PPT 落到代码。** v0.2 的 PROPOSAL 提到 scikit-learn 但未实现。v0.3 在 Tab 3 完成了端到端训练→评估→解释的 pipeline，让 dashboard 从"看图"升级为"建模+推断"。

3. **学术基础铺设。** 13 条参考文献覆盖了理论根基（Information Foraging、Cognitive Load）、方法支撑（survival analysis、dwell time validation）和评估框架（SUS），为 CHI 2027 投稿做好了文献准备。

4. **外部化 = 可重复性。** `config.yaml` 让仿真参数修改不需要改代码；`generate_stress_tests.py` 让任何人都能一键复现承压测试结果。这是 CHI 审稿人看重的 reproducibility。

---

### References to Earlier Versions

The original v0.1 game-analytics concept is archived below:

> *"Playtesting with Data: A Telemetry Dashboard for Game Analytics and Cognitive Bottleneck Evaluation* — We are building a simulation engine that generates behavioral telemetry from virtual players navigating puzzle-like level structures. Using Python, SQL, and regression models, we will trace stuck rates, dropout points, and cognitive load patterns across different level designs. The final deliverable is an interactive web dashboard—game-console-inspired UI combined with a data control panel—that visualizes these patterns in real time."
