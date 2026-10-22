"""Synthetic tests executing the actual v0.2 M5 control-flow block.

Explicit confirmed pivot/impulse packets are inputs, not generated market data.
The evaluator does NOT model TradingView requests or order fills.
"""
from pathlib import Path
import re
import unittest
from pine_subset import Expression, execute, functions, statements

ROOT = Path(__file__).resolve().parents[1]
SOURCE = (ROOT/'Fibonacci_v0.2_Strategy.pine').read_text()
BODY = SOURCE.split('if m5Close\n', 1)[1].split('\nz1 =', 1)[0]
PROGRAM = statements(BODY)
FEEDBACK = statements(SOURCE.split('// Feedback belongs', 1)[1].split('\nif m5Close', 1)[0].split('\n', 1)[1])


class Replay:
    def __init__(self, side=1):
        self.env = functions()
        self.env['na_value'] = float('nan')
        variables = SOURCE[SOURCE.index('var int seenStructureTime'):SOURCE.index('// Feedback belongs')]
        for line in variables.splitlines():
            m = re.match(r'var (?:int|float|array<\w+>) (\w+) = (.*)', line)
            if m:
                name, value = m.groups()
                self.env[name] = [] if 'array.new_' in value else float('nan') if value == 'na' else int(value)
        self.env.update(dict(fibTf='5', startDate=0, endDate=10**9, zoneShallow=.618, zoneDeep=.71, tolerance=.5, baseCount=3, breakoutBars=6, stopBuffer=.3, maxRisk=6, orderBars=1, maxTrades=1, trendMode='All Trades', useSession=False, useDxy=False, useSilver=False, externalWindow=3, executionBusy=False, executionFilled=False, entryAborted=False, sessionAllowed=True, ema200=105, **{'syminfo.mintick': .01}))
        for key in ('hph','hpl','hpt','hclosed','sah','sbh','seh','sath','sbth','sdh','dc','dp','dtc','sc','sp','stc'):
            self.env[key] = float('nan')
        self.env.update(sa5=100, sb5=120, sd5=1, se5=1, sat5=-10, sbt5=-3)
        self.side = side
        self.step(119, 110, 115)  # Activate without sweeping.
        # Most recent eligible M5 low is 106.5; older pivot intentionally outside zone.
        self.env['lows'], self.env['lowIds'] = [106.5, 95], [-2, -5]

    def step(self, high, low, close, **extra):
        e = self.env
        t = int(e['m5Index'])+1
        e.update(mh=high, ml=low, mc=close, mt=t, mtc=t, time_close=t, lph=float('nan'), lpl=float('nan'), lpt=t-3, buySignal=False, sellSignal=False, cancelEntry=False, signalStop=float('nan'), signalLimit=float('nan'), signalClass=0)
        e.update(extra)
        execute(FEEDBACK, e)
        execute(PROGRAM, e)
        return e

    def base(self):
        self.step(108, 106, 107)  # Sweep 106.5 in 105.8–107.64 zone.
        self.step(108.5, 106.2, 107.5)
        return self.step(108, 106.1, 107)


