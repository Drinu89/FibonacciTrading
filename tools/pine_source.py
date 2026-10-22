"""Remove explicitly marked read-only tracing for source-isolation checks."""


def without_trace(source):
    output = []
    inside = False
    for line in source.splitlines(keepends=True):
        if line.strip() == '// TRACE-BEGIN':
            assert not inside, 'Nested trace marker'
            inside = True
        elif line.strip() == '// TRACE-END':
            assert inside, 'Unmatched trace end'
            inside = False
        elif not inside:
            output.append(line)
    assert not inside, 'Unclosed trace marker'
    return ''.join(output)
