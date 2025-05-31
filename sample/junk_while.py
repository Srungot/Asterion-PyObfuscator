import random
import ast

def is_control_structure(line):
    """Check if the line is a control structure that requires indentation."""
    control_keywords = ['if', 'else:', 'elif', 'for', 'while', 'try:', 'except:', 'finally:', 'with', 'def', 'class']
    stripped = line.strip()
    return any(stripped.startswith(k) for k in control_keywords) and stripped.endswith(':')

class JunkWhileInjector:
    def __init__(self):
        self.var_counter = 0
        self.junk_patterns = [
            # Pattern 1: Simple while with pass
            lambda var: [
                f"{var} = True",
                f"while {var}:",
                f"    {var} = False"
            ],
            # Pattern 2: While with simple counter
            lambda var: [
                f"{var} = 1",
                f"while {var}:",
                f"    {var} = 0"
            ]
        ]
    
    def get_random_junk_while(self, indent_level):
        var_name = f"_w{self.var_counter}"
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

def add_junk_while_loops(content: str) -> str:
    """
    Add junk while loops to the Python code to make it harder to understand.
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
        injector = JunkWhileInjector()
        skip_next = False
        
        # Add initial junk loop
        new_lines.extend([
            "# Junk while loops added",
            "_initial = True",
            "while _initial:",
            "    _initial = False",
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
            
            # Add junk while loops with 50% chance
            if random.random() < 0.5:
                junk_while = injector.get_random_junk_while(indent_level)
                new_lines.append("")  # Empty line before
                new_lines.append(junk_while)
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
        print(f"Error in add_junk_while_loops: {str(e)}")
        return content 