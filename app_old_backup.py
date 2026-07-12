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

# ========== 侧边栏 ==========
st.sidebar.header("🎛️ 实验参数")
info_complexity = st.sidebar.slider("信息复杂度", 1, 10, 5)
top_n = st.sidebar.slider("显示信息块数量", 5, 20, 10)

# ========== 模拟数据（明天换成真实数据） ==========
np.random.seed(42)
df = pd.DataFrame({
    "block_id": range(1, top_n + 1),
    "dwell_time": np.random.uniform(0.5, 3.0, top_n),
    "dropout_flag": [1 if i > top_n * 0.6 else 0 for i in range(top_n)],
    "info_complexity": [min(10, info_complexity + np.random.randint(-1, 2)) for _ in range(top_n)]
})

# ========== 三页看板 ==========
tab1, tab2, tab3 = st.tabs([
    "📊 认知热力图",
    "⚠️ 流失预警",
    "🔮 未来研究方向"
])

# ---- Tab 1：认知热力图 ----
with tab1:
    st.subheader("信息块关注度分布（模拟数据）")
    fig1 = px.imshow(
        df.pivot_table(index="block_id", values="dwell_time").T,
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
        x="block_id",
        y="retention_rate",
        markers=True,
        labels={"block_id": "信息块编号", "retention_rate": "用户留存率"}
    )
    st.plotly_chart(fig2, use_container_width=True)

    st.markdown("---")
    st.markdown("**🚨 高风险流失点**")
    high_risk = df[df["dropout_flag"] == 1]["block_id"].tolist()
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

