import pytest

from chainfix import Fixb
from chainfix import Fixb32
from chainfix import Fixd
from chainfix import Fixd32
from chainfix import Ufixb
from chainfix import Ufixb32
from chainfix import Ufixd
from chainfix import Ufixd32


def test_fix():
    s = Fixd(0)
    print(s)
    assert s.max_int == 2 ** 31 - 1
    assert s.min_int == -(2 ** 31)

    u = Ufixd(0)
    print(u)
    assert u.max_int == 2 ** 32 - 1
    assert u.min_int == 0

    assert isinstance(s, Fixd)

    with pytest.raises(TypeError):
        Ufixd("5")

    f = Ufixd(5.12345, precision=2)

    assert f.value == 5.12
    assert f.int == 512

    print(f.value)


def test_fix_bounds():
    u10 = Ufixd(0, wordlength=16, precision=3)
    s10 = Fixd(0, wordlength=16, precision=3)

    u2 = Ufixb(0, wordlength=16, precision=3)
    s2 = Fixb(0, wordlength=16, precision=3)

    assert s10.max_int == 2 ** 15 - 1
    assert s10.min_int == -(2 ** 15)

    print("Unsigned base 10")
    assert u10.max_int == 65535
    assert u10.lower_bound == 0
    assert u10.upper_bound == 65.535

    print("Signed base 10")
    assert s10.max_int == 32767
    assert s10.lower_bound == -32.768
    assert s10.upper_bound == 32.767

    print("Unsigned base 2")
    assert u2.min_int == 0
    assert u2.max_int == 65535
    assert u2.lower_bound == 0
    assert u2.upper_bound == 8191.875

    print("Signed base 2")
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
