# v0.2.1 — diagnose through Pine Logs without CSV export

The strategy now emits `log.info` messages from its chart execution context. No CSV export is required. This is read-only instrumentation, not a change to trading rules. The v0.1 files remain frozen. Use the strategy for actual broker-emulator fills; the indicator logs setup candidates only.

## Start here

1. Copy the complete current `Fibonacci_v0.2_Strategy.pine` into your existing private Pine Editor strategy, Save and Add/update it on OANDA:XAUUSD M5. Confirm the title contains **v0.2.1 — STRUCTURE / LOGS**.
2. Open **Pine Logs** from Pine Editor. Select this script in the logs panel if several scripts are loaded, and show Info messages.
3. In Inputs → **Execution logs**, leave **Enable Pine Logs = ON** and **Log detail = Events** initially. Log start/end are separate from Entry start/end: changing a logging window never changes which trades qualify. End is exclusive.
4. Find `TRACE_SUMMARY` and `TRACE_SETTINGS`. Copy their text here, plus event messages around a missed setup or the single trade. Screenshots of the log panel are also usable. No TradingView run or log-panel operation has been performed by the agent.
5. For missing entries, choose **Detailed M5** and restrict the log window to one day or a few hours around the example. Keep the chart/entry history unchanged so earlier pivots and open positions still warm up normally. Recalculation will regenerate historical log messages.

Log messages explicitly print UTC closing timestamps. Date input widgets may display the chart timezone: set the chart to UTC while choosing the logging window, or convert correctly. The earlier UTC+2 chart screenshot is two hours ahead of UTC on that date. Entry and exit messages also print actual emulator trade timestamps separately from observation time.

TradingView retains a limited number of recent historical log entries (typically 10,000); long verbose runs can hide earlier events. Narrow the LOG window and recalculate rather than filtering the panel after an already oversized run. Detailed M5 includes prices and rejection booleans; Events intentionally omits routine bar/pivot checks.

## Messages to inspect

| Event | Meaning |
|---|---|
| `ANCHOR_CANDIDATE`, `ANCHOR_ADOPT` | A confirmed structure-derived candidate and its activation, with identity, prices and pivot times. Candidate detection during a locked setup does not mean adoption. |
| `CANDIDATE_INVALIDATED`, `SETUP_INVALIDATED` | Which origin/sweep breach occurred and the observed prices. |
| `M5_BAR` (Detailed) | M5 OHLC, current anchors/zone, occupancy/consumption/activation gates and source pending direction. |
| `ZONE_VISIT`, `PIVOT_CHECK` (Detailed) | Number of stored pivots and each pivot's proximity, sweep/reclaim and already-used result. A zone visit without an eligible previous pivot cannot start a setup. |
| `SWEEP_PIVOT`, `SWEEP_STARTED` | Exact qualifying pivot and first base candle/extreme. |
| `BASE_PROGRESS`, `BASE_FROZEN` | Base candle count and fixed breakout range. |
| `BREAKOUT_CHECK` (Detailed), `BREAKOUT_CONFIRMED`, `BREAKOUT_EXPIRED` | Close versus required range boundary and six-bar timing. |
| `FILTER_CHECK`, `EXTERNAL_WINDOW_EXPIRED` | Date/session/EMA/external outcomes; disabled external filters are labelled disabled, not claimed confirmed. |
| `ENTRY_RISK_CHECK` | Signal close, structural SL, risk at that close, risk cap, limit price and whether a pullback is necessary. |
| `ORDER_CANDIDATE`, `ORDER_SUBMITTED` | Qualified signal and requested broker order with quantity. Neither is a fill. |
| `ORDER_EXPIRED`, `ORDER_CANCEL_REQUEST` | Unfilled lifetime or observed invalidation. Expiry does not establish whether price, verification, margin, quantity or platform execution prevented a fill. |
| `ENTRY_FILLED`, `ENTRY_AND_EXIT_SAME_BAR` | Broker-emulator fill observation; closed-trade details supply prices when both occur within one bar. |
| `FILL_RISK_EXCEPTION` | Observed fill is beyond planned cap or on an invalid side of the stop. |
| `TP1_TOUCH_OBSERVED`, `BE_SUPPRESSED_ENTRY_BAR`, `BE_SEQUENCE_UNCERTAIN`, `BE_UPDATE_REQUEST` | Distinguish a price touch, ambiguous sequencing, suppression and a requested subsequent stop update. None claims an actual TP1 fill or immediate intrabar protection. |
| `TRADE_CLOSED` | Actual closed-trade entry/exit IDs, prices, quantity, timestamps, reported profit and commission. Do not subtract commission again without checking TradingView's profit semantics. |
| `TRACE_SUMMARY`, `TRACE_SETTINGS` | Full ENTRY-input-window counters (not log-window-only), current broker open/closed counts, capital, tick/point values and selected inputs. Verify actual cost/margin overrides in Properties separately. |

`impulse=` in the common prefix is the scanner's current setup identity. Execution messages include `position_impulse=` to retain the submitted trade's identity even if a newer candidate has been adopted by the observation time. Summary/settings intentionally print outside the message-date window at the last confirmed-history bar, so you can still see aggregate context.

## Limits

Logs observe script calculations and emulator feedback; they do not reveal ticks, rejected-order reasons unavailable to Pine, or a hidden broker order queue. Close-time invalidation/cancellation cannot undo an earlier intrabar fill. BE remains the same provisional execution-bar-close approximation. Calls are only emitted on confirmed chart bars. This release has local tests but has NOT been compiled or inspected in TradingView by the agent.

Source-isolation checks remove marked trace blocks and verify inherited trading logic is unchanged. Three added tests check actual-source logging gates, stage-event coverage and identical pipeline decisions with a read-only observer. They run through a constrained Python evaluator, not TradingView's log API.
