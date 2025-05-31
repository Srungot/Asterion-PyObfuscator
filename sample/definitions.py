import ast
import random
import string
from .attributes import should_preserve

def generate_random_name():
    random_str = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
    return f"_卐卐卐卐卐卐卐卐卐卐卐卐卐卐卐卐卐卐卐卐卐卐卐卐卐卐卐卐卐卐卐卐卐卐卐asterionv2卐卐卐卐卐卐卐卐卐卐卐卐卐卐卐卐卐卐卐卐卐卐卐卐卐卐卐卐卐卐卐卐卐卐卐_{random_str}"

class DefinitionRenamer(ast.NodeTransformer):
    def __init__(self):
        self.function_mapping = {}
        self.method_mapping = {}
        self.param_mapping = {}
    
    def should_rename_param(self, name):
        return not should_preserve(name, is_param=True)
    
    def collect_definitions(self, node):
        for child in ast.walk(node):
            if isinstance(child, ast.FunctionDef):
                is_method = bool(child.args.args and child.args.args[0].arg == 'self')
                
                if is_method:
                    if not should_preserve(child.name):
                        if child.name not in self.method_mapping:
                            self.method_mapping[child.name] = generate_random_name()
                else:
                    if not should_preserve(child.name):
                        if child.name not in self.function_mapping:
                            self.function_mapping[child.name] = generate_random_name()
                
                for arg in child.args.args:
                    if self.should_rename_param(arg.arg):
                        if arg.arg not in self.param_mapping:
                            self.param_mapping[arg.arg] = generate_random_name()
    
    def visit_FunctionDef(self, node):
        is_method = bool(node.args.args and node.args.args[0].arg == 'self')
        
        if is_method:
            if not should_preserve(node.name) and node.name in self.method_mapping:
                node.name = self.method_mapping[node.name]
        else:
            if not should_preserve(node.name) and node.name in self.function_mapping:
                node.name = self.function_mapping[node.name]
        
        for arg in node.args.args:
            if self.should_rename_param(arg.arg) and arg.arg in self.param_mapping:
                arg.arg = self.param_mapping[arg.arg]
        
        return self.generic_visit(node)
    
    def visit_Name(self, node):
        if node.id in self.param_mapping:
            return ast.Name(id=self.param_mapping[node.id], ctx=node.ctx)
        return node
    
    def visit_Call(self, node):
        if isinstance(node.func, ast.Attribute):
            if node.func.attr in self.method_mapping:
                node.func.attr = self.method_mapping[node.func.attr]
        elif isinstance(node.func, ast.Name):
            if node.func.id in self.function_mapping:
                node.func.id = self.function_mapping[node.func.id]
        
        for keyword in node.keywords:
            if keyword.arg in self.param_mapping:
                keyword.arg = self.param_mapping[keyword.arg]
        
        return self.generic_visit(node)

def rename_definitions(source_code):
    try:
        tree = ast.parse(source_code)
        
        renamer = DefinitionRenamer()
        
        renamer.collect_definitions(tree)
        
        modified_tree = renamer.visit(tree)
        
        ast.fix_missing_locations(modified_tree)
        
        return ast.unparse(modified_tree)
    except Exception as e:
        print(f"Error during definition renaming: {str(e)}")
        return source_code 