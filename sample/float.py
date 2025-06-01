import ast
import random
import math

class FloatObfuscator(ast.NodeTransformer):
    def __init__(self):
        self.methods = [
            self._obfuscate_with_division,
            self._obfuscate_with_multiplication,
            self._obfuscate_with_addition
        ]
    
    def _obfuscate_with_division(self, number):
        multiplier = random.randint(2, 10)
        return ast.BinOp(
            left=ast.Constant(value=number * multiplier),
            op=ast.Div(),
            right=ast.Constant(value=multiplier)
        )
    
    def _obfuscate_with_multiplication(self, number):
        factor = random.uniform(0.1, 10.0)
        return ast.BinOp(
            left=ast.Constant(value=number / factor),
            op=ast.Mult(),
            right=ast.Constant(value=factor)
        )
    
    def _obfuscate_with_addition(self, number):
        offset = random.uniform(-10.0, 10.0)
        return ast.BinOp(
            left=ast.Constant(value=number - offset),
            op=ast.Add(),
            right=ast.Constant(value=offset)
        )

    def _generate_obfuscated_float(self, number):
        if abs(number) < 0.0001 or math.isnan(number) or math.isinf(number):
            return ast.Constant(value=number)
            
        obfuscation_method = random.choice(self.methods)
        return obfuscation_method(number)

    def visit_Constant(self, node):
        if isinstance(node.value, float):
            return self._generate_obfuscated_float(node.value)
        return node

    def visit_Num(self, node):      
        if isinstance(node.n, float):
            return self._generate_obfuscated_float(node.n)
        return node

def obfuscate_floats(source_code):
    try:
        tree = ast.parse(source_code)
        obfuscator = FloatObfuscator()
        modified_tree = obfuscator.visit(tree)
        ast.fix_missing_locations(modified_tree)
        return ast.unparse(modified_tree)
    except Exception as e:
        print(f"Error during float obfuscation: {str(e)}")
        return source_code 