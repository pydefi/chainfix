import math
from typing import Any
from typing import TYPE_CHECKING
from typing import TypeVar
from typing import Union

__version__ = '0.0.1'

__all__ = ['Sfixd', 'Ufixd', 'Sfixb', 'Ufixb']

default_wordlength = 32
default_precision = 6

T = TypeVar("T")

FromTypes = Union[int, float]


class _Fix:
    """Fixed-Point Class

    The Fix class represents fractional numbers using a stored integer
    representation, with a fixed degree of precision.
    Integers are stored using two's complement representation.
    The range of representable numbers is determined by the number of bytes
    of underlying storage.
    The scale factor used to convert between real world values and stored
    integers is `base ** precision`
    """

    __slots__ = ("_int", "_base", "_signed", "_wordlength", "_precision")

    if TYPE_CHECKING:
        _int: int
        _base: int
        _signed: bool
        _wordlength: int
        _precision: int

    def __new__(

            cls,
            value: FromTypes,
            base: int,
            signed: bool,
            wordlength: int = default_wordlength,
            precision: int = default_precision
    ) -> Any:
        self = object.__new__(cls)
        self._base = base
        self._signed = signed
        self._wordlength = wordlength
        self._precision = precision

        if not isinstance(value, (int, float)):
            raise TypeError("Value {} must be int or float".format(value))

        stored_integer = int(round(value * self._base ** precision))
        self._int = stored_integer

        return self

    value = property(
        lambda self: self._int / self._base ** self._precision
    )

    precision = property(lambda self: self._precision)

    upper_bound = property(
        lambda self: self.max_int / self._base ** self._precision
    )

    lower_bound = property(
        lambda self: self.min_int / self._base ** self._precision
    )

    @property
    def max_int(self) -> int:
        if self._signed:
            return int(2 ** (self._wordlength - 1) - 1)
        else:
            return int(2 ** self._wordlength - 1)

    @property
    def min_int(self) -> int:
        if self._signed:
            return int(-(2 ** (self._wordlength - 1)))
        else:
            return int(0)

    int = property(lambda self: self._int)

    def __bool__(self) -> bool:
        return self._int != 0

    @property
    def hex(self) -> str:
        digits = math.ceil(self._wordlength / 4)
        if self._int >= 0:
            return "{num:0{digits}x}".format(num=self._int, digits=digits)
        else:
            return "{num:0{digits}x}".format(
                num=(2 ** self._wordlength + self._int), digits=digits
            )


class Sfix(_Fix):
    """A Signed fixed point number."""

    def __new__(cls,
                value: FromTypes,
                base: int,
                wordlength: int = default_wordlength,
                precision: int = default_precision
                ) -> Any:
        self = super().__new__(cls,
                               value=value,
                               base=base,
                               signed=True,
                               wordlength=wordlength,
                               precision=precision
                               )
        return self


class Ufix(_Fix):
    """An Unsigned fixed point number."""

    def __new__(cls,
                value: FromTypes,
                base: int,
                precision: int = default_precision,
                wordlength: int = default_wordlength
                ) -> Any:
        self = super().__new__(cls,
                               value=value,
                               base=base,
                               signed=False,
                               wordlength=wordlength,
                               precision=precision
                               )
        return self


class Sfixb(Sfix):
    """A Signed fixed point number (binary scaled)."""

    def __new__(cls,
                value: FromTypes = 0,
                precision: int = default_precision,
                wordlength: int = default_wordlength
                ) -> Any:
        self = super().__new__(cls,
                               base=2,
                               value=value,
                               precision=precision,
                               wordlength=wordlength
                               )
        return self


class Ufixb(Ufix):
    """An Unsigned fixed point number (binary scaled)."""

    def __new__(cls,
                value: FromTypes = 0,
                wordlength: int = default_wordlength,
                precision: int = default_precision
                ) -> Any:
        self = super().__new__(cls,
                               value=value,
                               base=2,
                               wordlength=wordlength,
                               precision=precision
                               )
        return self


class Sfixd(Sfix):
    """A Signed fixed point number (decimal scaled)."""

    def __new__(cls,
                value: FromTypes = 0,
                precision: int = default_precision,
                wordlength: int = default_wordlength
                ) -> Any:
        self = super().__new__(cls,
                               value=value,
                               base=10,
                               wordlength=wordlength,
                               precision=precision
                               )
        return self


class Ufixd(Ufix):
    """An Unsigned fixed point number (decimal scaled)."""

    def __new__(cls,
                value: FromTypes = 0,
                wordlength: int = default_wordlength,
                precision: int = default_precision
                ) -> Any:
        self = super().__new__(cls,
                               value=value,
                               base=10,
                               wordlength=wordlength,
                               precision=precision
                               )
        return self
