from __future__ import annotations

import secrets
import time
from dataclasses import dataclass

from ton_core.contrib.contracts.opcodes import OpCode
from ton_core.contrib.types import DEFAULT_SENDMODE, SendMode

__all__ = [
    "BaseWalletParams",
    "WalletHighloadV2Params",
    "WalletHighloadV3Params",
    "WalletPreprocessedV2Params",
    "WalletV1Params",
    "WalletV2Params",
    "WalletV3Params",
    "WalletV4Params",
    "WalletV5BetaParams",
    "WalletV5Params",
]


@dataclass
class BaseWalletParams:
    """Base parameters for wallet transaction building."""


@dataclass
class WalletV1Params(BaseWalletParams):
    """Transaction parameters for Wallet v1."""

    seqno: int | None = None
    """Sequence number (fetched from contract if None)."""


@dataclass
class WalletV2Params(BaseWalletParams):
    """Transaction parameters for Wallet v2."""

    seqno: int | None = None
    """Sequence number (fetched from contract if None)."""
    valid_until: int | None = None
    """Expiration unix timestamp, or None."""


@dataclass
class WalletV3Params(BaseWalletParams):
    """Transaction parameters for Wallet v3."""

    seqno: int | None = None
    """Sequence number (fetched from contract if None)."""
    valid_until: int | None = None
    """Expiration unix timestamp, or None."""


@dataclass
class WalletV4Params(BaseWalletParams):
    """Transaction parameters for Wallet v4."""

    seqno: int | None = None
    """Sequence number (fetched from contract if None)."""
    valid_until: int | None = None
    """Expiration unix timestamp, or None."""
    op_code: int = 0x00
    """Operation code (0x00 for simple transfer)."""


@dataclass
class WalletV5BetaParams(BaseWalletParams):
    """Transaction parameters for Wallet v5 Beta."""

    seqno: int | None = None
    """Sequence number (fetched from contract if None)."""
    valid_until: int | None = None
    """Expiration unix timestamp, or None."""
    op_code: int = OpCode.AUTH_SIGNED_EXTERNAL
    """Operation code (default: 0x7369676E)."""


@dataclass
class WalletV5Params(BaseWalletParams):
    """Transaction parameters for Wallet v5."""

    seqno: int | None = None
    """Sequence number (fetched from contract if None)."""
    valid_until: int | None = None
    """Expiration unix timestamp, or None."""
    op_code: int = OpCode.AUTH_SIGNED_EXTERNAL
    """Operation code (default: 0x7369676E)."""


@dataclass
class WalletHighloadV2Params(BaseWalletParams):
    """Transaction parameters for Highload Wallet v2."""

    bounded_id: int | None = None
    """Bounded query ID combining TTL and query_id (auto-generated if None)."""
    query_id: int | None = None
    """Random 32-bit query identifier (auto-generated if None)."""
    message_ttl: int = 60 * 5
    """Message time-to-live in seconds (default: 300)."""

    def __post_init__(self) -> None:
        """Auto-generate query_id and bounded_id if not provided."""
        if self.query_id is None:
            self.query_id = secrets.randbits(32)
        if self.bounded_id is None:
            now = int(time.time())
            ttl_u32 = (now + self.message_ttl) & 0xFFFFFFFF
            qid_u32 = self.query_id & 0xFFFFFFFF
            self.bounded_id = (ttl_u32 << 32) | qid_u32


@dataclass
class WalletHighloadV3Params(BaseWalletParams):
    """Transaction parameters for Highload Wallet v3."""

    value_to_send: int | None = None
    """Total value in nanotons (calculated from messages if None)."""
    created_at: int | None = None
    """Creation unix timestamp (auto-generated if None)."""
    query_id: int | None = None
    """Query identifier derived from created_at (auto-generated if None)."""
    send_mode: SendMode | int = DEFAULT_SENDMODE
    """Message send mode flags."""

    def __post_init__(self) -> None:
        """Auto-generate created_at and query_id if not provided."""
        if self.created_at is None:
            self.created_at = int(time.time() - 60)
        if self.query_id is None:
            self.query_id = self.created_at % (1 << 23)


@dataclass
class WalletPreprocessedV2Params(BaseWalletParams):
    """Transaction parameters for Preprocessed Wallet v2."""

    seqno: int | None = None
    """Sequence number (fetched from contract if None)."""
    valid_until: int | None = None
    """Expiration unix timestamp, or None."""

