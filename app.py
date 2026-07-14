"""
InfoFlow Simulator — Schema-Adaptive Telemetry Dashboard.

Upload ANY behavioral CSV and get targeted analysis:
  - Automatic column mapping (fuzzy keyword match)
  - Data quality audit
  - Adaptive visualizations (charts chosen by data shape)
  - Predictive dropout model (when target column present)
  - Simulation fallback when no data uploaded.
"""
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import (accuracy_score, precision_score, recall_score,
                             confusion_matrix, classification_report)
from sklearn.preprocessing import StandardScaler

# ============================================================================
# Page Config
# ============================================================================
st.set_page_config(
    page_title="InfoFlow Simulator",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============================================================================
# Constants
# ============================================================================
RANDOM_SEED = 710
MAX_STAGE = 5
BASE_DWELL_TIME = 2.5
STAGE_BASE_DIFFICULTY = {1: 0.2, 2: 0.35, 3: 0.5, 4: 0.65, 5: 0.8}

# Column name aliases for fuzzy matching
COLUMN_ALIASES = {
    "user_id": ["user_id", "user", "userid", "uid", "participant", "participant_id",
                "subject", "subject_id", "player", "player_id", "reader", "reader_id"],
    "level_id": ["level_id", "level", "stage", "stage_id", "block", "block_id",
                 "section", "section_id", "page", "page_id", "step", "step_id",
                 "node", "node_id"],
    "dwell_time": ["dwell_time", "dwell", "dwelltime", "duration", "time_spent",
                   "time_on_page", "reading_time", "view_time", "attention_time",
                   "duration_sec", "elapsed", "response_time", "rt"],
    "action_type": ["action_type", "action", "event", "event_type", "type",
                    "behavior", "interaction"],
    "dropout_flag": ["dropout_flag", "dropout", "drop_out", "churn", "churn_flag",
                     "abandon", "exit_flag", "bounce", "bounce_flag", "retention",
                     "retained", "attrition"],
    "information_density": ["information_density", "info_density", "density",
                            "complexity", "info_complexity", "difficulty",
                            "cognitive_load", "clutter"],
    "user_familiarity": ["user_familiarity", "familiarity", "experience",
                         "expertise", "proficiency", "skill_level", "domain_knowledge"],
    "action_timestamp": ["action_timestamp", "timestamp", "time", "datetime",
                         "date", "event_time", "log_time"],
}


def infer_schema(df: pd.DataFrame) -> dict:
    """
    Fuzzy-match DataFrame columns to canonical names.

    Returns a dict like {'user_id': 'UserID_col', 'level_id': 'Stage', ...}
    with only the keys whose columns were found.
    """
    mapping = {}
    df_cols_lower = {c.lower(): c for c in df.columns}

    for canonical, aliases in COLUMN_ALIASES.items():
        for alias in aliases:
            if alias in df_cols_lower:
                mapping[canonical] = df_cols_lower[alias]
                break

    return mapping


def data_quality_report(df: pd.DataFrame) -> pd.DataFrame:
    """Build a per-column quality summary DataFrame."""
    rows = []
    for col in df.columns:
        missing = df[col].isna().sum()
        missing_pct = missing / len(df) * 100
        dtype = str(df[col].dtype)
        unique = df[col].nunique()
        rows.append({
            "Column": col,
            "Type": dtype,
            "Missing": f"{missing} ({missing_pct:.1f}%)",
            "Unique Values": unique,
            "Sample": str(df[col].dropna().iloc[0]) if missing < len(df) else "N/A",
        })
    return pd.DataFrame(rows)


def run_simulation_data(info_complexity: int, top_n: int) -> pd.DataFrame:
    """Generate synthetic behavioral data (fallback when no CSV uploaded)."""
    np.random.seed(RANDOM_SEED)
    display_stage = min(top_n, MAX_STAGE)
    stages = list(range(1, display_stage + 1))

    data = {
        "level_id": stages,
        "dwell_time": [round(max(0.3, np.random.normal(
            BASE_DWELL_TIME * (1 + STAGE_BASE_DIFFICULTY[s] * 0.8), 0.5)), 2)
            for s in stages],
        "dropout_flag": [1 if s > info_complexity else 0 for s in stages],
        "info_complexity": [STAGE_BASE_DIFFICULTY[s] for s in stages],
    }
    return pd.DataFrame(data)


# ============================================================================
# Sidebar
# ============================================================================
st.sidebar.header("🎛️ Experiment Parameters")

info_complexity = st.sidebar.slider("Information Complexity (Simulation Mode)", 1, 5, 3)
top_n = st.sidebar.slider("Display Top N Blocks", 1, 20, 5)

st.sidebar.markdown("---")
st.sidebar.subheader("📂 Data Source")
uploaded_file = st.sidebar.file_uploader(
    "Upload Behavior Log CSV",
    type=["csv"],
    help="Drop ANY CSV with behavioral columns — the dashboard auto-detects the schema.",
)

# ============================================================================
# Data Loading
# ============================================================================
use_simulation = True
raw_df = None
schema = {}
df = None

if uploaded_file is not None:
    try:
        raw_df = pd.read_csv(uploaded_file)
        schema = infer_schema(raw_df)

        if schema:
            use_simulation = False
            # Normalize column references
            df = raw_df.copy()
            st.sidebar.success(
                f"✅ Loaded: {len(raw_df):,} rows × {len(raw_df.columns)} cols\n\n"
                f"Mapped: {', '.join(f'{k}→{v}' for k, v in schema.items())}"
            )
        else:
            st.sidebar.warning("⚠️ No recognizable columns. Falling back to simulation.")
    except Exception as e:
        st.sidebar.error(f"❌ Failed to parse CSV: {e}")

if use_simulation:
    df = run_simulation_data(info_complexity, top_n)
    st.sidebar.info("🔬 Current mode: **Simulated Data**")

# Ensure we have a working DataFrame
if df is None or df.empty:
    df = run_simulation_data(info_complexity, top_n)

# ============================================================================
# Main Dashboard
# ============================================================================
tab1, tab2, tab3, tab4 = st.tabs([
    "📋 Data Overview",
    "📊 Behavioral Analysis",
    "🤖 Predictive Model",
    "🔮 Future Directions",
])

# ============================================================================
# TAB 1: Data Overview
# ============================================================================
with tab1:
    st.subheader("Data Preview & Quality Audit")

    col_a, col_b = st.columns(2)
    with col_a:
        st.metric("Total Rows", f"{len(df):,}")
        st.metric("Total Columns", len(df.columns))
    with col_b:
        st.metric("Memory Usage", f"{df.memory_usage(deep=True).sum() / 1024:.1f} KB")
        if "dropout_flag" in schema:
            drop_col = schema["dropout_flag"]
            drop_rate = df[drop_col].mean() if df[drop_col].dtype in ("int64", "float64") else df[drop_col].astype(float).mean()
            st.metric("Overall Dropout Rate", f"{drop_rate:.2%}")

    st.markdown("---")
    st.subheader("🔍 Column Quality Report")
    quality = data_quality_report(df)
    st.dataframe(quality, use_container_width=True, hide_index=True)

    st.markdown("---")
    st.subheader("📄 Raw Data (first 50 rows)")
    st.dataframe(df.head(50), use_container_width=True)

    # Distributions for numeric columns
    numeric_cols = df.select_dtypes(include=["int64", "float64"]).columns.tolist()
    if numeric_cols:
        st.markdown("---")
        st.subheader("📈 Numeric Column Distributions")
        n_plots = min(len(numeric_cols), 6)
        cols_per_row = min(3, n_plots)
        rows_needed = (n_plots + cols_per_row - 1) // cols_per_row

        for row_idx in range(rows_needed):
            plot_cols = st.columns(cols_per_row)
            for ci in range(cols_per_row):
                idx = row_idx * cols_per_row + ci
                if idx < n_plots:
                    with plot_cols[ci]:
                        col = numeric_cols[idx]
                        fig = px.histogram(df, x=col, nbins=30, marginal="box",
                                           title=f"Distribution: {col}")
                        fig.update_layout(height=250)
                        st.plotly_chart(fig, use_container_width=True)

# ============================================================================
# TAB 2: Behavioral Analysis (Adaptive)
# ============================================================================
with tab2:
    st.subheader("Adaptive Behavioral Analysis")
    if not schema:
        st.info("Using simulation data. Upload a CSV for schema-adaptive analysis.")
        schema_for_charts = {"level_id": "level_id", "dwell_time": "dwell_time",
                             "dropout_flag": "dropout_flag",
                             "information_density": "info_complexity"}
    else:
        schema_for_charts = schema

    charts_rendered = 0

    # Chart 1: Stage × Dwell Time Heatmap
    dwell_col = schema_for_charts.get("dwell_time", None)
    level_col = schema_for_charts.get("level_id", None)
    if dwell_col and level_col:
        charts_rendered += 1
        st.markdown(f"### 🗺️ Attention Distribution: `{level_col}` × `{dwell_col}`")

        try:
            pivot = df.pivot_table(index=level_col, values=dwell_col, aggfunc="mean")
            fig = px.imshow(
                pivot.T if pivot.shape[0] > 1 else pivot,
                labels=dict(x=level_col, y="", color=f"Mean {dwell_col}"),
                aspect="auto",
                color_continuous_scale="YlOrRd",
            )
            fig.update_xaxes(tickmode="linear")
            st.plotly_chart(fig, use_container_width=True)
        except Exception:
            st.warning(f"Could not generate heatmap — check `{level_col}` values.")

    st.markdown("---")

    # Chart 2: Dropout / Retention Curve
    dropout_col = schema_for_charts.get("dropout_flag", None)
    if dropout_col and level_col:
        charts_rendered += 1
        st.markdown(f"### 📉 Retention Trend by `{level_col}`")

        try:
            stage_order = sorted(df[level_col].dropna().unique())
            ret_data = []
            for s in stage_order:
                mask = df[level_col] <= s
                if mask.sum():
                    drop_vals = pd.to_numeric(df.loc[mask, dropout_col], errors="coerce")
                    ret_data.append({
                        level_col: s,
                        "retention_rate": 1 - drop_vals.mean(),
                        "dropout_rate": drop_vals.mean(),
                    })
            ret_df = pd.DataFrame(ret_data)
            if not ret_df.empty:
                fig = px.line(ret_df, x=level_col, y="retention_rate", markers=True,
                              labels={level_col: level_col, "retention_rate": "Retention Rate"})
                fig.update_layout(yaxis_range=[0, 1.05])
                st.plotly_chart(fig, use_container_width=True)

                st.markdown("**🚨 High-Risk Stages**")
                high_risk = ret_df[ret_df["dropout_rate"] >= 0.5][level_col].tolist()
                if high_risk:
                    st.warning(f"Significant churn at {level_col}(s): **{high_risk}**")
                else:
                    st.success("No stages exceed 50% dropout under current data.")
        except Exception:
            st.warning("Could not compute retention trend.")

    st.markdown("---")

    # Chart 3: Density × Dropout (conditional)
    density_col = schema_for_charts.get("information_density", None)
    if density_col and dropout_col:
        charts_rendered += 1
        st.markdown(f"### 📊 Information Density vs. Dropout")

        try:
            density_vals = pd.to_numeric(df[density_col], errors="coerce")
            drop_vals = pd.to_numeric(df[dropout_col], errors="coerce")
            agg = df.copy()
            agg["_density"] = density_vals
            agg["_dropout"] = drop_vals
            grouped = agg.groupby("_density")["_dropout"].agg(["mean", "count"]).reset_index()
            grouped.columns = [density_col, "dropout_rate", "sample_size"]

            fig = px.scatter(
                grouped, x=density_col, y="dropout_rate",
                size="sample_size", trendline="ols",
                labels={density_col: density_col, "dropout_rate": "Dropout Rate"},
            )
            st.plotly_chart(fig, use_container_width=True)
        except Exception:
            st.warning("Could not generate density-dropout plot.")

    st.markdown("---")

    # Chart 4: Familiarity × Dropout (conditional)
    fam_col = schema_for_charts.get("user_familiarity", None)
    if fam_col and dropout_col:
        charts_rendered += 1
        st.markdown(f"### 👤 Familiarity vs. Dropout")

        try:
            fam_vals = pd.to_numeric(df[fam_col], errors="coerce")
            drop_vals = pd.to_numeric(df[dropout_col], errors="coerce")
            agg = df.copy()
            agg["_fam"] = fam_vals
            agg["_drop"] = drop_vals
            grouped = agg.groupby("_fam")["_drop"].mean().reset_index()
            grouped.columns = [fam_col, "dropout_rate"]

            fig = px.bar(grouped, x=fam_col, y="dropout_rate",
                         labels={fam_col: fam_col, "dropout_rate": "Dropout Rate"},
                         color="dropout_rate", color_continuous_scale="RdYlGn_r")
            st.plotly_chart(fig, use_container_width=True)
        except Exception:
            st.warning("Could not generate familiarity chart.")

    # Chart 5: Action Type Distribution (conditional)
    action_col = schema_for_charts.get("action_type", None)
    if action_col:
        charts_rendered += 1
        st.markdown(f"### 🏷️ Action Type Distribution")

        try:
            vc = df[action_col].value_counts().reset_index()
            vc.columns = [action_col, "count"]
            fig = px.pie(vc, names=action_col, values="count", hole=0.4)
            st.plotly_chart(fig, use_container_width=True)
        except Exception:
            st.warning("Could not generate action pie chart.")

    # Chart 6: Numeric correlation heatmap (always useful)
    numeric_cols_raw = df.select_dtypes(include=["int64", "float64"]).columns.tolist()
    if len(numeric_cols_raw) >= 2:
        charts_rendered += 1
        st.markdown("### 🔗 Numeric Feature Correlation")
        try:
            corr = df[numeric_cols_raw].corr()
            fig = px.imshow(corr, text_auto=".2f", aspect="auto",
                            color_continuous_scale="RdBu_r", zmin=-1, zmax=1)
            fig.update_layout(height=450)
            st.plotly_chart(fig, use_container_width=True)
        except Exception:
            st.warning("Could not generate correlation heatmap.")

    if charts_rendered == 0:
        st.warning("No chart-compatible columns detected. Upload a CSV with numeric/time columns.")

# ============================================================================
# TAB 3: Predictive Model
# ============================================================================
with tab3:
    st.subheader("🤖 Dropout Prediction Model")

    dropout_col = schema.get("dropout_flag") if schema else "dropout_flag"

    if dropout_col and dropout_col in df.columns:
        st.markdown(f"""
        **Target column:** `{dropout_col}`
        Auto-training a logistic regression on all numeric features (excluding the target).
        """)

        # Build feature matrix
        numeric_feats = df.select_dtypes(include=["int64", "float64"]).columns.tolist()
        # Remove target and identifier-like columns from features
        exclude_keywords = ["dropout", "user_id", "timestamp", "time", "id"]
        features = [c for c in numeric_feats
                    if c != dropout_col and not any(kw in c.lower() for kw in exclude_keywords)]

        if len(features) == 0:
            # Fallback: just use all numeric except target
            features = [c for c in numeric_feats if c != dropout_col]

        if len(features) >= 1:
            X = df[features].copy()
            y = pd.to_numeric(df[dropout_col], errors="coerce")

            # Drop rows where target is NaN
            mask = y.notna()
            X = X.loc[mask]
            y = y.loc[mask].astype(int)

            if len(y.unique()) >= 2 and len(y) >= 20:
                # Train/test split
                X_train, X_test, y_train, y_test = train_test_split(
                    X, y, test_size=0.3, random_state=42, stratify=y,
                )

                # Scale
                scaler = StandardScaler()
                X_train_s = scaler.fit_transform(X_train)
                X_test_s = scaler.transform(X_test)

                # Train
                model = LogisticRegression(max_iter=2000, class_weight="balanced")
                model.fit(X_train_s, y_train)
                y_pred = model.predict(X_test_s)

                # Metrics
                acc = accuracy_score(y_test, y_pred)
                prec = precision_score(y_test, y_pred, zero_division=0)
                rec = recall_score(y_test, y_pred, zero_division=0)
                cm = confusion_matrix(y_test, y_pred)

                col_m1, col_m2, col_m3, col_m4 = st.columns(4)
                col_m1.metric("Accuracy", f"{acc:.2%}")
                col_m2.metric("Precision", f"{prec:.2%}")
                col_m3.metric("Recall", f"{rec:.2%}")
                col_m4.metric("Test Samples", len(y_test))

                st.markdown("---")
                st.subheader("Confusion Matrix")
                fig_cm = px.imshow(cm, text_auto=True, aspect="auto",
                                   labels=dict(x="Predicted", y="Actual"),
                                   x=["No Dropout", "Dropout"],
                                   y=["No Dropout", "Dropout"],
                                   color_continuous_scale="Blues")
                st.plotly_chart(fig_cm, use_container_width=True)

                st.markdown("---")
                st.subheader("Feature Importance (Logistic Regression Coefficients)")
                coef_df = pd.DataFrame({
                    "Feature": features,
                    "Coefficient": model.coef_[0],
                    "Abs_Coefficient": np.abs(model.coef_[0]),
                }).sort_values("Abs_Coefficient", ascending=False)

                fig_coef = px.bar(
                    coef_df, x="Coefficient", y="Feature",
                    orientation="h",
                    color="Coefficient",
                    color_continuous_scale="RdBu",
                    title="Which features most influence dropout prediction?",
                )
                fig_coef.update_layout(yaxis={"categoryorder": "total ascending"})
                st.plotly_chart(fig_coef, use_container_width=True)

                st.caption(
                    "Positive coefficient → increases dropout probability. "
                    "Negative coefficient → decreases dropout probability."
                )
            else:
                st.warning(
                    f"Need ≥2 classes and ≥20 valid rows for modeling. "
                    f"Current: {len(y)} rows, {len(y.unique())} classes."
                )
        else:
            st.warning("No numeric feature columns available for modeling.")
    else:
        st.info(
            "No `dropout_flag` column detected. "
            "Upload a CSV with a binary dropout/churn column to enable predictive modeling."
        )

# ============================================================================
# TAB 4: Future Directions
# ============================================================================
with tab4:
    st.subheader("Research Roadmap")

    st.markdown("""
    ### 🎯 Current Stage: Schema-Adaptive Prototype

    The dashboard you are viewing can ingest **any behavioral CSV**, auto-detect
    its schema, and generate targeted analytics without manual configuration.

    ---

    ### 📍 Short-Term (Next Semester)
    - **IRB-approved human subject study** — 20–30 participants performing
      information-browsing tasks under controlled complexity conditions
    - **Simulated vs. real comparison** — validate simulation engine parameters
      against empirical dwell-time and dropout distributions
    - **Expert heuristic evaluation** — 3–5 HCI researchers review the dashboard
      via think-aloud protocol + System Usability Scale (SUS)

    ---

    ### 📍 Medium-Term (CHI 2027 Target)
    - **Real-world deployment** — partner with 1 newsroom or university course to
      collect authentic engagement telemetry
    - **Multimodal expansion** — incorporate eye-tracking and click heatmap data
    - **Survival analysis** — replace binary dropout with time-to-event modeling
      (Cox proportional hazards / Kaplan-Meier estimators)
    - **Personalized complexity adaptation** — reinforcement learning agent that
      adjusts information density per user in real time

    ---

    ### 📍 Long-Term Vision
    - **Cross-domain transfer** — apply the same pipeline to EdTech (learning
      dropout), e-commerce (cart abandonment), health (engagement retention)
    - **Open-source toolkit** — release as a `pip`-installable package for
      communication researchers and UX analysts
    - **CSCW / TOCHI journal submission** — longitudinal deployment study
    """)

    st.info(
        "This dashboard is a **methodological prototype** developed as part of "
        "the *Programming & Data Analysis for Journalism and Communication* "
        "course at Tsinghua University (July 2026)."
    )

# ============================================================================
# Footer
# ============================================================================
st.caption(
    "© InfoFlow Simulator · "
    "Schema-adaptive telemetry engine · "
    "Repo: https://github.com/yc-eagle/infoflow-simulator"
)
