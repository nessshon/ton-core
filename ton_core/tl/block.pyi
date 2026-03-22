from typing import Any

class BlockId:
    workchain: int
    shard: int
    seqno: int
    def __init__(self, workchain: int, shard: int | None, seqno: int) -> None: ...
    def to_dict(self) -> dict[str, int]: ...
    @classmethod
    def from_dict(cls, block_id: dict[str, Any]) -> BlockId: ...

class BlockIdExt:
    workchain: int
    shard: int
    seqno: int
    root_hash: bytes
    file_hash: bytes
    def __init__(
        self,
        workchain: int,
        shard: int | None,
        seqno: int,
        root_hash: str | bytes,
        file_hash: str | bytes,
    ) -> None: ...
    def to_dict(self) -> dict[str, int | str]: ...
    @classmethod
    def from_dict(cls, block_id_ext: dict[str, Any]) -> BlockIdExt: ...
    def to_bytes(self) -> bytes: ...
    @classmethod
    def from_bytes(cls, data: bytes) -> BlockIdExt: ...
    def __eq__(self, other: object) -> bool: ...
    def __hash__(self) -> bytes: ...  # type: ignore[override]
    def __repr__(self) -> str: ...
