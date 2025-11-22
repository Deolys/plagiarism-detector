import ast
from typing import List, Dict, Any
from app.utils.logger import get_logger
from app.core.exceptions import CodeParseError

logger = get_logger(__name__)

class CodeParser:
    @staticmethod
    def parse_code(code: str) -> List[Dict[str, Any]]:
        try:
            tree = ast.parse(code)
        except SyntaxError as e:
            logger.error(f"Syntax error in code: {e}")
            raise CodeParseError(f"Invalid Python code: {e}")

        blocks = []

        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                try:
                    func_code = ast.get_source_segment(code, node)
                    if func_code:
                        blocks.append({
                            "type": "function",
                            "name": node.name,
                            "code": func_code,
                            "lines": (node.lineno, node.end_lineno),
                            "signature": f"def {node.name}(...)"
                        })
                except Exception as e:
                    logger.warning(f"Could not extract function {node.name}: {e}")

            elif isinstance(node, ast.ClassDef):
                try:
                    class_code = ast.get_source_segment(code, node)
                    if class_code:
                        blocks.append({
                            "type": "class",
                            "name": node.name,
                            "code": class_code,
                            "lines": (node.lineno, node.end_lineno),
                            "signature": f"class {node.name}(...)"
                        })
                except Exception as e:
                    logger.warning(f"Could not extract class {node.name}: {e}")

        if not blocks:
            logger.warning("No functions or classes found in code")
            blocks.append({
                "type": "raw",
                "name": "full_code",
                "code": code,
                "lines": (1, len(code.split("\n"))),
                "signature": "full_code"
            })

        return blocks

code_parser = CodeParser()
