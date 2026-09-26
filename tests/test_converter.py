import pytest

from toolkit.converter import convert
from toolkit.errors import (
    BelowAbsoluteZeroError,
    IncompatibleUnitsError,
    InvalidValueError,
    UnknownUnitError,
)


@pytest.mark.parametrize(('value', 'from_unit', 'to_unit', 'expected'),
                         [ (1000, 'mm', 'm', 1),
                           (1.5, 'kg', 'g', 1500),
                           (0, 'c', 'f', 32),
                           (-273.15, 'c', 'k', 0),
                           (1000, 'MM', 'M', 1),
                           (2, 'km', 'cm', 200000)
                         ])
def test_convert_positive(value: float, from_unit: str,
                          to_unit: str, expected: float) -> None:
    assert convert(value, from_unit, to_unit) == pytest.approx(expected)


@pytest.mark.parametrize(('value', 'from_unit', 'to_unit', 'error'),
                         [
                             (-300, 'c', 'f', BelowAbsoluteZeroError),
                             (5, 'kg', 'm', IncompatibleUnitsError),
                             (5, 'm', 'lightyear', UnknownUnitError),
                             ('abs', 'm', 'km', InvalidValueError),
                         ])
def test_convert_negative(value: float, from_unit: str,
                          to_unit: str, error: type[Exception]) -> None:
    with pytest.raises(error):
        convert(value, from_unit, to_unit)