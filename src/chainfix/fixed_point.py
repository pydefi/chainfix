# Copyright (c) 2021 PyDefi Development Team.
# Distributed under the terms of the Modified BSD License.

import math
from fractions import Fraction
from typing import Any, TYPE_CHECKING, TypeVar, Union

default_wordlength = None
default_precision = None

T = TypeVar("T")

FromTypes = Union[int, float]


class _FixedPoint:
    """Fixed-Point Class

    The _Fix class represents fractional numbers using a stored integer
    representation, with a fixed degree of precision.
    Integers are stored using two's complement representation.
    The range of representable numbers is determined by the number of bytes
    of underlying storage.
    The scale factor used to convert between real world values and stored
    integers is `base ** precision`
    """

    __slots__ = ("_int", "_wordlength", "_precision")

    # Class attributes must be overridden by subclasses
    _base = None
    _signed = None

    if TYPE_CHECKING:
        _int: int
        _signed: bool
        _wordlength: int
        _precision: int

    def __new__(
            cls,
            value: FromTypes,
            wordlength: int = default_wordlength,
            precision: int = default_precision
    ) -> Any:
        self = object.__new__(cls)

        ctx = self.get_current_context()

        self._wordlength = wordlength if wordlength is not None else ctx.wordlength
        self._precision = precision if precision is not None else ctx.precision

        if not isinstance(value, (int, float)):
            raise TypeError("Value {} must be int or float".format(value))

        # Store integer with default saturate-on-overflow logic
        stored_integer = int(round(value * self._base ** self._precision))
        if stored_integer > self.max_int:
            raise ValueError('Value too large for data type.  Must be in range: {} to {}'.format(self.lower_bound, self.upper_bound))
        elif stored_integer < self.min_int:
            raise ValueError('Value too small for data type.  Must be in range: {} to {}'.format(self.lower_bound, self.upper_bound))
        else:
            self._int = stored_integer

        return self

    #: Real-world value
    value = property(
        lambda self: float(self._int / self._base ** self._precision)
    )

    def get_current_context(self):
        raise NotImplementedError

    # -----------------------------------------------------------------------
    # Data type inspection
    # -----------------------------------------------------------------------

    # Data type fixed base
    base = property(lambda self: self._base)

    # Data type fixed exponent
    wordlength = property(lambda self: self._wordlength)

    # Data type fixed exponent
    precision = property(lambda self: self._precision)

    # True if data type is signed
    signed = property(lambda self: self._signed)

    upper_bound = property(
        lambda self: self.max_int / self._base ** self._precision
    )

    lower_bound = property(
        lambda self: self.min_int / self._base ** self._precision
    )

    @property
    def max_int(self) -> int:
        """Maximum possible stored integer for data type. """
        if self._signed:
            return int(2 ** (self._wordlength - 1) - 1)
        else:
            return int(2 ** self._wordlength - 1)

    @property
    def min_int(self) -> int:
        """Minimum possible stored integer for data type. """
        if self._signed:
            return int(-(2 ** (self._wordlength - 1)))
        else:
            return int(0)

    #: Data type resolution (i.e. value of one LSB)
    lsb = property(lambda self: self._base ** -self._precision)

    def as_integer_ratio(self):
        """Return the exact real world value as a ratio of integers. """

        f = Fraction(self._int, self._base ** self._precision)
        return f.as_integer_ratio()

    # -----------------------------------------------------------------------
    # Stored Integer Properties
    # -----------------------------------------------------------------------

    #: Stored integer value
    int = property(lambda self: self._int)

    @property
    def hex(self) -> str:
        """Two's complement representation of stored integer (Hex value) """
        digits = math.ceil(self._wordlength / 4)
        if self._int >= 0:
            return "0x{num:0{digits}x}".format(num=self._int, digits=digits)
        else:
            return "0x{num:0{digits}x}".format(
                num=(2 ** self._wordlength + self._int), digits=digits
            )

    @property
    def bin(self) -> str:
        """Two's complement representation of stored integer
         (binary value) """
        digits = self._wordlength
        if self._int >= 0:
            return "0b{num:0{digits}b}".format(num=self._int, digits=digits)
        else:
            return "0b{num:0{digits}b}".format(
                num=(2 ** self._wordlength + self._int), digits=digits
            )

    # -----------------------------------------------------------------------
    # Representations and conversions
    # -----------------------------------------------------------------------

    def __repr__(self) -> str:
        return '{}({}, {}, {})'.format(self.__class__.__name__, self.value,
                                       self._wordlength, self._precision)

    def __str__(self) -> str:
        return str(self.value)

    def __bool__(self) -> bool:
        return self._int != 0

    def __float__(self) -> float:
        return float(self.value)

    def __int__(self) -> int:
        return int(self.value)


class _Fix(_FixedPoint):
    """A Signed fixed point number."""

    _signed = True

    def __new__(cls,
                value: FromTypes,
                wordlength: int = default_wordlength,
                precision: int = default_precision
                ) -> Any:
        self = super().__new__(cls,
                               value=value,
                               wordlength=wordlength,
                               precision=precision
                               )
        return self


class _Ufix(_FixedPoint):
    """An Unsigned fixed point number."""

    _signed = False

    def __new__(cls,
                value: FromTypes,
                wordlength: int = default_wordlength,
                precision: int = default_precision
                ) -> Any:
        self = super().__new__(cls,
                               value=value,
                               wordlength=wordlength,
                               precision=precision
                               )
        return self