class PipelineTests(unittest.TestCase):
    def test_valid_buy_reaches_submission_after_three_candle_base(self):
        r = Replay()
        e = r.base()
        self.assertEqual(e['state'], 2)
        self.assertFalse(e['buySignal'])
        e = r.step(109, 107, 108.6)
        self.assertTrue(e['buySignal'])
        self.assertEqual(e['state'], 4)
        self.assertAlmostEqual(e['signalStop'], 105.7)
        self.assertAlmostEqual(e['signalLimit'], 111.7)

    def test_valid_sell_reaches_submission(self):
        r = Replay()
        r.env.update(sa5=120, sb5=100, sd5=-1, se5=2)
        r.step(118, 110, 115)
        r.env['highs'], r.env['highIds'] = [113.5, 125], [-2, -5]
        r.step(114, 112, 113)
        r.step(113.8, 111.5, 112)
        r.step(113.9, 112, 113)
        e = r.step(113, 111, 111.4)
        self.assertTrue(e['sellSignal'])
        self.assertAlmostEqual(e['signalStop'], 114.3)
        self.assertAlmostEqual(e['signalLimit'], 108.3)

    def test_original_anchor_breach_invalidates_entire_impulse(self):
        r = Replay(); r.base()
        e = r.step(109, 99.9, 108.6)
        self.assertEqual(e['direction'], 0)
        self.assertEqual(e['state'], 0)
        self.assertFalse(e['buySignal'])

    def test_enabled_session_blocks_submission_without_changing_base_rules(self):
        r = Replay(); r.base()
        r.env.update(useSession=True, sessionAllowed=False)
        e = r.step(109, 107, 108.6)
        self.assertFalse(e['buySignal'])
        self.assertEqual(e['diagSessionBlocked'], 1)

    def test_base_extreme_is_frozen_while_waiting(self):
        r = Replay(); r.base()
        r.step(110, 106.5, 108)  # Wick beyond base but close inside.
        e = r.step(109, 107, 108.6)
        self.assertTrue(e['buySignal'])
        self.assertEqual(e['baseHigh'], 108.5)

    def test_sixth_breakout_allowed_seventh_expired(self):
        r = Replay(); r.base()
        for _ in range(5):
            r.step(108, 106.5, 107)
        self.assertTrue(r.step(109, 107, 108.6)['buySignal'])
        r = Replay(); r.base()
        for _ in range(6):
            r.step(108, 106.5, 107)
        self.assertEqual(r.env['state'], 0)
        self.assertFalse(r.step(109, 107, 108.6)['buySignal'])

    def test_strict_sweep_breach_cancels_and_touch_survives(self):
        r = Replay(); r.base()
        self.assertEqual(r.step(108, 106, 107)['state'], 2)
        e = r.step(109, 105.99, 108.6)
        self.assertEqual(e['state'], 0)
        self.assertFalse(e['buySignal'])

    def test_pending_entry_expires_after_one_bar_without_consuming_impulse(self):
        r = Replay(); r.base()
        r.step(109, 107, 108.6)
        e = r.step(110, 107, 109)
        self.assertTrue(e['cancelEntry'])
        self.assertEqual(e['tradesInImpulse'], 0)

    def test_fill_consumes_impulse_once(self):
        r = Replay(); r.base()
        r.step(109, 107, 108.6)
        e = r.step(110, 107, 109, executionFilled=True, executionBusy=True)
        self.assertEqual(e['tradesInImpulse'], 1)
        self.assertEqual(e['state'], 0)

    def test_swept_pivot_not_reused_after_failure(self):
        r = Replay(); r.base()
        r.step(108, 105.9, 107)
        e = r.step(108, 106, 107)
        self.assertEqual(e['state'], 0)
        self.assertEqual(e['diagSweeps'], 1)

    def test_new_candidate_does_not_replace_locked_base(self):
        r = Replay()
        r.step(108, 106, 107)
        e = r.step(108.5, 106.2, 107.5, sa5=110, sb5=100, sd5=-1, se5=2)
        self.assertEqual(e['origin'], 100)
        self.assertEqual(e['endpoint'], 120)
        self.assertEqual(e['direction'], 1)

    def test_wide_confirmation_submits_cap_requiring_pullback(self):
        r = Replay()
        r.step(112, 106, 107)
        r.step(111, 106.2, 108)
        r.step(111, 106.1, 109)
        e = r.step(114, 112, 113)
        self.assertTrue(e['buySignal'])
        self.assertLess(e['signalLimit'], e['mc'])
        self.assertEqual(e['diagCappedPullback'], 1)
        # Straight continuation never reaches the BUY limit: expiry is expected.
        e = r.step(116, 112, 115)
        self.assertTrue(e['cancelEntry'])

    def test_missing_enabled_external_data_cannot_submit(self):
        r = Replay(); r.env['useDxy'] = True; r.base()
        e = r.step(109, 107, 108.6)
        self.assertFalse(e['buySignal'])
        self.assertEqual(e['state'], 3)

    def test_external_additional_third_bar_allowed_fourth_not(self):
        r = Replay(); r.env['useDxy'] = True; r.base()
        r.step(109, 107, 108.6)
        for _ in range(2):
            r.step(110, 107, 109)
        t = r.env['m5Index']+1
        self.assertTrue(r.step(110, 107, 109, dc=99, dp=100, dtc=t)['buySignal'])
        r = Replay(); r.env['useDxy'] = True; r.base()
        r.step(109, 107, 108.6)
        for _ in range(3):
            r.step(110, 107, 109)
        t = r.env['m5Index']+1
        self.assertFalse(r.step(110, 107, 109, dc=99, dp=100, dtc=t)['buySignal'])

    def test_newly_confirmed_liquidity_pivot_not_used_same_candle(self):
        r = Replay(); r.env['lows'] = []; r.env['lowIds'] = []
        e = r.step(108, 106, 107, lpl=106.5, lpt=-2)
        self.assertEqual(e['state'], 0)
        e = r.step(108, 106, 107)
        self.assertEqual(e['state'], 1)


if __name__ == '__main__':
    unittest.main()
