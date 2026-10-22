"""Local source checks only. This is NOT a Pine compiler or backtest."""
from pathlib import Path
import re

root = Path(__file__).resolve().parents[1]
strategy = (root / 'Fibonacci_v0.1_Strategy.pine').read_text()
indicator = (root / 'Fibonacci_v0.1_Indicator.pine').read_text()
start = '// All setup decisions'
strategy_setup = strategy[strategy.index(start):strategy.index('// Cancel on each execution-bar close')].strip()
indicator_setup = indicator[indicator.index(start):indicator.index('alertcondition(')].strip()
assert strategy_setup == indicator_setup, 'Setup implementations diverged'
for source in (strategy, indicator):
    assert source.startswith('//@version=6')
    # Ignore strings/comments, then check paired delimiters. Not syntax validation.
    tokens = re.sub(r'"(?:\\.|[^"\\])*"|//[^\n]*', '', source)
    stack = []
    for char in tokens:
        if char in '([{':
            stack.append(char)
        elif char in ')]}':
            assert stack and stack.pop() == {')': '(', ']': '[', '}': '{'}[char]
    assert not stack
assert 'calc_on_every_tick=false' in strategy
assert 'calc_on_order_fills=false' in strategy
assert 'process_orders_on_close=false' in strategy
assert 'qty_percent' not in strategy
assert 'qty=' in strategy
assert 'limit=signalLimit' in strategy
assert 'if bar_index != prevFillBar' in strategy
assert 'time_close == mtc' in strategy_setup
assert '[ph[1], pl[1], time[fibRight + 1], time[1]]' in strategy_setup
assert 'mtc <= blockThroughM5' in strategy_setup
assert 'array.push(usedPivots, key)' in strategy_setup
assert 'array.clear(usedPivots)' in strategy_setup
assert strategy_setup.index('if not na(lph)') > strategy_setup.index('if found')
print('PASS: shared setup source matches; delimiters and execution/source safeguards checked.')
print('NOT CHECKED: Pine types/API compatibility, TradingView execution, history, or profitability.')
