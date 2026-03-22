from __future__ import annotations

import base64
import hashlib
import re
from contextlib import suppress
from dataclasses import dataclass
from enum import Enum
from typing import Any, ClassVar

from nacl.signing import SigningKey

from ton_core.boc.address import Address

__all__ = [
    "ADNL",
    "DEFAULT_SENDMODE",
    "DEFAULT_SUBWALLET_ID",
    "MAINNET_GENESIS_UTIME",
    "MASTERCHAIN_SHARD",
    "AddressLike",
    "BagID",
    "Binary",
    "BinaryLike",
    "ContractState",
    "DNSCategory",
    "DNSPrefix",
    "MetadataPrefix",
    "NetworkGlobalID",
    "PrivateKey",
    "PublicKey",
    "SendMode",
    "SignatureDomain",
    "WorkchainID",
]

AddressLike = Address | str
"""TON address: ``Address`` object or string representation."""

BinaryLike = str | int | bytes
"""Accepted binary input types."""

MASTERCHAIN_SHARD: int = -9223372036854775808
"""Default shard ID for the masterchain."""

MAINNET_GENESIS_UTIME: int = 1573822385
"""Unix timestamp of the mainnet genesis block."""

DEFAULT_SUBWALLET_ID: int = 698983191
"""Default subwallet ID used in wallet contracts."""


class NetworkGlobalID(int, Enum):
    """TON blockchain network identifier."""

    MAINNET = -239
    """Production network."""

    TESTNET = -3
    """Testing network."""

    TETRA = 662387
    """Tetra network."""


class WorkchainID(int, Enum):
    """TON blockchain workchain identifier."""

    BASECHAIN = 0
    """Default workchain for user contracts."""

    MASTERCHAIN = -1
    """Coordination workchain for validators and configuration."""


class MetadataPrefix(int, Enum):
    """Jetton/NFT metadata storage location prefix."""

    ONCHAIN = 0
    """Metadata stored directly on-chain."""

    OFFCHAIN = 1
    """Metadata stored off-chain with URI reference."""


class SendMode(int, Enum):
    """Message sending mode flags for TON transactions."""

    CARRY_ALL_REMAINING_BALANCE = 128
    """Send all remaining balance."""

    CARRY_ALL_REMAINING_INCOMING_VALUE = 64
    """Forward all remaining incoming value."""

    DESTROY_ACCOUNT_IF_ZERO = 32
    """Destroy account if balance reaches zero."""

    BOUNCE_IF_ACTION_FAIL = 16
    """Bounce transaction on action-phase failure."""

    IGNORE_ERRORS = 2
    """Continue execution despite errors."""

    PAY_GAS_SEPARATELY = 1
    """Pay forward fees separately from message value."""

    DEFAULT = 0
    """Standard mode with no special flags."""


DEFAULT_SENDMODE: int = SendMode.PAY_GAS_SEPARATELY | SendMode.IGNORE_ERRORS
"""Default send mode combining PAY_GAS_SEPARATELY and IGNORE_ERRORS."""


class DNSPrefix(int, Enum):
    """TON DNS record type prefix."""

    DNS_NEXT_RESOLVER = 0xBA93
    """Pointer to next resolver contract."""

    STORAGE = 0x7473
    """TON Storage bag-ID reference."""

    WALLET = 0x9FD3
    """Wallet address reference."""

    SITE = 0xAD01
    """ADNL address for TON Sites."""


class DNSCategory(int, Enum):
    """TON DNS record category as SHA-256 hash."""

    DNS_NEXT_RESOLVER = (
        11732114750494247458678882651681748623800183221773167493832867265755123357695
    )
    """Hash for next-resolver queries."""

    STORAGE = (
        33305727148774590499946634090951755272001978043137765208040544350030765946327
    )
    """Hash for storage bag-ID queries."""

    WALLET = (
        105311596331855300602201538317979276640056460191511695660591596829410056223515
    )
    """Hash for wallet address queries."""

    SITE = (
        113837984718866553357015413641085683664993881322709313240352703269157551621118
    )
    """Hash for site ADNL address queries."""

    ALL = 0
    """Query all categories."""


class ContractState(str, Enum):
    """TON smart-contract lifecycle state."""

    ACTIVE = "active"
    """Deployed and operational."""

    FROZEN = "frozen"
    """Frozen due to storage-fee debt."""

    UNINIT = "uninit"
    """Address exists but code is not deployed."""

    NONEXIST = "nonexist"
    """No balance or state."""


