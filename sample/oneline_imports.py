import ast
import re

def process_imports(content):
    lines = content.split('\n')
    imports = []
    non_imports = []
    current_imports = []
    
    for line in lines:
        stripped = line.strip()
        if stripped.startswith(('import ', 'from ')):
            current_imports.append(stripped)
        else:
            if current_imports:
                imports.append(';'.join(current_imports))
                current_imports = []
            if stripped:
                non_imports.append(line)
    
    if current_imports:
        imports.append(';'.join(current_imports))
    
    return '\n'.join(imports + [''] + non_imports) if imports else '\n'.join(non_imports) 