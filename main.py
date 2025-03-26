import streamlit as st
import sys
import os
from datetime import datetime

# 设置页面配置
st.set_page_config(
    page_title="基金分析工具",
    page_icon="📊",
    layout="wide"
)

# 导入UI模块
from ui.components import load_css
from ui.pages import load_favorite_funds

# 加载CSS样式
load_css()

# 初始化session state
if 'favorite_funds' not in st.session_state:
    st.session_state.favorite_funds = {}
if 'show_toast' not in st.session_state:
    st.session_state.show_toast = None

# 加载自选基金数据
if len(st.session_state.favorite_funds) == 0:
    st.session_state.favorite_funds = load_favorite_funds()

# 显示提示信息
if st.session_state.show_toast:
    st.toast(st.session_state.show_toast["message"], icon=st.session_state.show_toast["icon"])
    st.session_state.show_toast = None

# 主页内容
st.markdown("<h1 style='text-align: center; margin-top: 2rem;'>📊 基金分析工具</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 1.2rem;'>一站式基金分析与管理平台</p>", unsafe_allow_html=True)

# 修改侧边栏名称
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
    /* 确保侧边栏始终可见 */
    [data-testid="stSidebar"] {
        display: block !important;
    }
    /* 首页卡片样式 */
    .feature-container {
        display: flex;
        flex-wrap: wrap;
        justify-content: center;
        gap: 1.5rem;
        margin-top: 2rem;
    }
    .feature-card {
        background-color: white;
        border-radius: 10px;
        padding: 1.5rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        width: 280px;
        transition: transform 0.3s, box-shadow 0.3s;
        text-align: center;
    }
    .feature-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 20px rgba(0, 0, 0, 0.15);
    }
    .feature-icon {
        font-size: 2.5rem;
        margin-bottom: 1rem;
    }
    .feature-title {
        font-size: 1.3rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
    }
    .feature-description {
        color: #666;
        font-size: 0.9rem;
    }
    .center-btn {
        display: flex;
        justify-content: center;
        margin-top: 0.5rem;
    }
    .stMarkdown pre {
        display: none;  /* 隐藏代码框 */
    }
</style>
""", unsafe_allow_html=True)

# 创建两行功能卡片
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">🔍</div>
        <div class="feature-title">基金查询</div>
        <p class="feature-description">查询基金详情、历史净值、业绩表现及风险评估</p>
        <div class="center-btn">
            <a href="/基金查询" target="_self">
                <button style="background-color: #4CAF50; color: white; border: none; padding: 8px 16px; border-radius: 4px; cursor: pointer;">立即查询</button>
            </a>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">⭐</div>
        <div class="feature-title">自选基金</div>
        <p class="feature-description">管理您关注的基金，快速查看最新动态和表现</p>
        <div class="center-btn">
            <a href="/自选基金" target="_self">
                <button style="background-color: #2196F3; color: white; border: none; padding: 8px 16px; border-radius: 4px; cursor: pointer;">前往自选</button>
            </a>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
with col3:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">📈</div>
        <div class="feature-title">基金持仓</div>
        <p class="feature-description">记录您的基金持仓情况，分析投资组合表现</p>
        <div class="center-btn">
            <a href="/基金持仓" target="_self">
                <button style="background-color: #FF9800; color: white; border: none; padding: 8px 16px; border-radius: 4px; cursor: pointer;">管理持仓</button>
            </a>
        </div>
    </div>
    """, unsafe_allow_html=True)

# 添加垂直间距
st.markdown("<div style='height: 30px;'></div>", unsafe_allow_html=True)

# 第二行功能卡片  
col4, col5, col6 = st.columns(3)

with col4:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">🔄</div>
        <div class="feature-title">基金比较</div>
        <p class="feature-description">多基金对比分析，助您找出最适合的投资标的</p>
        <div class="center-btn">
            <a href="/基金比较" target="_self">
                <button style="background-color: #9C27B0; color: white; border: none; padding: 8px 16px; border-radius: 4px; cursor: pointer;">开始对比</button>
            </a>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
with col5:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">📆</div>
        <div class="feature-title">投资计划</div>
        <p class="feature-description">制定基金定投计划，模拟不同策略的投资收益</p>
        <div class="center-btn">
            <a href="/基金投资计划" target="_self">
                <button style="background-color: #E91E63; color: white; border: none; padding: 8px 16px; border-radius: 4px; cursor: pointer;">规划投资</button>
            </a>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
with col6:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-icon">🚀</div>
        <div class="feature-title">更多功能</div>
        <p class="feature-description">探索更多正在开发的高级功能和分析工具</p>
        <div class="center-btn">
            <a href="/待开发" target="_self">
                <button style="background-color: #607D8B; color: white; border: none; padding: 8px 16px; border-radius: 4px; cursor: pointer;">了解更多</button>
            </a>
        </div>
    </div>
    """, unsafe_allow_html=True)

# 页脚
st.markdown("""
<div style='text-align: center; margin-top: 4rem; padding: 1rem; color: #666; font-size: 0.8rem;'>
    <p>© 2025 基金分析工具 | 制作者：Brisbane Huang | 当前版本: 2.1.1</p>
    <p>本工具仅供学习和参考，不构成任何投资建议</p>
</div>
""", unsafe_allow_html=True)