"""
Hotel Booking Cancellation Dashboard
面向酒店收益经理（Revenue Manager）的取消率决策看板
"""

import streamlit as st
import pandas as pd

# ---------------------------------------------------------------------------
# 页面配置
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="酒店预订取消看板",
    page_icon="🏨",
    layout="wide",
)

# ---------------------------------------------------------------------------
# 数据加载与清洗
# ---------------------------------------------------------------------------
@st.cache_data
def load_data(path: str = "hotel_bookings.csv") -> pd.DataFrame:
    def load_data(path: str = "hotel_bookings.csv"):


    # ---- 清洗 1：ADR 异常值 ----
    # 原始数据中 adr 存在负值和极端值（如 5400），会严重拉高均值
    df = df[(df["adr"] >= 0) & (df["adr"] < 1000)]

    # ---- 清洗 2：构造标准月份时间戳，便于时间序列 ----
    month_map = {
        "January": 1, "February": 2, "March": 3, "April": 4,
        "May": 5, "June": 6, "July": 7, "August": 8,
        "September": 9, "October": 10, "November": 11, "December": 12,
    }
    df["arrival_month_num"] = df["arrival_date_month"].map(month_map)
    df["arrival_date"] = pd.to_datetime(
        dict(
            year=df["arrival_date_year"],
            month=df["arrival_month_num"],
            day=df["arrival_date_day_of_month"],
        ),
        errors="coerce",
    )

    return df


df = load_data()

# ---------------------------------------------------------------------------
# 标题与说明
# ---------------------------------------------------------------------------
st.title("🏨 酒店预订取消看板 —— 【团队名】")
st.caption(
    "面向 **酒店收益经理（Revenue Manager）**，支持'按渠道调整房量配额与押金政策'的决策。"
)

# ---------------------------------------------------------------------------
# 过滤器：只放决策者真正需要的
# ---------------------------------------------------------------------------
col_f1, col_f2 = st.columns(2)

with col_f1:
    hotel_choice = st.selectbox(
        "酒店类型",
        options=sorted(df["hotel"].unique()),
        help="City Hotel 与 Resort Hotel 的经营逻辑完全不同，分开看才有意义。",
    )

# 先按酒店类型过滤一次，供第二个过滤器选项
df_hotel = df[df["hotel"] == hotel_choice]

with col_f2:
    segment_choice = st.multiselect(
        "市场细分（Market Segment）",
        options=sorted(df_hotel["market_segment"].dropna().unique()),
        default=sorted(df_hotel["market_segment"].dropna().unique()),
        help="收益经理能动的就是不同渠道的房量配额，所以这是最相关的维度。",
    )

# 应用过滤
d = df_hotel[df_hotel["market_segment"].isin(segment_choice)]

if d.empty:
    st.warning("当前筛选条件下没有数据，请调整过滤器。")
    st.stop()

# ---------------------------------------------------------------------------
# 头条 KPI（≤3 个，5 秒内看完）
# ---------------------------------------------------------------------------
c1, c2, c3 = st.columns(3)

c1.metric("总取消率", f"{d['is_canceled'].mean():.1%}")
c2.metric("平均日房价（ADR）", f"€{d['adr'].mean():.2f}")
c3.metric("总预订量", f"{len(d):,}")

st.divider()

# ---------------------------------------------------------------------------
# 支撑图 1：取消率月度趋势
# ---------------------------------------------------------------------------
st.subheader("① 取消率月度趋势")
st.caption("解释头条数字为什么会波动 —— 旺季/淡季的取消行为差异明显。")

trend = (
    d.dropna(subset=["arrival_date"])
    .assign(month=d["arrival_date"].dt.to_period("M").astype(str))
    .groupby("month")["is_canceled"]
    .mean()
)
st.line_chart(trend, y_label="取消率")

# ---------------------------------------------------------------------------
# 支撑图 2：按市场细分的取消率
# ---------------------------------------------------------------------------
st.subheader("② 各市场细分取消率对比")
st.caption("找出'问题渠道'——收益经理据此调整配额或押金政策。")

seg = (
    d.groupby("market_segment")["is_canceled"]
    .mean()
    .sort_values(ascending=False)
)
st.bar_chart(seg, y_label="取消率")

# ---------------------------------------------------------------------------
# 底部：明细表（给想深挖的人）
# ---------------------------------------------------------------------------
with st.expander("📋 查看原始明细数据（前 500 行）"):
    st.dataframe(
        d[
            [
                "hotel", "arrival_date", "market_segment",
                "lead_time", "adr", "is_canceled",
            ]
        ].head(500),
        use_container_width=True,
    )

# ---------------------------------------------------------------------------
# 数据说明（Step 4 要求）
# ---------------------------------------------------------------------------
st.divider()
st.caption(
    "**数据来源：** Kaggle – Hotel Booking Demand (hotel_bookings.csv) ｜ "
    "**数据区间：** 2015-07 – 2017-08（Kaggle 快照）｜ "
    "**生产环境刷新频率：** 每日刷新，收益经理每周一审阅；"
    "当某渠道周取消率超历史均值 15% 时触发邮件告警。"
)
st.caption(
    "⚠️ 注：原始数据中 `children`、`company`、`agent` 存在缺失值；"
    "`adr` 已剔除负值与 ≥1000 的异常值；数据截至 2017 年，不代表当前市场。"
)
