# v0.2.0 — structure-selected anchors (experimental)

The user approved this separate variant on 2026-10-22. `Fibonacci_v0.1_*.pine` remains unchanged. This is an anchor-selection experiment, not a claim of improved trade count or profitability. The entry zone, liquidity sweep, base/breakout confirmation, capped entries, costs, quantity and provisional break-even execution are inherited unchanged.

## Exact source-timeframe anchor algorithm

Run in the selected Fibonacci timeframe: M5 baseline, M15/H1 separately selectable. Independent Fibonacci and liquidity pivots still default to 3 left / 3 right source bars.

1. Store the most recently confirmed swing high and low with their pivot timestamps. A candle qualifying as both pivot types is ignored. Evaluate structure breaks BEFORE inserting pivots newly confirmed on that candle.
2. A bullish break requires a source candle CLOSE strictly above a previously confirmed high. A bearish break requires a CLOSE strictly below a previously confirmed low. Wick-only breaks do not qualify. Both opposite pivots must be known, with high > low. A given pivot timestamp can be broken only once; sustained closes beyond it are not new breaks.
3. At a bullish break, freeze provisional Anchor A at the most recent already-confirmed low; bearish uses the most recent already-confirmed high. Reject a bullish break candle that has already strictly breached that low, and the inverse for SELL. These are explicit event-ordering assumptions.
4. Track the highest wick after the bullish break / lowest wick after the bearish break as the developing endpoint. This provisional leg is internal and cannot generate entries. Later same-direction breaks do not move its fixed origin. An opposite qualifying close-break replaces the developing leg; a strict originating-wick breach cancels it. No discretionary minimum size/ATR or EMA-direction filter is added.
5. Freeze Anchor B only when a same-direction pivot is confirmed whose pivot timestamp is at/after the break, later than Anchor A, and whose price equals the most extreme wick reached since the break. It must also exceed the broken high / fall below the broken low. If the endpoint is not confirmed, no new tradable Fibonacci exists.
6. Publish that candidate on its confirmation candle, not on its historical pivot candle. Ignore subsequent minor pivots unless a fresh eligible structure break and endpoint confirmation create another candidate. This reduces a particular source of minor-swing replacement; it is still a local confirmed-structure algorithm and need not reproduce every discretionary manual drawing.
7. Existing v0.1 setup-lock behavior is retained: before a liquidity sweep a newly confirmed candidate can replace anchors; once swept, hold anchors through base, breakout, filters and pending entry. New candidates continue to develop in the background. At release adopt the newest still-valid candidate. Genuine origin/sweep invalidations remain active.

## Timing and plots

On M5, current requested M5 data is used only at its confirmed closing timestamp. On a 30-second execution chart, source setup decisions still occur only at M5 closes. For M15/H1 all requested outputs are offset one source bar with lookahead_on; they are observed at the first subsequent eligible M5 close. No historical entry is moved back to the endpoint or break candle.

Diagnostics retain input-window counts for confirmed impulses, sweeps, bases, breakouts, submissions and fills. New Data Window fields expose source bullish/bearish BOS counts (ALL loaded source history, not date-window counts), developing direction and selected anchor timestamps. Pending-direction plots may change while a realtime source candle develops; entries do not use those provisional values. The confirmed endpoint is drawn from activation forward, not backdated.

## Compare fairly

Load `Fibonacci_v0.2_Strategy.pine` as a NEW script on the same OANDA:XAUUSD M5 chart used for v0.1. Keep dates, loaded history, quantity/margin, costs, Bar Magnifier, entry inputs and exits identical. First inspect whether anchors fit the intended large leg in the supplied example. Compare the complete pipeline, not only final trades: requiring structure can produce FEWER impulses or trades. Do not weaken risk limits to obtain a target count.

Record date/time of any missed discretionary setup, the selected anchor timestamps/prices, prior structure level, break close, endpoint confirmation time and cancellation/expiry reason. Do not infer all of that from aggregate performance or a cropped screenshot. Keep this development comparison outside the final holdout.

## Evidence and limits

- 12 local tests execute a constrained Python translation of the actual Pine structureEngine source with explicit synthetic confirmed-pivot inputs. They cover BUY/SELL symmetry, close-versus-wick breaks, confirmation delay, origin freezing/invalidation, endpoint chronology, repeated-level breaks, opposite breaks, frozen output and simultaneous pivot types.
- Source checks confirm exact shared logic within each strategy/indicator pair and unchanged inherited setup/execution rules. Frozen v0.1 files have no diff.
- These tests DO NOT compile Pine, validate TradingView's pivot implementation, reproduce request.security merging, execute broker orders or establish profitability.
- TradingView compilation, replay, chronological anchor verification and backtests remain pending. Immediate TP1-touch BE is still not faithfully implemented; the inherited execution-bar-close approximation remains prominently provisional.

Run local checks from the repository:

```sh
python tools/check_sources.py
python -m unittest discover -s tests -v
```
