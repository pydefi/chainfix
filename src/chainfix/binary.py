from typing import Any

from chainfix.context import get_binary_context
from chainfix.fixed_point import _Fix
from chainfix.fixed_point import _Ufix
from chainfix.fixed_point import default_precision
from chainfix.fixed_point import default_wordlength
from chainfix.fixed_point import FromTypes

__all__ = ['Fixb', 'Ufixb']


# --------------------------------------------------------------------------
# Binary Fixed Point Types
# --------------------------------------------------------------------------

class Fixb(_Fix):
    """A Signed fixed point number (binary scaled)."""
    _base = 2

    def __new__(cls,
                value: FromTypes = 0,
                wordlength: int = default_wordlength,
                precision: int = default_precision
                ) -> Any:
        self = super().__new__(cls,
                               value=value,
                               wordlength=wordlength,
                               precision=precision
                               )
        return self

    def get_current_context(self):
        return get_binary_context()


class Ufixb(_Ufix):
    """An Unsigned fixed point number (binary scaled)."""
    _base = 2

    def __new__(cls,
                value: FromTypes = 0,
                wordlength: int = default_wordlength,
                precision: int = default_precision
                ) -> Any:
        self = super().__new__(cls,
                               value=value,
                               wordlength=wordlength,
                               precision=precision
                               )
        return self

    def get_current_context(self):
        return get_binary_context()
