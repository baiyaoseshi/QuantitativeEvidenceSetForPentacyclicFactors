# Methodology (METHODOLOGY)

> **As-of date: 2026-08-11** · Companion dashboard: [Public Track Record](https://quantitativeevidencesetforpentacyclicfactors-a9dqp6rqqdseuigvx.streamlit.app/)
> Principle: **public evidence, private recipe** — performance, methodology and governance are fully verifiable; signal construction, weights, threshold values, filter/execution details and holdings are not disclosed.

---

## 1. Strategy class (concept level)

Long-only, all-market A-share strategy, medium-frequency holding (backtest average ~5 months):
cross-sectional score signals from a proprietary research framework → daily watchlist →
multi-layer risk filters → intraday execution. No leverage, no shorting, no derivatives. Ever.

## 2. Performance (backtest, full-stack simulation)

Simulation chain: signals → all production filters → execution simulation → full transaction
costs → fill-rate modeling below 100%.

| Basis | Period | Cumulative | Sharpe (time-series) | Max drawdown | Closed win rate |
|---|---|:--:|:--:|:--:|:--:|
| **Primary** | 2019-01 ~ 2026-07 | **+358.32%** | **1.33** | **-2.59%** | 88.71% |
| Full-history stress | 2005 ~ 2026-07 | +665.39% | 1.26 | -20.84% | 83.60% |

- Primary basis: **every year 2019-2025 positive** (win rates 72.7% ~ 96.3%; yearly table on the dashboard).
- Stress basis covers the 2008 / 2015 / 2018 bear regimes: 2015 closed 39/39 winners (+59.1% MTM);
  worst year 2018 (-11.7% MTM).
- **Reproducibility**: the full-history result was re-run on 2026-08-11 with the default
  configuration and matched the archived numbers exactly.

## 3. Parameter governance

1. **Every parameter has a source**: thresholds are calibrated from percentiles of historical
   distributions (e.g. P90) or from literature/physical constraints. Parameters without a
   documented source are not allowed in production. Grid-search results are adopted only when
   the optimum is interior to the grid; boundary optima are rejected as overfitting signals.
2. **Every switch has a verdict**: each filter/mechanism carries an independent A/B experiment
   (same data, same metrics); verdicts and result files are archived.
3. **Rejected by evidence = switched off** — complete list of mechanisms evaluated and disabled:
   hard stop-loss, time stop, calendar-month filter, strategy-level losing-streak circuit breaker,
   macro-credit gate, capital-flow linear gate, cross-sectional clipping, loss-cutting rotation,
   leverage (**permanently rejected**: ruin risk is unacceptable).
4. **Out-of-sample discipline**: thresholds of key protection mechanisms are calibrated on
   recent samples and validated out-of-sample by replaying historical extreme regimes
   (2007/2015 tops, 2021 crowding top) — never fitted on the extreme samples themselves.

## 4. Active disclosures (read before the numbers)

- **Losing-position holding**: no hard stop-loss; losing positions are held until the strategy's
  natural exit signal (up to **927 days** in-sample). Corollary: closed-trade win rate is
  systematically upward-biased; all equity/Sharpe/drawdown figures here are **mark-to-market,
  including unrealized losses**.
- **Crash risk**: black swans are unpredictable and this system does not claim to predict them;
  the holding side is **deliberately** unprotected — drawdown is the premium paid for crash
  insurance. The gap between -20.84% (full-history) and -2.59% (primary basis) is that premium.
- **Backtest ≠ live**: backtests are historical simulations; the companion paper-trading record
  (no real slippage impact) updates daily, with execution slippage attribution reported quarterly.
- **Small-capital constraints**: the impact of small-capital trading constraints is
  quantitatively modeled; control backtests at different capital levels show these constraints
  do not change the strategy's character.
- **Path dependence**: sub-period results starting from different years differ (cash/position
  path dependence) — which is exactly why the primary and full-history bases are presented side by side.
- **Sparse-signal years exist**: in weak years (e.g. 2023) trade count drops materially and
  returns concentrate in a few years — an inherent property of low-frequency strategies.

## 5. Verifiability

- **Live curve**: the [dashboard](https://quantitativeevidencesetforpentacyclicfactors-a9dqp6rqqdseuigvx.streamlit.app/)
  updates automatically after each close from the production daemon state, via a sanitizing
  export layer (normalized equity/drawdown only, first day = 100 — no amounts, no tickers,
  no signal internals).
- **Data sources**: Tushare market data, akshare realtime snapshots, public financials.
- This document and the dashboard data are hosted in a public repository with full git history.

*Last updated: 2026-08-11 (same as the as-of date).*
