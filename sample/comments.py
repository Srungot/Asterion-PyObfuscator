import ast
import re

class CommentRemover(ast.NodeTransformer):
    def visit_Module(self, node):
        if (ast.get_docstring(node)):
            node.body = node.body[1:]
        return self.generic_visit(node)
    
    def visit_ClassDef(self, node):
        if (ast.get_docstring(node)):
            node.body = node.body[1:]
        return self.generic_visit(node)
    
    def visit_FunctionDef(self, node):
        if (ast.get_docstring(node)):
            node.body = node.body[1:]
        return self.generic_visit(node)
    
    def visit_AsyncFunctionDef(self, node):
        if (ast.get_docstring(node)):
            node.body = node.body[1:]
        return self.generic_visit(node)

def remove_inline_comments(source):
    result = []
    in_string = False
    string_char = None
    i = 0
    
    while i < len(source):
        char = source[i]
        
        if char in ['"', "'"]:
            if not in_string:
                in_string = True
                string_char = char
            elif char == string_char:
                in_string = False
            result.append(char)
        
        elif char == '#' and not in_string:
            while i < len(source) and source[i] != '\n':
                i += 1
            if i < len(source):
                result.append('\n')
        
        else:
            result.append(char)
        
        i += 1
    
    return ''.join(result)

def remove_comments(source_code):
    try:
        tree = ast.parse(source_code)
        remover = CommentRemover()
        modified_tree = remover.visit(tree)
        ast.fix_missing_locations(modified_tree)
        
        code_without_docstrings = ast.unparse(modified_tree)
        
        final_code = remove_inline_comments(code_without_docstrings)
        
        final_code = '\n'.join(line for line in final_code.splitlines() if line.strip())
        
        return final_code
    
    except Exception as e:
        print(f"Error during comment removal: {str(e)}")
        return source_code 