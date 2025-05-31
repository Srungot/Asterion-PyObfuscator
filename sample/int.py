import ast
import random
import operator

class IntegerObfuscator(ast.NodeTransformer):
    def __init__(self):
        self.operators = [
            (operator.add, '+'),
            (operator.sub, '-'),
            (operator.mul, '*'),
        ]
    
    def _generate_obfuscated_number(self, number):
        """Generate an obfuscated mathematical expression for a number"""
        if abs(number) <= 1:       
            return ast.Constant(value=number)
            
        op_func, op_symbol = random.choice(self.operators)
        if op_symbol == '*':
            factors = []
            for i in range(2, min(11, abs(number) + 1)):
                if number % i == 0:
                    factors.append(i)
            
            if factors:
                factor1 = random.choice(factors)
                factor2 = number // factor1
                return ast.BinOp(
                    left=ast.Constant(value=factor1),
                    op=ast.Mult(),
                    right=ast.Constant(value=factor2)
                )
        else:
            if op_symbol == '+':
                part1 = random.randint(-abs(number), abs(number))
                part2 = number - part1
            else:
                part1 = number + random.randint(0, abs(number) * 2)
                part2 = part1 - number
                
            return ast.BinOp(
                left=ast.Constant(value=part1),
                op=ast.Add() if op_symbol == '+' else ast.Sub(),
                right=ast.Constant(value=part2)
            )
        
        return ast.Constant(value=number)

    def visit_Constant(self, node):
        if isinstance(node.value, int) and not isinstance(node.value, bool):
            return self._generate_obfuscated_number(node.value)
        return node

    def visit_Num(self, node):      
        if isinstance(node.n, int):
            return self._generate_obfuscated_number(node.n)
        return node

def obfuscate_integers(source_code):
    """
    Replace integer literals with obfuscated mathematical expressions
    """
    try:
        tree = ast.parse(source_code)
        obfuscator = IntegerObfuscator()
        modified_tree = obfuscator.visit(tree)
        ast.fix_missing_locations(modified_tree)
        return ast.unparse(modified_tree)
    except Exception as e:
        print(f"Error during integer obfuscation: {str(e)}")
        return source_code 