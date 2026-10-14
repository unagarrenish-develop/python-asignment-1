"""Q7: Interactive calculator with custom exceptions. Enter quit to stop."""
import re

class FormulaError(Exception): pass
class InvalidFormatError(FormulaError): pass
class UnknownVariableError(FormulaError): pass
class DivisionByZeroError(FormulaError): pass
class UnsupportedOperatorError(FormulaError): pass

FORMULA = re.compile(r"^\s*([A-Za-z_]\w*|[+-]?(?:\d+(?:\.\d*)?|\.\d+))\s*([^\s])\s*([A-Za-z_]\w*|[+-]?(?:\d+(?:\.\d*)?|\.\d+))\s*$")
ASSIGNMENT = re.compile(r"^\s*([A-Za-z_]\w*)\s*=\s*([+-]?(?:\d+(?:\.\d*)?|\.\d+))\s*$")

def number(token, variables):
    if re.fullmatch(r"[A-Za-z_]\w*", token):
        if token not in variables: raise UnknownVariableError(f"Unknown variable: {token}")
        return variables[token]
    try: return float(token)
    except ValueError: raise InvalidFormatError("Operand must be a number or known variable")

def calculate(left, op, right):
    if op not in {"+", "-", "*", "/", "%"}:
        raise UnsupportedOperatorError(f"Unsupported operator: {op}")
    if op in {"/", "%"} and right == 0:
        raise DivisionByZeroError("Division by zero")
    return {"+": lambda: left+right, "-": lambda: left-right, "*": lambda: left*right,
            "/": lambda: left/right, "%": lambda: left%right}[op]()

def main():
    variables = {}
    while True:
        try: line = input()
        except EOFError: break
        if line.strip().lower() == "quit": break
        try:
            assignment = ASSIGNMENT.fullmatch(line)
            if assignment:
                variables[assignment.group(1)] = float(assignment.group(2))
                continue
            match = FORMULA.fullmatch(line)
            if not match: raise InvalidFormatError("Use operand operator operand")
            left_token, op, right_token = match.groups()
            result = calculate(number(left_token, variables), op, number(right_token, variables))
            print(int(result) if result.is_integer() else result)
        except FormulaError as exc:
            print(f"{type(exc).__name__}: {exc}")

if __name__ == "__main__":
    main()
