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

import pytest

from chainfix import Fixb
from chainfix import Fixb32
from chainfix import Fixd
from chainfix import Fixd32
from chainfix import get_decimal_context, set_decimal_context
from chainfix import Ufixb
from chainfix import Ufixb32
from chainfix import Ufixd
from chainfix import Ufixd32


def test_decimal_context_defaults():
    s = Fixd(0)

    assert s.precision == 18
    assert s.wordlength == 256


def test_binary_context_defaults():
    s = Fixb(0)
    assert s.wordlength == 32
    assert s.precision == 16


def test_binary_context_overrides():
    s = Fixb(0)
    assert s.wordlength == 32
    assert s.precision == 16

    s = Fixb(0, 19, 13)
    assert s.wordlength == 19
    assert s.precision == 13

    s = Fixb(0, 19)
    assert s.wordlength == 19
    assert s.precision == 16

    s = Fixb(0, precision=2)
    assert s.wordlength == 32
    assert s.precision == 2


def test_decimal_context_overrides():
    s = Fixd(0)
    assert s.wordlength == 256
    assert s.precision == 18

    s = Fixd(0, 19, 13)
    assert s.wordlength == 19
    assert s.precision == 13

    s = Fixd(0, 19)
    assert s.wordlength == 19
    assert s.precision == 18

    s = Fixd(0, precision=2)
    assert s.wordlength == 256
    assert s.precision == 2


def test_ranges():
    s = Fixd(0, 32)
    assert s.max_int == 2 ** 31 - 1
    assert s.min_int == -(2 ** 31)

    u = Ufixd(0, 32)
    assert u.max_int == 2 ** 32 - 1
    assert u.min_int == 0


def test_get_context1():
    ctx = get_decimal_context()
    ctx_save = ctx.copy()

    ctx.wordlength = 18
    ctx.precision = 8

    x = Fixd(0)
    assert x.wordlength == 18
    assert x.precision == 8

    set_decimal_context(ctx_save)


def test_get_context2():
    ctx = get_decimal_context()
    ctx_save = ctx.copy()

    ctx.wordlength = 33
    ctx.precision = 7

    x = Fixd(0)
    assert x.wordlength == 33
    assert x.precision == 7

    set_decimal_context(ctx_save)


def test_fix():
    s = Fixd(0)

    with pytest.raises(TypeError):
        Ufixd("5")

    f = Ufixd(5.12345, precision=2)

    assert f.value == 5.12
    assert f.int == 512


def test_fix_bounds():
    u10 = Ufixd(0, wordlength=16, precision=3)
    s10 = Fixd(0, wordlength=16, precision=3)

    u2 = Ufixb(0, wordlength=16, precision=3)
    s2 = Fixb(0, wordlength=16, precision=3)

    assert s10.max_int == 2 ** 15 - 1
    assert s10.min_int == -(2 ** 15)

    # Unsigned base 10
    assert u10.max_int == 65535
    assert u10.lower_bound == 0
    assert u10.upper_bound == 65.535

    # Signed base 10
    assert s10.max_int == 32767
    assert s10.lower_bound == -32.768
    assert s10.upper_bound == 32.767

    # Unsigned base 2
    assert u2.min_int == 0
    assert u2.max_int == 65535
    assert u2.lower_bound == 0
    assert u2.upper_bound == 8191.875

    # Signed base 2
    assert s2.min_int == -32768
    assert s2.max_int == 32767
    assert s2.lower_bound == -4096
    assert s2.upper_bound == 4095.875

    assert u10.max_int == 2 ** 16 - 1
    assert u10.min_int == 0


def test_bool():
    u = Fixd(-1)
    assert u
    u = Ufixd(0)
    assert not u


def test_undefined_ops():
    with pytest.raises(TypeError):
        Ufixd(3.1) + Ufixd(3.3)


def test_stored_hex_bin():
    assert Ufixd(33, 16, 0).hex == '0x0021'
    assert Ufixd(33, 16, 0).bin == '0b0000000000100001'

    assert Fixd(-2, 16, 0).hex == '0xfffe'
    assert Fixd(-2, 16, 0).bin == '0b1111111111111110'


def test_32_bit_types():
    assert Ufixd32(0, 2).lower_bound == 0.00
    assert Ufixd32(0, 2).upper_bound == 42949672.95

    assert Fixd32(0, 2).lower_bound == -21474836.48
    assert Fixd32(0, 2).upper_bound == 21474836.47

    assert Ufixb32(0, 2).lower_bound == 0.00
    assert Ufixb32(0, 2).upper_bound == 1073741823.75

    assert Fixb32(0, 2).lower_bound == -536870912.0
    assert Fixb32(0, 2).upper_bound == 536870911.75


def test_integer_ratio():
    x = Fixb(17 / 8, 32, 6)
    n, d = x.as_integer_ratio()
    assert n == 17
    assert d == 8

    x = Fixd(17 / 8, 32, 6)
    n, d = x.as_integer_ratio()
    assert n == 17
    assert d == 8
