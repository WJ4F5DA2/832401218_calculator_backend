"""Safe mathematical expression parsing and evaluation.

Implements a hand-written tokenizer and recursive-descent parser.
No eval/exec is used: user input is never executed as program code.

Supported syntax:
    + - * /          binary operators (with correct precedence)
    unary + and -    e.g. -5, 3 * -2
    ( )              parentheses
    decimal numbers  e.g. 3.14, .5, 2.

Errors are reported through ExpressionError, including a user-friendly
message for invalid expressions and division by zero.
"""
from dataclasses import dataclass


class ExpressionError(Exception):
    """Raised when an expression cannot be parsed or evaluated."""


@dataclass
class Token:
    kind: str  # "num", "op", "lparen", "rparen"
    value: str


def tokenize(expression):
    """Split an expression string into a list of tokens."""
    tokens = []
    i = 0
    length = len(expression)
    while i < length:
        ch = expression[i]
        if ch.isspace():
            i += 1
            continue
        if ch.isdigit() or ch == ".":
            start = i
            while i < length and (expression[i].isdigit() or expression[i] == "."):
                i += 1
            number = expression[start:i]
            if number.count(".") > 1:
                raise ExpressionError("Invalid number: %s" % number)
            tokens.append(Token("num", number))
        elif ch in "+-*/":
            tokens.append(Token("op", ch))
            i += 1
        elif ch == "(":
            tokens.append(Token("lparen", ch))
            i += 1
        elif ch == ")":
            tokens.append(Token("rparen", ch))
            i += 1
        else:
            raise ExpressionError("Invalid character: %s" % ch)
    if not tokens:
        raise ExpressionError("Empty expression")
    return tokens


class Parser:
    """Recursive-descent parser for arithmetic expressions.

    Grammar:
        expr    := term (("+" | "-") term)*
        term    := factor (("*" | "/") factor)*
        factor  := ("+" | "-") factor | primary
        primary := NUMBER | "(" expr ")"
    """

    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def parse(self):
        value = self._parse_expr()
        if self.pos != len(self.tokens):
            raise ExpressionError("Unexpected token: %s" % self._peek().value)
        return value

    def _peek(self):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return None

    def _parse_expr(self):
        value = self._parse_term()
        while self._peek() is not None and self._peek().kind == "op" and (
            self._peek().value in "+-"
        ):
            op = self.tokens[self.pos].value
            self.pos += 1
            right = self._parse_term()
            value = value + right if op == "+" else value - right
        return value

    def _parse_term(self):
        value = self._parse_factor()
        while self._peek() is not None and self._peek().kind == "op" and (
            self._peek().value in "*/"
        ):
            op = self.tokens[self.pos].value
            self.pos += 1
            right = self._parse_factor()
            if op == "*":
                value = value * right
            else:
                if right == 0:
                    raise ExpressionError("Division by zero")
                value = value / right
        return value

    def _parse_factor(self):
        token = self._peek()
        if token is None:
            raise ExpressionError("Unexpected end of expression")
        if token.kind == "op" and token.value in "+-":
            self.pos += 1
            operand = self._parse_factor()
            return operand if token.value == "+" else -operand
        return self._parse_primary()

    def _parse_primary(self):
        token = self._peek()
        if token is None:
            raise ExpressionError("Unexpected end of expression")
        if token.kind == "num":
            self.pos += 1
            return float(token.value)
        if token.kind == "lparen":
            self.pos += 1
            value = self._parse_expr()
            closing = self._peek()
            if closing is None or closing.kind != "rparen":
                raise ExpressionError("Missing closing parenthesis")
            self.pos += 1
            return value
        raise ExpressionError("Unexpected token: %s" % token.value)


def format_number(value):
    """Format a float result, dropping a trailing .0 for integers."""
    if value == int(value) and abs(value) < 1e16:
        return str(int(value))
    return str(round(value, 10))


def evaluate(expression):
    """Evaluate an expression string and return the formatted result.

    Args:
        expression: The raw expression text sent by the front end.

    Returns:
        The result formatted as a string, e.g. "20" or "3.14".

    Raises:
        ExpressionError: If the expression is invalid or divides by zero.
    """
    if not isinstance(expression, str) or not expression.strip():
        raise ExpressionError("Empty expression")
    tokens = tokenize(expression)
    value = Parser(tokens).parse()
    return format_number(value)
