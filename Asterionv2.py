import sys, ast, os, argparse
from sample.strings import find_and_encode_strings
from sample.variables import rename_variables
from sample.classes import rename_classes
from sample.definitions import rename_definitions
from sample.comments import remove_comments
from sample.self import rename_self_references
from sample.booleans import obfuscate_booleans
from sample.int import obfuscate_integers
from sample.float import obfuscate_floats
from sample.remove_line import remove_empty_lines
from sample.onliner_var import process_file
from sample.oneline_imports import process_imports
from sample.watermark import add_watermark
from sample.junk_var import add_junk_vars
from sample.tab_1 import convert_indentation
from sample.junk_for import add_junk_for_loops
from sample.junk_while import add_junk_while_loops
from sample.check_integrity import inject_integrity_checks
from sample.dead_code import insert_dead_code
from sample.anti_beautify import anti_beautify
from sample.beautify import beautify_code
import platform
import getpass
import hashlib

def get_hwid() -> str:
    machine_uuid = platform.node()
    username = getpass.getuser()
    raw_data = f"{machine_uuid}{username}".encode('utf-8')
    hwid = hashlib.sha256(raw_data).hexdigest()
    return hwid

def validate_syntax(content):
    try:
        ast.parse(content)
        return True
    except SyntaxError:
        return False

def obfuscate_file(input_file, output_file=None, options=None):
    if not os.path.exists(input_file):
        print(f"Error: Input file '{input_file}' not found.")
        return False

    if output_file is None:
        filename, ext = os.path.splitext(input_file)
        output_file = f"{filename}_asterion{ext}"

    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            content = f.read()

        content = content.replace("é", "e")
        content = content.replace("è", "e")
        content = content.replace("ê", "e")
        content = content.replace("ë", "e")
        content = content.replace("à", "a")
        content = content.replace("â", "a")
        content = content.replace("ä", "a")
        content = content.replace("î", "i")
        content = content.replace("ï", "i")
        content = content.replace("ô", "o")
        content = content.replace("ö", "o")
        content = content.replace("ù", "u")
        content = content.replace("û", "u")
        content = content.replace("ü", "u")
        content = content.replace("ÿ", "y")
        content = content.replace("ç", "c")
        content = content.replace("É", "E")
        content = content.replace("È", "E")
        content = content.replace("Ê", "E")
        content = content.replace("Ë", "E")
        content = content.replace("À", "A")
        content = content.replace("Â", "A")
        content = content.replace("Ä", "A")
        content = content.replace("Î", "I")
        content = content.replace("Ï", "I")
        content = content.replace("Ô", "O")
        content = content.replace("Ö", "O")
        content = content.replace("Ù", "U")
        content = content.replace("Û", "U")
        content = content.replace("Ü", "U")
        content = content.replace("Ÿ", "Y")
        content = content.replace("Ç", "C")

        if options.get('remove_comments', True):
            content = remove_comments(content)
            if not validate_syntax(content):
                raise SyntaxError("Invalid syntax after removing comments")
        
        if options.get('dead_code', True):
            content = insert_dead_code(content)
            if not validate_syntax(content):
                raise SyntaxError("Invalid syntax after inserting dead code")
        
        if options.get('junk_while', True):
            content = add_junk_while_loops(content)
            if not validate_syntax(content):
                raise SyntaxError("Invalid syntax after adding junk while loops")
        
        if options.get('junk_for', True):
            content = add_junk_for_loops(content)
            if not validate_syntax(content):
                raise SyntaxError("Invalid syntax after adding junk for loops")
        
        if options.get('rename_classes', True):
            content = rename_classes(content)
            if not validate_syntax(content):
                raise SyntaxError("Invalid syntax after renaming classes")
        
        if options.get('rename_functions', True):
            content = rename_definitions(content)
            if not validate_syntax(content):
                raise SyntaxError("Invalid syntax after renaming definitions")
        
        if options.get('rename_self', True):
            content = rename_self_references(content)
            if not validate_syntax(content):
                raise SyntaxError("Invalid syntax after renaming self references")
        
        if options.get('rename_vars', True):
            content = rename_variables(content)
            if not validate_syntax(content):
                raise SyntaxError("Invalid syntax after renaming variables")
        
        if options.get('obf_bools', True):
            content = obfuscate_booleans(content)
            if not validate_syntax(content):
                raise SyntaxError("Invalid syntax after obfuscating booleans")
        
        if options.get('obf_ints', True):
            content = obfuscate_integers(content)
            if not validate_syntax(content):
                raise SyntaxError("Invalid syntax after obfuscating integers")
        
        if options.get('obf_floats', True):
            content = obfuscate_floats(content)
            if not validate_syntax(content):
                raise SyntaxError("Invalid syntax after obfuscating floats")
        
        if options.get('encode_strings', True):
            content = find_and_encode_strings(content)
            if not validate_syntax(content):
                raise SyntaxError("Invalid syntax after encoding strings")
        
        if options.get('oneline_vars', True):
            content = process_file(content)
            if not validate_syntax(content):
                raise SyntaxError("Invalid syntax after processing variables")
        
        if options.get('remove_lines', True):
            content = remove_empty_lines(content)
            if not validate_syntax(content):
                raise SyntaxError("Invalid syntax after removing empty lines")

        if options.get('junk_vars', True):
            content = add_junk_vars(content)
            if not validate_syntax(content):
                raise SyntaxError("Invalid syntax after adding junk variables")
        
        if options.get('convert_tabs', True):
            content = convert_indentation(content)
            if not validate_syntax(content):
                raise SyntaxError("Invalid syntax after converting indentation")
        
        if options.get('oneline_imports', True):
            content = process_imports(content)
            if not validate_syntax(content):
                raise SyntaxError("Invalid syntax after processing imports")
        
        if options.get('watermark', True):
            content = add_watermark(content)
            if not validate_syntax(content):
                raise SyntaxError("Invalid syntax after adding watermark")
        
        base_content = "#this file has been obfuscated with Asterion v2 paid by @srungot\n#don't change this file, it will break all\n" + content
        
        if options.get('integrity_check', True):
            content = inject_integrity_checks(base_content)
            if not validate_syntax(content):
                raise SyntaxError("Invalid syntax after injecting integrity checks")

        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(content)

        print(f"Successfully obfuscated file. Output saved to: {output_file}")
        return True

    except Exception as e:
        print(f"Error during obfuscation: {str(e)}")
        return False

