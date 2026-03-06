# CLAUDE.md

## Project Overview

Chainfix is a Python library providing fixed-point data types for representing numbers with a fixed degree of precision. It supports binary (base-2), decimal (base-10), and arbitrary base-N fixed-point representations. Used in signal processing, hardware design (FPGAs/ASICs), blockchain/DeFi, and financial applications.

**Version**: 0.1.2 (Alpha)
**License**: Apache License 2.0
**Python**: >=3.8 (tested on 3.8–3.13)
**No external runtime dependencies** — standard library only.

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
