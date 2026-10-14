"""Q3: Recursive Expression Engine with memoization and cycle detection.
Supports non-negative integers, variable names, +, -, *, and parentheses.
"""
import sys
import re

TOKEN_RE = re.compile(r"\s*(\d+|[A-Za-z_]\w*|[()+*-])")

class InvalidExpression(Exception): pass
class DependencyCycle(Exception): pass

def tokenize(expression):
    tokens, pos = [], 0
    while pos < len(expression):
        match = TOKEN_RE.match(expression, pos)
        if not match:
            if expression[pos:].strip() == "":
                break
            raise InvalidExpression("Invalid token")
        tokens.append(match.group(1))
        pos = match.end()
    return tokens

class Parser:
    def __init__(self, tokens, resolve):
        self.tokens, self.i, self.resolve = tokens, 0, resolve

    def parse(self):
        value = self.expression()
        if self.i != len(self.tokens):
            raise InvalidExpression("Unexpected token")
        return value

    def expression(self):
        value = self.term()
        while self.i < len(self.tokens) and self.tokens[self.i] in ("+", "-"):
            op = self.tokens[self.i]; self.i += 1
            right = self.term()
            value = value + right if op == "+" else value - right
        return value

    def term(self):
        value = self.factor()
        while self.i < len(self.tokens) and self.tokens[self.i] == "*":
            self.i += 1
            value *= self.factor()
        return value

    def factor(self):
        if self.i >= len(self.tokens):
            raise InvalidExpression("Missing operand")
        token = self.tokens[self.i]; self.i += 1
        if token.isdigit():
            return int(token)
        if token == "(":
            value = self.expression()
            if self.i >= len(self.tokens) or self.tokens[self.i] != ")":
                raise InvalidExpression("Missing closing parenthesis")
            self.i += 1
            return value
        if token in ("+", "-", "*", ")"):
            raise InvalidExpression("Unexpected operator or parenthesis")
        return self.resolve(token)

def main():
    lines = sys.stdin.read().splitlines()
    try:
        v = int(lines[0].strip())
        definitions = {}
        for line in lines[1:v+1]:
            if "=" not in line: raise InvalidExpression("Definition must contain =")
            name, expr = map(str.strip, line.split("=", 1))
            if not re.fullmatch(r"[A-Za-z_]\w*", name): raise InvalidExpression("Invalid variable name")
            definitions[name] = expr
        target = "\n".join(lines[v+1:]).strip()
        cache, visiting = {}, set()
        def resolve(name):
            if name in cache: return cache[name]
            if name not in definitions: raise InvalidExpression(f"Unknown variable: {name}")
            if name in visiting: raise DependencyCycle()
            visiting.add(name)
            value = evaluate(definitions[name])
            visiting.remove(name)
            cache[name] = value
            return value
        def evaluate(expr):
            return Parser(tokenize(expr), resolve).parse()
        print(evaluate(target))
    except DependencyCycle:
        print("CYCLE")
    except (ValueError, InvalidExpression, IndexError, RecursionError):
        print("INVALID")

if __name__ == "__main__":
    main()
