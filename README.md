# Welcome to Chainfix
![chainfix](https://github.com/pydefi/chainfix/raw/main/docs/logo/chainfix_logo.png)

![ci](https://github.com/pydefi/chainfix/actions/workflows/tox.yml/badge.svg)

Chainfix provides a way to represent numbers and perform simple math operations using fixed-point data types.

Chainfix supports binary fixed-point (base-2), decimal fixed-point (base-10)
or even arbitrary (base-N) fixed-point types.

Fixed-point data types are used in a wide range of computing applications. 
Binary-fixed point types are commonly used in the design of specialized hardware, 
FPGAs, ASICS, and signal processing applications.  

Decimal-fixed point types are commonly found in financial applications, blockchain, 
decentralized finance, and smart contracts
(e.g. the [solidity programming language](https://docs.soliditylang.org/)).


# Examples

## Decimal fixed-point representations

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

## Binary fixed-point representations

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


# Contributing

Chainfix can be installed in developer mode after cloning the repository:

```shell
$ pip install -e .
```

To run all tests:

```shell
$ pytest
```






