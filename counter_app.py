import streamlit as st
import pandas as pd
from datetime import date

# 页面标题和样式
st.set_page_config(page_title="今日点击挑战", page_icon="🎯", layout="centered")
st.markdown("""
    <style>
        body {
            background-color: #F5E6C8; /* 土黄色 */
            color: #333;
            font-family: Arial, sans-serif;
        }
        .big-text {
            font-size: 2.5rem;
            margin: 2rem 0;
        }
        .counter-number {
            font-size: 4rem;
            font-weight: bold;
        }
        .button {
            font-size: 3.5rem;
            padding: 2rem 4rem;
            background-color: #FFD700;
            border: none;
            border-radius: 10px;
            cursor: pointer;
            margin: 1.5rem;
        }
        
        .reset-button {
            font-size: 1.5rem;
            padding: 0.8rem 1.5rem;
            background-color: #FFA500;
            border: none;
            border-radius: 10px;
            cursor: pointer;
            margin: 1rem;
        }
        .ranking-table {
            margin-top: 2rem;
            border-collapse: collapse;
            width: 100%;
        }
        .ranking-table th, .ranking-table td {
            border: 1px solid #ddd;
            padding: 0.5rem;
            text-align: left;
        }
    </style>
""", unsafe_allow_html=True)

# 初始化 session_state
if "current_count" not in st.session_state:
    st.session_state.current_count = 0
if "today_count" not in st.session_state:
    st.session_state.today_count = 0
if "ranking_data" not in st.session_state:
    st.session_state.ranking_data = pd.DataFrame(columns=["Date", "Total Clicks"])
if "last_date" not in st.session_state:
    st.session_state.last_date = date.today()

# 检查日期是否变化
today = date.today()
if today != st.session_state.last_date:
    st.session_state.current_count = 0
    st.session_state.today_count = 0
    st.session_state.ranking_data = pd.DataFrame(columns=["Date", "Total Clicks"])
    st.session_state.last_date = today

# 页面内容
st.markdown("<div class='big-text'>🎯 今日点击挑战</div>", unsafe_allow_html=True)
st.markdown("<div class='big-text'>看看今天你能点多少次</div>", unsafe_allow_html=True)

# 当前点击次数
st.markdown(f"<div class='counter-number'>{st.session_state.current_count}</div>", unsafe_allow_html=True)

# 今日统计
st.markdown(f"<div class='big-text'>📅 今日总点击次数: {st.session_state.today_count}</div>", unsafe_allow_html=True)

# 点击按钮
if st.button("👉 点我一下", key="click_button", help="点击增加计数"):
    st.session_state.current_count += 1
    st.session_state.today_count += 1
    
    # 更新排行榜
    new_entry = pd.DataFrame([{
        "Date": today.strftime("%Y-%m-%d"),
        "Total Clicks": st.session_state.today_count
    }])
    st.session_state.ranking_data = pd.concat([st.session_state.ranking_data, new_entry], ignore_index=True)
    
    # 显示特殊提示
    if st.session_state.today_count == 10:
        st.success("🎉 刚刚热身！")
    elif st.session_state.today_count == 50:
        st.success("💪 手速不错！")
    elif st.session_state.today_count == 100:
        st.success("🔥 已经上头了！")
    elif st.session_state.today_count >= 200:
        st.success("👑 今天就是点击之王！")

# 重置按钮
if st.button("🔄 重置今天计数", key="reset_button"):
    st.session_state.current_count = 0
    st.session_state.today_count = 0
    st.rerun()

# 每日排行榜
st.markdown("<div class='big-text'>🏆 每日点击排行榜</div>", unsafe_allow_html=True)
st.markdown("<table class='ranking-table'>", unsafe_allow_html=True)
st.markdown("<tr><th>日期</th><th>点击次数</th></tr>", unsafe_allow_html=True)
for _, row in st.session_state.ranking_data.sort_values(by="Total Clicks", ascending=False).head(10).iterrows():
    st.markdown(f"<tr><td>{row['Date']}</td><td>{row['Total Clicks']}</td></tr>", unsafe_allow_html=True)
st.markdown("</table>", unsafe_allow_html=True)

# 说明
st.markdown("""
    <div style='margin-top: 2rem; font-size: 1.2rem;'>
        <p>说明：点击按钮增加计数，今日数据会自动重置。排行榜显示历史最高点击次数。</p>
    </div>
""", unsafe_allow_html=True)