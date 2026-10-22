# Changelog

## 0.2.1 — 2026-10-22 — execution logs without CSV export

Added opt-in/configurable Pine Logs (enabled by default) to the v0.2 strategy and shared setup logs to its indicator. Events cover anchor activation/invalidation, qualifying sweeps, bases, breakouts, filters, planned risk/caps, submissions, observed fills, cancellation/expiry, provisional BE and closed trades. Detailed M5 mode includes bar/zone/pivot rejection data; independent log dates allow narrow traces without altering trade history. Added full-window summary/settings messages and stable execution impulse identity in logged trade details. v0.1 remains unchanged.

Validation: source isolation confirms logging/display-only changes, identical shared setup source, and unchanged inherited trading statements and execution wrapper. All 30 local tests pass (27 existing plus three logging tests through the constrained evaluator). No TradingView compilation, log-panel run, actual log output or new backtest is claimed. See docs/PINE_LOGS.md for use and limitations.

## Post-v0.2 audit — 2026-10-22 — no Pine logic changes

User supplied a one-closed-trade v0.2 screenshot and reported worsening frequency. Added a test-only evaluator of actual M5 Pine control-flow statements and 15 synthetic pipeline regressions, bringing local tests to 27. Reproduced the base-confirmation/risk-cap/one-bar-expiry interaction; no stuck-state fault was found in covered cases. No TradingView fills, request.security behavior or historical profitability were validated by these tests. Preserved all Pine files and documented the exact same-run data needed for a bar-by-bar audit in docs/LOW_FREQUENCY_AUDIT.md. No fix or performance improvement is claimed.

## 0.2.0 — 2026-10-22 — separate structure-anchor experiment

Added Fibonacci_v0.2_Strategy.pine and Fibonacci_v0.2_Indicator.pine after user approval. New anchor candidates require a source-timeframe close beyond previously confirmed structure and a subsequently confirmed extreme pivot. Developing origins stay fixed; minor unbroken pivot pairs no longer create candidates. Added confirmed endpoint and source-structure Data Window fields. Preserved v0.1 Pine files and all inherited setup, order, risk and provisional BE rules.

Validation: 12 local synthetic engine tests passed using a constrained translation of actual Pine source. Source checks verify shared indicator/strategy detectors and unchanged inherited trading logic. These do not compile Pine or test TradingView pivot merging/execution. TradingView compilation/replay/backtests remain unrun; no performance or trade-count improvement is claimed. See docs/V0_2_STRUCTURE_VARIANT.md.

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
