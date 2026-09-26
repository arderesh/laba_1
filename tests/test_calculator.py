import pytest

from toolkit.calculator import calculate, to_npr, tokenize
from toolkit.constants import MINUS, MUL, NUM, PLUS, UMINUS
from toolkit.errors import (
    DivisionByZeroError,
    EmptyExpressionError,
    InvalidExpressionError,
    InvalidTokenError,
)


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
def test_caltulate_positive(expression: str, expected: float) -> None:
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
def test_calculate_negative(expression: str, error: type[Exception]) -> None:
    with pytest.raises(error):
        calculate(expression)


def test_tokenize_distinguishes_unary_and_binary_minus():
    tokens = tokenize("-2 * -3")
    assert tokens[0][0] == UMINUS
    assert tokens[1][0] == NUM
    assert tokens[2][0] == MUL
    assert tokens[3][0] == UMINUS
    assert tokens[4][0] == NUM


def test_tokenize_minus_after_number_is_binary():
    tokens = tokenize("5 - 3")
    assert tokens[1][0] == MINUS


def test_to_npr_respects_precedence():
    rpn = to_npr(tokenize("2+3*4"))
    assert [tok[0] for tok in rpn] == [NUM, NUM, NUM, MUL, PLUS]