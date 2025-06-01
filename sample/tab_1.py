def convert_indentation(content: str) -> str:
    lines = content.split('\n')
    converted_lines = []
    
    for line in lines:
        leading_spaces = len(line) - len(line.lstrip())
        new_indentation = ' ' * (leading_spaces // 4)
        converted_lines.append(new_indentation + line.lstrip())
    
    return '\n'.join(converted_lines) 