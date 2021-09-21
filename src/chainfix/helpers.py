# Copyright (c) 2021 PyDefi Development Team.
# Distributed under the terms of the Modified BSD License.

from typing import Any

from chainfix.binary import Fixb
from chainfix.binary import Ufixb
from chainfix.decimal import Fixd
from chainfix.decimal import Ufixd
from chainfix.fixed_point import FromTypes


# --------------------------------------------------------------------------
# 32-bit Helper Types
# --------------------------------------------------------------------------
class Fixb32(Fixb):

    def __new__(cls,
                value: FromTypes = 0,
                precision: int = None
                ) -> Any:
        self = super().__new__(cls,
                               value=value,
                               wordlength=32,
                               precision=precision
                               )
        return self


class Ufixb32(Ufixb):

    def __new__(cls,
                value: FromTypes = 0,
                precision: int = None
                ) -> Any:
        self = super().__new__(cls,
                               value=value,
                               wordlength=32,
                               precision=precision
                               )
        return self


class Fixd32(Fixd):

    def __new__(cls,
                value: FromTypes = 0,
                precision: int = None
                ) -> Any:
        self = super().__new__(cls,
                               value=value,
                               wordlength=32,
                               precision=precision
                               )
        return self


class Ufixd32(Ufixd):

    def __new__(cls,
                value: FromTypes = 0,
                precision: int = None
                ) -> Any:
        self = super().__new__(cls,
                               value=value,
                               wordlength=32,
                               precision=precision
                               )
        return self
