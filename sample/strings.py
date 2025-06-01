import base64
import re
import zlib
import marshal
import random
import binascii
import ast
from bitstring import BitArray


def rot_encode(text, shift):
    result = ""
    for char in text:
        if char.isalpha():
            ascii_offset = ord('A') if char.isupper() else ord('a')
            rotated = chr((ord(char) - ascii_offset + shift) % 26 + ascii_offset)
            result += rotated
        else:
            result += char
    return result

def rot_decode(text, shift):
    return rot_encode(text, -shift)

def encode_with_methods(string):
    rot_methods = [
        (f'rot{i}', lambda s, i=i: rot_encode(s.decode('utf-8') if isinstance(s, bytes) else s, i).encode('utf-8'))
        for i in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20,
                 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40,
                 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 100, 150, 200, 250, 300, 350, 400, 450, 500,
                 1000, 2000, 3000, 4000, 5000, 10000]
    ]
    
    compression_methods = [
        ('base64', lambda s: base64.b64encode(s if isinstance(s, bytes) else s.encode('utf-8'))),
        ('base85', lambda s: base64.b85encode(s if isinstance(s, bytes) else s.encode('utf-8'))),
        ('zlib', lambda s: zlib.compress(s if isinstance(s, bytes) else s.encode('utf-8'))),
        ('marshal', lambda s: marshal.dumps(s.decode('utf-8') if isinstance(s, bytes) else s)),
        ('hex', lambda s: binascii.hexlify(s if isinstance(s, bytes) else s.encode('utf-8')))
    ]
    
    current_data = string
    encoding_sequence = []
    
    random.shuffle(rot_methods)
    rot_count = 0
    for method_name, method_func in rot_methods:
        if rot_count >= 12:      
            break
        try:
            new_data = method_func(current_data)
            current_data = new_data
            encoding_sequence.append(method_name)
            print(f"Successfully applied {method_name}")
            rot_count += 1
        except Exception as e:
            print(f"Failed to apply {method_name}: {str(e)}")
    
    random.shuffle(compression_methods)
    compression_count = 0
    for method_name, method_func in compression_methods:
        if compression_count >= 3:        
            break
        try:
            new_data = method_func(current_data)
            current_data = new_data
            encoding_sequence.append(method_name)
            print(f"Successfully applied {method_name}")
            compression_count += 1
        except Exception as e:
            print(f"Failed to apply {method_name}: {str(e)}")
    
    if len(encoding_sequence) < 15:
        print(f"Only managed to apply {len(encoding_sequence)} methods: {', '.join(encoding_sequence)}")
        raise ValueError("Could not apply minimum 15 encoding methods")
    
    final_encoded = base64.b64encode(current_data).decode('utf-8')
    return final_encoded, encoding_sequence

class StringTransformer(ast.NodeTransformer):
    def visit_JoinedStr(self, node):
        parts = []
        for value in node.values:
            if isinstance(value, ast.Constant):
                if value.value:       
                    encoded, sequence = encode_with_methods(value.value)
                    parts.append(self.create_decode_chain(encoded, sequence))
                else:
                    parts.append('""')
            elif isinstance(value, ast.FormattedValue):
                parts.append(f"str({ast.unparse(value.value)})")
        
        if not parts:
            return ast.Constant(value="")
        
        joined = " + ".join(parts)
        return ast.parse(joined).body[0].value
    
    def visit_Constant(self, node):
        if isinstance(node.value, str) and node.value:
            encoded, sequence = encode_with_methods(node.value)
            decode_expr = self.create_decode_chain(encoded, sequence)
            return ast.parse(decode_expr).body[0].value
        return node
    
    def create_decode_chain(self, encoded_data, sequence):
        decode_chain = f"base64.b64decode('{encoded_data}'.encode('utf-8'))"
        needs_decode = True
        
        for method in reversed(sequence):
            if method == 'marshal':
                decode_chain = f"marshal.loads({decode_chain})"
                needs_decode = False      
            elif method == 'zlib':
                decode_chain = f"zlib.decompress({decode_chain})"
                needs_decode = True
            elif method == 'base85':
                decode_chain = f"base64.b85decode({decode_chain})"
                needs_decode = True
            elif method == 'base64':
                decode_chain = f"base64.b64decode({decode_chain})"
                needs_decode = True
            elif method == 'hex':
                decode_chain = f"binascii.unhexlify({decode_chain})"
                needs_decode = True
            elif method.startswith('rot'):
                shift = int(method[3:])
                if needs_decode:
                    decode_chain = f"{decode_chain}.decode('utf-8')"
                    needs_decode = False
                decode_chain = f"''.join(chr((ord(c) - (ord('A') if c.isupper() else ord('a')) - {shift}) % 26 + (ord('A') if c.isupper() else ord('a'))) if c.isalpha() else c for c in {decode_chain})"
                decode_chain = f"({decode_chain}).encode('utf-8')"
                needs_decode = True

        if needs_decode:
            decode_chain += ".decode('utf-8')"
        
        return decode_chain

def find_and_encode_strings(content):
    required_imports = """import base64
import zlib
import marshal
import binascii"""
    
    try:
        tree = ast.parse(content)
        transformer = StringTransformer()
        modified_tree = transformer.visit(tree)
        ast.fix_missing_locations(modified_tree)
        
        return required_imports + "\n" + ast.unparse(modified_tree)
    except Exception as e:
        print(f"Error during string transformation: {str(e)}")
        return content