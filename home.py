"""
home.py

Streamlit 首页：展示团队信息、目标受众与示例 KPI 占位。

自动生成自 README.md 中的项目说明（摘自 README，详见仓库）。
"""

import streamlit as st

# 页面配置
st.set_page_config(page_title="team7 — Hotel Booking Cancellation Dashboard", layout="wide")

# 顶部头部
st.title("team7 — Hotel Booking Cancellation Dashboard")
st.markdown("---")

# 团队信息侧边栏
with st.sidebar:
    st.header("团队信息")
    st.markdown("**团队名：** team7")
    st.markdown("**成员：** Li xirun, Li yifei, Sun chengyu, Wang xibei")
    st.markdown("---")
    st.markdown("## 数据集与说明")
    st.markdown("数据集：Hotel Booking Demand（Kaggle）\n\n有关数据集与设计决策的详细信息，请查看仓库根目录下的 README.md。")

# 目标受众与使用场景
st.header("为谁而建")
st.markdown(
    """
    本仪表盘的主要受众是：**酒店收益经理（Revenue Manager）**。

    他们的职责包括定价、房量配额与超售控制。当某个市场细分（渠道）的取消率显著高于整体平均时，收益经理
    需要快速调整该渠道的配额或押金策略，以减少空房损失。

    使用频率与节奏：收益经理通常在**每周一**审阅数据并制定下阶段配额计划；数据建议**每日刷新**以保证信息的时效性。
    详细的背景、展示范围和数据陷阱均记录在 README.md 中。"""
)

st.markdown("---")

# 示例 KPI 区（占位）
st.header("头条 KPI（示例占位）")
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("总取消率", "-- %", delta="--")
with col2:
    st.metric("平均日房价 (ADR)", "--", delta="--")
with col3:
    st.metric("总预订量", "--", delta="--")

st.info("这些 KPI 目前为占位显示。把数据加载到项目中的数据处理模块后，这里会显示实时计算的数值。")

# 支撑图表说明（占位）
st.header("支撑图表（示例占位）")
st.markdown("1. 取消率月度趋势 —— 用于观察旺季/淡季的取消行为差异。\n2. 各市场细分取消率对比 —— 用于定位可能的问题渠道。")
st.warning("真实图表需要先在 `hotel_bookings.csv` 上完成预处理与聚合。")

# 运行提示
st.markdown("---")
st.subheader("如何运行")
st.markdown(
    "在项目根目录下运行：\n\n```bash\npip install -r requirements.txt  # 若有 requirements.txt，安装依赖\nstreamlit run home.py\n```\n\n若需要我把示例图表和数据加载代码也补上，可以告诉我你希望的图表（例如折线图、柱状图），我会继续实现。"
)

# 页脚备注
st.markdown("---")
st.caption("说明：更多关于数据来源、决策者、展示范围、刷新频率与数据陷阱的信息，请参阅 README.md（仓库根目录）。")
