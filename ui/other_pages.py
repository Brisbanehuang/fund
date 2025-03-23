import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime
from src.fund_data import get_fund_data, get_fund_info
import random

def fund_compare_page():
    """基金比较页面"""
    st.markdown('<h1 class="main-header">基金比较</h1>', unsafe_allow_html=True)
    
    # 初始化session state用于存储基金比较数据
    if 'compare_funds' not in st.session_state:
        st.session_state.compare_funds = []
    if 'compare_start_date' not in st.session_state:
        st.session_state.compare_start_date = None
    if 'compare_end_date' not in st.session_state:
        st.session_state.compare_end_date = None
    
    # 加载自选基金数据
    # 每次进入页面都重新加载最新的自选基金数据
    from ui.pages import load_favorite_funds
    favorite_funds = load_favorite_funds()
    st.session_state.favorite_funds = favorite_funds
    print(f"基金比较页面加载自选基金数据，共 {len(favorite_funds)} 支基金")
    
    # 选择投资区间部分
    st.markdown('<h2 class="section-header">设置投资区间</h2>', unsafe_allow_html=True)
    date_cols = st.columns(2)
    
    # 获取当前日期作为默认结束日期
    today = datetime.now().date()
    
    with date_cols[0]:
        start_date = st.date_input(
            "开始日期",
            value=st.session_state.compare_start_date or today,
            key="compare_start_date_input"
        )
    with date_cols[1]:
        end_date = st.date_input(
            "结束日期",
            value=st.session_state.compare_end_date or today,
            key="compare_end_date_input"
        )
    
    # 快速选择投资区间
    st.markdown("#### 快速选择投资区间")
    period_cols = st.columns(7)
    periods = {
        "近一周": 7,
        "近一月": 30,
        "近三月": 90,
        "近半年": 180,
        "近一年": 365,
        "近两年": 730,
        "近三年": 1095
    }
    
    def update_date_range(days):
        # 使用当前日期作为结束日期
        end_date = datetime.now().date()
        # 计算开始日期
        from datetime import timedelta
        start_date = end_date - timedelta(days=days)
        # 更新session state
        st.session_state.compare_start_date = start_date
        st.session_state.compare_end_date = end_date
        # 重新加载页面以应用新的日期范围
        st.rerun()
    
    for i, (period_name, days) in enumerate(periods.items()):
        with period_cols[i]:
            if st.button(period_name, key=f"compare_period_{days}"):
                update_date_range(days)
    
    # 保存选择的日期范围到session state
    st.session_state.compare_start_date = start_date
    st.session_state.compare_end_date = end_date
    
    # 基金选择部分
    st.markdown('<h2 class="section-header">选择基金进行比较</h2>', unsafe_allow_html=True)
    
    # 添加两个默认的基金输入框
    if len(st.session_state.compare_funds) == 0:
        st.session_state.compare_funds = ["", ""]
    
    # 生成随机颜色函数
    def get_random_color():
        colors = [
            '#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', 
            '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf'
        ]
        return random.choice(colors)
    
    # 显示基金输入框
    fund_inputs = []
    
    # 添加自定义CSS样式，确保按钮和输入框严格对齐
    st.markdown("""
    <style>
    /* 输入框和按钮对齐样式 */
    button {
        height: 2.4rem !important;  /* 固定按钮高度 */
        line-height: 1.6 !important;
        margin-top: 0 !important;
        margin-bottom: 0 !important;
    }
    /* 输入框调整 */
    div[data-testid="stTextInput"] > div > div > input {
        height: 2.4rem !important;  /* 固定输入框高度 */
        line-height: 2.4rem !important;
        margin-bottom: 0 !important;
        margin-top: 0 !important;
    }
    div[data-testid="column"] {
        padding: 0.25rem !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    for i, fund_code in enumerate(st.session_state.compare_funds):
        # 添加标签行，为每个基金输入框添加标签
        st.markdown(f"**基金代码 #{i+1}**")
        
        # 使用容器确保一行内布局一致
        with st.container():
            fund_row = st.columns([4, 1, 1])
            with fund_row[0]:
                fund_inputs.append(st.text_input(f"基金代码输入框 #{i+1}", value=fund_code, key=f"fund_code_{i}", label_visibility="collapsed"))
            
            with fund_row[1]:
                if st.button("从自选中选择", key=f"favorite_{i}", use_container_width=True):
                    st.session_state[f"show_favorite_modal_{i}"] = True
            
            with fund_row[2]:
                if len(st.session_state.compare_funds) > 2:
                    if st.button("删除", key=f"remove_{i}", use_container_width=True):
                        st.session_state.compare_funds.pop(i)
                        st.rerun()
                else:
                    # 占位空间，保持对齐
                    st.write("&nbsp;", unsafe_allow_html=True)
        
        # 添加一点空间在行与行之间
        st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
    
    # 显示自选基金选择模态窗口
    for i in range(len(st.session_state.compare_funds)):
        if st.session_state.get(f"show_favorite_modal_{i}", False):
            with st.expander("从自选基金中选择", expanded=True):
                # 确保自选基金数据已正确加载
                if not st.session_state.favorite_funds or len(st.session_state.favorite_funds) == 0:
                    print("警告：自选基金数据为空或未正确加载")
                    st.info('您还没有添加任何自选基金，请先在"基金查询"页面添加基金到自选')
                else:
                    print(f"显示自选基金选择，共 {len(st.session_state.favorite_funds)} 支基金")
                    # 创建多列布局显示自选基金
                    cols_per_row = 3
                    funds = list(st.session_state.favorite_funds.items())
                    
                    for j in range(0, len(funds), cols_per_row):
                        cols = st.columns(cols_per_row)
                        for k in range(cols_per_row):
                            if j + k < len(funds):
                                fund_code, fund_data = funds[j + k]
                                fund_name = fund_data['fund_info'].get('fund_name', '未知基金')
                                # 截断长名称
                                if len(fund_name) > 15:
                                    fund_name = fund_name[:15] + "..."
                                
                                with cols[k]:
                                    if st.button(f"{fund_name}\n{fund_code}", key=f"select_fund_{i}_{j+k}"):
                                        # 选择该基金并关闭模态窗口
                                        st.session_state.compare_funds[i] = fund_code
                                        st.session_state[f"show_favorite_modal_{i}"] = False
                                        st.rerun()
                
                # 添加关闭按钮
                if st.button("关闭", key=f"close_modal_{i}"):
                    st.session_state[f"show_favorite_modal_{i}"] = False
                    st.rerun()
    
    # 添加按钮
    if st.button("+ 添加另一个基金进行比较"):
        st.session_state.compare_funds.append("")
        st.rerun()
    
    # 比较按钮
    if st.button("开始比较", type="primary"):
        if not all(fund_inputs):
            st.error("请填写所有基金代码")
        else:
            # 更新session state中的基金代码
            st.session_state.compare_funds = fund_inputs
            # 显示比较结果
            st.markdown('<h2 class="section-header">基金收益率比较</h2>', unsafe_allow_html=True)
            
            # 收集所有基金的数据
            fund_data = {}
            fund_info = {}
            valid_funds = []
            
            # 创建进度条
            progress_bar = st.progress(0)
            
            for i, fund_code in enumerate(fund_inputs):
                if fund_code:
                    try:
                        with st.spinner(f"正在获取基金 {fund_code} 数据..."):
                            # 获取基金数据
                            df = get_fund_data(fund_code)
                            info = get_fund_info(fund_code)
                            
                            if not df.empty:
                                fund_data[fund_code] = df
                                fund_info[fund_code] = info
                                valid_funds.append(fund_code)
                            else:
                                st.error(f"未能获取到基金 {fund_code} 的数据")
                    except Exception as e:
                        st.error(f"获取基金 {fund_code} 数据时出错: {str(e)}")
                
                # 更新进度条
                progress_bar.progress((i + 1) / len(fund_inputs))
            
            # 完成进度条
            progress_bar.progress(1.0)
            
            if valid_funds:
                # 显示基金比较结果
                display_fund_comparison(fund_data, fund_info, start_date, end_date)
            else:
                st.error("没有有效的基金数据可以比较")

def display_fund_comparison(fund_data, fund_info, start_date, end_date):
    """显示基金比较图表"""
    # 转换日期为pandas datetime格式
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)
    
    # 准备绘制收益率曲线图
    fig = go.Figure()
    
    # 定义颜色列表
    colors = [
        '#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', 
        '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf'
    ]
    
    # 显示基金基本信息
    st.markdown("### 参与比较的基金")
    
    for i, (fund_code, df) in enumerate(fund_data.items()):
        # 获取投资区间的数据
        mask = (df['date'] >= start_date) & (df['date'] <= end_date)
        period_df = df.loc[mask].copy()
        
        if period_df.empty:
            st.warning(f"基金 {fund_code} 在所选时间区间内没有数据")
            continue
        
        # 获取基金名称
        info = fund_info[fund_code]
        fund_name = info.get('fund_name', f'基金{fund_code}')
        if '(' in fund_name:
            fund_name = fund_name.split('(')[0]
        elif '（' in fund_name:
            fund_name = fund_name.split('（')[0]
        
        # 使用函数取模来循环使用颜色
        color = colors[i % len(colors)]
        
        # 计算收益率
        if 'acc_nav' in period_df.columns and not period_df['acc_nav'].isna().all():
            # 使用累计净值计算收益率
            start_acc_nav = period_df['acc_nav'].iloc[0]
            period_df['return_rate'] = (period_df['acc_nav'] / start_acc_nav - 1) * 100
        else:
            # 使用单位净值计算收益率
            start_nav = period_df['nav'].iloc[0]
            period_df['return_rate'] = (period_df['nav'] / start_nav - 1) * 100
        
        # 将收益率曲线添加到图表
        fig.add_trace(go.Scatter(
            x=period_df['date'],
            y=period_df['return_rate'],
            mode='lines',
            name=f"{fund_name} ({fund_code})",
            line=dict(color=color, width=2)
        ))
        
        # 显示基金信息和累计收益率
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f"**{fund_name}** ({fund_code})")
        with col2:
            final_return = period_df['return_rate'].iloc[-1] if not period_df.empty else 0
            st.markdown(f"累计收益率: **{final_return:.2f}%**")
        with col3:
            fund_type = info.get('fund_type', '未知类型')
            st.markdown(f"基金类型: {fund_type}")
    
    # 设置图表布局
    fig.update_layout(
        title='基金投资区间收益率比较',
        xaxis_title='日期',
        yaxis_title='收益率(%)',
        hovermode='x unified',
        showlegend=True,
        height=600,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="center",
            x=0.5
        )
    )
    
    # 添加零线作为参考
    fig.add_hline(y=0, line_width=1, line_dash="dash", line_color="gray")
    
    # 显示图表
    st.plotly_chart(fig, use_container_width=True)
    
    # 显示投资区间信息
    st.markdown(f"**投资区间：** {start_date.strftime('%Y-%m-%d')} 至 {end_date.strftime('%Y-%m-%d')}")
    
def fund_investment_plan_page():
    """基金投资计划页面"""
    st.markdown('<h1 class="main-header">基金投资计划</h1>', unsafe_allow_html=True)
    st.info("🚧 此功能正在开发中，敬请期待...")
    
def more_features_page():
    """更多功能页面"""
    st.markdown('<h1 class="main-header">更多功能</h1>', unsafe_allow_html=True)
    st.info("🚧 更多功能正在开发中，敬请期待...")