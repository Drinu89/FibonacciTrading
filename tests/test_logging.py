"""Test actual-source trace gating and observation using the local subset runner.

Does not execute TradingView's log API or validate Pine compilation.
"""
import unittest
from pathlib import Path
from tools.pine_source import without_trace
from pine_subset import execute, functions, statements
from test_setup_pipeline import Replay

ROOT = Path(__file__).resolve().parents[1]
SOURCE = (ROOT/'Fibonacci_v0.2_Strategy.pine').read_text()
LOGGER = statements(SOURCE.split('traceLog(string eventName', 1)[1].split('=>\n', 1)[1].split('// TRACE-END', 1)[0])
LOGGED_BODY = statements(SOURCE.split('if m5Close\n', 1)[1].split('\nz1 =', 1)[0])


class LoggingTests(unittest.TestCase):
    def logger_env(self):
        messages = []
        e = functions()
        e.update(enableTrace=True, traceStart=100, traceEnd=200, traceMode='Events', detailedOnly=False, time_close=150, impulseId=9, state=2, direction=-1, eventName='CHECK', detail='reason=test')
        e['barstate.isconfirmed'] = True
        e['str.format_time'] = lambda *args: str(args[0])
        e['log.info'] = lambda *args: messages.append(args)
        return e, messages

    def test_logger_respects_toggle_window_confirmation_and_verbosity(self):
        for overrides, expected in [({}, 1), ({'enableTrace': False}, 0), ({'time_close': 99}, 0), ({'time_close': 100}, 1), ({'time_close': 200}, 0), ({'barstate.isconfirmed': False}, 0), ({'detailedOnly': True}, 0), ({'detailedOnly': True, 'traceMode': 'Detailed M5'}, 1)]:
            with self.subTest(overrides=overrides):
                env, messages = self.logger_env()
                env.update(overrides)
                execute(LOGGER, env)
                self.assertEqual(len(messages), expected)
                if messages:
                    self.assertEqual(messages[0][2], 'CHECK')
                    self.assertEqual(messages[0][-1], 'reason=test')

    def test_logged_pipeline_reports_stages_without_changing_decisions(self):
        observed = []
        unlogged = Replay()
        logged = Replay()
        # Replace only the execution engine for the logged replay with the actual
        # source that includes tracing. Callback emulates a read-only observer.
        import test_setup_pipeline as module
        original_program = module.PROGRAM
        def capture(name, detail, detailed=False):
            observed.append((name, detail, detailed))
            return 0
        logged.env.update({'traceLog': capture, 'format.mintick': 'tick', 'str.format_time': lambda *args: str(args[0]), 'str.tostring': lambda x, *args: str(x), 'mo': 107, 'sp5': 0})
        keys = ['state','impulseId','origin','endpoint','baseHigh','baseLow','buySignal','sellSignal','submittedStop','submittedLimit','tradesInImpulse','diagSweeps','diagBases','diagBreakouts','diagSubmissions']
        try:
            for row in [(108,106,107),(108.5,106.2,107.5),(108,106.1,107),(109,107,108.6),(110,107,109)]:
                module.PROGRAM = original_program
                plain = unlogged.step(*row)
                module.PROGRAM = LOGGED_BODY
                traced = logged.step(*row)
                for key in keys:
                    a,b = plain[key],traced[key]
                    # NaN is expected for order prices until submission.
                    self.assertTrue(a == b or a != a and b != b, (key,a,b))
        finally:
            module.PROGRAM = original_program
        names = {x[0] for x in observed}
        self.assertTrue({'SWEEP_PIVOT','SWEEP_STARTED','BASE_PROGRESS','BASE_FROZEN','BREAKOUT_CONFIRMED','FILTER_CHECK','ENTRY_RISK_CHECK','ORDER_CANDIDATE','ORDER_EXPIRED','M5_BAR'}.issubset(names))
        risk = next(detail for name,detail,_ in observed if name == 'ENTRY_RISK_CHECK')
        self.assertIn('risk_at_signal=', risk)
        self.assertIn('pullback_required=', risk)

    def test_required_execution_events_and_balanced_trace_blocks(self):
        without_trace(SOURCE)
        for name in ['ORDER_SUBMITTED','ENTRY_FILLED','ENTRY_AND_EXIT_SAME_BAR','ORDER_CANCEL_REQUEST','TP1_TOUCH_OBSERVED','BE_SUPPRESSED_ENTRY_BAR','BE_SEQUENCE_UNCERTAIN','BE_UPDATE_REQUEST','TRADE_CLOSED','FILL_RISK_EXCEPTION']:
            self.assertIn('traceLog("'+name+'"', SOURCE)
        stripped = without_trace(SOURCE)
        self.assertNotIn('log.info(', stripped)
        self.assertNotIn('traceLog(', stripped)
        self.assertNotIn('tracePendingImpulse', stripped)


if __name__ == '__main__':
    unittest.main()
