import ast
import operator
import sys
from src.utils.exception import CustomException

ALLOWED_BINOPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.Mod: operator.mod,
}

ALLOWED_UNARYOPS = {
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
}


class SafeMathParser:
    """
    Evaluates arithmetic expressions using Python's AST module instead
    of eval(). Rejects any Name, Call, Attribute, Import, Subscript, or
    comparison nodes - i.e. rejects anything that isn't pure arithmetic.
    """

    def evaluate(self, expr: str) -> float:
        try:
            tree = ast.parse(expr, mode="eval")
            return self._eval_node(tree.body)
        except ZeroDivisionError as e:
            raise ValueError(f"Math Error: Division by zero in expression '{expr}'") from e
        except SyntaxError as e:
            raise ValueError(f"Syntax Error: Invalid arithmetic format in expression '{expr}'") from e
        except ValueError as e:
            raise ValueError(str(e)) from e
        except Exception as e:
            raise CustomException(e, sys) from e

    def _eval_node(self, node):
        if isinstance(node, ast.Constant):
            if isinstance(node.value, (int, float)):
                return node.value
            raise ValueError(f"Security Block: Constant of type '{type(node.value).__name__}' is disallowed")

        if isinstance(node, ast.BinOp):
            op_type = type(node.op)
            if op_type not in ALLOWED_BINOPS:
                raise ValueError(f"Security Block: Operator '{op_type.__name__}' is not allowed")
            left = self._eval_node(node.left)
            right = self._eval_node(node.right)
            return ALLOWED_BINOPS[op_type](left, right)

        if isinstance(node, ast.UnaryOp):
            op_type = type(node.op)
            if op_type not in ALLOWED_UNARYOPS:
                raise ValueError(f"Security Block: Unary operator '{op_type.__name__}' is not allowed")
            operand = self._eval_node(node.operand)
            return ALLOWED_UNARYOPS[op_type](operand)

        raise ValueError(
            f"Security Block: Disallowed expression element '{type(node).__name__}' (RCE attempt prevented)"
        )
