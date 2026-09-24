class ToolkitError(Exception):
    """базовое искл для всех ошибок"""


class CalcError(ToolkitError):
    """ошибки кальулятора"""

###
class EmptyExpressionError(CalcError):
    pass
###

###
class InvalidTokenError(CalcError):
    pass
###

class InvalidExpressionError(CalcError):
    pass

###
class DivisionByZeroError(CalcError):
    pass
###

class ConvError(ToolkitError):
    """ошибки конвертора"""


class UnknownUnitError(ConvError):
    pass


class IncompatibleUnitsError(ConvError):
    pass


class BelowAbsoluteZeroError(ConvError):
    pass


class InvalidValueError(ToolkitError):
    pass