import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# ========== 页面设置 ==========
st.set_page_config(
    page_title="InfoFlow Simulator",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ========== 全局参数（与第一段数据生成脚本完全对齐） ==========
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

# ========== 侧边栏 ==========
st.sidebar.header("🎛️ 实验参数 ")
info_complexity = st.sidebar.slider("信息复杂度（模拟模式生效）", 1, 5, 3)
top_n = st.sidebar.slider("显示信息块数量", 1, 5, 5)

st.sidebar.markdown("---")
st.sidebar.subheader("📂 数据来源")
uploaded_file = st.sidebar.file_uploader("上传行为日志 CSV", type="csv")

# ========== 数据加载逻辑：上传文件优先，无文件则用模拟数据 ==========
if uploaded_file is not None:
    # 读取上传的 CSV 文件
    raw_df = pd.read_csv(uploaded_file)
    required_cols = ["user_id", "level_id", "action_type", "dwell_time", "dropout_flag"]
    
    # 字段校验
    if not all(col in raw_df.columns for col in required_cols):
        st.sidebar.error("CSV 字段不匹配，请确保包含：user_id, level_id, action_type, dwell_time, dropout_flag")
        use_simulation = True
    else:
        use_simulation = False
        
        # 按阶段聚合统计，对齐看板所需字段结构
        # 1. 每个阶段的平均停留时间
        stage_dwell = (
            raw_df.groupby("level_id")["dwell_time"]
            .mean()
            .round(2)
            .reset_index()
        )
        
        # 2. 每个阶段的流失率（仅统计 exit 行为）
        exit_df = raw_df[raw_df["action_type"] == "exit"]
        stage_dropout = (
            exit_df.groupby("level_id")["dropout_flag"]
            .mean()
            .reset_index()
        )
        
        # 3. 阶段难度映射
        stage_difficulty = pd.DataFrame({
            "level_id": list(stage_base_difficulty.keys()),
            "info_complexity": list(stage_base_difficulty.values())
        })
        
        # 合并成最终看板数据
        df = (
            stage_dwell
            .merge(stage_dropout, on="level_id")
            .merge(stage_difficulty, on="level_id")
            .sort_values("level_id")
            .reset_index(drop=True)
        )
        
        # 按滑块限制显示数量
        df = df.head(top_n)
        
        st.sidebar.success(
            f"已加载真实日志\n"
            f"总记录数：{len(raw_df)} 条\n"
            f"覆盖阶段：{df['level_id'].min()} ~ {df['level_id'].max()}"
        )
else:
    use_simulation = True

# 模拟数据生成（与第一段参数完全一致）
if use_simulation:
    np.random.seed(RANDOM_SEED)
    display_stage = min(top_n, MAX_STAGE)
    stages = list(range(1, display_stage + 1))

    dwell_time_list = []
    dropout_flag_list = []
    complexity_list = []

    for stage in stages:
        # 停留时间公式与生成脚本完全对齐
        base_dwell = BASE_DWELL_TIME * (1 + stage_base_difficulty[stage] * 0.8)
        dwell = np.random.normal(loc=base_dwell, scale=0.5)
        dwell_time_list.append(round(max(0.3, dwell), 2))
        
        # 流失规则：阶段高于复杂度阈值则标记流失
        dropout_flag = 1 if stage > info_complexity else 0
        dropout_flag_list.append(dropout_flag)
        
        complexity_list.append(stage_base_difficulty[stage])

    df = pd.DataFrame({
        "level_id": stages,
        "dwell_time": dwell_time_list,
        "dropout_flag": dropout_flag_list,
        "info_complexity": complexity_list
    })
    
    st.sidebar.info("当前使用：模拟生成数据")

# ========== 三页看板（原有功能完整保留） ==========
tab1, tab2, tab3 = st.tabs([
    "📊 认知热力图",
    "⚠️ 流失预警",
    "🔮 未来研究方向"
])

# ---- Tab 1：认知热力图 ----
with tab1:
    st.subheader("信息块关注度分布")
    fig1 = px.imshow(
        df.pivot_table(index="level_id", values="dwell_time").T,
        labels=dict(x="信息块编号", y="", color="停留时长（秒）"),
        aspect="auto",
        color_continuous_scale="YlOrRd"
    )
    fig1.update_xaxes(tickmode="linear")
    st.plotly_chart(fig1, use_container_width=True)

# ---- Tab 2：流失预警 ----
with tab2:
    st.subheader("用户流失趋势")
    df["retention_rate"] = 1 - df["dropout_flag"].expanding().mean()
    fig2 = px.line(
        df,
        x="level_id",
        y="retention_rate",
        markers=True,
        labels={"level_id": "信息块编号", "retention_rate": "用户留存率"}
    )
    st.plotly_chart(fig2, use_container_width=True)

    st.markdown("---")
    st.markdown("**🚨 高风险流失点**")
    high_risk = df[df["dropout_flag"] >= 0.5]["level_id"].tolist()
    if high_risk:
        st.warning(f"信息块 {high_risk} 出现明显流失")
    else:
        st.success("当前参数下无明显流失点")

# ---- Tab 3：未来方向 ----
with tab3:
    st.subheader("研究拓展蓝图")
    st.markdown("""
    1. **引入真实用户眼动数据**
    2. **多模态信息流（文本 + 图像）**
    3. **个性化信息复杂度自适应算法**
    4. **跨设备注意力迁移研究**
    """)
    st.info("本看板为模拟演示，用于教学与研究原型展示")

# ========== 底部声明 ==========
st.caption("© InfoFlow Simulator · 项目仓库：https://github.com/yc-eagle/infoflow-simulator")