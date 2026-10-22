# Changelog

## 0.1.1 — 2026-10-22 — low-frequency diagnostic build

User reported almost no trades and supplied a Strategy Tester screenshot. Added an on-chart pipeline table to both scripts: observed M5 coverage, impulse/sweep/base/breakout counts, submitted candidates, strategy-observed fills, pullback caps, invalidations, expirations and filter blocks. Added an invalid entry-date-range error. No trading rules, default risk settings, costs, or entry permissiveness were changed.

Local checks passed: identical indicator/strategy setup source, delimiter/safeguard audit, and exact comparison of shared trading statements against 0.1.0 after removing diagnostics and the invalid-date guard. These are source checks, not Pine compilation. 0.1.1 TradingView compilation and runtime diagnostics remain pending. The screenshot does not establish the cause of low trade frequency; see docs/RESULTS.md.

## 0.1.0 — 2026-10-22 — agreed baseline implementation, execution provisional

Replaced the initial exploratory draft with the user-agreed M5 Fibonacci-zone/liquidity-sweep baseline. Added independent 3/3 pivots, locked impulse IDs, 61.8–71% zone, two-pivot eligibility, sweep reuse prevention, three-candle base including sweep, six-bar breakout window, capped one-bar entries, one executed trade per impulse, EMA classification, optional external/session filters, entry-date windows and EUR 300 capital.

Stop defaults to sweep wick plus $0.30, planned price-distance cap $6. Entire 0.01-lot exposure stays open: +$6 TP1 triggers BE, +$12 TP2 is informational, +$20 final target closes all. Actual lot conversion, fees and margin remain unverified illustrative settings. Alternative final target distance is configurable; TP4 and all partial exits remain disabled.

Added 30-second execution-chart support with M5 setup decisions and Bar Magnifier requested. **Immediate TP1-touch BE is NOT implemented faithfully**: current update occurs at execution-bar close and is suppressed on entry bar to avoid using pre-entry extrema. No actual TP1 order fill is claimed. The strategy title, chart warning and documentation label results provisional. This technical requirement remains unresolved, not silently relaxed.

Updated AGENTS.md, README, agreed specification and TradingView validation checklist. Initial draft Pine copies were preserved outside checkout in /tmp during this session; they are not a persistent version archive. The initial files were subsequently committed and pushed as `44c9bab`; no persistent release archive was created separately.

Evidence:
- Local source audit: identical shared setup sections, balanced delimiters and selected no-partial/confirmed-data/order safeguards checked using `python tools/check_sources.py`.
- Pine compilation: NOT RUN; no TradingView compiler available here.
- TradingView replay, order behavior and seconds-data checks: NOT RUN.
- Broker contract, quantity and margin verification: OUTSTANDING.
- Immediate-BE execution validation: OUTSTANDING.
- Backtests, optimization, forward tests and holdout validation: NOT RUN.
- Profit factor, drawdown, net profit, trade count, win rate, expectancy, monthly returns and losing streaks: UNAVAILABLE.

Future results must record exact revision, feed, dates, chart resolution, input/property values, commissions/spread/slippage, margin, contract conversion, Bar Magnifier coverage, evidence exports, outcomes and limitations. Do not report source checks as compilation or profitability evidence.
