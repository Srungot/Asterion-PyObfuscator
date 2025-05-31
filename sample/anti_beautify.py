import ast
import random
import string

def generate_random_name(length=10):
    return '_' + ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def generate_complex_expression(value):
    ops = [
        lambda x: f"({x} and {x})",
        lambda x: f"({x} or {x})",
        lambda x: f"(not not {x})",
        lambda x: f"(({x}) if ({x}) else ({x}))",
    ]
    return random.choice(ops)(value)

def wrap_in_lambda(code):
    var = generate_random_name()
    return f"(lambda {var}: {code})({generate_complex_expression('True')})"

def create_nested_parentheses(code):
    for _ in range(random.randint(2, 4)):
        code = f"({code})"
    return code

def create_line_noise():
    templates = [
        "exec(chr({0})+chr({1})+chr({2}))",
        "(lambda: {0})()",
        "globals().update({{chr({0}): {1}}})",
    ]
    return random.choice(templates).format(
        random.randint(32, 126),
        random.randint(32, 126),
        random.randint(32, 126)
    )

def anti_beautify(content):
    tree = ast.parse(content)
    lines = content.split('\n')
    new_lines = []
    current_line = 0

    for node in ast.walk(tree):
        if isinstance(node, ast.Expr) and hasattr(node, 'lineno'):
            while current_line < node.lineno - 1:
                line = lines[current_line]
                if line.strip():
                    indent = ' ' * (len(line) - len(line.lstrip()))
                    if random.random() < 0.3:
                        if '=' in line and 'import' not in line:
                            parts = line.split('=')
                            if len(parts) == 2:
                                var_name = parts[0].strip()
                                value = parts[1].strip()
                                line = f"{indent}{var_name} = {wrap_in_lambda(value)}"
                        elif 'return' in line:
                            value = line.replace('return', '').strip()
                            if value:
                                line = f"{indent}return {create_nested_parentheses(value)}"
                new_lines.append(line)
                current_line += 1

            if random.random() < 0.2:
                indent = ' ' * (len(lines[current_line]) - len(lines[current_line].lstrip()))
                new_lines.append(f"{indent}{create_line_noise()}")

    while current_line < len(lines):
        new_lines.append(lines[current_line])
        current_line += 1

    result = '\n'.join(new_lines)
    try:
        ast.parse(result)
        return result
    except SyntaxError:
        return content 