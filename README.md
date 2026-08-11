# QuantitativeEvidenceSetForPentacyclicFactors

仅展示五环因子量化金融能力证据。

**公开证据，保密配方**：本仓库公开业绩与方法论（净值曲线、回撤、分年统计、治理纪律、风险披露），
不公开信号构造、因子权重、阈值数值与持仓明细。

## 入口

- **实盘验证看板（每日自动更新）**：
  <https://quantitativeevidencesetforpentacyclicfactors-a9dqp6rqqdseuigvx.streamlit.app/>
- 方法学说明：[中文](METHODOLOGY.md) · [English](METHODOLOGY_EN.md)

## 口径速览（2026-08-11）

| 口径 | 区间 | 累计收益 | Sharpe | 最大回撤 |
|---|---|:--:|:--:|:--:|
| 主口径 | 2019-01 ~ 2026-07 | +358.32% | 1.33 | -2.59% |
| 全时段压力测试 | 2005 ~ 2026-07 | +665.39% | 1.26 | -20.84% |

## 仓库内容

| 文件 | 说明 |
|---|---|
| `app.py` | Streamlit 只读看板（部署于 Streamlit Community Cloud） |
| `data/equity_public.json` | 脱敏实盘净值（归一化首日=100，每日由生产 daemon 自动导出推送） |
| `METHODOLOGY.md` / `METHODOLOGY_EN.md` | 方法学说明（含主动披露与参数治理纪律） |
| `_daily_push.ps1` | 每日数据更新脚本（本地运行记录，公开以保持更新机制可审计） |
