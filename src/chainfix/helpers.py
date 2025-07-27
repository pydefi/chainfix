# Copyright 2021 PyDefi Development Team
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

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
