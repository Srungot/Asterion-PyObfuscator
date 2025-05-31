import ast
import random
import string

def generate_random_name():
    random_str = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
    return f"_卐卐卐卐卐卐卐卐卐卐卐卐卐卐卐卐卐卐卐卐卐卐卐卐卐卐卐卐卐卐卐卐卐卐卐asterionv2卐卐卐卐卐卐卐卐卐卐卐卐卐卐卐卐卐卐卐卐卐卐卐卐卐卐卐卐卐卐卐卐卐卐卐_{random_str}"

class BooleanObfuscator(ast.NodeTransformer):
    def __init__(self):
        self.true_var = generate_random_name()
        self.false_var = generate_random_name()
        
    def get_bool_assignments(self):
        """Generate the string containing boolean assignments"""
        return f"{self.true_var} = True\n{self.false_var} = False\n"
    
    def visit_Module(self, node):
        node = self.generic_visit(node)
        return node
    
    def visit_Constant(self, node):
        if isinstance(node.value, bool):
            return ast.Name(
                id=self.true_var if node.value else self.false_var,
                ctx=ast.Load()
            )
        return node
    
    def visit_NameConstant(self, node):
        if isinstance(node.value, bool):
            return ast.Name(
                id=self.true_var if node.value else self.false_var,
                ctx=ast.Load()
            )
        return node

def obfuscate_booleans(source_code):
    try:
        obfuscator = BooleanObfuscator()
        
        tree = ast.parse(source_code)
        
        modified_tree = obfuscator.visit(tree)
        
        ast.fix_missing_locations(modified_tree)
        
        obfuscated_code = ast.unparse(modified_tree)
        
        lines = obfuscated_code.split('\n')
        insert_pos = 0
        for i, line in enumerate(lines):
            if not (line.startswith('import ') or line.startswith('from ')):
                insert_pos = i
                break
        
        bool_assignments = obfuscator.get_bool_assignments().split('\n')
        lines[insert_pos:insert_pos] = bool_assignments
        
        return '\n'.join(lines)
        
    except Exception as e:
        print(f"Error during boolean obfuscation: {str(e)}")
        return source_code 