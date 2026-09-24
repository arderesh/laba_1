from toolkit.constants import UPLUS, UMINUS, OPERATORS, BINARY_OPS, UNARY_OPS

expr = [('NUM', '5.13'), ('UPLUS', '+'), ('NUM', '2'), ('MUL', '*')]

while len(expr) > 1:
    if expr[1][0] == UMINUS:
        del expr[1]
        number = '-' + expr[0][1]
        new_n = ('NUM', number)
        expr[0] = new_n
    elif expr[1][0] == UPLUS:
        del expr[1]
        number = expr[0][1]
        new_n = ('NUM', number)
        expr[0] = new_n
    break
print(expr)