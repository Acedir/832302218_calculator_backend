"""
calculator.py
安全的数学表达式解析与计算模块。

"""


class CalcError(Exception):
    pass


# ============ 1. 词法分析 ============

class Token:
    NUMBER = "NUMBER"
    OP = "OP"
    LPAREN = "LPAREN"
    RPAREN = "RPAREN"

    def __init__(self, type_, value):
        self.type = type_
        self.value = value

    def __repr__(self):
        return f"Token({self.type}, {self.value})"


def tokenize(expr: str):
    tokens = []
    i = 0
    n = len(expr)

    while i < n:
        ch = expr[i]

        # 跳过空白
        if ch.isspace():
            i += 1
            continue

        # 运算符（把 × ÷ 统一成 * /）
        if ch in "+-*/×÷":
            op = {"×": "*", "÷": "/"}.get(ch, ch)
            tokens.append(Token(Token.OP, op))
            i += 1
            continue
        if ch == "%":
            # % 视为除以 100
            tokens.append(Token(Token.OP, "/"))
            tokens.append(Token(Token.NUMBER, 100))
            i += 1
            continue

        # 左右括号
        if ch == "(":
            tokens.append(Token(Token.LPAREN, "("))
            i += 1
            continue
        if ch == ")":
            tokens.append(Token(Token.RPAREN, ")"))
            i += 1
            continue

        # 数字（含小数）
        if ch.isdigit() or ch == ".":
            j = i
            dot_count = 0
            while j < n and (expr[j].isdigit() or expr[j] == "."):
                if expr[j] == ".":
                    dot_count += 1
                    if dot_count > 1:
                        raise CalcError(f"非法数字格式（位置 {j}）")
                j += 1
            num_str = expr[i:j]
            if num_str == ".":
                raise CalcError("非法数字 '.'")
            tokens.append(Token(Token.NUMBER, float(num_str)))
            i = j
            continue

        raise CalcError(f"非法字符：'{ch}'")

    if not tokens:
        raise CalcError("表达式为空")

    return tokens


# ============ 2. 语法分析 + 计算 ============

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def peek(self):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return None

    def consume(self):
        tok = self.peek()
        self.pos += 1
        return tok

    def parse(self):
        result = self.parse_expression()
        if self.pos < len(self.tokens):
            raise CalcError("表达式末尾有多余内容")
        return result

    # 表达式 := 项 (('+' | '-') 项)*
    def parse_expression(self):
        left = self.parse_term()
        while True:
            tok = self.peek()
            if tok and tok.type == Token.OP and tok.value in ("+", "-"):
                op = self.consume().value
                right = self.parse_term()
                left = left + right if op == "+" else left - right
            else:
                break
        return left

    # 项 := 因子 (('*' | '/') 因子)*
    def parse_term(self):
        left = self.parse_factor()
        while True:
            tok = self.peek()
            if tok and tok.type == Token.OP and tok.value in ("*", "/"):
                op = self.consume().value
                right = self.parse_factor()
                if op == "*":
                    left = left * right
                else:
                    if right == 0:
                        raise CalcError("除数不能为 0")
                    left = left / right
            else:
                break
        return left

    # 因子 := ('+' | '-') 因子 | 基本
    def parse_factor(self):
        tok = self.peek()
        if tok and tok.type == Token.OP and tok.value in ("+", "-"):
            op = self.consume().value
            val = self.parse_factor()
            return val if op == "+" else -val
        return self.parse_primary()

    # 基本 := 数字 | '(' 表达式 ')'
    def parse_primary(self):
        tok = self.peek()
        if tok is None:
            raise CalcError("表达式意外结束")

        if tok.type == Token.NUMBER:
            self.consume()
            return tok.value

        if tok.type == Token.LPAREN:
            self.consume()
            val = self.parse_expression()
            closing = self.peek()
            if closing is None or closing.type != Token.RPAREN:
                raise CalcError("缺少右括号")
            self.consume()
            return val

        raise CalcError(f"非法 token：{tok.value}")


# ============ 3. 对外接口 ============

def calculate(expr: str):
    if not isinstance(expr, str):
        raise CalcError("表达式必须是字符串")

    expr = expr.strip()
    if not expr:
        raise CalcError("表达式为空")
    if len(expr) > 200:
        raise CalcError("表达式过长")

    tokens = tokenize(expr)
    parser = Parser(tokens)
    result = parser.parse()

    if abs(result) > 1e15:
        raise CalcError("结果数值过大")

    # 去掉浮点误差：整数就返回 int，小数保留 10 位
    if result == int(result):
        return int(result)
    return round(result, 10)