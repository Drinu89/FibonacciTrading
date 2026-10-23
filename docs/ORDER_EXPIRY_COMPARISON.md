# Order-expiry comparison — supplied logs analyzed 2026-10-23

## Conclusion

The 3-M5-bar lifetime increased fills from one to four on ten matched candidate orders. All three additional fills closed at their structural stops with adverse execution and commission. The original near-entry exit was unchanged. The longer lifetime did not improve this supplied sample; it is not established as a better default. Four closed trades and unresolved BE sequencing are insufficient for a robust strategy-selection decision.

## Source and comparability

- Lifetime 1: `pine-logs-Fibonacci v0.2.1 — STRUCTURE _ LOGS.csv`, 1,078 rows, SHA-256 `90b52c6a3f088fa2181c6d70c79246e8df2e6681dbb1cc6e868f02e21956c2bc`.
- Lifetime 3: `pine-logs-Fibonacci v0.2.1 — STRUCTURE _ LOGS (1).csv`, 1,112 rows, SHA-256 `b7dfcb6e3f98fccc9713f716d7c19ee2e6baf24e530b784e50c3c7cbefada937`.

Files were read as data only. Both log configurations identify OANDA:XAUUSD, M5 chart/Fib timeframe, EUR 300, tick 0.001, point value 1, qty 1 mapped from 0.01 lot, independent 3/3 pivots, BE trigger 6 and full target 20. Every ORDER_CANDIDATE in the new run records lifetime_M5=3; all ten in the previous run record 1.

The latest summary reports 5,350 M5 bars/342 impulses, versus 5,186/331 previously: the newer file extends into 23 October. Thus whole-run history is not identical. However all TEN submitted candidate timestamps, directions, entry caps and structural stops match exactly, and no extra submitted order appears in the added history. The single trade common to both runs has identical entry, exit, profit and commission. This supports a matched-order fill comparison; it does not establish a perfectly controlled full-history A/B test or verify every unlogged Properties override.

The new file contains two summary/settings snapshots (5,349 then 5,350 bars), not two complete independent tests. Use the last snapshot and unique trade records; do not sum summary counters.

## Observed comparison

| Metric | 1-bar lifetime | 3-bar lifetime |
|---|---:|---:|
| Submitted orders | 10 | 10 |
| Filled and closed trades | 1 | 4 |
| Unfilled expirations | 9 | 6 |
| Positive-net closed trades | 0 | 0 |
| Sum of reported closed P&L | EUR -0.7481 | EUR -19.0953 |
| Reported commission | EUR 0.7392 | EUR 2.9725 |
| Net expectancy / closed trade (tiny sample) | EUR -0.7481 | EUR -4.7738 |

Reported profit already includes commission in these logs; do not subtract it again. This is reconstructed closed-trade P&L, not an independently run TradingView backtest. Full equity drawdown, monthly returns and other missing metrics are not inferred from four trade records.

## Filled trades in the 3-bar run

Actual entry times are Europe/Malta, not the later script observation close.

| Impulse | Actual entry (Malta) | Side | Entry | Exit | Reported net EUR | Interpretation |
|---|---|---|---:|---:|---:|---|
| 82 | 2026-10-02 19:30 | SELL | 4136.795 | 4142.805 | -6.0817 | Additional structural-stop exit plus costs |
| 95 | 2026-10-05 12:55 | BUY | 4160.755 | 4160.745 | -0.7481 | Original near-entry stop plus costs |
| 196 | 2026-10-13 03:55 | SELL | 4164.415 | 4170.425 | -6.1311 | Additional structural-stop exit plus costs |
| 202 | 2026-10-13 12:35 | SELL | 4183.566 | 4189.576 | -6.1345 | Additional structural-stop exit plus costs |

The three additional fills contributed EUR -18.3473. Their logged initial stop distances were 6.000 Gold price dollars; adverse stop execution made entry-to-exit price distance 6.010, before account-currency conversion and fees. None reached its full +20 final exit.

## Execution limitation requiring attention

For impulse 196, entered 13 October at 03:55 Malta (01:55 UTC), the next calculation observed TP1 within the ENTRY bar and also an entry-price return. `BE_SUPPRESSED_ENTRY_BAR` explicitly prevented BE because the favorable extreme could have occurred before entry. A subsequent full stop was logged. These Events logs do not establish whether TP1 was reached after entry, so the loss must not be retroactively replaced with a BE exit. Conversely, the result does not validate intended immediate-BE behavior. The original impulse-95 trade also retains a same-M5-bar sequencing warning.

The changing scanner impulse/side in a message prefix does not mean the position reversed: `position_impulse` and actual signed quantity identify the executed trade.

## Next development comparison

Preserve these runs. Do not promote three-bar expiry merely to increase frequency. If testing the next predeclared entry variant, restore expiry to ONE bar and compare baseCount=2 versus the original baseCount=3, keeping the $6 cap and all other inputs/costs fixed on the SAME fixed entry window. This targets signal-close risk after confirmation, unlike extending the pullback order lifetime. It is an explicit aggressive-entry experiment, not a bug fix or an approved new baseline. No Pine defaults were changed by this analysis.

Treat any resulting profitability as exploratory until immediate-BE execution is validated with finer sequencing evidence or timestamped forward observations. A no-Premium alternative is logging/observing future setups as they occur; do not assume seconds-chart history is available. Keep final holdout untouched.
