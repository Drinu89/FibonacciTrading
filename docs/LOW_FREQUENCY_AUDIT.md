# Low-frequency audit — 2026-10-22

## What is established

The supplied v0.1.1 M5 table recorded 934 impulses, 21 qualifying sweeps, 13 bases, 6 breakouts/submissions and 2 fills. Five caps required pullbacks and four orders expired. Optional filters blocked zero submissions. The user then supplied a v0.2 performance screenshot showing one closed trade; its pipeline table and exact trade details were not supplied.

Adding a structure requirement was an approved anchor experiment, not a demonstrated fix for low trade frequency. It can further reduce eligible impulses. It should not be promoted as a solution or tuned until the actual rejected/expired setups are traced.

## Reproduced rule interaction (synthetic, not historical evidence)

Suppose a SELL sweep reaches 4092.00. With the frozen 0.30 buffer, SL is 4092.30. Suppose the three-candle base low is 4082.00 and the confirming close is 4081.00. A market entry there would require 11.30 price dollars of stop distance, exceeding the 6.00 cap. The permitted sell limit is 4086.30, requiring a rally of 5.30 from the confirming close. A straight decline cannot fill it, and the order expires after one M5 candle.

This is consistent with the approved cap/expiry behavior. It is not a confirmed trading-engine defect. Shortening confirmation or lengthening expiry would change frozen rules and must be tested as an explicit separate decision, not silently patched. Increasing risk is not justified by low frequency.

## Stronger independent checks

Previous local tests exercised the anchor engine only. Added a test-only evaluator for the actual Pine M5 control-flow statements, with explicit confirmed impulse/pivot packets. It does not maintain a separately rewritten trading algorithm.

27 local tests now pass: 12 anchor tests plus 15 setup-pipeline tests. Pipeline coverage includes valid BUY/SELL submissions, base timing/freezing, sixth versus seventh breakout bars, strict sweep/origin invalidation, one-bar unfilled expiry, fill consumption feedback, pivot reuse prevention, locked anchors, capped pullback behavior, missing external data, external confirmation boundaries, session gating and newly confirmed liquidity-pivot availability.

These tests have not identified a stuck-state fault in the covered cases. That does not prove the complete TradingView implementation correct. They DO NOT execute Pine, model request.security/bar merging, generate confirmed pivots, simulate limit/stop fills, or reproduce the user's historical run. Broker feedback is explicitly injected. Source consistency checks also pass. No Pine strategy logic was changed during this audit.

## Data needed before another strategy change

Obtain the same-run OANDA:XAUUSD M5 chart-data CSV (include script outputs where available), Strategy Tester List of trades export, and current Inputs/Properties including pivot/timeframe settings, quantity, costs and Bar Magnifier. Preserve dates/settings. Raw bar timestamps are needed to map manual setups and anchor availability; a performance screenshot cannot locate a rejection.

Then trace one discretionary missed setup through anchor confirmation, pivot eligibility, sweep, frozen base, breakout, cap, order lifetime and fills. Compare chart-script state/impulse plots with the local replay. Separate a coding defect from an agreed rule that excludes the desired trade. Numerical profitability and frequency acceptance remain unvalidated.

The latest EUR 0.75 loss could be compatible with an entry-price stop plus fees, but only the actual trade export can establish whether that occurred. It must not be asserted from the aggregate screenshot. Immediate intrabar break-even remains an existing unresolved limitation.
