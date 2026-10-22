# Uploaded Pine Logs diagnosis — 2026-10-22

Source: `pine-logs-Fibonacci v0.2.1 — STRUCTURE _ LOGS.csv`. 1,078 CSV rows; SHA-256 `90b52c6a3f088fa2181c6d70c79246e8df2e6681dbb1cc6e868f02e21956c2bc`. The file was read as data only. This is analysis of user-supplied TradingView output, not an agent-run backtest.

## Confirmed run context

```text
TRACE_SUMMARY v0.2.1 | symbol=OANDA:XAUUSD chart=5 fib=5 | full INPUT-window counters, NOT log-window-only: bars=5186 impulses=331 sweeps=33 bases=21 breakouts=10 candidates=10 fills=1 unfilled_expiry=9 pullback_caps=9 | broker_open=0 broker_closed=1 | BE remains provisional
```

```text
TRACE_SETTINGS | capital=300 EUR tick=0.001 pointvalue=1 | lots=0.01 units_per_lot=100 units_per_TV_qty=1 | Fib_pivots=3/3 liquidity_pivots=3/3 | BE_trigger=6 full_target=20 | log_window_UTC=2020-01-01 00:00..2099-01-01 00:00 | Verify commission, margin and slippage in Strategy Properties
```

## Pipeline

| Stage | Count |
|---|---:|
| Confirmed anchor candidates | 331 |
| Qualifying sweeps | 33 |
| Completed bases | 21 |
| Confirmed breakouts | 10 |
| Submitted orders | 10 |
| Observed fills | 1 |
| Unfilled order expirations | 9 |

Of 33 sweeps, 12 invalidated during base formation. Of the 21 completed bases, eight invalidated while waiting for breakout and three expired; ten produced breakouts and orders. All ten logged filter checks passed. DXY and Silver were disabled; session/date and EMA checks passed.

## Every submitted order

Times below are Europe/Malta (UTC+2 on these dates). Distances are Gold price dollars, not EUR account risk.

| Signal time (Malta) | Impulse | Side | Signal close | Stop | Signal risk | Entry cap | Outcome | Next-bar range | Cap reached? |
|---|---:|---|---:|---:|---:|---:|---|---|---|
| 2026-09-28 18:45 | 14 | SELL | 4132.055 | 4148.470 | 16.415 | 4142.470 | Expired | 4129.340–4134.925 | No |
| 2026-09-30 05:35 | 37 | SELL | 4175.550 | 4184.891 | 9.341 | 4178.892 | Expired | 4174.110–4177.695 | No |
| 2026-10-02 19:25 | 82 | SELL | 4133.490 | 4142.795 | 9.305 | 4136.795 | Expired | 4130.180–4135.325 | No |
| 2026-10-05 02:20 | 87 | BUY | 4151.730 | 4140.554 | 11.176 | 4146.554 | Expired | 4151.235–4157.875 | No |
| 2026-10-05 12:55 | 95 | BUY | 4160.720 | 4155.319 | 5.401 | 4161.319 | Filled | Not included in Events log | Actual fill logged |
| 2026-10-09 07:20 | 163 | BUY | 4190.715 | 4177.014 | 13.701 | 4183.014 | Expired | 4189.405–4191.425 | No |
| 2026-10-13 03:50 | 196 | SELL | 4152.645 | 4170.415 | 17.770 | 4164.415 | Expired | 4151.225–4157.940 | No |
| 2026-10-13 12:25 | 202 | SELL | 4182.385 | 4189.566 | 7.181 | 4183.566 | Expired | 4180.625–4183.420 | No |
| 2026-10-19 14:00 | 269 | SELL | 4161.360 | 4176.375 | 15.015 | 4170.375 | Expired | 4158.805–4163.450 | No |
| 2026-10-20 03:05 | 277 | SELL | 4123.530 | 4139.766 | 16.236 | 4133.767 | Expired | 4123.260–4129.570 | No |

