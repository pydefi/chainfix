# Copyright (c) 2021 PyDefi Development Team.
# Distributed under the terms of the Modified BSD License.

from typing import Any

from chainfix.context import get_decimal_context
from chainfix.fixed_point import _Fix
from chainfix.fixed_point import _Ufix
from chainfix.fixed_point import default_precision
from chainfix.fixed_point import default_wordlength
from chainfix.fixed_point import FromTypes


# --------------------------------------------------------------------------
# Decimal Fixed Point Types
# --------------------------------------------------------------------------

class Fixd(_Fix):
    """A Signed fixed point number (decimal scaled)."""
    _base = 10

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
        return get_decimal_context()


class Ufixd(_Ufix):
    """An Unsigned fixed point number (decimal scaled)."""
    _base = 10

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
        return get_decimal_context()
