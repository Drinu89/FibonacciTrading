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

## User-supplied v0.2 performance screenshot

Displayed September 28–October 22, 2026, EUR 300 capital, net P&L −EUR 0.75 (−0.25%), maximum drawdown EUR 2.25 (0.75%), profitable trades 0/1, profit factor 0, and one Long closed trade in the breakdown. The user reports worse trade frequency. No v0.2 pipeline table, raw bars, exact input/property record or trade export is available. The agent did not run this backtest. The screenshot alone does not establish the reason for the loss or omitted trades.

An additional source/pipeline audit is recorded in LOW_FREQUENCY_AUDIT.md. No trading rules were modified during that audit.

## User-uploaded v0.2.1 Pine Logs CSV — analyzed 2026-10-22

Analyzed 1,078 uploaded rows. Confirmed OANDA:XAUUSD, M5 chart and Fib timeframe, EUR 300, tick 0.001, point value 1, qty 1 mapped from 0.01 lot. Summary: 5,186 M5 bars, 331 impulses, 33 sweeps, 21 bases, 10 breakouts/submissions, one fill and nine unfilled expirations; nine entry caps required pullbacks. All nine expired caps were outside their next-bar high/low ranges. All ten filter checks passed. Risk at signal close ranged 5.401–17.770 Gold price dollars (median 12.4385), while maximum permitted distance was 6.00.

The single trade entered 4160.755, reached the BE trigger, and exited 4160.745. Reported closed profit −EUR 0.7480818451 includes EUR 0.7391988451 commission. TP1/entry-return intrabar ordering was flagged uncertain. See UPLOADED_LOG_DIAGNOSIS.md for all ten orders and source hash. No agent-run TradingView backtest, new profitability result, or immediate-BE validation is claimed. Raw uploaded financial logs remain outside the Git checkout. No Pine rules were modified during analysis.