Nine of ten signals exceeded the $6 signal-close stop-distance cap. Signal-close risk ranged from $5.401 to $17.770; median $12.4385. All nine corresponding limits were outside the logged next-bar tradable high/low range. That absence alone suffices to explain those non-fills; there is no need to attribute them to margin or a stuck state. This does not prove every other execution detail correct.

## Why confirmation and the risk cap conflict

For BUY, signal close must exceed the highest wick of the entire three-candle base, including the sweep. Stop is below the sweep low. Therefore signal-close risk is greater than `base high − sweep low + buffer`. SELL mirrors this. In 16 of the 21 completed bases, that lower bound already exceeded $6. A close-based breakout entry for those bases necessarily needs an improved fill price to respect the cap.

Example: on 5 October at 02:20 Malta (00:20 UTC), BUY signal close 4151.730, stop 4140.554, risk 11.176, maximum permitted entry 4146.554. The next M5 low was 4151.235, never reaching the entry limit; the order expired. This is the specified cap/expiry behavior, not evidence that a touched limit was ignored.

The approved v0.2 anchor experiment produced ten submissions in this logged run, but did not remove the shared entry-execution bottleneck. The root interaction is now supported by actual logs rather than a synthetic example.

## The single filled trade

- 2026-10-05 13:00 Malta (observation close): `ENTRY_FILLED` — position_impulse=95 side=1 qty=1 fill=4160.755 SL=4155.319 actual_stop_distance=5.436 BE_trigger=4166.755 final_TP=4180.755 fill_UTC=2026-10-05 10:55:00
- 2026-10-05 13:30 Malta (observation close): `TP1_TOUCH_OBSERVED` — position_impulse=95 entry=4160.755 trigger=4166.755 entry_bar=false also_returned_to_entry=true; observed at execution-bar close, not an actual TP1 fill
- 2026-10-05 13:30 Malta (observation close): `BE_SEQUENCE_UNCERTAIN` — TP1 and entry return occurred in this execution bar; ordering not established
- 2026-10-05 13:30 Malta (observation close): `BE_UPDATE_REQUEST` — position_impulse=95 new_SL=4160.755; effective only for subsequent emulator execution; not retroactive
- 2026-10-05 13:35 Malta (observation close): `TRADE_CLOSED` — position_impulse=95 trade_index=0 entry_id=Long exit_id=Long bracket qty=1 entry=4160.755 exit=4160.745 reported_profit=-0.7480818451 commission=0.7391988451 entry_UTC=2026-10-05 10:55:00 exit_UTC=2026-10-05 11:30:00

Actual entry was 4160.755 and exit 4160.745: adverse price movement 0.010, equal to ten logged minimum ticks. Reported closed profit is −EUR 0.7480818451, with EUR 0.7391988451 commission. The difference is −EUR 0.008883. The logged loss is therefore consistent with a near-entry BE stop plus adverse execution and commission; it was not a full structural-stop loss. Do not subtract the commission a second time from the reported profit.

The TP1 observation explicitly flagged that price also returned to entry in the same M5 bar. The log does not establish intrabar order. The existing execution-bar-close BE update remains provisional; no immediate-BE validation follows from this trade.

CSV Date marks the chart bar time; message UTC marks observation close, five minutes later on M5. Actual entry/exit timestamps in trade messages are separate. The exit was timestamped 11:30 UTC and observed at the 11:35 UTC calculation; that is not evidence of a five-minute late fill.

## Next controlled experiment — decision pending

Preserve v0.1 and current v0.2 results and the $6 cap. The user has been asked to choose ONE isolated comparison: increase existing order lifetime from one to three M5 bars, or reduce the base from three to two candles. These are rule variants, not coding fixes. No rule change has been applied from this upload. The Events file does not contain sufficient later OHLC to establish whether a longer-lived order would have filled or become profitable. Do not optimize against the final holdout.

Minor numerical detail: several rounded stops/caps differ by one 0.001 tick from exact-decimal arithmetic. That is consistent with binary floating-point floor/ceil at a tick boundary. It does not explain the nine misses: even the closest missed sell cap remained 0.146 above the following candle high. No numerical patch or performance improvement is claimed in this analysis.
