def convert_indentation(content: str) -> str:
    """
    Convert 4-space indentation to 1-space indentation in Python code.
    
    Args:
        content (str): The Python code content with 4-space indentation
        
    Returns:
        str: The Python code content with 1-space indentation
    """
    lines = content.split('\n')
    converted_lines = []
    
    for line in lines:
        # Count leading spaces
        leading_spaces = len(line) - len(line.lstrip())
        # Calculate new indentation (1 space per level instead of 4)
        new_indentation = ' ' * (leading_spaces // 4)
        # Add the line with new indentation
        converted_lines.append(new_indentation + line.lstrip())
    
    return '\n'.join(converted_lines) 