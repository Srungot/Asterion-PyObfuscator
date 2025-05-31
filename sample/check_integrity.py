import hashlib
import ast
import random
import base64

def generate_fake_hash():
    return ''.join(random.choice('0123456789abcdef') for _ in range(64))

def generate_code_hash(code: str) -> str:
    code_bytes = code.encode('utf-8')
    return hashlib.sha256(code_bytes).hexdigest()

def extract_hash_from_code(code: str) -> tuple[str, str]:
    lines = code.split('\n')
    real_hash = None
    for i, line in enumerate(lines):
        if line.startswith('#') and len(line) > 65:
            hashes = [h.strip() for h in line[1:].split() if len(h.strip()) == 64]
            if hashes and hashes[-1] == generate_code_hash('\n'.join(lines[:i] + lines[i+1:])):
                real_hash = hashes[-1]
                code_without_hash = '\n'.join(lines[:i] + lines[i+1:])
                return real_hash, code_without_hash
    return None, code

def generate_random_var():
    return '_' + ''.join(random.choice('abcdefghijklmnopqrstuvwxyz') for _ in range(5))

def generate_integrity_check_code(hash_value: str) -> str:
    var1, var2, var3 = generate_random_var(), generate_random_var(), generate_random_var()
    check_code = f"""
{var1}=lambda:{var2}
{var2}=lambda:open(__file__,'r',encoding='utf-8').read()
{var3}=(lambda c:exit(1)if not any(any(h==hashlib.sha256('\\n'.join(c.split('\\n')[:i]+c.split('\\n')[i+1:]).encode('utf-8')).hexdigest()for h in[x.strip()for x in l[1:].split()if len(x.strip())==64])for i,l in enumerate(c.split('\\n'))if l.startswith('#')and len(l)>65)else None)({var2}())"""
    return check_code

def add_hash_with_decoys(code: str) -> str:
    real_hash = generate_code_hash(code)
    num_decoys = random.randint(157, 567)
    decoy_hashes = [generate_fake_hash() for _ in range(num_decoys)]
    hash_position = random.randint(0, num_decoys)
    all_hashes = decoy_hashes[:hash_position] + [real_hash] + decoy_hashes[hash_position:]
    hash_line = '#' + ' '.join(all_hashes)

    return hash_line + '\n' + code

def inject_integrity_checks(code: str) -> str:
    tree = ast.parse(code)
    functions = [node for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
    
    lines = code.split('\n')
    insertion_points = []
    
    for func in functions:
        if len(func.body) > 2:
            insertion_points.append(func.body[0].lineno)
    
    if not insertion_points:
        return code
    
    selected_points = random.sample(insertion_points, min(len(insertion_points), 3))
    selected_points.sort(reverse=True)
    
    for point in selected_points:
        indent = ' ' * (len(lines[point-1]) - len(lines[point-1].lstrip()))
        check_code = generate_integrity_check_code(generate_code_hash(code))
        check_code = '\n'.join(indent + line for line in check_code.split('\n') if line)
        lines.insert(point, check_code)
    
    imports = "import hashlib,sys;from sys import exit"
    lines.insert(0, imports)
    
    code = '\n'.join(lines)
    return add_hash_with_decoys(code)

def verify_code_integrity(file_path: str) -> bool:
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        stored_hash, code_without_hash = extract_hash_from_code(content)
        if not stored_hash:
            print("No integrity hash found in the file")
            return False
        
        current_hash = generate_code_hash(code_without_hash)
        
        if current_hash == stored_hash:
            print("Code integrity verified: The file has not been modified")
            return True
        else:
            print("Warning: Code integrity check failed - The file has been modified")
            return False
            
    except Exception as e:
        print(f"Error during integrity check: {str(e)}")
        return False

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python check_integrity.py <file_to_check>")
        sys.exit(1)
    
    file_to_check = sys.argv[1]
    verify_code_integrity(file_to_check) 