def main():
    parser = argparse.ArgumentParser(description='Asterion v2 Python Obfuscator')
    parser.add_argument('input_file', help='Input Python file to obfuscate')
    
    parser.add_argument('--no-comments', action='store_false', dest='remove_comments', help='Disable comments removal')
    parser.add_argument('--no-dead-code', action='store_false', dest='dead_code', help='Disable dead code insertion')
    parser.add_argument('--no-junk-while', action='store_false', dest='junk_while', help='Disable junk while loops')
    parser.add_argument('--no-junk-for', action='store_false', dest='junk_for', help='Disable junk for loops')
    parser.add_argument('--no-rename-classes', action='store_false', dest='rename_classes', help='Disable class renaming')
    parser.add_argument('--no-rename-functions', action='store_false', dest='rename_functions', help='Disable function renaming')
    parser.add_argument('--no-rename-self', action='store_false', dest='rename_self', help='Disable self reference renaming')
    parser.add_argument('--no-rename-vars', action='store_false', dest='rename_vars', help='Disable variable renaming')
    parser.add_argument('--no-obf-bools', action='store_false', dest='obf_bools', help='Disable boolean obfuscation')
    parser.add_argument('--no-obf-ints', action='store_false', dest='obf_ints', help='Disable integer obfuscation')
    parser.add_argument('--no-obf-floats', action='store_false', dest='obf_floats', help='Disable float obfuscation')
    parser.add_argument('--no-encode-strings', action='store_false', dest='encode_strings', help='Disable string encoding')
    parser.add_argument('--no-oneline-vars', action='store_false', dest='oneline_vars', help='Disable one-line variable processing')
    parser.add_argument('--no-remove-lines', action='store_false', dest='remove_lines', help='Disable empty line removal')
    parser.add_argument('--no-junk-vars', action='store_false', dest='junk_vars', help='Disable junk variable insertion')
    parser.add_argument('--no-convert-tabs', action='store_false', dest='convert_tabs', help='Disable tab conversion')
    parser.add_argument('--no-oneline-imports', action='store_false', dest='oneline_imports', help='Disable one-line import processing')
    parser.add_argument('--no-watermark', action='store_false', dest='watermark', help='Disable watermark')
    parser.add_argument('--no-anti-beautify', action='store_false', dest='anti_beautify', help='Disable anti-beautify')
    parser.add_argument('--no-integrity', action='store_false', dest='integrity_check', help='Disable integrity check')
    
    parser.add_argument('--beautify', action='store_true', help='Beautify the output code')

    args = parser.parse_args()

    if 1 == 1:
        output_file = args.input_file.replace(".py", "_asterionv2.py")
        
        options = {
            'remove_comments': args.remove_comments,
            'dead_code': args.dead_code,
            'junk_while': args.junk_while,
            'junk_for': args.junk_for,
            'rename_classes': args.rename_classes,
            'rename_functions': args.rename_functions,
            'rename_self': args.rename_self,
            'rename_vars': args.rename_vars,
            'obf_bools': args.obf_bools,
            'obf_ints': args.obf_ints,
            'obf_floats': args.obf_floats,
            'encode_strings': args.encode_strings,
            'oneline_vars': args.oneline_vars,
            'remove_lines': args.remove_lines,
            'junk_vars': args.junk_vars,
            'convert_tabs': args.convert_tabs,
            'oneline_imports': args.oneline_imports,
            'watermark': args.watermark,
            'anti_beautify': args.anti_beautify,
            'integrity_check': args.integrity_check
        }
        
        if obfuscate_file(args.input_file, output_file, options):
            if args.beautify:
                print("Beautifying code...")
                with open(output_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                beautified = beautify_code(content)
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(beautified)
                print("Code beautification complete.")
    else:
        print("Invalid license")

if __name__ == "__main__":
    main()
    input("Press Enter to continue...")