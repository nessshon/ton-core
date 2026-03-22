from collections.abc import Callable
from typing import Any

from bitarray import bitarray

from ...boc.slice import Slice

def read_arbitrary_uint(n: int, ser: bitarray) -> tuple[int, bitarray]: ...
def deserialize_unary(ser: Slice) -> int: ...
def deserialize_hml(ser: Slice, m: int) -> tuple[int, bitarray]: ...
def deserialize_hashmap_node(cs: Slice, m: int, ret_dict: dict[str, Any], prefix: bitarray) -> None: ...
def deserialize_hashmap_aug_node(
    cs: Slice,
    m: int,
    ret_dict: dict[str, Any],
    extras: list[Any],
    prefix: bitarray,
    x_deserializer: Callable[..., Any],
    y_deserializer: Callable[..., Any],
) -> None: ...
def parse(slice: Slice, key_length: int, ret_dict: dict[str, Any], prefix: bitarray) -> None: ...
def parse_aug(
    slice: Slice,
    key_length: int,
    ret_dict: dict[str, Any],
    extras: list[Any],
    prefix: bitarray,
    x_deserializer: Callable[..., Any],
    y_deserializer: Callable[..., Any],
) -> None: ...
def parse_hashmap(dict_cell: Slice, key_len: int) -> dict[str, Any] | None: ...
def parse_hashmap_aug(
    dict_cell: Slice,
    key_len: int,
    x_deserializer: Callable[..., Any],
    y_deserializer: Callable[..., Any],
) -> tuple[dict[int, Any], list[Any]] | None: ...
