import random
import string
import ast

def generate_random_var():
    """Generate a random variable name with random number of underscores and a random letter"""
    left_underscores = '_' * random.randint(20, 100)
    right_underscores = '_' * random.randint(20, 100)
    
    letter = random.choice(string.ascii_uppercase)
    
    var_name = f"{left_underscores}{letter}{right_underscores}"
    return var_name

def generate_junk_line():
    """Generate a complete junk variable line"""
    var_name = generate_random_var()
    value_var = generate_random_var()
    return f"{var_name} = \"\"\n{value_var} = {var_name}"

def add_junk_vars(content):
    """Add junk variables between each line of code"""
    tree = ast.parse(content)
    
    lines = content.split('\n')
    result_lines = []
    
    for line in lines:
        if line.strip():       
            result_lines.append(line)
            for _ in range(random.randint(1, 3)):
                result_lines.append(generate_junk_line())
        else:
            result_lines.append(line)
    
    result = '\n'.join(result_lines)
    
    try:
        ast.parse(result)
        return result
    except SyntaxError:
        return content 