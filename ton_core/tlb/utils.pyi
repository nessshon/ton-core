from collections.abc import Callable
from typing import Any

from ton_core.boc.cell import Cell
from ton_core.boc.slice import Slice
from ton_core.tlb.tlb import TlbScheme

class HashUpdate(TlbScheme):
    old_hash: bytes
    new_hash: bytes
    def __init__(self, old_hash: bytes, new_hash: bytes) -> None: ...
    def serialize(self) -> Cell: ...
    @classmethod
    def deserialize(cls, cell_slice: Slice) -> HashUpdate: ...

class MerkleUpdate(TlbScheme):
    cell: Cell
    old_hash: bytes
    new_hash: bytes
    old: object
    new: object
    def __init__(self, cell: Cell, old_hash: bytes, new_hash: bytes, old: object, new: object) -> None: ...
    @classmethod
    def serialize(cls, *args: Any) -> None: ...
    @classmethod
    def deserialize(cls, cell: Cell, deserializer: Callable[..., Any]) -> MerkleUpdate | None: ...

def deserialize_shard_hashes(cell_slice: Slice) -> dict[Any, Any] | None: ...

def uint64_to_int64(num: int) -> int: ...
