import streamlit as st
import sys
import os
import json
from datetime import datetime

# 设置页面配置
st.set_page_config(
    page_title="基金查询 | 基金分析工具",
    page_icon="📊",
    layout="wide"
)

# 导入UI模块
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from ui.components import load_css
from ui.pages import fund_query_page, load_favorite_funds
from src.fund_data import get_fund_data, get_fund_info

# 加载CSS样式
load_css()

# 修改侧边栏主页名称
st.markdown("""
<style>
    /* 使用更精确的选择器确保修改"main"为"主页" */
    [data-testid="stSidebarNav"] li:first-child span {
        visibility: hidden;
        position: relative;
    }
    [data-testid="stSidebarNav"] li:first-child span::after {
        content: "主页";
        visibility: visible;
        position: absolute;
        left: 0;
    }
</style>
""", unsafe_allow_html=True)

# 初始化session state
if 'fund_code' not in st.session_state:
    st.session_state.fund_code = ''
if 'fund_data' not in st.session_state:
    st.session_state.fund_data = None
if 'start_date' not in st.session_state:
    st.session_state.start_date = None
if 'end_date' not in st.session_state:
    st.session_state.end_date = None
if 'favorite_funds' not in st.session_state:
    st.session_state.favorite_funds = {}
if 'current_view' not in st.session_state:
    st.session_state.current_view = None
if 'previous_fund_code' not in st.session_state:
    st.session_state.previous_fund_code = None
if 'show_toast' not in st.session_state:
    st.session_state.show_toast = None
if 'detail_fund_code' not in st.session_state:
    st.session_state.detail_fund_code = None

# 加载自选基金数据
if len(st.session_state.favorite_funds) == 0:
    st.session_state.favorite_funds = load_favorite_funds()

# 显示提示信息
if st.session_state.show_toast:
    st.toast(st.session_state.show_toast["message"], icon=st.session_state.show_toast["icon"])
    st.session_state.show_toast = None

# 设置当前视图
st.session_state.current_view = "fund_query"

# 显示基金查询页面
fund_query_page() 