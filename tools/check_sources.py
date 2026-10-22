"""Local source checks only. This is NOT a Pine compiler or backtest."""
from pathlib import Path
import re
from pine_source import without_trace

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
# The structure variant must also share its detector exactly with its indicator.
v2s = (root / 'Fibonacci_v0.2_Strategy.pine').read_text()
v2i = (root / 'Fibonacci_v0.2_Indicator.pine').read_text()
v2shared = v2s[v2s.index(start):v2s.index('// Cancel on each execution-bar close')].strip()
assert v2shared == v2i[v2i.index(start):v2i.index('alertcondition(')].strip()
assert '[a[1], b[1], d[1], eventTime[1], at[1], bt[1], pendingSide[1], buys[1], sells[1]]' in v2shared
for source in (v2s, v2i):
    tokens = re.sub(r'"(?:\\.|[^"\\])*"|//[^\n]*', '', source)
    stack = []
    for char in tokens:
        if char in '([{':
            stack.append(char)
        elif char in ')]}':
            assert stack and stack.pop() == {')': '(', ']': '[', '}': '{'}[char]
    assert not stack
# The execution wrapper, including costs, fills and provisional BE, is identical.
marker = '// Cancel on each execution-bar close'
assert strategy[strategy.index(marker):].strip() == without_trace(v2s[v2s.index(marker):]).strip()
# Following candidate detection, preserve every existing setup/order rule.
marker = '    // A queued impulse can become invalid'
end = '// This table reports setup events'
old_rules = strategy[strategy.index(marker):strategy.index(end)].strip()
new_rules = without_trace(v2s[v2s.index(marker):v2s.index('// Source counters include all loaded source history')]).strip()
new_rules = new_rules.replace('        selectedOriginTime := latestOriginTime\n', '').replace('        selectedEndpointTime := latestEndpointTime\n', '')
assert old_rules == new_rules
print('PASS: both indicator/strategy pairs match; inherited setup rules and execution wrapper are unchanged; delimiters and safeguards checked.')
print('NOT CHECKED: Pine types/API compatibility, TradingView execution, history, or profitability.')
