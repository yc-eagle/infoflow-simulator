import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# ========== Page Config ==========
st.set_page_config(
    page_title="InfoFlow Simulator",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ========== Global Params (Aligned with data generation script) ==========
RANDOM_SEED = 710
MAX_STAGE = 5
BASE_DWELL_TIME = 2.5
stage_base_difficulty = {
    1: 0.2,
    2: 0.35,
    3: 0.5,
    4: 0.65,
    5: 0.8
}

# ========== Sidebar ==========
st.sidebar.header("🎛️ Experiment Parameters")
info_complexity = st.sidebar.slider("Information Complexity (Simulation Mode)", 1, 5, 3)
top_n = st.sidebar.slider("Display Top N Blocks", 1, 5, 5)

st.sidebar.markdown("---")
st.sidebar.subheader("📂 Data Source")
uploaded_file = st.sidebar.file_uploader("Upload Behavior Log CSV", type="csv")

# ========== Data Loading Logic ==========
if uploaded_file is not None:
    raw_df = pd.read_csv(uploaded_file)
    required_cols = ["user_id", "level_id", "action_type", "dwell_time", "dropout_flag"]
    
    if not all(col in raw_df.columns for col in required_cols):
        st.sidebar.error("CSV field mismatch. Required: user_id, level_id, action_type, dwell_time, dropout_flag")
        use_simulation = True
    else:
        use_simulation = False
        
        stage_dwell = raw_df.groupby("level_id")["dwell_time"].mean().round(2).reset_index()
        exit_df = raw_df[raw_df["action_type"] == "exit"]
        stage_dropout = exit_df.groupby("level_id")["dropout_flag"].mean().reset_index()
        stage_difficulty = pd.DataFrame({
            "level_id": list(stage_base_difficulty.keys()),
            "info_complexity": list(stage_base_difficulty.values())
        })
        
        df = (
            stage_dwell
            .merge(stage_dropout, on="level_id")
            .merge(stage_difficulty, on="level_id")
            .sort_values("level_id")
            .reset_index(drop=True)
        )
        df = df.head(top_n)
        
        st.sidebar.success(
            f"Real logs loaded\n"
            f"Total records: {len(raw_df)}\n"
            f"Stages covered: {df['level_id'].min()} ~ {df['level_id'].max()}"
        )
else:
    use_simulation = True

# Simulation Data Generation
if use_simulation:
    np.random.seed(RANDOM_SEED)
    display_stage = min(top_n, MAX_STAGE)
    stages = list(range(1, display_stage + 1))

    dwell_time_list = []
    dropout_flag_list = []
    complexity_list = []

    for stage in stages:
        base_dwell = BASE_DWELL_TIME * (1 + stage_base_difficulty[stage] * 0.8)
        dwell = np.random.normal(loc=base_dwell, scale=0.5)
        dwell_time_list.append(round(max(0.3, dwell), 2))
        dropout_flag = 1 if stage > info_complexity else 0
        dropout_flag_list.append(dropout_flag)
        complexity_list.append(stage_base_difficulty[stage])

    df = pd.DataFrame({
        "level_id": stages,
        "dwell_time": dwell_time_list,
        "dropout_flag": dropout_flag_list,
        "info_complexity": complexity_list
    })
    
    st.sidebar.info("Current mode: Simulated Data")

# ========== Dashboard Tabs ==========
tab1, tab2, tab3 = st.tabs([
    "📊 Cognitive Heatmap",
    "⚠️ Churn Prediction",
    "🔮 Future Directions"
])

# ---- Tab 1: Heatmap ----
with tab1:
    st.subheader("Information Block Attention Distribution")
    fig1 = px.imshow(
        df.pivot_table(index="level_id", values="dwell_time").T,
        labels=dict(x="Block ID", y="", color="Dwell Time (s)"),
        aspect="auto",
        color_continuous_scale="YlOrRd"
    )
    fig1.update_xaxes(tickmode="linear")
    st.plotly_chart(fig1, use_container_width=True)

# ---- Tab 2: Churn ----
with tab2:
    st.subheader("User Retention Trend")
    df["retention_rate"] = 1 - df["dropout_flag"].expanding().mean()
    fig2 = px.line(
        df,
        x="level_id",
        y="retention_rate",
        markers=True,
        labels={"level_id": "Block ID", "retention_rate": "Retention Rate"}
    )
    st.plotly_chart(fig2, use_container_width=True)

    st.markdown("---")
    st.markdown("**🚨 High Risk Churn Points**")
    high_risk = df[df["dropout_flag"] >= 0.5]["level_id"].tolist()
    if high_risk:
        st.warning(f"Significant churn detected at Block(s) {high_risk}")
    else:
        st.success("No significant churn points under current parameters")

# ---- Tab 3: Future Work ----
with tab3:
    st.subheader("Research Roadmap")
    st.markdown("""
    1. **Integrate real-world eye-tracking data**
    2. **Multimodal information flow (Text + Image)**
    3. **Adaptive algorithm for personalized info complexity**
    4. **Cross-device attention transfer study**
    """)
    st.info("This dashboard is a simulation prototype for educational and research purposes.")

# ========== Footer ==========
st.caption("© InfoFlow Simulator · Repo: https://github.com/yc-eagle/infoflow-simulator")
