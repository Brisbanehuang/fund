import streamlit as st
import sys
import os
import json
from datetime import datetime

# 设置页面配置
st.set_page_config(
    page_title="自选基金 | 基金分析工具",
    page_icon="📊",
    layout="wide"
)

# 导入UI模块
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from ui.components import load_css, display_fund_analysis
from ui.pages import favorite_funds_page, load_favorite_funds
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
if 'show_fund_detail' not in st.session_state:
    st.session_state.show_fund_detail = False

# 加载自选基金数据
if len(st.session_state.favorite_funds) == 0:
    st.session_state.favorite_funds = load_favorite_funds()

# 显示提示信息
if st.session_state.show_toast:
    st.toast(st.session_state.show_toast["message"], icon=st.session_state.show_toast["icon"])
    st.session_state.show_toast = None

# 隐藏警告信息
st.markdown("""
<style>
.stException, .stWarning {
    display: none;
}
</style>
""", unsafe_allow_html=True)

# 获取URL参数来查看是否需要显示详情
params = st.query_params
detail_code = params.get("detail", "")

if detail_code:
    st.session_state.detail_fund_code = detail_code
    st.session_state.show_fund_detail = True
elif "detail" in params:
    # 如果参数存在但为空，返回到列表页面
    st.session_state.show_fund_detail = False
    st.query_params.clear()

# 保存自选基金数据
def save_favorite_funds():
    """保存自选基金数据到本地文件"""
    file_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "favorite_funds.json")
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(st.session_state.favorite_funds, f, ensure_ascii=False)

# 设置当前视图
st.session_state.current_view = "favorite_funds"

# 基金详情显示函数
def show_fund_detail(fund_code):
    try:
        # 获取基金数据
        with st.spinner("正在获取基金数据..."):
            df = get_fund_data(fund_code)
            fund_info = get_fund_info(fund_code)
        
        # 显示基金名称作为标题 - 确保基金名称正确
        fund_name = fund_info.get('fund_name', f'基金 {fund_code}')
        # 清理基金名称中的代码部分
        if '(' in fund_name:
            fund_name = fund_name.split('(')[0]
        elif '（' in fund_name:
            fund_name = fund_name.split('（')[0]
            
        st.markdown(f'<h1 class="main-header">{fund_name}</h1>', unsafe_allow_html=True)
        
        # 添加返回按钮
        if st.button("← 返回自选基金列表"):
            st.session_state.show_fund_detail = False
            st.query_params.clear()
            st.rerun()
        
        # 检查基金是否在自选中
        is_favorite = fund_code in st.session_state.favorite_funds
        col1, col2 = st.columns([6, 1])
        with col2:
            if is_favorite:
                if st.button("移出自选", use_container_width=True):
                    del st.session_state.favorite_funds[fund_code]
                    save_favorite_funds()
                    st.session_state.show_toast = {"message": "已从自选中移除！", "icon": "✅"}
                    st.session_state.show_fund_detail = False
                    st.query_params.clear()
                    st.rerun()
            else:
                if st.button("加入自选", use_container_width=True):
                    # 重新获取最新的基金信息
                    last_update_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    
                    # 保存到自选基金
                    st.session_state.favorite_funds[fund_code] = {
                        'fund_info': fund_info,
                        'last_update': last_update_time
                    }
                    save_favorite_funds()
                    st.session_state.show_toast = {"message": f"基金 {fund_code} 已添加到自选！", "icon": "✅"}
                    st.rerun()
        
        if not df.empty:
            # 显示基金分析内容
            display_fund_analysis(df, fund_info)
        else:
            st.error("未能获取到基金数据，请检查基金代码是否正确。")
            
    except Exception as e:
        st.error(f"发生错误: {str(e)}")

# 显示页面内容
if st.session_state.show_fund_detail and st.session_state.detail_fund_code:
    show_fund_detail(st.session_state.detail_fund_code)
else:
    # 显示自选基金列表
    favorite_funds_page() 