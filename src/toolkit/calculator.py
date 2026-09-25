from toolkit.constants import NUM, PLUS, MINUS, MUL, DIV, BINARY_OPS, UNARY_OPS, OPERATORS, UMINUS, PRECEDENCE, UPLUS
from toolkit.errors import EmptyExpressionError, DivisionByZeroError, InvalidExpressionError, InvalidTokenError
from decimal import Decimal


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

        elif (ch == '.' and i > 0 and i + 1 < len(expr) and expr[i - 1].isdigit() and expr[i + 1].isdigit()):
            number += ch

        elif ch in OPERATORS:
            if number != '':
                if number.count('.') > 1:
                    raise InvalidTokenError(f'Неверное число: {number}')
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
        if number.count('.') > 1:
            raise InvalidTokenError(f'Неверное число: {number}')
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
    stack = []
    for tok_type, tok_val in expr:
        if tok_type == NUM:
            stack.append(Decimal(tok_val))

        elif tok_type == UMINUS:
            if not stack:
                raise InvalidExpressionError('Нет числа после унарного минуса')
            stack.append(-stack.pop())

        elif tok_type == UPLUS:
            if not stack:
                raise InvalidExpressionError('Нет числа после унарого плюса')

        elif tok_type in BINARY_OPS:
            if len(stack) < 2:
                raise InvalidExpressionError('Должно быть как минимум два операнда для вычисления')
            b = stack.pop()
            a = stack.pop()

            if tok_type == PLUS:
                stack.append(a + b)

            elif tok_type == MINUS:
                stack.append(a - b)

            elif tok_type == MUL:
                stack.append(a * b)

            elif tok_type == DIV:
                if b == 0:
                    raise DivisionByZeroError('Деление на ноль')
                stack.append(a / b)

        else:
            raise InvalidExpressionError('Неизвестный токен')

    if len(stack) != 1:
        raise InvalidExpressionError('Остались лишние операторы, выражение неверное')

    return float(stack[0])


def calculate(expression: str) -> float:
    tokens = tokenize(expression)
    validate(tokens)
    return eval_npr(to_npr(tokens))