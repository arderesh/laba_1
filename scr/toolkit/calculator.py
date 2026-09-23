from toolkit.constants import NUM, PLUS, MINUS, MUL, DIV, BINARY_OPS, UNARY_OPS, OPERATORS, UMINUS, PRECEDENCE, UPLUS


def tokenize(expr):
    tokens = []
    number = ''
    for ch in expr:
        if ch == ' ':
            continue

        if ch.isdigit():
            number += ch
            continue

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

    if number != '':
        tokens.append((NUM, number))


    return tokens


def push_op(stack, res, op):
    while stack and PRECEDENCE.get(stack[-1][0]) >= PRECEDENCE[op[0]]:
        res.append(stack.pop())
    stack.append(op)


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




    # if tokens[0][0] == UMINUS:
    #     stack.append('-')
    #
    #     for i in range(1, len(tokens)):
    #         if tokens[i][0] == NUM:
    #             res.append(tokens[i][1])
    #         elif tokens[i][0] in UNARY_OPS and tokens[i - 1][0] in OPERATORS:
    #             res.append(tokens[i][1])
    #         elif tokens[i][0] in OPERATORS:
    #             push_op(stack, res, tokens[i][1])
    # else:
    #     for i in range(len(tokens)):
    #         if tokens[i][1].isdigit():
    #             res.append(tokens[i][1])
    #         elif tokens[i][0] in UNARY_OPS and tokens[i - 1][0] in OPERATORS:
    #             res.append(tokens[i][1])
    #         elif tokens[i][0] in OPERATORS:
    #             push_op(stack, res, tokens[i][1])
    #
    # return res, stack

expression = input()
tokens = tokenize(expression)
print(tokens)
print(to_npr(tokens))