@dataclass(slots=True, frozen=True)
class SignatureDomain:
    """Ed25519 signature domain for TON networks.

    For L1 networks (mainnet/testnet) the domain is empty (no prefix).
    For L2 networks the signature is computed over an SHA-256 domain prefix
    prepended to the data.
    """

    EMPTY_TAG: ClassVar[int] = 0x0E1D571B
    L2_TAG: ClassVar[int] = 0x71B34EE1

    network: NetworkGlobalID
    """Network identifier."""

    @property
    def is_l2(self) -> bool:
        """True if the network requires domain-prefixed signatures."""
        return self.network not in (NetworkGlobalID.MAINNET, NetworkGlobalID.TESTNET)

    @property
    def prefix(self) -> bytes | None:
        """32-byte SHA-256 domain prefix for signing, or None for L1."""
        if not self.is_l2:
            return None
        tag = self.L2_TAG.to_bytes(4, "little")
        global_id = int(self.network).to_bytes(4, "little", signed=True)
        domain_hash = hashlib.sha256(tag + global_id).digest()
        empty_hash = hashlib.sha256(self.EMPTY_TAG.to_bytes(4, "little")).digest()
        if domain_hash == empty_hash:
            return None
        return domain_hash

    def data_to_sign(self, data: bytes) -> bytes:
        """Prepend domain prefix to data if L2, otherwise return unchanged.

        :param data: Raw data bytes.
        :return: Data with domain prefix prepended, or original data.
        """
        p = self.prefix
        return (p + data) if p is not None else data


class Binary:
    """Binary data wrapper with multi-format input/output.

    Accepts bytes, integers, hex strings (0x-prefixed or plain), base64
    strings, and decimal-integer strings.
    """

    def __init__(self, raw: BinaryLike, size: int = 32) -> None:
        """Initialize Binary with the given raw value and expected size.

        :param raw: Input data.
        :param size: Expected byte length (default: 32).
        """
        self._size = size
        self._bytes = self._parse(raw)

    @property
    def size(self) -> int:
        """Expected byte length."""
        return self._size

    def _parse(self, value: Any) -> bytes:
        if isinstance(value, bytes):
            return value
        if isinstance(value, int):
            length = max(1, (value.bit_length() + 7) // 8)
            return value.to_bytes(length, "big")

        if isinstance(value, str):
            s = value.strip()

            if s.lower().startswith("0x"):
                return bytes.fromhex(s[2:])

            if (
                len(s) % 2 == 0
                and re.compile(r"^[0-9a-fA-F]+$").fullmatch(s)
                and len(s) == self._size * 2
            ):
                return bytes.fromhex(s)

            with suppress(Exception):
                return base64.b64decode(s, validate=True)

            n = int(s, 10)
            length = max(1, (n.bit_length() + 7) // 8)
            return n.to_bytes(length, "big")

        raise ValueError(f"Invalid binary type: {type(value).__name__}.")

    @property
    def as_bytes(self) -> bytes:
        """Data as bytes, left-padded with zeros to size."""
        return self._bytes.rjust(self._size, b"\x00")

    @property
    def as_int(self) -> int:
        """Data as big-endian unsigned integer."""
        return int.from_bytes(self.as_bytes, byteorder="big")

    @property
    def as_hex(self) -> str:
        """Data as lowercase hex string."""
        return self.as_bytes.hex()

    @property
    def as_b64(self) -> str:
        """Data as base64-encoded string."""
        return base64.b64encode(self.as_bytes).decode()

    def __eq__(self, other: object) -> bool:
        """Return True if both Binary instances hold the same bytes."""
        return isinstance(other, Binary) and self.as_bytes == other.as_bytes

    def __repr__(self) -> str:
        """Return a debug string with class name and base64-encoded value."""
        return f"{self.__class__.__name__}<{self.as_b64!r}>"


class PublicKey(Binary):
    """Ed25519 public key (32 bytes)."""

    def __init__(self, raw: BinaryLike) -> None:
        """Initialize PublicKey from raw key data.

        :param raw: 32-byte public key data.
        """
        super().__init__(raw, size=32)


class PrivateKey(Binary):
    """Ed25519 private key with automatic public-key derivation.

    Accepts a 32-byte seed or a 64-byte keypair (private + public).
    """

    def __init__(self, raw: BinaryLike) -> None:
        """Initialize PrivateKey from a seed or full keypair.

        :param raw: 32-byte seed or 64-byte keypair.
        :raises ValueError: If parsed length is neither 32 nor 64 bytes.
        """
        raw_bytes = self._parse(raw)

        if len(raw_bytes) == 32:
            signing_key = SigningKey(raw_bytes)
            raw_bytes += signing_key.verify_key.encode()
        elif len(raw_bytes) == 64:
            pass
        else:
            raise ValueError("Private key must be 32 or 64 bytes.")

        self._public_part = raw_bytes[32:]
        super().__init__(raw_bytes[:32], size=32)

    @property
    def public_key(self) -> PublicKey:
        """Derived Ed25519 public key."""
        return PublicKey(self._public_part)

    @property
    def keypair(self) -> Binary:
        """Full 64-byte keypair (private + public)."""
        raw = self.as_bytes + self.public_key.as_bytes
        return Binary(raw, size=64)


class ADNL(Binary):
    """ADNL address (32 bytes)."""

    def __init__(self, raw: BinaryLike) -> None:
        """Initialize ADNL from raw address data.

        :param raw: 32-byte ADNL address.
        """
        super().__init__(raw, 32)

    def __repr__(self) -> str:
        """Return a debug string with class name and uppercase hex value."""
        return f"{self.__class__.__name__}<{self.as_hex.upper()}>"


class BagID(ADNL):
    """TON Storage bag identifier (32 bytes)."""

