import ast

def remove_empty_lines(source_code):
    """
    Remove ALL empty lines from the source code
    """
    try:
        lines = source_code.splitlines()
        
        result_lines = [line for line in lines if line.strip()]
        
        return '\n'.join(result_lines)
        
    except Exception as e:
        print(f"Error during empty line removal: {str(e)}")
        return source_code 