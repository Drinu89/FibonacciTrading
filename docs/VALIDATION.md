# Validation checklist — all TradingView checks pending

## Local checks

Run `python tools/check_sources.py` from the checkout. It checks shared source equality, delimiters and selected execution safeguards. It does not compile or execute Pine. No available local Pine compiler or TradingView API is configured.

## TradingView compilation and behavioral acceptance

Record exact script revision, provider, chart type, dates, settings, costs, chart execution resolution and Bar Magnifier coverage. Save compiler diagnostics before changing code. Check both indicator and strategy independently.

Use replay and screenshots to verify these cases, for BUY and SELL:

1. M5 pivots appear only after three right bars; a liquidity pivot confirmed on the sweep candle is ineligible until the next candle. HTF pivots first become actionable at the next eligible M5 close, not retrospectively at their extrema. Reload and confirm closed-bar setup markers are stable.
2. Sweep pivot inside zone or exactly $0.50 outside is eligible; farther is not. Sweep candle must intersect actual zone and close strictly reclaimed. Touch without penetration or close equal to pivot fails. Either of last two pivots can qualify. Both swept together cannot be reused separately.
3. Sweep candle 1 plus candles 2–3 form the frozen base. Candle 3 cannot be the breakout. Candle 4 is first allowed breakout; the sixth subsequent candle is the final allowed close. The base must never expand after candle 3.
4. Touch of sweep extreme survives; strict breach cancels. No restart on that M5 candle. Another attempt needs a different eligible confirmed pivot. Original-anchor breach cancels the entire impulse. A consumed impulse cannot trade again.
5. New Fib candidates do not replace locked setups; the latest valid one can be adopted after release. Check candidate invalidation while locked and one candle processing delay after invalidation/expiry.
6. External confirmation is disabled in baseline. When separately enabled, missing or stale symbol data fails. Agreement at breakout is eligible; additional bars 1–3 eligible; bar 4 too late. A delayed confirmation also needs a close still beyond the fixed base boundary.
7. Check capped orders above/below market, pullback fills, no-fill expiry on next M5 close, strict invalidation, gaps past SL and session/date boundaries. Do not assume close-time cancellation happened earlier intrabar. Inspect limit verification and tick rounding.
8. Protective stop and full target must be attached when entry fills, including entry/exit in the same chart bar. Quantity and margin must permit a trade at EUR 300 using verified broker/feed conversion. Verify actual fill-to-stop distance and target measured from fill.
9. TP1 is a price threshold, no partial close. Fill-bar extrema never activate BE. On later execution bars TP1 touch updates BE only after that bar closes. Confirm stop at actual entry; net result may be negative after costs. Test BUY and SELL.
10. Explicitly inspect TP1 then entry-return, entry-return then TP1, original SL then TP1, gaps and both-in-one-30s-bar cases. On bars where trades close before script evaluation, warning counters may miss ambiguity. Do not call this immediate intrabar BE. Record unresolved cases; lower OHLC alone is not tick evidence.
11. Verify EMA class at submission remains stored during trade. All Trades accepts neutral; the two filtered modes exclude it. Compare indicator setup candidates with strategy submissions, accepting documented differences due to fills, occupied positions and consumption.

## Performance evaluation — blocked until execution accepted

Freeze exact chronological development/validation/final holdout dates before selection (suggested proportions 60/20/20). Do not select dates from a winning screenshot. Ensure sufficient history/warmup and adequate trades across trending, ranging, quiet and volatile regimes. Entry-date controls do not liquidate existing positions; specify treatment of trades crossing boundaries. Test 300 and 1,000 EUR balances with identical exposure and realistic margin.

Export current-run trades and Strategy Tester performance. Report:

- Net profit after costs, profit factor, maximum equity drawdown (EUR and percent), closed trades and win rate.
- Expectancy = total net closed P&L / closed trades. Do not silently omit commissions; verify export semantics before calculating.
- Calendar-month realized return = change in realized month-end balance / prior month-end realized balance. Report open P&L separately and disclose account-currency conversion.
- Longest consecutive negative-net-trade streak; zero-net trades break the streak.
- BUY/SELL and trend/countertrend breakdown, trade frequency and unfilled-order behavior. Filtered reruns can change later eligible trades, so they are not identical to grouping the original trade export.
- Margin rejections, gaps, ambiguous intrabar sequences and lower-timeframe coverage limitations.

No numerical acceptance thresholds have been agreed. Set drawdown, sample size and performance criteria before choosing a candidate. Undefined ratios and unavailable metrics remain unavailable, not zero.

First inspect the unchanged baseline, then vary one factor at a time: Fib timeframe, session, external filters individually/together, trend filter, target distance. Later experiments: alternate levels, aggressive two-candle base, 3/6/9 breakout windows, ATR tolerance, structure targets, actual partial exits on divisible volume. Keep final holdout untouched, assess parameter neighbors/cost stress and conduct forward observation. MT5 EA remains deferred until TradingView validation is accepted.
