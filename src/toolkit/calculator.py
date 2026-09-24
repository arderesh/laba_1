from toolkit.constants import NUM, PLUS, MINUS, MUL, DIV, BINARY_OPS, UNARY_OPS, OPERATORS, UMINUS, PRECEDENCE, UPLUS
from toolkit.errors import EmptyExpressionError, DivisionByZeroError, InvalidExpressionError, InvalidTokenError


def tokenize(expr):
    if not expr or not expr.strip():
        raise EmptyExpressionError("Выражение пустое. Ошибка!")

    tokens = []
    number = ''
    for i in range(len(expr)):
        ch = expr[i]
        if ch == ' ':
            continue

        elif ch.isdigit():
            number += ch
            continue

        elif ch == '.' and expr[i - 1].isdigit() and expr[i + 1].isdigit():
            number += ch

        elif ch in OPERATORS:
            if number != '':
                tokens.append((NUM, number))
                number = ''

            if ch == '+':
                if not tokens or tokens[-1][0] in BINARY_OPS or tokens[-1][0] in UNARY_OPS:
                    tokens.append((UPLUS, ch))
                else:
                    tokens.append((PLUS, ch))
                continue

            if ch == '-':
                if not tokens or tokens[-1][0] in BINARY_OPS or tokens[-1][0] in UNARY_OPS:
                    tokens.append((UMINUS, ch))
                else:
                    tokens.append((MINUS, ch))
                continue

            if ch == '*':
                tokens.append((MUL, ch))
                continue

            if ch == '/':
                tokens.append((DIV, ch))
                continue

        else:
            raise InvalidTokenError(f'Неверный символ в выражении: {ch}')

    if number != '':
        tokens.append((NUM, number))

    return tokens


def push_op(stack, res, op):
    while stack and PRECEDENCE.get(stack[-1][0]) >= PRECEDENCE[op[0]]:
        res.append(stack.pop())
    stack.append(op)

def validate(tokens):
    if not tokens:
        raise EmptyExpressionError('Выражение пустое. Ошибка')

    if tokens[0][0] in (MUL, DIV):
        raise InvalidExpressionError('Первым знаком в выражении не может быть * или /. Ошибка')

    if tokens[-1][0] != NUM:
        raise InvalidExpressionError('Выражение должно заканчиваться числом. Ошибка')

    for i in range(len(tokens) - 1):
        current = tokens[i][0]
        later = tokens[i + 1][0]

        if current in BINARY_OPS and later in BINARY_OPS:
            raise InvalidExpressionError('Два бинарных оператора подряд. Ошибка')

        if current == NUM and later == NUM:
            raise InvalidExpressionError('Два числа без оператора. Ошибка')

        if current in UNARY_OPS and later != NUM:
            raise InvalidExpressionError('Унарный оператор не перед числом. Ошибка')

def to_npr(tokens):
    res = []
    stack = []

    for tok in tokens:
        if tok[0] == NUM:
            res.append(tok)

        elif tok[0] in UNARY_OPS:
            stack.append(tok)

        elif tok[0] in BINARY_OPS:
            push_op(stack, res, tok)

    while stack:
        res.append(stack.pop())

    return res

def eval_npr(expr):
    i = 0
    while i < len(expr) - 1:
        if expr[i][0] == NUM and expr[i + 1][0] == 'UMINUS':
            del expr[i + 1]
            number = '-' + expr[i][1]
            new_n = ('NUM', number)
            expr[i] = new_n
        elif expr[i][0] == NUM and expr[i + 1][0] == 'UPLUS':
            del expr[i + 1]
            number = expr[i][1]
            new_n = ('NUM', number)
            expr[i] = new_n
        i += 1

    i = 0
    while len(expr) != 1:
        if expr[i][0] == NUM and expr[i + 1][0] == NUM and expr[i + 2][0] in BINARY_OPS:
            first_num = float(expr[i][1])
            second_num = float(expr[i + 1][1])

            op = expr[i + 2][1]

            if op == '+':
                res = first_num + second_num

            elif op == '-':
                res = first_num - second_num

            elif op == '*':
                res = first_num * second_num

            elif op == '/':
                if second_num == 0:
                    raise DivisionByZeroError('Деление на ноль. Ошибка')
                else:
                    res = first_num / second_num

            result = ('NUM', str(res))
            expr[i] = result

            del expr[i + 1], expr[i + 1]

            i = 0
        else:
            i += 1

    return float(expr[0][1])


expression = input()
tokens = tokenize(expression)
# print(to_npr(tokens))
validate(tokens)
print(eval_npr(to_npr(tokens)))