# Agreed v0.1 specification and implementation status

Version 0.1.0. User-approved planning supersedes the earlier draft. BUY/SELL rules mirror each other. Prices are absolute XAUUSD price dollars, never an implicit pip conversion. EUR account capital is separate from USD-denominated Gold price movement.

## Frozen setup rules

- OANDA XAUUSD. All setup decisions on completed M5 candles. Standard candles only.
- Fibonacci timeframe independently selectable M5 (baseline), M15, H1. No combined timeframe signals.
- Independent Fib and liquidity pivot strength, each default 3 left/3 right. A pivot is usable only after confirmation. Use wick prices. Built-in TradingView pivot tie behavior applies. Ignore Fib bars that qualify as both high and low.
- Impulse: a newly confirmed high above the most recent earlier confirmed low creates BUY low-to-high; a newly confirmed low below the most recent earlier confirmed high creates SELL high-to-low. No additional higher-high/higher-low sequence requirement. This precise automatic interpretation replaces discretionary “significance.”
- Each confirmed impulse receives an increasing local ID. Before a sweep, a newer impulse can replace it. Once swept, preserve anchors through base, breakout, external confirmation and pending entry. New candidates continue to be observed while locked. At release, the newest still-valid candidate may replace it. Never redraw historical anchors/signals.
- HTF confirmed pivots become actionable at the first subsequent M5 close receiving the completed HTF result. M5 Fib pivots become known on their confirmation close, but no sweep is accepted on the activation candle.
- Entry zone 61.8%–71%, calculated as `endpoint + (origin - endpoint) * ratio`; sorted into lower/upper prices for both directions.
- Inspect the TWO most recent confirmed M5 liquidity pivots of the appropriate side, already confirmed before the sweep candle. Pivot price must be within zone or $0.50 of its nearest boundary. Sweep candle high/low range must intersect the actual zone. BUY strictly wicks below and closes above the pivot; SELL reverses. No extra body/wick ratio filter. If one candle sweeps several qualifying pivots, mark all swept so the same event cannot restart using the second pivot.
- Sweep candle is base candle 1; candles 2–3 must not strictly breach its extreme. Equality survives. Freeze highest/lowest wick of these three. Breakout must occur on one of the next six M5 closes, including number six; BUY close strictly above base high, SELL strictly below base low. Do not expand the base while waiting.
- A strict wick breach of the sweep extreme cancels the attempt; original anchor breach invalidates the impulse. No same-candle restart. Failed attempts may retry using a different eligible pivot, never a reused pivot within that impulse. One executed trade per impulse by default; failed/unfilled entries do not consume it.
- EMA 200 on M5 close: BUY above/SELL below = trend; reverse = countertrend; equality = neutral. Freeze class at order-submission signal. Default All Trades; optional Trend-Following Only/Countertrend Only exclude neutral.
- External filters default OFF. DXY `TVC:DXY`, Silver `OANDA:XAGUSD`; independently configurable. Compare confirmed M5 close with close three bars earlier. BUY DXY down/Silver up; SELL inverse. Missing/stale data fails an enabled filter. On breakout allow agreement immediately or within three additional M5 candles, inclusive, with price still closing beyond the frozen breakout level. This extra persistence condition is an explicit implementation assumption. No external-filter wait when both disabled.
- Session restriction OFF, default sample session 07:00–17:00 UTC if enabled. It gates submissions, not forced exits. No forced day/week closure or daily limits. 1–3 daily trades is an observation target, never an entry quota. Entry-date inputs permit independent development/validation/holdout runs; existing positions retain exits past the end date.

## Orders, capital and exits

- Planned stop beyond sweep wick by $0.30; round outward to tick grid. Max planned fill-to-stop distance $6.
- BUY limit = stop + $6, rounded down. SELL limit = stop − $6, rounded up. Submit only after confirmed breakout/filter qualification. The cap can require a pullback and is not a stop-entry continuation order. It can fill back inside the base; that consequence was disclosed during planning. Never substitute a market entry.
- Entry valid for one subsequent M5 candle. Cancel unfilled order at that close, or when invalidation is observed. A close-based cancellation cannot undo an earlier same-bar fill. Gaps can cross protective stops; no guaranteed monetary loss cap.
- Initial capital EUR 300; change to EUR 1,000 in Strategy Properties. 0.01 broker lot, configurable. Provisional conversion 100 Gold units per broker lot / 1 Gold unit per TradingView quantity gives qty 1; VERIFY against RaiseFX and OANDA feed specifications. Qty is not automatically EUR risk-sized. Commission 0.01% per fill, slippage 10 minimum ticks, limit verification one tick, and 1% margin (illustrative 1:100) are placeholders requiring calibration. No claim these are RaiseFX's actual terms.
- Structural stop and relative full-profit bracket are submitted with entry. Full target defaults +$20 from actual fill (rounded to nearest tick). TP1 +$6 is a BE price trigger, never an order or partial fill. TP2 +$12 informational. TP4 disabled; final target is configurable for separate experiments. At BE, stop moves to actual entry, not entry plus costs. Keep all volume until stop or full target; no partial exits.

## Unresolved execution requirement — not silently replaced

INTENDED: move stop to entry immediately when TP1 is reached. IMPLEMENTED PROVISIONAL APPROXIMATION: observe TP1 at execution-bar close, then update the protective order for subsequent execution. M5 chart resolution is coarse; running the strategy on a 30-second chart with identical M5 setup data reduces the delay but does not eliminate it. No validated tick execution model exists in this workspace.

`calc_on_every_tick` and `calc_on_order_fills` remain OFF to avoid presenting realtime-only or fill-recalculation behavior as historical evidence. Bar Magnifier is requested to improve the emulator's order-fill sequencing, subject to account/data coverage; it does not run script calculations on every magnified tick. Fill-bar extrema may predate the entry, so the implementation deliberately does NOT activate BE from the entry bar's high/low. This can miss a genuine immediate trigger; later 30-second bars can also contain unresolved touch/return sequences. Warning counts flag some surviving-position ambiguities but are not exhaustive, especially trades closed within a bar.

Therefore immediate-BE acceptance is outstanding. Results from this file are exploratory, not approved baseline performance. Validate against timestamped forward observations; do not declare a touched TP1 to have preceded SL without evidence. A future validated execution implementation must retain the same M5 setup rules. MT5 coding remains deferred; eventual tick-data comparison comes only after TradingView validation.

## Indicator differences

Indicator and strategy share identical setup source. The indicator has no broker fill feedback: its triangles are capped-order candidates, not executed trades; candidates expire after the configured order lifetime. It cannot enforce actual executed-trade consumption or occupied-position suppression, so its later candidates may differ from the strategy's. Only the strategy can establish simulated fills and one-trade-per-impulse enforcement.
