import ast
import random
import string

def generate_random_name():
    random_str = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
    return f"_卐卐卐卐卐卐卐卐卐卐卐卐卐卐卐卐卐卐卐卐卐卐卐卐卐卐卐卐卐卐卐卐卐卐卐asterionv2卐卐卐卐卐卐卐卐卐卐卐卐卐卐卐卐卐卐卐卐卐卐卐卐卐卐卐卐卐卐卐卐卐卐卐_{random_str}"

class SelfRenamer(ast.NodeTransformer):
    def __init__(self):
        self.self_mappings = {}         
        self.current_class = None
        self.in_method = False
    
    def visit_ClassDef(self, node):
        old_class = self.current_class
        self.current_class = node.name
        if self.current_class not in self.self_mappings:
            self.self_mappings[self.current_class] = generate_random_name()
        
        node.body = [self.visit(n) for n in node.body]
        
        self.current_class = old_class
        return node
    
    def visit_FunctionDef(self, node):
        if self.current_class is not None:
            old_in_method = self.in_method
            self.in_method = True
            
            if node.args.args and node.args.args[0].arg == 'self':
                node.args.args[0].arg = self.self_mappings[self.current_class]
            
            node.body = [self.visit(n) for n in node.body]
            
            self.in_method = old_in_method
            return node
        return self.generic_visit(node)
    
    def visit_Name(self, node):
        if (self.current_class is not None and 
            self.in_method and 
            isinstance(node, ast.Name) and 
            node.id == 'self'):
            return ast.Name(id=self.self_mappings[self.current_class], ctx=node.ctx)
        return node

def rename_self_references(source_code):
    try:
        tree = ast.parse(source_code)
        
        renamer = SelfRenamer()
        modified_tree = renamer.visit(tree)
        
        ast.fix_missing_locations(modified_tree)
        
        return ast.unparse(modified_tree)
    except Exception as e:
        print(f"Error during self renaming: {str(e)}")
        return source_code 