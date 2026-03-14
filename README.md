# 📦 ton-core

[![TON](https://img.shields.io/badge/TON-grey?logo=TON&logoColor=40AEF0)](https://ton.org)
![Python Versions](https://img.shields.io/badge/Python-3.10%20--%203.14-black?color=FFE873&labelColor=3776AB)
[![PyPI](https://img.shields.io/pypi/v/ton-core.svg?color=FFE873&labelColor=3776AB)](https://pypi.python.org/pypi/ton-core)
[![License](https://img.shields.io/pypi/l/ton-core)](https://github.com/nessshon/ton-core/blob/main/LICENSE)

**This is an alias package for [pytoniq-core](https://github.com/yungwine/pytoniq-core).**

The version of this package always matches the version of pytoniq-core.

## Installation

```bash
pip install ton-core
```

## Usage

```python
# Instead of:
from pytoniq_core import Address, Cell, Builder

# You can use:
from ton_core import Address, Cell, Builder
```

All classes, functions, and constants from `pytoniq-core` are available through `ton-core`.

## Original Package

**Author:** Maksim Kurbatov  
**Repo:** [pytoniq-core](https://github.com/yungwine/pytoniq-core)  
**PyPI:** [pytoniq-core](https://pypi.org/project/pytoniq-core/)  

## License

[MIT License](LICENSE) — same as the original package.