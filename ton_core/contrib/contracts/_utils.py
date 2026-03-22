from __future__ import annotations

from ton_core.boc.address import Address
from ton_core.boc.slice import Slice


def _load_std_address(cs: Slice) -> Address | None:
    """Load standard address from slice, ignoring external addresses.

    :param cs: Source slice.
    :return: Standard address, or ``None`` if addr_none or external.
    """
    addr = cs.load_address()
    return addr if isinstance(addr, Address) else None
