import ast
import re

def find_consecutive_assignments(content):
    lines = content.split('\n')
    groups = []
    current_group = []
    current_indent = None
    
    for line in lines:
        stripped = line.strip()
        if not stripped:     
            if current_group:
                groups.append((current_indent, current_group))
                current_group = []
            continue
            
        if re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*\s*=\s*.+$', stripped):
            indent = len(line) - len(line.lstrip())
            
            if not current_group:
                current_indent = indent
                current_group = [line]
            elif indent == current_indent:
                current_group.append(line)
            else:
                if current_group:
                    groups.append((current_indent, current_group))
                current_indent = indent
                current_group = [line]
        else:
            if current_group:
                groups.append((current_indent, current_group))
                current_group = []
    
    if current_group:
        groups.append((current_indent, current_group))
    
    return groups

def convert_to_oneline(group):
    lines = [line.strip() for line in group]
    return ';'.join(lines)

def oneline_variables(content):
    groups = find_consecutive_assignments(content)
    
    if not groups:
        return content
    
    lines = content.split('\n')
    for indent, group in reversed(groups):
        if len(group) > 1:        
            start_idx = None
            for i, line in enumerate(lines):
                if line == group[0]:
                    start_idx = i
                    break
            
            if start_idx is not None:
                oneliner = ' ' * indent + convert_to_oneline(group)
                lines[start_idx:start_idx + len(group)] = [oneliner]
    
    return '\n'.join(lines)

def process_file(content):
    try:
        ast.parse(content)
        return oneline_variables(content)
    except Exception as e:
        print(f"Error during variable onelining: {str(e)}")
        return content 