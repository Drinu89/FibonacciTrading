"""Execute a constrained Python translation of the actual Pine anchor engine.

Confirmed pivot values are explicit test inputs. This does not implement Pine's
pivot finder, request.security merging, broker execution, or a Pine compiler.
"""
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = (ROOT / 'Fibonacci_v0.2_Strategy.pine').read_text()
ENGINE = SOURCE.split('// BEGIN STRUCTURE ENGINE\n', 1)[1].split('// END STRUCTURE ENGINE', 1)[0]


def translated_engine():
    body = ENGINE.split('structureEngine() =>\n', 1)[1]
    persistent = re.findall(r'^    var (?:float|int) (\w+) =', body, re.M)
    lines = ['def step(self, *, high, low, close, time, ph=None, pl=None, pivot_time=None):']
    for raw in body.splitlines():
        text = raw.strip()
        if not text or text.startswith('//'):
            continue
        if text.startswith(('ph = ta.', 'pl = ta.')):
            continue
        if text == 'pivotTime = time[fibRight]':
            raw = raw.replace('time[fibRight]', 'pivot_time')
        if text.startswith('var '):
            match = re.fullmatch(r'var (?:float|int) (\w+) = (.+)', text)
            name, value = match.groups()
            lines.append(f'    if not hasattr(self, "{name}"): self.{name} = {"None" if value == "na" else value}')
            continue
        line = raw.replace(':=', '=').replace('math.max', 'max').replace('math.min', 'min')
        line = re.sub(r'\bna\(', 'is_na(', line)
        for name in sorted(persistent, key=len, reverse=True):
            line = re.sub(rf'\b{name}\b', f'self.{name}', line)
        if line.strip().startswith(('if ', 'else if ')):
            line = line.replace('else if ', 'elif ', 1) + ':'
        if line.strip().startswith('['):
            line = line[:len(line) - len(line.lstrip())] + 'return ' + line.strip()
        lines.append(line)
    namespace = {'is_na': lambda value: value is None}
    exec('\n'.join(lines), namespace)
    return type('PineEngineTranslation', (), {'step': namespace['step']})


Engine = translated_engine()


def seed():
    e = Engine()
    e.step(high=100, low=80, close=90, time=0, pl=80, pivot_time=-3)
    e.step(high=109, low=90, close=100, time=1, ph=110, pivot_time=-2)
    return e


class StructureTests(unittest.TestCase):
    def test_minor_pivot_pair_does_not_create_impulse(self):
        e = seed()
        result = e.step(high=107, low=90, close=100, time=2, ph=108, pivot_time=-1)
        self.assertEqual(result[2], 0)
        self.assertIsNone(result[3])

    def test_wick_only_break_does_not_qualify(self):
        e = seed()
        result = e.step(high=115, low=95, close=109, time=2)
        self.assertEqual(result[6], 0)
        self.assertEqual(result[7], 0)

    def test_close_break_waits_for_confirmed_endpoint_and_locks_origin(self):
        e = seed()
        broken = e.step(high=115, low=95, close=112, time=2)
        self.assertEqual(broken[6], 1)
        self.assertIsNone(broken[3])
        e.step(high=117, low=91, close=113, time=3, pl=90, pivot_time=0)
        e.step(high=114, low=100, close=112, time=4)
        result = e.step(high=114, low=100, close=112, time=6, ph=117, pivot_time=3)
        self.assertEqual(result[:6], [80, 117, 1, 6, -3, 3])
        self.assertEqual(result[7], 1)

    def test_sell_symmetry(self):
        e = Engine()
        bars = [
            dict(high=100, low=80, close=90, time=0, pl=80, pivot_time=-3),
            dict(high=109, low=90, close=100, time=1, ph=110, pivot_time=-2),
            dict(high=115, low=95, close=112, time=2),
            dict(high=117, low=91, close=113, time=3, pl=90, pivot_time=0),
            dict(high=114, low=100, close=112, time=6, ph=117, pivot_time=3),
        ]
        for row in bars:
            mirrored = dict(high=1000-row['low'], low=1000-row['high'], close=1000-row['close'], time=row['time'])
            if 'ph' in row:
                mirrored['pl'] = 1000-row['ph']
            if 'pl' in row:
                mirrored['ph'] = 1000-row['pl']
            if 'pivot_time' in row:
                mirrored['pivot_time'] = row['pivot_time']
            result = e.step(**mirrored)
        self.assertEqual(result[:6], [920, 883, -1, 6, -3, 3])
        self.assertEqual(result[8], 1)

    def test_more_extreme_wick_defers_endpoint(self):
        e = seed()
        e.step(high=115, low=95, close=112, time=2)
        e.step(high=118, low=100, close=114, time=3)
        r = e.step(high=114, low=100, close=112, time=5, ph=115, pivot_time=2)
        self.assertIsNone(r[3])
        r = e.step(high=114, low=100, close=112, time=6, ph=118, pivot_time=3)
        self.assertEqual(r[1:4], [118, 1, 6])

    def test_origin_breach_discards_developing_leg(self):
        e = seed()
        e.step(high=115, low=95, close=112, time=2)
        e.step(high=114, low=79, close=95, time=3)
        r = e.step(high=105, low=90, close=100, time=5, ph=115, pivot_time=2)
        self.assertEqual(r[6], 0)
        self.assertIsNone(r[3])

    def test_origin_touch_survives(self):
        e = seed()
        e.step(high=115, low=95, close=112, time=2)
        e.step(high=114, low=80, close=95, time=3)
        r = e.step(high=105, low=90, close=100, time=5, ph=115, pivot_time=2)
        self.assertEqual(r[:4], [80, 115, 1, 5])

    def test_same_level_cannot_repeat_break(self):
        e = seed()
        for t in range(2, 7):
            r = e.step(high=115, low=95, close=112, time=t)
        self.assertEqual(r[7], 1)
        self.assertIsNone(r[3])

    def test_endpoint_before_break_rejected(self):
        e = seed()
        e.step(high=115, low=95, close=112, time=2)
        r = e.step(high=114, low=95, close=112, time=3, ph=115, pivot_time=1)
        self.assertIsNone(r[3])

    def test_opposite_close_break_replaces_developing_direction(self):
        e = seed()
        e.step(high=115, low=95, close=112, time=2)
        e.step(high=108, low=95, close=100, time=3, pl=90, pivot_time=0)
        r = e.step(high=108, low=85, close=88, time=4)
        self.assertEqual(r[6], -1)
        self.assertEqual(r[8], 1)
        r = e.step(high=100, low=87, close=95, time=7, pl=85, pivot_time=4)
        self.assertEqual(r[:4], [110, 85, -1, 7])

    def test_confirmed_output_not_redrawn_by_minor_pivot(self):
        e = seed()
        e.step(high=115, low=95, close=112, time=2)
        frozen = e.step(high=110, low=95, close=100, time=5, ph=115, pivot_time=2)
        later = e.step(high=108, low=95, close=100, time=9, ph=112, pivot_time=6)
        self.assertEqual(frozen[:6], later[:6])

    def test_simultaneous_pivot_types_are_ignored(self):
        e = seed()
        e.step(high=115, low=95, close=112, time=2)
        r = e.step(high=110, low=95, close=100, time=5, ph=115, pl=90, pivot_time=2)
        self.assertIsNone(r[3])


if __name__ == '__main__':
    unittest.main()
