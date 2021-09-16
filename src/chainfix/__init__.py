from typing import Any, TYPE_CHECKING, TypeVar, Union

__version__ = '0.0.1'

__all__ = ['Sfixd', 'Ufixd', 'Sfixb', 'Ufixb']

default_width = 4
default_precision = 6

T = TypeVar("T")


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

    __slots__ = ("_base", "_int", "_precision", "_signed", "_width")

    if TYPE_CHECKING:
        _base: int
        _int: int
        _precision: int
        _signed: bool
        _width: int

    def __new__(

            cls,
            base: int,
            value: Union[int, float],
            signed: bool,
            precision: int = default_precision,
            width: int = default_width,
    ) -> Any:
        self = object.__new__(cls)
        self._base = base
        self._signed = signed
        self._precision = precision
        self._width = width

        if not isinstance(value, (int, float)):
            raise TypeError("Value {} must be int or float".format(value))

        stored_integer = int(round(value * self._base ** precision))
        self._int = stored_integer

        return self

    value = property(
        lambda self: self._int / self._base ** self._precision
    )

    precision = property(lambda self: self._precision)

    num_bits = property(lambda self: 8 * self._width)

    upper_bound = property(
        lambda self: self.max_int / self._base ** self._precision
    )

    lower_bound = property(
        lambda self: self.min_int / self._base ** self._precision
    )

    @property
    def max_int(self) -> int:
        if self._signed:
            return int(2 ** (self.num_bits - 1) - 1)
        else:
            return int(2 ** self.num_bits - 1)

    @property
    def min_int(self) -> int:
        if self._signed:
            return int(-(2 ** (self.num_bits - 1)))
        else:
            return int(0)

    int = property(lambda self: self._int)

    def __bool__(self) -> bool:
        return self._int != 0

    @property
    def hex(self) -> str:
        digits = self._width * 2
        if self._int >= 0:
            return "{num:0{digits}x}".format(num=self._int, digits=digits)
        else:
            return "{num:0{digits}x}".format(
                num=(2 ** self.num_bits + self._int), digits=digits
            )


class Sfix(_Fix):
    """A Signed fixed point number."""

    def __new__(cls,
                base: int,
                value: Union[int, float] = 0,
                precision: int = default_precision,
                width: int = default_width
                ) -> Any:
        self = super().__new__(cls,
                               base=base,
                               value=value,
                               signed=True,
                               precision=precision,
                               width=width,
                               )
        return self


class Ufix(_Fix):
    """An Unsigned fixed point number."""

    def __new__(cls,
                base: int,
                value: Union[int, float] = 0,
                precision: int = default_precision,
                width: int = default_width
                ) -> Any:
        self = super().__new__(cls,
                               base=base,
                               value=value,
                               signed=False,
                               precision=precision,
                               width=width,
                               )
        return self


class Sfixb(Sfix):
    """A Signed fixed point number (binary scaled)."""

    def __new__(cls,
                value: Union[int, float] = 0,
                precision: int = default_precision,
                width: int = default_width
                ) -> Any:
        self = super().__new__(cls,
                               base=2,
                               value=value,
                               precision=precision,
                               width=width
                               )
        return self


class Ufixb(Ufix):
    """An Unsigned fixed point number (binary scaled)."""

    def __new__(cls,
                value: Union[int, float] = 0,
                precision: int = default_precision,
                width: int = default_width
                ) -> Any:
        self = super().__new__(cls,
                               base=2,
                               value=value,
                               precision=precision,
                               width=width
                               )
        return self


class Sfixd(Sfix):
    """A Signed fixed point number (decimal scaled)."""

    def __new__(cls,
                value: Union[int, float] = 0,
                precision: int = default_precision,
                width: int = default_width
                ) -> Any:
        self = super().__new__(cls,
                               base=10,
                               value=value,
                               precision=precision,
                               width=width
                               )
        return self


class Ufixd(Ufix):
    """An Unsigned fixed point number (decimal scaled)."""

    def __new__(cls,
                value: Union[int, float] = 0,
                precision: int = default_precision,
                width: int = default_width
                ) -> Any:
        self = super().__new__(cls,
                               base=10,
                               value=value,
                               precision=precision,
                               width=width
                               )
        return self
