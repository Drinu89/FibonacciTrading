"""Small test-only evaluator for the straight-line Pine subset in the M5 block.

Not a Pine compiler: no security merging, broker emulator, history or pivot finder.
Reads the production source rather than maintaining a second strategy model.
"""
import ast
import math
import re

TOKEN = re.compile(r'\s*(?:("(?:\\.|[^"\\])*")|(\d+(?:\.\d*)?)|([A-Za-z_]\w*(?:\.[A-Za-z_]\w*)*)|(==|!=|<=|>=|[+*/%<>()?:,\-]))')
PRIORITY = {'or': 1, 'and': 2, '==': 3, '!=': 3, '<': 3, '>': 3, '<=': 3, '>=': 3, '+': 4, '-': 4, '*': 5, '/': 5, '%': 5}


class Expression:
    def __init__(self, text):
        self.tokens = []
        position = 0
        while position < len(text):
            match = TOKEN.match(text, position)
            if not match:
                raise ValueError(text[position:])
            self.tokens.append(next(x for x in match.groups() if x is not None))
            position = match.end()
        self.i = 0
        self.tree = self.parse(0)
        assert self.i == len(self.tokens), self.tokens[self.i:]

    def peek(self):
        return self.tokens[self.i] if self.i < len(self.tokens) else None

    def take(self):
        result = self.tokens[self.i]
        self.i += 1
        return result

    def parse(self, minimum):
        token = self.take()
        if token in ('not', '-', '+'):
            left = ('unary', token, self.parse(6))
        elif token == '(':
            left = self.parse(0)
            assert self.take() == ')'
        elif token.startswith('"'):
            left = ('literal', ast.literal_eval(token))
        elif token[0].isdigit():
            left = ('literal', float(token) if '.' in token else int(token))
        elif self.peek() == '(':
            self.take()
            args = []
            while self.peek() != ')':
                args.append(self.parse(0))
                if self.peek() != ',':
                    break
                self.take()
            assert self.take() == ')'
            left = ('call', token, args)
        else:
            left = ('name', token)
        while self.peek() in PRIORITY and PRIORITY[self.peek()] >= minimum:
            op = self.take()
            right = self.parse(PRIORITY[op] + 1)
            left = ('binary', op, left, right)
        if minimum == 0 and self.peek() == '?':
            self.take()
            yes = self.parse(0)
            assert self.take() == ':'
            no = self.parse(0)
            left = ('conditional', left, yes, no)
        return left

    def run(self, env):
        def visit(node):
            kind = node[0]
            if kind == 'literal':
                return node[1]
            if kind == 'name':
                return env[node[1]]
            if kind == 'call':
                return env[node[1]](*(visit(x) for x in node[2]))
            if kind == 'conditional':
                return visit(node[2]) if visit(node[1]) else visit(node[3])
            if kind == 'unary':
                value = visit(node[2])
                return {'not': lambda: not value, '-': lambda: -value, '+': lambda: +value}[node[1]]()
            op = node[1]
            left = visit(node[2])
            if op == 'and':
                return bool(left) and bool(visit(node[3]))
            if op == 'or':
                return bool(left) or bool(visit(node[3]))
            right = visit(node[3])
            operations = {'==': lambda: left == right, '!=': lambda: left != right, '<': lambda: left < right, '>': lambda: left > right, '<=': lambda: left <= right, '>=': lambda: left >= right, '+': lambda: left + right, '-': lambda: left - right, '*': lambda: left * right, '/': lambda: left / right, '%': lambda: left % right}
            return operations[op]()
        return visit(self.tree)


def statements(text):
    lines = []
    for line in text.splitlines():
        if line.strip() and not line.lstrip().startswith('//'):
            lines.append((len(line)-len(line.lstrip()), line.strip()))

    def block(index, indent):
        result = []
        while index < len(lines) and lines[index][0] == indent:
            content = lines[index][1]
            if content.startswith('if '):
                branches = []
                while True:
                    condition = None if content == 'else' else Expression(content.split('if ', 1)[1])
                    index += 1
                    body, index = block(index, lines[index][0])
                    branches.append((condition, body))
                    if index >= len(lines) or lines[index][0] != indent or not lines[index][1].startswith('else'):
                        break
                    content = lines[index][1]
                result.append(('if', branches))
                continue
            if content.startswith('for '):
                name, rest = content[4:].split(' = ', 1)
                first, last = rest.split(' to ', 1)
                index += 1
                body, index = block(index, lines[index][0])
                result.append(('for', name, Expression(first), Expression(last), body))
                continue
            assignment = re.fullmatch(r'(?:(?:bool|float|int|string) )?(\w+) (:=|\+=|-=|=) (.*)', content)
            if assignment:
                name, op, value = assignment.groups()
                result.append(('assign', name, op, Expression(value)))
            else:
                result.append(('expr', Expression(content)))
            index += 1
        return result, index
    result, end = block(0, lines[0][0])
    assert end == len(lines), lines[end:]
    return result


def execute(program, env):
    for node in program:
        kind = node[0]
        if kind == 'assign':
            value = node[3].run(env)
            name, op = node[1:3]
            env[name] = env[name] + value if op == '+=' else env[name] - value if op == '-=' else value
        elif kind == 'if':
            for condition, body in node[1]:
                if condition is None or condition.run(env):
                    execute(body, env)
                    break
        elif kind == 'for':
            for number in range(int(node[2].run(env)), int(node[3].run(env)) + 1):
                env[node[1]] = number
                execute(node[4], env)
        elif kind == 'expr':
            node[1].run(env)
        else:
            raise ValueError(kind)


def functions():
    return {'na': lambda x: x is None or isinstance(x, float) and math.isnan(x), 'true': True, 'false': False, 'math.min': min, 'math.max': max, 'math.floor': math.floor, 'math.ceil': math.ceil, 'array.clear': lambda a: a.clear(), 'array.size': len, 'array.get': lambda a, i: a[i], 'array.includes': lambda a, x: x in a, 'array.push': lambda a, x: a.append(x), 'array.unshift': lambda a, x: a.insert(0, x), 'array.pop': lambda a: a.pop(), 'str.tostring': lambda x: str(x)}
