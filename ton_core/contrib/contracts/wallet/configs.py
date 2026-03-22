from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from ton_core.boc.cell import Cell
from ton_core.contrib.contracts.wallet.tlb import WalletV5SubwalletID
from ton_core.contrib.types import DEFAULT_SUBWALLET_ID, PublicKey

__all__ = [
    "BaseContractConfig",
    "BaseWalletConfig",
    "WalletHighloadV2Config",
    "WalletHighloadV3Config",
    "WalletPreprocessedV2Config",
    "WalletV1Config",
    "WalletV2Config",
    "WalletV3Config",
    "WalletV4Config",
    "WalletV5BetaConfig",
    "WalletV5Config",
]


@dataclass
class BaseContractConfig:
    """Base configuration class for TON contracts."""


@dataclass
class BaseWalletConfig(BaseContractConfig):
    """Base configuration for TON wallet contracts."""

    public_key: PublicKey | None = None
    """Ed25519 public key for the wallet."""

    def to_dict(self) -> dict[str, Any]:
        """Convert configuration fields to a dictionary."""
        return asdict(self)


@dataclass
class WalletV1Config(BaseWalletConfig):
    """Configuration for Wallet v1 contracts."""

    seqno: int = 0
    """Sequence number for transaction ordering (default: 0)."""


@dataclass
class WalletV2Config(BaseWalletConfig):
    """Configuration for Wallet v2 contracts."""

    seqno: int = 0
    """Sequence number for transaction ordering (default: 0)."""


@dataclass
class WalletV3Config(BaseWalletConfig):
    """Configuration for Wallet v3 contracts."""

    seqno: int = 0
    """Sequence number for transaction ordering (default: 0)."""
    subwallet_id: int = DEFAULT_SUBWALLET_ID
    """Subwallet identifier for wallet isolation (default: 698983191)."""


@dataclass
class WalletV4Config(BaseWalletConfig):
    """Configuration for Wallet v4 contracts."""

    seqno: int = 0
    """Sequence number for transaction ordering (default: 0)."""
    subwallet_id: int = DEFAULT_SUBWALLET_ID
    """Subwallet identifier for wallet isolation (default: 698983191)."""
    plugins: Cell | None = None
    """Optional dictionary cell containing installed plugins."""


@dataclass
class WalletV5BetaConfig(BaseWalletConfig):
    """Configuration for Wallet v5 Beta contracts."""

    seqno: int = 0
    """Sequence number for transaction ordering (default: 0)."""
    subwallet_id: WalletV5SubwalletID | None = None
    """Enhanced subwallet identifier with network and workchain info."""
    plugins: Cell | None = None
    """Optional dictionary cell containing installed plugins."""


@dataclass
class WalletV5Config(BaseWalletConfig):
    """Configuration for Wallet v5 contracts."""

    is_signature_allowed: bool = True
    """Whether signature authentication is enabled (default: True)."""
    seqno: int = 0
    """Sequence number for transaction ordering (default: 0)."""
    subwallet_id: WalletV5SubwalletID | None = None
    """Enhanced subwallet identifier with network and workchain info."""
    plugins: Cell | None = None
    """Optional dictionary cell containing installed plugins."""


@dataclass
class WalletHighloadV2Config(BaseWalletConfig):
    """Configuration for Highload Wallet v2 contracts."""

    subwallet_id: int = DEFAULT_SUBWALLET_ID
    """Subwallet identifier for wallet isolation (default: 698983191)."""
    last_cleaned: int = 0
    """Timestamp of last query cleanup operation (default: 0)."""
    old_queries: Cell | None = None
    """Optional dictionary cell storing processed query IDs for replay protection."""


@dataclass
class WalletHighloadV3Config(BaseWalletConfig):
    """Configuration for Highload Wallet v3 contracts."""

    subwallet_id: int = DEFAULT_SUBWALLET_ID
    """Subwallet identifier for wallet isolation (default: 698983191)."""
    old_queries: Cell | None = None
    """Optional dictionary cell storing old processed query IDs."""
    queries: Cell | None = None
    """Optional dictionary cell storing current processed query IDs."""
    last_clean_time: int = 0
    """Timestamp of last query cleanup operation (default: 0)."""
    timeout: int = 60 * 5
    """Query expiration timeout in seconds (default: 300 seconds / 5 minutes)."""


@dataclass
class WalletPreprocessedV2Config(BaseWalletConfig):
    """Configuration for Preprocessed Wallet v2 contracts."""

    seqno: int = 0
    """Sequence number for transaction ordering (default: 0)."""

