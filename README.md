# InfoFlow Simulator

**A Schema-Adaptive Telemetry Dashboard for Information Engagement Analytics**

> *Course:* Programming & Data Analysis for Journalism and Communication in the Age of AI
> *Instructor:* Yuan (John) Yao
> *Team:* Yicheng Jiang (Lead), Shuoyang Jin, Jiaxin Wang, Quanquan Lu
> *Date:* July 2026

---

## What Makes This Different

> **Traditional dashboards require a data scientist to write bespoke queries for every new dataset.** InfoFlow Simulator flips this: upload *any* behavioral CSV, and the dashboard auto-detects its schema, dynamically selects appropriate visualizations, trains a baseline dropout prediction model, and produces a structured analysis report — **no manual configuration needed.**

This is a **methodological prototype** demonstrating a schema-adaptive approach to telemetry analytics. It is not a human-subject study; it uses synthetic data to stress-test the pipeline so that the same engine works reliably when real data arrives.

---

## Quick Start

### Prerequisites
- Python 3.9+
- Git

### Run the Dashboard

```bash
# 1. Clone the repository
git clone https://github.com/yc-eagle/infoflow-simulator.git
cd infoflow-simulator

# 2. (Optional) Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate      # On macOS/Linux
# .venv\Scripts\activate       # On Windows

# 3. Install dependencies
python -m pip install -r requirements.txt

# 4. Launch the dashboard
python -m streamlit run app.py

# 5. Open your browser to:
# http://localhost:8501
```

---

## Dashboard Tabs

| Tab | What It Does |
|-----|-------------|
| **Data Overview** | Column quality audit, missingness report, distribution plots |
| **Behavioral Analysis** | Adaptive charts — heatmaps, retention curves, density–dropout scatter, familiarity analysis — selected automatically based on which columns exist in your data |
| **Predictive Model** | Auto-trained logistic regression on dropout prediction with confusion matrix and feature importance |
| **Future Directions** | Research roadmap from current prototype to CHI 2027 submission |

---

## Schema-Adaptive Engine

The core innovation is `infer_schema()`: a fuzzy column-name matcher that maps arbitrary CSV headers to canonical semantic roles.

| If your CSV has a column named... | It's recognized as... |
|-----------------------------------|----------------------|
| `user_id`, `UserID`, `player`, `participant` | `user_id` |
| `stage`, `block`, `section`, `page`, `node` | `level_id` |
| `duration`, `time_spent`, `reading_time`, `rt` | `dwell_time` |
| `churn`, `abandon`, `exit_flag`, `bounce` | `dropout_flag` |
| `complexity`, `difficulty`, `cognitive_load` | `information_density` |
| `familiarity`, `expertise`, `proficiency` | `user_familiarity` |

Charts and models are rendered **conditionally** — only if the relevant columns are detected. Different datasets produce different dashboard outputs.

---

## Repository Structure

```
infoflow-simulator/
├── app.py                     # Streamlit dashboard (4-tab, schema-adaptive)
├── config.yaml                # Simulation engine parameters (externalized)
├── requirements.txt           # Python dependencies
├── data/
│   ├── program.py             # Simulation engine (callable + CLI)
│   ├── generate_stress_tests.py  # Batch stress-test generator
│   ├── data_inquire/          # SQL queries + sample database
│   └── stress_test_output/    # 5 diverse test CSVs
├── docs/
│   └── COLLABORATION_GUIDE.md # Git workflow for team members
├── assets/                    # Slides & images
├── FINAL_REPORT.qmd           # Quarto report (CHI-targeted)
├── references.bib             # Academic references
├── PROPOSAL.md                # Capstone proposal
├── AI_DISCLOSURE.md           # AI use statement
├── VERSION_LOG.md             # Version evolution (game → journalism)
└── README.md                  # This file
```

---

## Team Members & Roles

| Role | Member | Responsibilities |
|------|--------|-----------------|
| **Team Lead / Architect** | Yicheng Jiang | Simulation engine, schema inference, config externalization, integration, stress testing |
| **Data Analyst / Modeler** | Shuoyang Jin | SQL queries, adaptive query generation, logistic regression pipeline, feature importance |
| **Frontend / Dashboard** | Jiaxin Wang | Streamlit dashboard, schema-adaptive chart rendering, CSV upload & column mapping, deployment |
| **Narrative / Communication** | Quanquan Lu | Theoretical framing, innovation statement, FINAL_REPORT, literature review, AI disclosure |

---

## Research Roadmap (Toward CHI 2027)

```
Current (Prototype)
  → Schema-adaptive dashboard validated on 5 synthetic datasets
  → "Any CSV works" stress test passed

Short-Term (Next Semester)
  → IRB-approved human subject study (N = 20–30)
  → Expert heuristic evaluation (SUS + think-aloud)
  → Calibrate simulation parameters against empirical dwell-time data

Medium-Term (CHI 2027 Target)
  → Real-world deployment case study (1 newsroom or course partner)
  → Survival analysis (Cox PH + Kaplan-Meier)
  → Multimodal data integration (eye-tracking, click heatmaps)

Long-Term
  → Cross-domain transfer (EdTech, e-commerce, health)
  → Open-source pip package release
  → CSCW / TOCHI journal submission
```

---

## AI Usage Disclosure

AI coding assistants (ChatGPT, Copilot) were used for boilerplate generation, debugging, and syntax explanation. All AI-generated code was reviewed, tested, and understood before integration. The final report narrative was team-written. See [AI_DISCLOSURE.md](AI_DISCLOSURE.md).

---

## License

[MIT](LICENSE)
