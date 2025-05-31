import random
import ast

def is_control_structure(line):
    """Check if the line is a control structure that requires indentation."""
    control_keywords = ['if', 'else:', 'elif', 'for', 'while', 'try:', 'except:', 'finally:', 'with', 'def', 'class']
    stripped = line.strip()
    return any(stripped.startswith(k) for k in control_keywords) and stripped.endswith(':')

class JunkForInjector:
    def __init__(self):
        self.var_counter = 0
        self.junk_patterns = [
            # Pattern 1: Simple for with pass
            lambda var: [
                f"for _ in range(1):",
                f"    pass"
            ],
            # Pattern 2: For with simple operation
            lambda var: [
                f"{var} = 0",
                f"for _ in [0]:",
                f"    {var} = 1"
            ]
        ]
    
    def get_random_junk_for(self, indent_level):
        var_name = f"_f{self.var_counter}"
        self.var_counter += 1
        pattern_func = random.choice(self.junk_patterns)
        junk_code = pattern_func(var_name)
        
        # Add proper indentation
        indented_lines = []
        for line in junk_code:
            spaces = indent_level
            if "    " in line:
                spaces += 4
                line = line.replace("    ", "", 1)
            indented_lines.append(" " * spaces + line)
        return "\n".join(indented_lines)

def add_junk_for_loops(content: str) -> str:
    """
    Add junk for loops to the Python code to make it harder to understand.
    """
    try:
        # First, validate the input code
        try:
            ast.parse(content)
        except:
            print("Input code is not valid Python")
            return content

        lines = content.split("\n")
        new_lines = []
        injector = JunkForInjector()
        skip_next = False
        
        # Add initial junk loop
        new_lines.extend([
            "# Junk for loops added",
            "_initial = 0",
            "for _ in range(1):",
            "    _initial = 1",
            ""
        ])
        
        i = 0
        while i < len(lines):
            line = lines[i].rstrip()
            new_lines.append(line)
            
            if skip_next:
                skip_next = False
                i += 1
                continue
            
            # Skip empty lines and special lines
            if not line.strip() or any(line.lstrip().startswith(word) for word in [
                'import', 'from', '@', '#', 'return', 'yield', 'raise', 'break', 'continue', 'pass'
            ]):
                i += 1
                continue
            
            # Skip if this is a control structure, but mark to add after its block
            if is_control_structure(line):
                skip_next = True
                i += 1
                continue
                
            # Get the indentation level
            indent_level = len(line) - len(line.lstrip())
            
            # Add junk for loops with 50% chance
            if random.random() < 0.5:
                junk_for = injector.get_random_junk_for(indent_level)
                new_lines.append("")  # Empty line before
                new_lines.append(junk_for)
                new_lines.append("")  # Empty line after
            
            i += 1
        
        result = "\n".join(new_lines)
        
        # Final validation
        try:
            compile(result, '<string>', 'exec')
            return result
        except Exception as e:
            print(f"Final validation failed: {str(e)}")
            return content
            
    except Exception as e:
        print(f"Error in add_junk_for_loops: {str(e)}")
        return content 