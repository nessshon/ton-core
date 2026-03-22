from __future__ import annotations

from ton_core.boc.address import Address
from ton_core.boc.builder import Builder
from ton_core.boc.cell import Cell
from ton_core.boc.slice import Slice
from ton_core.contrib.utils import cell_to_b64, cell_to_hex, normalize_hash
from ton_core.tlb.account import StateInit
from ton_core.tlb.block import CurrencyCollection
from ton_core.tlb.tlb import TlbScheme
from ton_core.tlb.transaction import (
    ExternalMsgInfo,
    InternalMsgInfo,
)
from ton_core.tlb.transaction import (
    MessageAny as MessageAnyBase,
)

__all__ = [
    "ExternalMessage",
    "InternalMessage",
    "MessageAny",
    "WalletMessage",
]


class WalletMessage(TlbScheme):
    """Wallet message wrapping send mode and a ``MessageAny`` cell reference."""

    send_mode: int
    """Send mode flags encoded as an 8-bit unsigned integer."""

    message: MessageAnyBase
    """The message payload wrapped as a ``MessageAny`` reference."""

    def __init__(self, send_mode: int, message: MessageAnyBase) -> None:
        """Initialize a wallet message.

        :param send_mode: Send mode flags encoded as an 8-bit unsigned integer.
        :param message: The message payload wrapped as a ``MessageAny`` reference.
        """
        self.send_mode = send_mode
        self.message = message

    def serialize(self) -> Cell:
        """Serialize to ``Cell``."""
        builder = Builder()
        builder.store_uint(self.send_mode, 8)
        builder.store_ref(self.message.serialize())
        return builder.end_cell()

    @classmethod
    def deserialize(cls, cell_slice: Slice) -> WalletMessage:
        """Deserialize from ``Slice``."""
        send_mode = cell_slice.load_uint(8)
        message = MessageAnyBase.deserialize(cell_slice.load_ref().begin_parse())
        return cls(send_mode=send_mode, message=message)


class MessageAny(MessageAnyBase):
    """Base class for TON messages with serialization helpers."""

    def to_cell(self) -> Cell:
        """Serialize to ``Cell``."""
        return self.serialize()

    def to_boc(self) -> bytes:
        """Serialize to BoC bytes."""
        return self.to_cell().to_boc()

    @property
    def as_hex(self) -> str:
        """Hex-encoded BoC string."""
        return cell_to_hex(self.to_cell())

    @property
    def as_b64(self) -> str:
        """Base64-encoded BoC string."""
        return cell_to_b64(self.to_cell())

    @property
    def normalized_hash(self) -> str:
        """Normalized message hash as hex string."""
        return normalize_hash(self)


class ExternalMessage(MessageAny):
    """External message for sending transactions to the TON blockchain."""

    def __init__(
        self,
        src: Address | None = None,
        dest: Address | None = None,
        import_fee: int = 0,
        body: Cell | None = None,
        state_init: StateInit | None = None,
    ) -> None:
        """Initialize an external message.

        :param src: Source address, or ``None``.
        :param dest: Destination contract address, or ``None``.
        :param import_fee: Import fee in nanotons.
        :param body: Signed message body cell, or ``None``.
        :param state_init: ``StateInit`` for deployment, or ``None``.
        """
        info = ExternalMsgInfo(src, dest, import_fee)
        super().__init__(info, state_init, body or Cell.empty())


class InternalMessage(MessageAny):
    """Internal message for on-chain contract-to-contract communication."""

    def __init__(
        self,
        ihr_disabled: bool | None = True,
        bounce: bool | None = None,
        bounced: bool | None = False,
        src: Address | str | None = None,
        dest: Address | str | None = None,
        value: CurrencyCollection | int = 0,
        ihr_fee: int = 0,
        fwd_fee: int = 0,
        created_lt: int = 0,
        created_at: int = 0,
        body: Cell | None = None,
        state_init: StateInit | None = None,
    ) -> None:
        """Initialize an internal message.

        :param ihr_disabled: Disable instant hypercube routing.
        :param bounce: Bounce on error, or ``None`` for auto-detect.
        :param bounced: Whether this is a bounced message.
        :param src: Source address, or ``None``.
        :param dest: Destination address, or ``None``.
        :param value: Amount in nanotons or ``CurrencyCollection``.
        :param ihr_fee: IHR fee in nanotons.
        :param fwd_fee: Forward fee in nanotons.
        :param created_lt: Logical time when created.
        :param created_at: Unix timestamp when created.
        :param body: Message body cell, or ``None``.
        :param state_init: ``StateInit`` for deployment, or ``None``.
        """
        if isinstance(src, str):
            src = Address(src)
        if isinstance(dest, str):
            dest = Address(dest)
        if bounce is None:
            bounce = dest.is_bounceable if dest and isinstance(dest, Address) else False
        if body is None:
            body = Cell.empty()
        if isinstance(value, int):
            value = CurrencyCollection(value)

        info = InternalMsgInfo(
            ihr_disabled=ihr_disabled,
            bounce=bounce,
            bounced=bounced,
            src=src,
            dest=dest,
            value=value,
            ihr_fee=ihr_fee,
            fwd_fee=fwd_fee,
            created_lt=created_lt,
            created_at=created_at,
        )
        super().__init__(info, state_init, body)

