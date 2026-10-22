# Supplied evidence and unresolved diagnosis

## User screenshot received 2026-10-22 — earlier v0.1 strategy

The user reports almost no trades. The screenshot displays:

- Date range: September 28, 2026–October 22, 2026.
- Capital: EUR 300.
- Total P&L: −EUR 11.16 (−3.72%).
- Maximum drawdown: EUR 11.16 (3.72%).
- Profitable trades: 0.00%, 0/2.
- Profit factor: 0.

This is user-supplied TradingView evidence, not a backtest run by this agent. Exact script revision, instrument/feed, execution chart timeframe, Inputs/Properties, seconds/Bar Magnifier coverage and trade details have not been supplied. A screenshot of performance totals cannot establish which setup stage limits trades, whether rules were followed, or expected future profitability. No optimization decision follows from two trades.

## Next comparison

Use diagnostic release 0.1.1 with the same data and configuration. Record the bottom-right table, input/property screenshots and trade list. Do not compare different periods or loosen parameters while diagnosing. The agent verified trading statements unchanged by instrumentation through a local source comparison; no 0.1.1 TradingView execution has been performed here.

Immediate-BE behavior is still provisional. The diagnostic changes do not fix or validate that known limitation.

## User-supplied v0.1.1 diagnostic table — M5 confirmed

The user confirmed M5 execution and supplied a table showing 5,172 observed M5 bars (2026-09-27 22:00 UTC–2026-10-22 15:00 UTC), 934 confirmed impulses, 21 qualifying sweeps, 13 completed bases, 6 breakouts, 6 submitted candidates, 2 observed fills, 5 caps requiring a pullback, 202/12 anchor/sweep invalidations, 3/0 breakout/external expirations, 4 unfilled expirations and zero session/date/EMA/external blocks. Inputs/Properties and trade export remain incomplete.

A subsequent chart showed stepped automatic zones alongside a larger manually drawn bearish Fibonacci. Source inspection confirmed v0.1 permits minor pivot pairs to replace anchors before a sweep. That motivates the separately approved v0.2 anchor experiment; it does not prove the exact reason the discretionary example was missed. No v0.2 TradingView results have been supplied.
