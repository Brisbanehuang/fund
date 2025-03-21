import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import os
import json
from datetime import datetime

# 自定义CSS样式
def load_css():
    """加载自定义CSS样式"""
    st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        margin-bottom: 1rem;
        background-color: white;
        padding: 1rem 0;
    }
    .fixed-top {
        position: sticky;
        top: 0;
        background-color: white;
        z-index: 999;
        padding: 1rem 0;
        border-bottom: 1px solid #eee;
        margin-bottom: 2rem;
    }
    .input-container {
        display: flex;
        align-items: center;
        gap: 1rem;
    }
    .section-header {
        font-size: 1.8rem;
        font-weight: bold;
        margin: 1.5rem 0;
    }
    .sidebar-header {
        font-size: 1.2rem;
        font-weight: bold;
        margin-bottom: 1rem;
    }
    .main {
        padding: 0rem 1rem;
    }
    .stButton>button {
        width: 100%;
        height: 42px;  /* 与输入框高度保持一致 */
    }
    .reportview-container {
        background: #f0f2f6;
    }
    .metric-label {
        font-size: 1rem;
        color: #555;
        margin-top: 0.5rem;
    }
    div[data-testid="stToolbar"] {
        display: none;
    }
    /* 确保输入框和按钮在同一水平线上 */
    div.row-widget.stTextInput {
        margin-bottom: 0;
    }
    /* 自选基金卡片样式 */
    .fund-card {
        border: 1px solid #ddd;
        border-radius: 8px;
        padding: 1.2rem;
        margin-bottom: 1rem;
        background-color: white;
        height: 100%;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    .fund-card h4 {
        margin: 0 0 1rem 0;
        font-size: 1.1rem;
        color: #333;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }
    .fund-card p {
        margin: 0.5rem 0;
        color: #666;
        font-size: 0.9rem;
    }
    .fund-card .info-row {
        display: flex;
        justify-content: space-between;
        margin: 0.5rem 0;
    }
    .fund-card .update-time {
        color: #999;
        font-size: 0.8rem;
        margin-top: 0.5rem;
    }
    .fund-card .button-group {
        display: flex;
        gap: 0.5rem;
        margin-top: 1rem;
    }
    </style>
    """, unsafe_allow_html=True)

def display_fund_analysis(df, fund_info, show_header=True):
    """显示基金分析内容"""
    if show_header:
        st.markdown('<h2 class="section-header">基金基本信息</h2>', unsafe_allow_html=True)
    
    # 显示基金基本信息
    col1, col2 = st.columns(2)
    with col1:
        # 处理基金名称，移除代码部分
        fund_name = fund_info.get('fund_name', '未获取到')
        if '(' in fund_name:
            fund_name = fund_name.split('(')[0]
        elif '（' in fund_name:
            fund_name = fund_name.split('（')[0]
        st.markdown(f"**基金名称：** {fund_name}")
        st.markdown(f"**基金公司：** {fund_info.get('fund_company', '未获取到')}")
        st.markdown(f"**基金经理：** {fund_info.get('fund_manager', '未获取到')}")
    with col2:
        st.markdown(f"**基金代码：** {fund_info.get('fund_code', '未获取到')}")
        st.markdown(f"**基金类型：** {fund_info.get('fund_type', '未获取到')}")
        
        # 修改申购状态显示逻辑
        is_buy = fund_info.get('is_buy')
        if is_buy is True:
            purchase_status = "可申购"
        elif is_buy is False:
            purchase_status = "暂停申购"
        else:
            purchase_status = "未知"
            
        st.markdown(f"**申购状态：** {purchase_status}")
        st.markdown(f"**最小申购金额：** {fund_info.get('min_purchase', 0)}元")
    
    # 添加更多信息部分
    with st.expander("更多基金信息", expanded=False):
        # 显示投资主题信息（如果有）
        themes = fund_info.get('investment_themes', [])
        if themes:
            st.markdown("**投资主题：**")
            theme_str = ", ".join([theme.get('name', '') for theme in themes])
            st.markdown(f"{theme_str}")
        
        # 显示其他名称（如果有）
        other_name = fund_info.get('other_name', '')
        if other_name:
            st.markdown(f"**别名/其他名称：** {other_name}")
        
        # 显示最近更新日期（如果有）
        update_date = fund_info.get('update_date', '')
        if update_date:
            st.markdown(f"**数据更新日期：** {update_date}")
        
        # 显示基金公司ID（如果有）
        fund_company_id = fund_info.get('fund_company_id', '')
        if fund_company_id:
            st.markdown(f"**基金公司ID：** {fund_company_id}")
    
    # 显示基金数据分析结果
    st.markdown('<h2 class="section-header">净值走势</h2>', unsafe_allow_html=True)
    
    # 创建净值走势图
    fig = go.Figure()
    
    # 根据基金类型显示不同的数据
    is_money_fund = fund_info.get('is_money_fund', False)
    if is_money_fund:
        fig.add_trace(go.Scatter(
            x=df['date'],
            y=df['nav'],
            mode='lines',
            name='每万份收益',
            line=dict(color='#1f77b4', width=2)
        ))
        fig.update_layout(
            title='每万份收益走势图',
            xaxis_title='日期',
            yaxis_title='每万份收益（元）',
            hovermode='x unified',
            showlegend=True,
            height=500
        )
    else:
        # 使用累计净值替代单位净值
        if 'acc_nav' in df.columns and not df['acc_nav'].isna().all():
            fig.add_trace(go.Scatter(
                x=df['date'],
                y=df['acc_nav'],
                mode='lines',
                name='累计净值',
                line=dict(color='#1f77b4', width=2)
            ))
            fig.update_layout(
                title='基金累计净值走势图',
                xaxis_title='日期',
                yaxis_title='累计净值',
                hovermode='x unified',
                showlegend=True,
                height=500
            )
        else:
            # 如果没有累计净值数据，则使用单位净值
            fig.add_trace(go.Scatter(
                x=df['date'],
                y=df['nav'],
                mode='lines',
                name='单位净值',
                line=dict(color='#1f77b4', width=2)
            ))
            fig.update_layout(
                title='基金净值走势图 (累计净值数据不可用，显示单位净值)',
                xaxis_title='日期',
                yaxis_title='单位净值',
                hovermode='x unified',
                showlegend=True,
                height=500
            )
    
    # 显示图表
    st.plotly_chart(fig, use_container_width=True)
    
    # 基本统计信息
    st.markdown('<h2 class="section-header">基金统计信息</h2>', unsafe_allow_html=True)
    
    # 计算统计指标
    latest_date = df['date'].max()
    latest_nav = df['nav'].iloc[-1]
    establishment_date = df['date'].min()
    
    if is_money_fund:
        # 计算七日年化收益率
        last_7_days = df[df['date'] > latest_date - pd.Timedelta(days=7)]['nav']
        seven_day_sum = last_7_days.sum()
        seven_day_return = (seven_day_sum / 10000) * 100  # 七日累计收益率
        seven_day_annual = (pow(1 + seven_day_return/100, 365/7) - 1) * 100  # 七日年化收益率
        
        # 计算历史七日年化收益率序列
        df['rolling_7day_sum'] = df['nav'].rolling(window=7).sum()
        df['rolling_7day_return'] = (df['rolling_7day_sum'] / 10000) * 100
        df['rolling_7day_annual'] = (pow(1 + df['rolling_7day_return']/100, 365/7) - 1) * 100
        
        max_7day_annual = df['rolling_7day_annual'].max()
        min_7day_annual = df['rolling_7day_annual'].min()
        
        # 显示统计信息
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric(f"最新每万份收益（{latest_date.strftime('%Y-%m-%d')}）", f"{latest_nav:.4f}元")
        with col2:
            st.metric("七日年化收益率", f"{seven_day_annual:.2f}%")
        with col3:
            st.metric(f"历史最高七日年化（{df.loc[df['rolling_7day_annual'].idxmax(), 'date'].strftime('%Y-%m-%d')}）", f"{max_7day_annual:.2f}%")
        with col4:
            st.metric(f"历史最低七日年化（{df.loc[df['rolling_7day_annual'].idxmin(), 'date'].strftime('%Y-%m-%d')}）", f"{min_7day_annual:.2f}%")
        
        # 显示额外的统计信息
        st.markdown("---")
        st.markdown(f"**基金成立日期：** {establishment_date.strftime('%Y-%m-%d')}")
        st.markdown(f"**最新数据日期：** {latest_date.strftime('%Y-%m-%d')}")
    else:
        # 非货币基金的原有统计逻辑
        nav_change = (df['nav'].iloc[-1] / df['nav'].iloc[0] - 1) * 100
        max_nav = df['nav'].max()
        max_nav_date = df[df['nav'] == max_nav]['date'].iloc[0]
        min_nav = df['nav'].min()
        min_nav_date = df[df['nav'] == min_nav]['date'].iloc[0]
        total_return = ((df['nav'].iloc[-1] / df['nav'].iloc[0]) - 1) * 100
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric(f"最新净值（{latest_date.strftime('%Y-%m-%d')}）", f"{latest_nav:.4f}")
        with col2:
            st.metric("累计收益（最新净值/首日净值-1）", f"{nav_change:.2f}%")
        with col3:
            st.metric(f"历史最高（{max_nav_date.strftime('%Y-%m-%d')}）", f"{max_nav:.4f}")
        with col4:
            st.metric(f"历史最低（{min_nav_date.strftime('%Y-%m-%d')}）", f"{min_nav:.4f}")
        
        st.markdown("---")
        st.markdown(f"**基金成立日期：** {establishment_date.strftime('%Y-%m-%d')}")
        st.markdown(f"**最新数据日期：** {latest_date.strftime('%Y-%m-%d')}")
        st.markdown(f"**成立至今累计收益：** {total_return:.2f}%")
    
    # 添加基金投资天数指标分析
    st.markdown('<h2 class="section-header">基金投资天数指标分析</h2>', unsafe_allow_html=True)
    
    # 日期选择
    col1, col2 = st.columns([2, 3])
    with col1:
        st.markdown("#### 选择投资区间")
    with col2:
        # 快速选择按钮
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
            # 使用当前选择的结束日期，而不是数据集的最大日期
            current_end_date = st.session_state.get('end_date_input', df['date'].max().date())
            # 转换为datetime以便进行日期计算
            current_end_date = pd.to_datetime(current_end_date)
            start_date = current_end_date - pd.Timedelta(days=days)
            # 确保开始日期不早于基金成立日期
            if start_date < df['date'].min():
                start_date = df['date'].min()
            st.session_state.start_date = start_date.date()
            st.session_state.end_date = current_end_date.date()
        
        for i, (period_name, days) in enumerate(periods.items()):
            with period_cols[i]:
                if st.button(period_name, key=f"period_{days}"):
                    update_date_range(days)
    
    # 日期选择器
    date_cols = st.columns(2)
    with date_cols[0]:
        start_date = st.date_input(
            "开始日期",
            min_value=establishment_date.date(),
            max_value=latest_date.date(),
            value=st.session_state.start_date or establishment_date.date(),
            key="start_date_input"
        )
    with date_cols[1]:
        end_date = st.date_input(
            "结束日期",
            min_value=establishment_date.date(),
            max_value=latest_date.date(),
            value=st.session_state.end_date or latest_date.date(),
            key="end_date_input"
        )
    
    # 转换日期为datetime
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)
    
    # 获取选定期间的数据
    mask = (df['date'] >= start_date) & (df['date'] <= end_date)
    period_df = df.loc[mask].copy()
    
    # 在投资区间信息上方添加两个图表：收益率曲线图和单位净值曲线图
    if not period_df.empty and start_date <= end_date and not is_money_fund:
        # 1. 收益率曲线图（从起始日期0%开始，用累计净值计算）
        if 'acc_nav' in period_df.columns and not period_df['acc_nav'].isna().all():
            # 计算累计收益率曲线
            start_acc_nav = period_df['acc_nav'].iloc[0]
            period_df['return_rate'] = (period_df['acc_nav'] / start_acc_nav - 1) * 100
            
            # 绘制收益率曲线图
            fig_return = go.Figure()
            fig_return.add_trace(go.Scatter(
                x=period_df['date'],
                y=period_df['return_rate'],
                mode='lines',
                name='收益率曲线',
                line=dict(color='#ff7f0e', width=2)
            ))
            fig_return.update_layout(
                title='投资区间收益率曲线',
                xaxis_title='日期',
                yaxis_title='收益率(%)',
                hovermode='x unified',
                showlegend=True,
                height=400
            )
            # 添加零线以便参考
            fig_return.add_hline(y=0, line_width=1, line_dash="dash", line_color="gray")
            st.plotly_chart(fig_return, use_container_width=True)
        else:
            # 如果没有累计净值数据，则使用单位净值
            start_nav = period_df['nav'].iloc[0]
            period_df['return_rate'] = (period_df['nav'] / start_nav - 1) * 100
            
            # 绘制收益率曲线图
            fig_return = go.Figure()
            fig_return.add_trace(go.Scatter(
                x=period_df['date'],
                y=period_df['return_rate'],
                mode='lines',
                name='收益率曲线 (使用单位净值计算)',
                line=dict(color='#ff7f0e', width=2)
            ))
            fig_return.update_layout(
                title='投资区间收益率曲线 (使用单位净值计算)',
                xaxis_title='日期',
                yaxis_title='收益率(%)',
                hovermode='x unified',
                showlegend=True,
                height=400
            )
            # 添加零线以便参考
            fig_return.add_hline(y=0, line_width=1, line_dash="dash", line_color="gray")
            st.plotly_chart(fig_return, use_container_width=True)
        
        # 2. 单位净值曲线图（显示选定区间的单位净值）
        fig_nav = go.Figure()
        fig_nav.add_trace(go.Scatter(
            x=period_df['date'],
            y=period_df['nav'],
            mode='lines',
            name='单位净值',
            line=dict(color='#2ca02c', width=2)
        ))
        fig_nav.update_layout(
            title='投资区间单位净值曲线',
            xaxis_title='日期',
            yaxis_title='单位净值',
            hovermode='x unified',
            showlegend=True,
            height=400
        )
        st.plotly_chart(fig_nav, use_container_width=True)
    
    if not period_df.empty and start_date <= end_date:
        # 计算投资天数
        trading_days = len(period_df)
        calendar_days = (end_date - start_date).days + 1
        
        if is_money_fund:
            # 计算货币基金的收益指标
            total_income = period_df['nav'].sum()  # 区间内每日万份收益之和
            cumulative_return = (total_income / 10000) * 100  # 累计收益率
            annual_return = (pow(1 + cumulative_return/100, 365/calendar_days) - 1) * 100  # 年化收益率
            
            # 显示指标分析结果
            st.markdown("### 投资区间基本信息")
            st.markdown(f"- **投资天数：** {calendar_days}天（其中交易日{trading_days}天）")
            
            st.markdown("### 收益类指标")
            col1, col2 = st.columns(2)
            with col1:
                st.metric("年化收益率", f"{annual_return:.2f}%",
                        help="年化收益率 = (1 + 累计收益率)^(365/投资天数) - 1")
            with col2:
                st.metric("区间累计收益率", f"{cumulative_return:.2f}%",
                        help="累计收益率 = (区间内每日万份收益之和/10000) × 100%")
        else:
            # 非货币基金的原有计算逻辑
            period_return = (period_df['nav'].iloc[-1] / period_df['nav'].iloc[0] - 1) * 100
            annual_return = (pow(1 + period_return/100, 252/trading_days) - 1) * 100
            
            # 计算风险类指标
            period_df['daily_return'] = period_df['nav'].pct_change()
            # 计算区间波动率
            mean_return = period_df['daily_return'].mean()
            volatility = np.sqrt(((period_df['daily_return'] - mean_return) ** 2).sum() / (trading_days - 1)) * 100
            
            period_df['rolling_max'] = period_df['nav'].expanding().max()
            period_df['drawdown'] = (period_df['nav'] - period_df['rolling_max']) / period_df['rolling_max'] * 100
            max_drawdown = abs(period_df['drawdown'].min())
            
            # 显示指标分析结果
            st.markdown("### 投资区间基本信息")
            st.markdown(f"- **投资天数：** {calendar_days}天（其中交易日{trading_days}天）")
            st.markdown(f"- **区间起始净值：** {period_df['nav'].iloc[0]:.4f}")
            st.markdown(f"- **区间结束净值：** {period_df['nav'].iloc[-1]:.4f}")
            
            st.markdown("### 收益类指标")
            col1, col2 = st.columns(2)
            with col1:
                st.metric("年化收益率", f"{annual_return:.2f}%",
                        help="年化收益率 = (1 + 期间总收益率)^(252/投资天数) - 1")
            with col2:
                st.metric("区间累计收益率", f"{period_return:.2f}%",
                        help="累计收益率 = (期末净值 - 期初净值) / 期初净值")
            
            st.markdown("### 风险类指标")
            col1, col2 = st.columns(2)
            with col1:
                st.metric("区间波动率", f"{volatility:.2f}%",
                        help="波动率 = √(Σ(日收益率 - 平均收益率)²/(交易天数-1))")
            with col2:
                st.metric("最大回撤", f"{max_drawdown:.2f}%",
                        help="最大回撤 = (期间最高点净值 - 期间最低点净值) / 期间最高点净值")
    else:
        st.error("请选择有效的投资区间")