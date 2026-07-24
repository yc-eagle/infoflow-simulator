# Version Log: InfoFlow Simulator

---

## v0.4 — Final Polish & Deployment (Jul 24, 2026)

**Title:** InfoFlow Simulator: Final fixes, config unification, and public deployment

**Core changes:**

- **Deployment** — Live dashboard on Streamlit Community Cloud: [infoflow-simulator.streamlit.app](https://infoflow-simulator.streamlit.app/)
- **Config unification** — `app.py` now loads all constants from `config.yaml` via `_CFG` dict; no more hardcoded duplicates
- **Simulation integration** — `app.py` fallback mode now calls `data/program.py` `run_simulation()` directly instead of a stripped-down reimplementation
- **Stress test fix** — `stress_4_low_familiarity` now actually skews user familiarity low (`familiarity_low_bias=True`, ~70% at levels 1–2); dropout 46.43% vs baseline 40.98%
- **`program.py`** — Added `familiarity_low_bias` parameter for weighted familiarity distribution
- **`data_inquire/` cleanup** — `add_database.py` rewritten as proper CSV→SQLite import; `plot_chart.py` deduplicated; SQL column names unified to English; renamed `familiarity&stage_dropout.sql` → `familiarity_stage_dropout.sql`
- **`export_tables_en.py`** — Simplified to standardise column names across existing Excel sheets
- **README** — Added student IDs, live demo link, `LICENSE` file
- **Stress test data** — All 5 datasets regenerated with fixes applied

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

#### Yicheng Jiang — Team Lead / Architecture / Integration

- **`config.yaml`** — Externalized all simulation parameters; change config without touching code
- **`data/program.py` refactor** — Wrapped as callable `run_simulation(**kwargs)` + CLI entry (`--seed`, `--logs`, `--users`, `--stages`). Priority: explicit args > config.yaml > hardcoded defaults
- **`data/generate_stress_tests.py`** — One-click generation of 5 diverse stress-test CSVs:
  | Dataset | Logs | Users | Feature |
  |--------|--------|--------|------|
  | `stress_1_default` | 2000 | 130 | Baseline config |
  | `stress_2_small_sample` | 300 | 30 | Small-N edge case |
  | `stress_3_high_difficulty` | 1500 | 100 | Elevated difficulty all stages |
  | `stress_4_low_familiarity` | 2000 | 130 | Low user familiarity skew |
  | `stress_5_extra_wide` | 3000 | 200 | Large-scale stress test |
- **Pipeline** — End-to-end: "upload any CSV → auto-detect schema → adaptive charts + model"
- **`app_old_backup.py`** — Deleted (dead code cleanup)

#### Jiaxin Wang — Dashboard / Frontend

- **`infer_schema()` fuzzy column-name mapping engine** — No exact column-name match required. 8 semantic keyword dictionaries covering 50+ common aliases:
  | Semantic Role | Recognized Keywords (examples) |
  |----------|-------------------|
  | `user_id` | `UserID, player, participant, subject, reader` |
  | `level_id` | `Stage, block, section, page, node, step` |
  | `dwell_time` | `Duration, time_spent, reading_time, rt, elapsed` |
  | `dropout_flag` | `Churn, abandon, exit_flag, bounce, attrition` |
  | `information_density` | `Complexity, difficulty, cognitive_load, clutter` |
  | `user_familiarity` | `Familiarity, expertise, proficiency, skill_level` |
- **Data Overview tab** — Column quality audit (missing%, dtype, unique count) + numeric distribution histograms + box plots + raw data preview
- **Behavioral Analysis tab (adaptive)** — 6 chart types rendered conditionally based on detected columns:
  1. `level_id + dwell_time` → attention heatmap
  2. `level_id + dropout_flag` → retention curve + high-risk stage warnings
  3. `information_density + dropout_flag` → density vs. dropout scatter (with OLS trendline)
  4. `user_familiarity + dropout_flag` → familiarity vs. dropout bar chart
  5. `action_type` → action type pie chart
  6. Multiple numeric columns → correlation matrix heatmap
- **UI upgrade** — 3 tab → 4 tab, sidebar shows detected column mappings

#### Shuoyang Jin — Data Analysis / Predictive Modeling

- **Predictive Model tab** — On detecting `dropout_flag` column:
  - Auto-selects numeric features (excludes ID, timestamps)
  - 70/30 stratified split + StandardScaler
  - LogisticRegression with `class_weight='balanced'`
  - Output: Accuracy / Precision / Recall metric cards
  - Confusion matrix heatmap
  - Coefficient-ranked feature importance bar chart (with direction annotation)
- **Adaptive feature engineering** — Keyword filtering (excludes `dropout`, `user_id`, `timestamp`) prevents target leakage

#### Quanquan Lu — Narrative / Communication / Theory

- **`FINAL_REPORT.qmd` complete report** — Expanded from empty template to 8-chapter academic report:
  1. Introduction (with innovation statement)
  2. Related Work (Information Foraging → Cognitive Load → Dwell Time → Dashboard Design)
  3. Method (Simulation Engine + Schema-Adaptive Dashboard + Predictive Modeling + Stress Testing Protocol)
  4. Results (Simulation Output + Dashboard Demo + Model Performance)
  5. Limitations & Future Work (with empirical roadmap to CHI 2027)
  6. Team Collaboration
  7. Conclusion
  8. AI Usage Disclosure
- **`references.bib`** — Expanded from 1 placeholder to 13 real academic references:
  - Information Foraging Theory (Pirolli & Card, 1999; Pirolli, 2007)
  - Cognitive Load Theory (Sweller, 1988; Paas et al., 2003)
  - Dwell Time as Engagement Signal (Liu et al., 2014; Yi et al., 2014)
  - Dashboard Design & Sensemaking (Few, 2006; Saraiya et al., 2005)
  - Survival Analysis (Cox, 1972; Kaplan & Meier, 1958)
  - Usability Evaluation (Brooke, 1996)
  - ML Interpretability (Agarwal et al., 2019)
  - Information Complexity & Attention (Khot et al., 2018)
- **Innovation statement** — Three-layer innovation (paradigm: "Schema-Adaptive" + method: "Simulation-to-Deployment" + cross-domain transferability)
- **`README.md`** — Rewritten with quick start, schema mapping table, research roadmap

---

### Architecture Changes (v0.2 → v0.3)

```
v0.2 (Jul 9)                          v0.3 (Jul 14)
─────────────                         ─────────────
app.py (3 tabs, fixed charts) →       app.py (4 tabs, schema-adaptive)
  - 2 sliders                            - infer_schema() fuzzy matcher
  - 2 hardcoded charts                   - 6 conditional chart types
  - strict column name match             - adaptive feature engineering
                                         - LogisticRegression + confusion matrix + feature importance

data/program.py (script)      →       data/program.py (callable function + CLI)
  - hardcoded parameters                - config.yaml externalization
  - python program.py only              - run_simulation(**kwargs) API
                                         - generate_stress_tests.py × 5 datasets

requirements.txt (198 lines)   →       requirements.txt (5 lines)
  - conda freeze dump                    - minimal core dependencies

references.bib (1 placeholder) →       references.bib (13 real references)

FINAL_REPORT.qmd (empty)       →       FINAL_REPORT.qmd (8-chapter report)

README.md                      →       Added innovation statement + roadmap

New:
  config.yaml                    ← Simulation parameter externalization
  data/generate_stress_tests.py  ← Stress test generator
  data/stress_test_output/       ← 5 test datasets
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

1. **"Any data works" — stress validation first.** v0.2 only handled CSVs with exact column names `user_id, level_id, action_type, dwell_time, dropout_flag`. v0.3's `infer_schema()` lets any CSV auto-detect and generate analysis — the key leap from "demo" to "tool."

2. **Predictive modeling from slides to code.** v0.2's PROPOSAL mentioned scikit-learn but didn't implement it. v0.3 completed an end-to-end train→evaluate→explain pipeline in Tab 3, upgrading the dashboard from "viewing charts" to "modeling + inference."

3. **Academic foundation laid.** 13 references cover theoretical grounding (Information Foraging, Cognitive Load), methodological support (survival analysis, dwell time validation), and evaluation frameworks (SUS), preparing the literature base for a CHI 2027 submission.

4. **Externalization = reproducibility.** `config.yaml` allows parameter changes without code edits; `generate_stress_tests.py` lets anyone reproduce stress-test results in one command — exactly what CHI reviewers value in reproducibility.

---

### References to Earlier Versions

The original v0.1 game-analytics concept is archived below:

> *"Playtesting with Data: A Telemetry Dashboard for Game Analytics and Cognitive Bottleneck Evaluation* — We are building a simulation engine that generates behavioral telemetry from virtual players navigating puzzle-like level structures. Using Python, SQL, and regression models, we will trace stuck rates, dropout points, and cognitive load patterns across different level designs. The final deliverable is an interactive web dashboard—game-console-inspired UI combined with a data control panel—that visualizes these patterns in real time."
