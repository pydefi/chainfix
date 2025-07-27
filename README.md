# Welcome to Chainfix
![chainfix](https://github.com/pydefi/chainfix/raw/main/docs/logo/chainfix_logo.png)

[![CI](https://github.com/pydefi/chainfix/actions/workflows/tox.yml/badge.svg)](https://github.com/pydefi/chainfix/actions/workflows/tox.yml)
[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)](https://github.com/pydefi/chainfix)
[![License](https://img.shields.io/github/license/pydefi/chainfix)](https://github.com/pydefi/chainfix/blob/main/LICENSE.txt)

Chainfix provides a way to represent numbers and perform simple math operations using fixed-point data types.

Chainfix supports binary fixed-point (base-2), decimal fixed-point (base-10)
or even arbitrary (base-N) fixed-point types.

Fixed-point data types are used in a wide range of computing applications. 
Binary-fixed point types are commonly used in the design of specialized hardware, 
FPGAs, ASICS, and signal processing applications.  

Decimal-fixed point types are commonly found in financial applications, blockchain, 
decentralized finance, and smart contracts
(e.g. the [solidity programming language](https://docs.soliditylang.org/)).


# Decimal fixed-point representations

The real-world value &pi; can be represented with limited precision using 
two bytes in **decimal** fixed point format

```python
>>> from chainfix import * 
>>> from math import pi
>>> pid = Fixd(pi, wordlength=16, precision=4)
Fixd(3.1416, 16, 4)
```

The `.int` property returns the stored integer value:   

```python
>>> pid.int
31416
```

The resolution of the decimal fixed-point data type is `10 ** -precision`, which 
is also the value of one least significant bit:

```python
>>> pid.lsb
0.0001
```

The range of numbers that can be represented with this precision using 16 bits is:

```python
>>> (pid.lower_bound, pid.upper_bound)
(-3.2768, 3.2767)
```

The real-world value can also be displayed as an exact ratio of integers

```python
>>> pid.as_integer_ratio()
(3927, 1250)
```

The `.hex` property returns the two's complement representation of the stored integer

```python
>>> pid.hex
'0x7ab8'
```

When `Fixd` stores a negative number, the MSB of the stored integer is always 1: 

```python
>>> Fixd(-pi, 16, 4).hex
'0x8548'
```




# Binary fixed-point representations

Likewise, &pi; can also be represented with limited precision using 
two bytes in **binary** fixed point format

```python
>>> pib = Fixb(pi, 16, 12)
Fixb(3.1416015625, 16, 12)
```

The `.int` property returns the stored integer value:   

```python
>>> pib.int
12868
```

The resolution of the decimal fixed-point data type is `2 ** -precision`, which 
is also the value of one least significant bit:

```python
>>> pib.lsb
0.000244140625
```

The range of numbers that can be represented with this precision using 16 bits is:

```python
>>> (pib.lower_bound, pib.upper_bound)
(-8.0, 7.999755859375)
```

The `.hex` property returns the two's complement representation of the stored integer

```python
>>> pib.hex
'0x3244'
```

When `Fixb` is used to store a negative number, the MSB of the stored integer is always 1: 

```python
>>> Fixb(-pi, 16, 4).hex
'0xffce'
```

# Contexts

Chainfix provides a fixed-point `context` to control the default behavior for new fixed-point objects.

The current context can be retrieved using

```python
>>> ctx = get_decimal_context()
>>> ctx.wordlength
256
>>> ctx.precision
18
```

for `Fixd` and `Ufixd` values or

```python
>>> ctx = get_binary_context()
>>> ctx.wordlength
32
>>> ctx.precision
16
```

for `Fixb` and `Ufixb` values.

The context can be modified to change the behavior of newly constructed values:

```python
>>> get_decimal_context().wordlength = 20
>>> get_decimal_context().precision = 5
>>> Fixd(pi)
Fixd(3.14159, 20, 5)
```

When passed through the constructor, the values for `wordlength` and `precision` always take precedence over the
context.

```python
>>> Fixd(pi, precision=10)
Fixd(3.1415926536, 256, 10)
```

Note that resulting data type has insufficinet range to represent the value pi.

# Future Work

* Support math operations for fixed-point types using the applicable context

# Contributing

## Package Installation
```bash
# Create virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate

# Install in development mode
pip install -e .

# Install with testing dependencies
pip install -e .[dev]  # if dev dependencies are defined
```

## Testing
```bash
# Run all tests
pytest

# Run tests with tox (multiple Python versions)
tox
```






