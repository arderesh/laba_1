import pytest
from toolkit.calculator import calculate, to_npr, tokenize
from toolkit.constants import MINUS, PLUS, NUM, MUL, UMINUS
from toolkit.errors import EmptyExpressionError, DivisionByZeroError, InvalidExpressionError, InvalidTokenError

@pytest.mark.parametrize(
    ("expression", "expected"),
    [   ("2+3*4", 14),
        ("10 / 4", 2.5),
        ("-2 * -3", 6),
        ("1+-2", -1),
        (" 2 + 3 * 4 ", 14),
        ("1.2*3", 3.6),
        ("+5", 5),
        ("7", 7)]
)
def test_caltulate_positive(expression, expected):
    assert calculate(expression) == pytest.approx(expected)


@pytest.mark.parametrize(
    ("expression", "error"),
    [   ("", EmptyExpressionError),
        ("   ", EmptyExpressionError),
        ("2*/3", InvalidExpressionError),
        ("2+", InvalidExpressionError),
        ("*3", InvalidExpressionError),
        ("2+a", InvalidTokenError),
        ("2..3", InvalidTokenError),
        ("1/0", DivisionByZeroError)]
)
def test_calculate_negative(expression, error):
    with pytest.raises(error):
        calculate(expression)