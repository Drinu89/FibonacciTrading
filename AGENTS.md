# Persistent project rules

- Build and validate the TradingView Pine strategy first. Do not implement an MQL5 EA until the user accepts documented TradingView validation.
- Never promise profitability or invent backtests, compilation results, statistics, or execution evidence. Label proposed, locally checked, TradingView compiled, backtested, and out-of-sample validated work distinctly.
- Use Pine Script v6. Keep indicator and strategy setup detection identical. Document intentional execution differences.
- No future-data access, retrospective signals, or repainting entry logic. HTF requests must use confirmed data; explain offsets and lookahead settings. Confirm entries at chart-bar close, and preserve realistic order timing.
- Maintain BUY and SELL support, configurable levels and confirmations, explicit swing lifecycle rules, costs, version names, and CHANGELOG.md.
- Follow docs/V0_1_SPEC.md, agreed with the user. Baseline includes EMA 200 classification and TP1-triggered break-even; external filters are optional and disabled. Partial exits and MT5 remain deferred. Do not silently change frozen rules. Any execution approximation must stay prominently labelled provisional.
- Record instrument/feed, timezone, dates, inputs, costs, order settings, and code version for every result. Retain chronological out-of-sample data; never optimize against the final holdout.
- Evaluate profit factor, drawdown, net profit, trade count, win rate, expectancy, monthly returns, and maximum consecutive losing trades. Include cost sensitivity, parameter stability, and different market regimes; never select solely by net profit.
- Use the existing isolated checkout; do not create worktrees unless requested. Preserve user changes and never embed credentials.

- The user approved a separate v0.2 structure-anchor experiment: follow docs/V0_2_STRUCTURE_VARIANT.md. Preserve frozen v0.1 Pine files. Compare identical entry/risk/exit settings; do not claim additional trades or performance before supplied results.
