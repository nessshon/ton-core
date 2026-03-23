# 📦 TON Core

[![TON](https://img.shields.io/badge/TON-grey?logo=TON&logoColor=40AEF0)](https://ton.org)
![Python Versions](https://img.shields.io/badge/Python-3.10%20--%203.14-black?color=FFE873&labelColor=3776AB)
[![PyPI](https://img.shields.io/pypi/v/ton-core.svg)](https://pypi.python.org/pypi/ton-core)
[![License](https://img.shields.io/github/license/nessshon/ton-core)](https://github.com/nessshon/ton-core/blob/main/LICENSE)
[![Donate](https://img.shields.io/badge/Donate-TON-blue)](https://tonviewer.com/UQCZq3_Vd21-4y4m7Wc-ej9NFOhh_qvdfAkAYAOHoQ__Ness)

![Image](https://raw.githubusercontent.com/nessshon/ton-core/main/assets/banner.png)

![Downloads](https://pepy.tech/badge/ton-core)
![Downloads](https://pepy.tech/badge/ton-core/month)
![Downloads](https://pepy.tech/badge/ton-core/week)

### Python core for [TON Blockchain](https://ton.org)

Primitives, data types, TLB schemas, contract tools, and crypto utilities for TON.

> Based on [pytoniq-core](https://github.com/yungwine/pytoniq-core) by [Maksim Kurbatov](https://github.com/yungwine)

**Features**

- **Primitives** — core data types for cells, addresses, slices, and hash maps
- **TLB Schemas** — transactions, blocks, accounts, and config parameters
- **Contracts** — wallets, jettons, NFTs, DNS, and Telegram
- **Crypto** — mnemonics, keys, signing, and encryption
- **Utilities** — conversion, encoding, and helpers

## Installation

```bash
pip install ton-core
```

## Usage

```python
from ton_core import Address, begin_cell, cell_to_b64, to_nano

# Parse a TON address
destination = Address("UQCZq3_Vd21-4y4m7Wc-ej9NFOhh_qvdfAkAYAOHoQ__Ness")

# Convert TON to nanotons
amount = to_nano("0.5")

# Build a message body
body = begin_cell()
body.store_uint(0, 32)
body.store_string("Hello from ton-core!")
cell = body.end_cell()

# Serialize to base64
payload = cell_to_b64(cell)
```

More examples available in [pytoniq-core/examples](https://github.com/yungwine/pytoniq-core/tree/master/examples).

## License

This repository is distributed under the [MIT License](https://github.com/nessshon/ton-core/blob/main/LICENSE).
