import ast
import random
import string

def generate_random_class_name():
    random_str = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
    return f"_卐卐卐卐卐卐卐卐卐卐卐卐卐卐卐卐卐卐卐卐卐卐卐卐卐卐卐卐卐卐卐卐卐卐卐asterionv2卐卐卐卐卐卐卐卐卐卐卐卐卐卐卐卐卐卐卐卐卐卐卐卐卐卐卐卐卐卐卐卐卐卐卐_{random_str}"

class ClassRenamer(ast.NodeTransformer):
    def __init__(self):
        self.class_mapping = {}
    
    def visit_ClassDef(self, node):
        if node.name not in self.class_mapping and not node.name.startswith('_'):
            self.class_mapping[node.name] = generate_random_class_name()
        
        if node.name in self.class_mapping:
            node.name = self.class_mapping[node.name]
        
        new_bases = []
        for base in node.bases:
            if isinstance(base, ast.Name) and base.id in self.class_mapping:
                new_bases.append(ast.Name(id=self.class_mapping[base.id], ctx=base.ctx))
            else:
                new_bases.append(base)
        node.bases = new_bases
        
        return self.generic_visit(node)
    
    def visit_Name(self, node):
        if node.id in self.class_mapping:
            return ast.Name(id=self.class_mapping[node.id], ctx=node.ctx)
        return node

def rename_classes(source_code):
    try:
        tree = ast.parse(source_code)
        
        renamer = ClassRenamer()
        modified_tree = renamer.visit(tree)
        
        ast.fix_missing_locations(modified_tree)
        
        return ast.unparse(modified_tree)
    except Exception as e:
        print(f"Error during class renaming: {str(e)}")
        return source_code 