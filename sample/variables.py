import ast
import random
import string
from .attributes import should_preserve

def generate_random_name():
    random_str = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
    return f"_卐卐卐卐卐卐卐卐卐卐卐卐卐卐卐卐卐卐卐卐卐卐卐卐卐卐卐卐卐卐卐卐卐卐卐asterionv2卐卐卐卐卐卐卐卐卐卐卐卐卐卐卐卐卐卐卐卐卐卐卐卐卐卐卐卐卐卐卐卐卐卐卐_{random_str}"

class AttributeCollector(ast.NodeVisitor):
    def __init__(self):
        self.attributes = set()
        
    def visit_Attribute(self, node):
        self.attributes.add(node.attr)
        self.generic_visit(node)
        
    def visit_keyword(self, node):
        self.attributes.add(node.arg)
        self.generic_visit(node)

class VariableRenamer(ast.NodeTransformer):
    def __init__(self):
        self.variable_mapping = {}
        self.function_params = set()
    
    def visit_FunctionDef(self, node):
        for arg in node.args.args:
            if not should_preserve(arg.arg, is_param=True):
                self.function_params.add(arg.arg)
        
        result = self.generic_visit(node)
        
        for arg in node.args.args:
            if arg.arg in self.function_params:
                self.function_params.remove(arg.arg)
        
        return result
    
    def visit_Call(self, node):
        for keyword in node.keywords:
            if not should_preserve(keyword.arg, is_param=True) and keyword.arg in self.variable_mapping:
                keyword.arg = self.variable_mapping[keyword.arg]
        return self.generic_visit(node)
    
    def visit_Attribute(self, node):
        if isinstance(node.value, ast.Name):
            return ast.Attribute(
                value=self.visit(node.value),
                attr=node.attr,
                ctx=node.ctx
            )
        return self.generic_visit(node)
    
    def visit_Name(self, node):
        if should_preserve(node.id) or node.id in self.function_params:
            return node
            
        if isinstance(node.ctx, ast.Store):
            if node.id not in self.variable_mapping and not should_preserve(node.id):
                self.variable_mapping[node.id] = generate_random_name()
        
        if node.id in self.variable_mapping:
            return ast.Name(id=self.variable_mapping[node.id], ctx=node.ctx)
        return node

def rename_variables(source_code):
    try:
        tree = ast.parse(source_code)
        
        renamer = VariableRenamer()
        modified_tree = renamer.visit(tree)
        
        ast.fix_missing_locations(modified_tree)
        
        return ast.unparse(modified_tree)
    except Exception as e:
        print(f"Error during variable renaming: {str(e)}")
        return source_code 