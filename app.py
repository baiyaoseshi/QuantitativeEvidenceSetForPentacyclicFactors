"""公开只读看板 (2026-08-11, 公开化任务)
=====================================================
部署目标: Streamlit Community Cloud (免费档), 公开 URL。
数据: 仅读取 data/equity_public.json (脱敏导出层 quant/public_export.py 生成,
      字段契约 {d, e, dd} — 归一化净值, 首日=100, 无金额/无代码/无信号)。
本目录可整体推送公开仓库: 不含任何策略实现、阈值数值、持仓信息。
对照 PUBLIC_BOUNDARY.md 检查表发布前逐项自查。
"""
import json, os
import pandas as pd
import streamlit as st

st.set_page_config(page_title="策略公开验证看板", layout="wide")

DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', 'equity_public.json')

# ── 口径 (回测, 静态) — 口径更新时同步修改本节与 METHODOLOGY.md ──
ASOF = "2026-08-11"          # 口径日期
BACKTEST_RANGE = "2019-01 ~ 2026-07"
STRESS_RANGE = "2005 ~ 2026-07 (全时段压力测试)"

YEARLY = [  # 分年统计 (仅百分比; 来源: 定稿回测, 口径日期见上)
    {"年份": 2019, "交易对": 54, "胜率": "96.3%", "平均盈亏": "+12.53%"},
    {"年份": 2020, "交易对": 35, "胜率": "82.9%", "平均盈亏": "+8.27%"},
    {"年份": 2021, "交易对": 35, "胜率": "91.4%", "平均盈亏": "+8.47%"},
    {"年份": 2022, "交易对": 17, "胜率": "82.4%", "平均盈亏": "+4.68%"},
    {"年份": 2023, "交易对": 11, "胜率": "72.7%", "平均盈亏": "+6.61%"},
    {"年份": 2024, "交易对": 45, "胜率": "86.7%", "平均盈亏": "+8.10%"},
    {"年份": 2025, "交易对": 51, "胜率": "90.2%", "平均盈亏": "+15.93%"},
]

st.title("策略公开验证看板")
st.caption(f"口径日期: {ASOF} · 本看板只读, 每日收盘后自动更新实盘净值 · 方法论详见 METHODOLOGY.md")

# ── 回测业绩 (百分比口径) ──
st.header("回测业绩（全栈模拟：信号→过滤→执行→成本）")
c1, c2, c3, c4 = st.columns(4)
c1.metric("年化 Sharpe (时序)", "1.33")
c2.metric("最大累计回撤", "-2.59%")
c3.metric("累计收益率", "+358.32%", help=f"区间: {BACKTEST_RANGE}")
c4.metric("平仓胜率", "88.71%")
st.markdown(f"**全时段压力测试**（{STRESS_RANGE}，含 2015/2007 崩盘 regime）：累计 **+665.39%** / Sharpe **1.26** / 最大回撤 **-20.84%**。")
st.dataframe(pd.DataFrame(YEARLY), hide_index=True, use_container_width=True)
st.caption("注: 胜率/盈亏比仅计已平仓; 总资产/Sharpe/回撤为含浮动盈亏的 MTM 诚实口径。金额已归一化隐藏。")

st.divider()

# ── 实盘净值 (脱敏曲线) ──
st.header("实盘纸交易净值（归一化，首日=100）")
if not os.path.exists(DATA_FILE):
    st.info("实盘曲线数据尚未生成。本地运行 quant/public_export.py 后此处每日更新。")
else:
    doc = json.load(open(DATA_FILE, 'r', encoding='utf-8'))
    series = doc.get('series', [])
    if not series:
        st.info("数据文件为空, 等待首个导出日。")
    else:
        df = pd.DataFrame(series)
        df['d'] = pd.to_datetime(df['d'])
        df = df.set_index('d')
        st.caption(f"起始日 {doc['meta'].get('start_date')} · 最近更新 {doc['meta'].get('updated')} · 共 {len(series)} 个交易日")
        m1, m2, m3 = st.columns(3)
        m1.metric("当前净值", f"{df['e'].iloc[-1]:.2f}")
        m2.metric("当前回撤", f"{df['dd'].iloc[-1]:.2f}%")
        m3.metric("历史最大回撤", f"{df['dd'].min():.2f}%")
        st.subheader("净值曲线")
        st.line_chart(df['e'])
        st.subheader("回撤曲线 (%)")
        st.area_chart(df['dd'])

st.divider()

# ── 主动披露 ──
st.header("主动披露（读数前请先读此节）")
st.markdown("""
- **持仓机制**：浮亏仓位不设硬止损，持有至策略自然卖出信号（回测样本内最长 927 天）。
  平仓胜率因此系统性偏高；总资产/Sharpe/回撤已按含浮亏的 MTM 口径呈现。
- **regime 边界**：黑天鹅不可预测，本系统不声称能预测崩盘；持仓侧**不做**崩盘保护——
  用可承受的回撤购买崩盘保险（全时段 -20.84% vs 主口径 -2.59% 的差额即保费定价）。
- **回测≠实盘**：回测含执行模拟与全部交易成本；实盘为纸交易（无真实资金滑点冲击），
  两者存在执行折价，按季度归因公布。
- **永不使用杠杆**。
""")

st.caption("公开证据 · 保密配方：本看板公开业绩与方法论，不公开信号构造、阈值与持仓明细。")
