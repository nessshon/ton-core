from collections.abc import Callable
from typing import Any, TypeVar

from ...boc.address import Address
from ...boc.cell import Cell
from ...boc.slice import Slice

Key = int | str | bytes | Address

_H = TypeVar("_H", bound="HashMap")


class DictError(Exception): ...


class HashMap:
    size: int
    map: dict[int, Any]
    key_serializer: Callable[..., Any] | None
    value_serializer: Callable[..., Any] | None

    def __init__(
        self,
        key_size: int,
        key_serializer: Callable[..., Any] | None = ...,
        value_serializer: Callable[..., Any] | None = ...,
        map_: dict[int, Any] | None = ...,
    ) -> None: ...
    def set_int_key(self: _H, int_key: int, value: Any) -> _H: ...
    def set(self: _H, key: Key, value: Any, hash_key: bool = ...) -> _H: ...
    def with_address_values(self: _H) -> _H: ...
    def with_uint_values(self: _H, length: int) -> _H: ...
    def with_int_values(self: _H, length: int) -> _H: ...
    def with_coins_values(self: _H) -> _H: ...
    def serialize(self) -> Cell | None: ...
    @classmethod
    def from_cell(cls, dict_cell: Cell, key_length: int) -> HashMap: ...
    @staticmethod
    def parse(
        dict_cell: Slice,
        key_length: int,
        key_deserializer: Callable[..., Any] | None = ...,
        value_deserializer: Callable[..., Any] | None = ...,
    ) -> dict[Any, Any] | None: ...
