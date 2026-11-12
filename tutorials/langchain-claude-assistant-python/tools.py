"""Two local tools for the assistant: a calculator and a notes reader."""
import ast
import operator
from pathlib import Path

from langchain_core.tools import tool

NOTES_FILE = Path(__file__).with_name("notes.txt")

OPS = {
    ast.Add: operator.add, ast.Sub: operator.sub, ast.Mult: operator.mul,
    ast.Div: operator.truediv, ast.Pow: operator.pow, ast.USub: operator.neg,
}


def _eval(node):
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return node.value
    if isinstance(node, ast.BinOp) and type(node.op) in OPS:
        if isinstance(node.op, ast.Pow) and abs(_eval(node.right)) > 100:
            raise ValueError("exponent is too large")
        return OPS[type(node.op)](_eval(node.left), _eval(node.right))
    if isinstance(node, ast.UnaryOp) and type(node.op) in OPS:
        return OPS[type(node.op)](_eval(node.operand))
    raise ValueError("only numbers and + - * / ** are allowed")


@tool
def calculator(expression: str) -> str:
    """Evaluate an arithmetic expression such as '1250 + 480' or '(3 + 4) * 2.5'."""
    try:
        return str(_eval(ast.parse(expression, mode="eval").body))
    except (ValueError, SyntaxError, ZeroDivisionError, OverflowError) as err:
        return f"Error: {err}"


@tool
def read_notes() -> str:
    """Return the full text of the user's notes file."""
    if not NOTES_FILE.exists():
        return "Error: the notes file does not exist."
    return NOTES_FILE.read_text()


TOOLS = [calculator, read_notes]

if __name__ == "__main__":
    # Call the tools directly, with no model, to check them first.
    for expr in ["1250 + 480", "(3 + 4) * 2.5", "2 ** 10", "10 / 0", "__import__('os')", "9 ** 9 ** 9"]:
        print(f"calculator({expr!r}) -> {calculator.invoke({'expression': expr})}")
    print("read_notes() ->")
    print(read_notes.invoke({}))
