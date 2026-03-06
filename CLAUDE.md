# CLAUDE.md

## Project Overview

Chainfix is a Python library providing fixed-point data types for representing numbers with a fixed degree of precision. It supports binary (base-2), decimal (base-10), and arbitrary base-N fixed-point representations.

**Primary role**: Scalar specification and verification layer for fixed-point formats — defining, inspecting, and verifying individual fixed-point values with bit-exact precision. Not a bulk compute or tensor library.

**Use cases**:
- **Blockchain / DeFi**: Decimal fixed-point (256-bit, 18 decimals) matching Solidity conventions
- **Hardware / FPGA / ASIC / Signal Processing**: Binary fixed-point (8–64 bit) for design verification
- **Financial**: Decimal fixed-point with exact representation (no floating-point error)

**Version**: 0.1.2 (Alpha)
**License**: Apache License 2.0
**Python**: >=3.8 (tested on 3.8–3.13)
**No external runtime dependencies** — standard library only (`math`, `fractions`, `enum`, `contextvars`, `typing`).

## Repository Structure

```
src/chainfix/              # Main package (src layout)
├── __init__.py            # Public API, version, __all__
├── fixed_point.py         # Base classes: _FixedPoint, _Fix, _Ufix
├── decimal.py             # Decimal fixed-point: Fixd, Ufixd
├── binary.py              # Binary fixed-point: Fixb, Ufixb
├── context.py             # Context management (DecimalContext, BinaryContext)
└── helpers.py             # 32-bit convenience types (Fixd32, Ufixb32, etc.)
tests/
└── test_fix.py            # Test suite (pytest)
.github/workflows/
├── tox.yml                # CI: matrix testing across Python versions
└── publish-to-test-pypi.yml  # Publish on release
```

## Development Commands

```bash
# Setup
python3 -m venv venv && source venv/bin/activate
pip install -e .                # Install in dev mode
pip install pytest pytest-cov   # Install test dependencies

# Run tests
pytest                                          # Basic run
pytest --cov=chainfix --cov-report=term-missing # With coverage

# Multi-version testing
pip install tox tox-gh-actions
tox
```

## Architecture & Key Conventions

### Class Hierarchy

`_FixedPoint` (base) → `_Fix` (signed) / `_Ufix` (unsigned) → concrete types:
- **Decimal**: `Fixd`, `Ufixd` (base-10)
- **Binary**: `Fixb`, `Ufixb` (base-2)
- **32-bit helpers**: `Fixd32`, `Ufixd32`, `Fixb32`, `Ufixb32`

### Naming Conventions

- Private base classes are prefixed with `_` (e.g., `_FixedPoint`, `_Fix`)
- Public types use short names: `Fix` + type indicator (`d`=decimal, `b`=binary), `U` prefix for unsigned
- Context functions: `get_<type>_context()` / `set_<type>_context()`

### Patterns

- **`__new__`** for object construction (immutable value types)
- **`__slots__`** for memory efficiency: `("_int", "_wordlength", "_precision")`
- **Read-only properties** for computed values (`value`, `hex`, `bin`, `upper_bound`, `lower_bound`, `lsb`)
- **`contextvars.ContextVar`** for thread-safe global defaults
- **Overflow handling**: raises `ValueError` for out-of-range values (saturate behavior)
- **Two's complement** for signed negative number representation

### Code Style

- Standard PEP 8 conventions
- Type hints from `typing` module (`Union`, `TypeVar`, `Optional`)
- Apache License 2.0 header on all source files
- One import per line, sorted by module
- Comprehensive docstrings on public classes and methods

### Public API

All public exports are listed in `src/chainfix/__init__.py` via `__all__`. When adding new public types or functions, update both the imports and `__all__` in that file.

## Testing

- Tests live in `tests/test_fix.py`
- Use `pytest` — no other test framework
- Coverage target: ~93% (branch coverage enabled)
- Coverage config is in `pyproject.toml` under `[tool.coverage.*]`
- CI runs `pytest --cov=chainfix --cov-report=xml --cov-report=term-missing`

## CI/CD

- **Testing**: GitHub Actions matrix across Python 3.8–3.13 on ubuntu-latest (`.github/workflows/tox.yml`)
- **Coverage**: Uploaded to Codecov on Python 3.12 runs only
- **Publishing**: Triggered on GitHub release → builds sdist + wheel → publishes to PyPI (`.github/workflows/publish-to-test-pypi.yml`)
- **Build system**: setuptools with `pyproject.toml` (PEP 517/518)

## Known Issues

### Precision loss from float dependency (Bugs #2 and #3)

The `value` property (`fixed_point.py:80`) and stored integer computation (`fixed_point.py:68`) use Python `float` (64-bit IEEE 754), which silently loses precision for the 256-bit blockchain use case. The `as_integer_ratio()` method correctly uses `Fraction` but the rest of the pipeline does not.

**Planned fix**: Accept `str`, `Decimal`, and `Fraction` as input types alongside `int`/`float`. Use `Fraction` internally for stored integer computation when inputs are exact types or word length exceeds 64 bits. Keep the `float` fast path for small word lengths (DSP/hardware use case).

### Missing arithmetic operators

No `__add__`, `__sub__`, `__mul__`, `__eq__`, or `__hash__` are implemented. The README mentions "simple math operations" but `Ufixd(3.1) + Ufixd(3.3)` raises `TypeError`.

### Missing overflow modes

The `Overflow.WRAP` enum exists in `context.py` but only `SATURATE` (raise `ValueError`) is implemented.

## Design Direction

Chainfix is a **scalar specification and verification library**, not a tensor/compute framework. For bulk DSP/GPU workloads, the intended approach is bridging to existing tensor frameworks (PyTorch quantization, NumPy) rather than reimplementing array operations.

The priority roadmap:
1. Fix scalar precision (accept `Fraction`/`Decimal`/`str`, exact internal arithmetic)
2. Add basic arithmetic operators with well-defined result type rules
3. Add `__eq__` and `__hash__` (these are immutable value types)
4. Add format descriptor / bridge methods for interop with PyTorch, NumPy
