import ast
import random
import string

def generate_random_name(length=10):
    return '_' + ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def generate_complex_condition():
    a = random.randint(1, 100)
    b = random.randint(1, 100)
    c = random.randint(1, 100)
    return f"({a} * {b} % {c} == {(a * b) % c - 1})"

def generate_dead_code():
    templates = [
        "{var1} = 0\nif {condition}: {var1} = [{var2} for _ in range({num})]",
        "if {condition}: {var1} = {num1}\nelse: {var1} = {num2}",
        "{var1} = [{i} for {i} in range({num}) if {condition}]",
        "{var1} = sum([{num1}, {num2}]) if {condition} else {num1}",
        "{var1} = {num1}\nwhile {condition}: {var1} += 1; break"
    ]
    
    template = random.choice(templates)
    vars = {
        'var1': generate_random_name(),
        'var2': generate_random_name(),
        'i': generate_random_name(),
        'num': random.randint(1, 5),
        'num1': random.randint(1, 50),
        'num2': random.randint(1, 50),
        'condition': generate_complex_condition()
    }
    
    return template.format(**vars)

def insert_dead_code(content):
    tree = ast.parse(content)
    lines = content.split('\n')
    new_lines = []
    current_line = 0
    
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
            if hasattr(node, 'lineno'):
                while current_line < node.lineno - 1:
                    new_lines.append(lines[current_line])
                    current_line += 1
                
                if random.random() < 0.2:
                    indent = ' ' * (len(lines[current_line]) - len(lines[current_line].lstrip()))
                    dead_code = generate_dead_code()
                    dead_code_lines = dead_code.split('\n')
                    for line in dead_code_lines:
                        new_lines.append(indent + line)
    
    while current_line < len(lines):
        new_lines.append(lines[current_line])
        current_line += 1
    
    result = '\n'.join(new_lines)
    try:
        ast.parse(result)
        return result
    except SyntaxError:
        return content 