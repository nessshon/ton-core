from __future__ import annotations

from ton_core.boc import begin_cell
from ton_core.boc.cell import Cell
from ton_core.boc.slice import Slice
from ton_core.tlb.tlb import TlbScheme

__all__ = [
    "VanityDeployBody",
]


class VanityDeployBody(TlbScheme):
    """Message body for deploying contracts via Vanity."""

    def __init__(self, code: Cell, data: Cell) -> None:
        """Initialize VanityDeployBody.

        :param code: Contract code cell.
        :param data: Contract initial data cell.
        """
        self.code = code
        self.data = data

    def serialize(self) -> Cell:
        """Serialize to Cell."""
        cell = begin_cell()
        cell.store_ref(self.code)
        cell.store_ref(self.data)
        return cell.end_cell()

    @classmethod
    def deserialize(cls, cs: Slice) -> VanityDeployBody:
        """Deserialize from Slice."""
        return cls(code=cs.load_ref(), data=cs.load_ref())
