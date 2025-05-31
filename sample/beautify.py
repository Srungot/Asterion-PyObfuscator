import ast
import black
import pathlib

def beautify_code(content: str) -> str:
    try:
        ast.parse(content)
        mode = black.Mode(
            line_length=88,
            string_normalization=True,
            is_pyi=False,
        )
        beautified = black.format_str(content, mode=mode)
        return beautified
    except Exception as e:
        print(f"Error during beautification: {str(e)}")
        return content 