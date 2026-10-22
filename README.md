# Fibonacci Trading v0.1

Pine Script v6 implementation of the agreed XAUUSD liquidity-sweep/Fibonacci baseline. **Not compiled in TradingView, not backtested, and not validated for profitability. Immediate intrabar break-even remains unresolved; the supplied strategy is explicitly provisional.**

## Open these scripts

- [Fibonacci_v0.1_Strategy.pine](Fibonacci_v0.1_Strategy.pine): capped BUY/SELL entries, protective brackets, configurable full target and provisional BE.
- [Fibonacci_v0.1_Indicator.pine](Fibonacci_v0.1_Indicator.pine): confirmed M5 setup candidates, Fibonacci zone, base, EMA 200 and alert conditions.
- [Agreed specification](docs/V0_1_SPEC.md): frozen rules, assumptions, quantity conversion and execution limitations.
- [Validation checklist](docs/VALIDATION.md): required TradingView/manual checks and performance records.

## Load in TradingView

1. Open standard `OANDA:XAUUSD` candles. Copy the entire strategy file into a new Pine Editor strategy, save and Add to chart. Use M5 for initial setup inspection. Only M5 and 30-second charts are supported.
2. Compile the indicator separately on M5. Candidate triangles indicate capped order submissions, not fills. Configure candidate alerts Once Per Bar Close. The strategy's filled orders are the execution record.
3. For a finer but still provisional BE approximation, run the strategy on a **30-second chart**. Setup and external-filter calculations remain M5. Check availability of seconds history and Bar Magnifier coverage. M5 and 30-second charts can expose different total history and fill outcomes; compare only overlapping dates.
4. In Strategy Properties use EUR 300 initial capital, then EUR 1,000 for a separate comparison. Verify RaiseFX contract size, OANDA quantity/point value, margin requirements and fees. Defaults assume 100 Gold units per broker lot and one unit per TradingView quantity: 0.01 lot becomes quantity 1. These assumptions have not been verified. Margin defaults to illustrative 1%; adjust to broker terms before interpreting exposure/results.
5. Keep the frozen defaults: M5 Fib 3/3, liquidity 3/3, 61.8–71%, $0.50 proximity, 3 base candles including sweep, 6 breakout bars, $0.30 stop buffer, $6 risk cap, one-bar entry expiry, one executed trade per impulse. DXY/Silver OFF; EMA filter All Trades; session OFF.
6. Keep On Every Tick, After Order Fill and Fill Orders On Bar Close OFF. Calibrate commission/slippage/spread assumptions rather than interpreting illustrative defaults as broker costs. Native emulator slippage does not model a variable bid/ask spread, and limit fills have different cost mechanics from stops/market orders.
7. Set Entry start/end dates for each test window. Earlier data still warms up EMA/pivots; setup state can develop before start. Only new submissions are date-gated. An order submitted before the end can fill before cancellation is evaluated; use boundary inspection. Existing trades keep exits after end.

## Read results cautiously

TP1 is +$6 in Gold price from actual fill, not $6 guaranteed EUR cash profit. It closes no volume. The implementation updates BE at execution-bar close AFTER detecting a touch; it cannot claim immediate TP1-touch protection. On the entry bar BE is deliberately suppressed because extrema may predate the fill. Bar Magnifier does not fix calculation timing. The on-chart warning must remain visible during validation.

Full exit defaults +$20 from fill. To test the TP2 alternative, change final distance to $12; do not enable fictitious partial exits. Entry caps may fill on pullbacks after breakout confirmation. Unfilled orders are permitted; never force a market replacement. Stops can gap/slip beyond planned risk.

Strategy Tester supplies standard performance data. Export trades for expectancy, calendar-month returns, losing streaks and trend/direction grouping. No custom statistics are claimed computed in this release; follow the validation checklist for definitions. Do not optimize until compilation, setup and execution checks are complete.

## Status

Local source consistency and focused risk/lifecycle checks are recorded in CHANGELOG.md. They are not Pine compilation or a TradingView backtest. Immediate BE validation, broker specification verification, actual historical/forward results and out-of-sample evaluation remain outstanding. No MQL5 EA has been implemented.

## Investigating low trade frequency (v0.1.1)

Load the diagnostic build with the SAME symbol, chart timeframe, history and inputs as the earlier run. Leave **Show setup diagnostics** enabled. Its bottom-right table reports the pipeline and actual observed history; it is not a performance table. Share the table, strategy Inputs/Properties, and List of trades for the same run. Use the strategy table (the indicator cannot observe fills).

- Few sweeps versus impulses: investigate anchor choice, previously confirmed liquidity pivots and actual zone intersections on the chart.
- Sweeps but few bases: inspect sweep-extreme invalidations.
- Bases but few breakouts: inspect range width and six-bar expiry.
- Breakouts but few submissions: inspect session/date, EMA and external filter blocks.
- Submissions but few fills: inspect entry caps requiring pullbacks, one-bar expiry, invalidation, order size, margin and capital.

These are diagnostic possibilities, not established causes or recommendations to loosen the frozen baseline. Counts apply to loaded input-window data, which can differ from the Strategy Tester displayed range. Events may cross date boundaries and categories can overlap; do not subtract rows as if they were mutually exclusive. No claim that the diagnostic release increases trades or improves performance.
