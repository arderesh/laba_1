from toolkit.errors import BelowAbsoluteZeroError, InvalidValueError, UnknownUnitError, IncompatibleUnitsError

LENG = {
    "mm": 0.001,
    "cm": 0.01,
    "dm": 0.1,
    "m": 1.0,
    "km": 1000.0
}

MASSA = {
    "mg": 0.001,
    "g": 1.0,
    "kg": 1000.0
}

TEMP = ('c', 'f', 'k')

ABS_ZERO = {
    'c': -273.15,
    'f': -459.67,
    'k': 0
}


def group(unit):
    if unit in LENG:
        return "length"
    elif unit in MASSA:
        return "mass"
    elif unit in TEMP:
        return "temperature"
    raise UnknownUnitError('Неизвестная единица')


def to_c(unit, value):
    if unit == 'c':
        return value
    elif unit == 'f':
        return (value - 32) * 5 / 9
    elif unit == 'k':
        return value - 273.15


def from_c(unit, value):
    if unit == 'c':
        return value
    if unit == 'f':
        return value * 9 / 5 + 32
    elif unit == 'k':
        return value + 273.15


def convert(value, from_unit, to_unit):
    if not isinstance(value, (int, float)):
        raise InvalidValueError('Значение должно быть числом')

    from_unit = from_unit.lower()
    to_unit = to_unit.lower()

    group_from = group(from_unit)
    group_to = group(to_unit)

    if group_from != group_to:
        raise IncompatibleUnitsError('Группы должны быть одинаковыми')

    if group_from == 'temperature':
        if value < ABS_ZERO[from_unit]:
            raise BelowAbsoluteZeroError('Значение температуры ниже абсолютного нуля')
        cels = to_c(from_unit, value)
        return float(from_c(to_unit, cels))

    if group_from == 'length':
        gr = LENG
    else:
        gr = MASSA

    base_unit = value * gr[from_unit]

    return float(base_unit / gr[to_unit])