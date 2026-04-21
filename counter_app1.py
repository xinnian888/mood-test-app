import streamlit as st
import pandas as pd
from datetime import date

st.set_page_config(
    page_title="今日点击挑战",
    page_icon="🎯",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# -----------------------------
# 页面样式
# -----------------------------
st.markdown(
    """
    <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no">
    <style>
        html, body, [data-testid="stAppViewContainer"] {
            background-color: #d8bf8a;
            overscroll-behavior: none;
            touch-action: manipulation;
        }

        [data-testid="stHeader"] {
            background: rgba(0,0,0,0);
        }

        [data-testid="stAppViewContainer"] > .main {
            padding-top: 1.5rem;
            padding-bottom: 2rem;
        }

        .main-wrap {
            max-width: 760px;
            margin: 0 auto;
            text-align: center;
        }

        .title-text {
            font-size: 2.4rem;
            font-weight: 800;
            color: #2f2416;
            margin-bottom: 0.4rem;
            line-height: 1.2;
        }

        .sub-text {
            font-size: 1.2rem;
            color: #4d3b22;
            margin-bottom: 1.4rem;
            line-height: 1.5;
        }

        .count-label {
            font-size: 1.2rem;
            color: #5a4323;
            margin-top: 0.5rem;
            margin-bottom: 0.2rem;
            font-weight: 700;
        }

        .count-number {
            font-size: 5.2rem;
            font-weight: 900;
            color: #1f1408;
            line-height: 1;
            margin-bottom: 0.6rem;
        }

        .today-count {
            font-size: 1.25rem;
            color: #3d2d17;
            margin-bottom: 1rem;
            font-weight: 700;
        }

        .tip-box {
            background: rgba(255,255,255,0.35);
            border-radius: 18px;
            padding: 0.9rem 1rem;
            margin: 0.8rem auto 1.2rem auto;
            color: #3b2a14;
            font-size: 1.15rem;
            font-weight: 700;
            max-width: 520px;
        }

        div.stButton > button {
            width: 100%;
            min-height: 95px;
            font-size: 2rem;
            font-weight: 800;
            border-radius: 20px;
            border: none;
            background: #f4b942;
            color: #2b1d0b;
            box-shadow: 0 6px 0 rgba(120, 77, 16, 0.35);
            transition: transform 0.05s ease, box-shadow 0.05s ease, background 0.2s ease;
            touch-action: manipulation;
        }

        div.stButton > button:hover {
            background: #f1b02b;
        }

        div.stButton > button:active {
            transform: translateY(3px);
            box-shadow: 0 3px 0 rgba(120, 77, 16, 0.35);
        }

        .section-title {
            font-size: 1.6rem;
            font-weight: 800;
            color: #2f2416;
            margin-top: 1.5rem;
            margin-bottom: 0.8rem;
            text-align: center;
        }

        .small-note {
            margin-top: 1rem;
            font-size: 1rem;
            color: #4f3d24;
            line-height: 1.6;
            text-align: center;
        }

        /* 数据表字体稍微大一点 */
        [data-testid="stDataFrame"] div {
            font-size: 1rem !important;
        }

        /* 手机端进一步放大 */
        @media (max-width: 768px) {
            .title-text {
                font-size: 2rem;
            }

            .sub-text {
                font-size: 1.05rem;
            }

            .count-number {
                font-size: 4.6rem;
            }

            div.stButton > button {
                min-height: 88px;
                font-size: 1.8rem;
            }
        }
    </style>

    <script>
        // 尽量减少双击放大
        let lastTouchEnd = 0;
        document.addEventListener('touchend', function (event) {
            const now = (new Date()).getTime();
            if (now - lastTouchEnd <= 300) {
                event.preventDefault();
            }
            lastTouchEnd = now;
        }, { passive: false });

        // 禁止双击缩放
        document.addEventListener('dblclick', function(event) {
            event.preventDefault();
        }, { passive: false });
    </script>
    """,
    unsafe_allow_html=True
)

# -----------------------------
# 初始化状态
# -----------------------------
today = date.today().strftime("%Y-%m-%d")

if "last_date" not in st.session_state:
    st.session_state.last_date = today

if "current_count" not in st.session_state:
    st.session_state.current_count = 0

if "today_count" not in st.session_state:
    st.session_state.today_count = 0

# 用 dict 存排行榜，速度比每次 concat DataFrame 更轻
if "ranking_dict" not in st.session_state:
    st.session_state.ranking_dict = {}

# 跨天自动重置今日数据
if st.session_state.last_date != today:
    st.session_state.current_count = 0
    st.session_state.today_count = 0
    st.session_state.last_date = today

# 确保今天在排行榜里有记录
if today not in st.session_state.ranking_dict:
    st.session_state.ranking_dict[today] = st.session_state.today_count


# -----------------------------
# 提示语函数
# -----------------------------
def get_tip(clicks: int) -> str:
    if clicks >= 200:
        return "👑 今天就是点击之王"
    elif clicks >= 100:
        return "🔥 已经上头了"
    elif clicks >= 50:
        return "💪 手速不错"
    elif clicks >= 10:
        return "🎉 刚刚热身"
    else:
        return "👉 先点起来再说"


# -----------------------------
# 页面主结构
# -----------------------------
st.markdown("<div class='main-wrap'>", unsafe_allow_html=True)

st.markdown("<div class='title-text'>🎯 今日点击挑战</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-text'>看看今天你能点多少次</div>", unsafe_allow_html=True)

count_placeholder = st.empty()
today_placeholder = st.empty()
tip_placeholder = st.empty()

count_placeholder.markdown(
    f"""
    <div class='count-label'>当前点击次数</div>
    <div class='count-number'>{st.session_state.current_count}</div>
    """,
    unsafe_allow_html=True
)

today_placeholder.markdown(
    f"<div class='today-count'>📅 今日日期：{today}　｜　今日总点击：{st.session_state.today_count}</div>",
    unsafe_allow_html=True
)

tip_placeholder.markdown(
    f"<div class='tip-box'>{get_tip(st.session_state.today_count)}</div>",
    unsafe_allow_html=True
)

# 两个按钮并排，手机上也好点
col1, col2 = st.columns([3, 2], gap="small")

with col1:
    if st.button("👉 点我一下", use_container_width=True):
        st.session_state.current_count += 1
        st.session_state.today_count += 1
        st.session_state.ranking_dict[today] = st.session_state.today_count
        st.rerun()

with col2:
    if st.button("🔄 重置今天计数", use_container_width=True):
        st.session_state.current_count = 0
        st.session_state.today_count = 0
        st.session_state.ranking_dict[today] = 0
        st.rerun()

# 排行榜
st.markdown("<div class='section-title'>🏆 每日点击排行榜</div>", unsafe_allow_html=True)

ranking_df = pd.DataFrame(
    [{"日期": k, "点击次数": v} for k, v in st.session_state.ranking_dict.items()]
).sort_values(by="点击次数", ascending=False)

if not ranking_df.empty:
    st.dataframe(
        ranking_df,
        use_container_width=True,
        hide_index=True
    )
else:
    st.info("当前还没有排行榜数据")

st.markdown(
    """
    <div class='small-note'>
        说明：点击按钮增加计数，日期变化后会自动开始新的一天。<br>
        当前版本已经尽量优化了点击体验，但原生 Streamlit 仍然是“点一次重跑一次”，所以它会比纯前端页面更慢一点。
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown("</div>", unsafe_allow_html=True)