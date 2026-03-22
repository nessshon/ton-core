from __future__ import annotations

import base64
import dataclasses
import socket
import struct
import typing as t
from contextlib import suppress
from dataclasses import dataclass, field
from typing import TypeVar

from ton_core.contrib.types import BinaryLike, PublicKey
from ton_core.contrib.utils import load_json

__all__ = [
    "MAINNET_GLOBAL_CONFIG_URL",
    "TESTNET_GLOBAL_CONFIG_URL",
    "AdnlAddressConfig",
    "AdnlAddressListConfig",
    "BlockRef",
    "ConfigModel",
    "DhtConfig",
    "DhtNodeConfig",
    "DhtNodeIDConfig",
    "DhtNodesConfig",
    "GlobalConfig",
    "LiteServerConfig",
    "LiteServerIDConfig",
    "ValidatorConfig",
    "get_mainnet_global_config",
    "get_testnet_global_config",
    "load_global_config",
]

_T = TypeVar("_T", bound="ConfigModel")

MAINNET_GLOBAL_CONFIG_URL = "https://ton.org/global-config.json"
"""URL for the TON mainnet global configuration."""

TESTNET_GLOBAL_CONFIG_URL = "https://ton.org/testnet-global-config.json"
"""URL for the TON testnet global configuration."""


class ConfigModel:
    """Base for config dataclasses with generic ``from_dict``.

    Filters unknown keys (including ``@type``) and passes only
    fields declared on the dataclass to the constructor.
    """

    @classmethod
    def from_dict(cls: type[_T], data: dict[str, t.Any]) -> _T:
        """Create from a dictionary, ignoring unknown keys.

        :param data: Raw dictionary (e.g. from JSON).
        :return: Instance of the config model.
        """
        known = {f.name for f in dataclasses.fields(cls)}  # type: ignore[arg-type]
        return cls(**{k: v for k, v in data.items() if k in known})


@dataclass
class LiteServerIDConfig(ConfigModel):
    """Liteserver public key identifier."""

    key: str


@dataclass
class LiteServerConfig(ConfigModel):
    """TON liteserver connection configuration.

    :param port: TCP port number for ADNL connection.
    :param ip: IP address as string or signed 32-bit integer.
    :param id: Server public key as ``LiteServerIDConfig`` or raw binary.
    """

    port: int
    ip: str | int
    id: LiteServerIDConfig | BinaryLike

    @property
    def pub_key(self) -> bytes:
        """Server Ed25519 public key as bytes."""
        if isinstance(self.id, LiteServerIDConfig):
            raw: BinaryLike = self.id.key
        else:
            raw = self.id
        return PublicKey(raw).as_bytes

    @property
    def host(self) -> str:
        """IP address in dotted-decimal notation."""
        with suppress(Exception):
            packed_id = struct.pack(">i", int(self.ip))
            return socket.inet_ntoa(packed_id)
        return str(self.ip)

    @property
    def endpoint(self) -> str:
        """Host and port as ``host:port`` string."""
        return f"{self.host}:{self.port}"

    @classmethod
    def from_dict(cls, data: dict[str, t.Any]) -> LiteServerConfig:
        """Create from a dictionary, resolving nested ``id``.

        :param data: Dictionary with ``port``, ``ip``, and ``id`` keys.
        :return: Parsed :class:`LiteServerConfig`.
        """
        id_raw = data.get("id")
        if isinstance(id_raw, dict):
            id_val: LiteServerIDConfig | BinaryLike = LiteServerIDConfig.from_dict(id_raw)
        elif id_raw is not None:
            id_val = id_raw
        else:
            raise TypeError("Missing 'id' in liteserver config")
        return cls(port=data["port"], ip=data["ip"], id=id_val)


@dataclass
class BlockRef(ConfigModel):
    """TON blockchain block identifier from global configuration.

    :param file_hash: Base64-encoded file hash.
    :param root_hash: Base64-encoded root cell hash.
    :param workchain: Workchain ID (-1 masterchain, 0 basechain).
    :param shard: Shard identifier, or ``None`` for masterchain.
    :param seqno: Block sequence number, or ``None``.
    """

    file_hash: str
    root_hash: str
    workchain: int
    shard: int | None = None
    seqno: int | None = None

    @staticmethod
    def _hash_to_hex(v: str) -> str:
        """Convert base64-encoded hash to hexadecimal."""
        return base64.b64decode(v).hex()

    @property
    def root_hash_hex(self) -> str:
        """Root hash as hexadecimal string."""
        return self._hash_to_hex(self.root_hash)

    @property
    def file_hash_hex(self) -> str:
        """File hash as hexadecimal string."""
        return self._hash_to_hex(self.file_hash)


@dataclass
class AdnlAddressConfig(ConfigModel):
    """ADNL UDP address entry.

    :param ip: IP address as signed 32-bit integer.
    :param port: UDP port number.
    """

    ip: str | int
    port: int

    @property
    def host(self) -> str:
        """IP address in dotted-decimal notation."""
        with suppress(Exception):
            packed = struct.pack(">i", int(self.ip))
            return socket.inet_ntoa(packed)
        return str(self.ip)

    @property
    def endpoint(self) -> str:
        """Host and port as ``host:port`` string."""
        return f"{self.host}:{self.port}"


@dataclass
class AdnlAddressListConfig(ConfigModel):
    """ADNL address list with version metadata.

    :param addrs: List of ADNL UDP addresses.
    :param version: Address list version.
    :param reinit_date: Reinitialization timestamp.
    :param priority: Address list priority.
    :param expire_at: Expiration timestamp.
    """

    addrs: list[AdnlAddressConfig] = field(default_factory=list)
    version: int = 0
    reinit_date: int = 0
    priority: int = 0
    expire_at: int = 0

    @classmethod
    def from_dict(cls, data: dict[str, t.Any]) -> AdnlAddressListConfig:
        """Create from a dictionary, resolving nested addresses.

        :param data: Dictionary with ``addrs`` and optional metadata keys.
        :return: Parsed :class:`AdnlAddressListConfig`.
        """
        addrs_raw = data.get("addrs", [])
        addrs = [
            AdnlAddressConfig.from_dict(a) if isinstance(a, dict) else a
            for a in addrs_raw
        ]
        return cls(
            addrs=addrs,
            version=data.get("version", 0),
            reinit_date=data.get("reinit_date", 0),
            priority=data.get("priority", 0),
            expire_at=data.get("expire_at", 0),
        )


@dataclass
class DhtNodeIDConfig(ConfigModel):
    """DHT node public key identifier."""

    key: str


@dataclass
class DhtNodeConfig(ConfigModel):
    """DHT node entry from global configuration.

    :param id: Node public key as ``DhtNodeIDConfig`` or raw binary.
    :param addr_list: ADNL address list for this node.
    :param version: Node configuration version.
    :param signature: Base64-encoded Ed25519 signature.
    """

    id: DhtNodeIDConfig | BinaryLike
    addr_list: AdnlAddressListConfig
    version: int
    signature: str

    @property
    def pub_key(self) -> bytes:
        """Node Ed25519 public key as bytes."""
        if isinstance(self.id, DhtNodeIDConfig):
            raw: BinaryLike = self.id.key
        else:
            raw = self.id
        return PublicKey(raw).as_bytes

    @property
    def host(self) -> str:
        """IP address of the first address entry."""
        if self.addr_list.addrs:
            return self.addr_list.addrs[0].host
        return ""

    @property
    def port(self) -> int:
        """UDP port of the first address entry."""
        if self.addr_list.addrs:
            return self.addr_list.addrs[0].port
        return 0

    @property
    def endpoint(self) -> str:
        """Host and port as ``host:port`` string."""
        return f"{self.host}:{self.port}"

    @classmethod
    def from_dict(cls, data: dict[str, t.Any]) -> DhtNodeConfig:
        """Create from a dictionary.

        :param data: Dictionary with ``id``, ``addr_list``, ``version``, ``signature`` keys.
        :return: Parsed :class:`DhtNodeConfig`.
        """
        id_raw = data.get("id")
        if isinstance(id_raw, dict):
            id_val: DhtNodeIDConfig | BinaryLike = DhtNodeIDConfig.from_dict(id_raw)
        elif id_raw is not None:
            id_val = id_raw
        else:
            raise TypeError("Missing 'id' in DHT node config")

        addr_list_raw = data.get("addr_list", {})
        if isinstance(addr_list_raw, dict):
            addr_list = AdnlAddressListConfig.from_dict(addr_list_raw)
        elif isinstance(addr_list_raw, AdnlAddressListConfig):
            addr_list = addr_list_raw
        else:
            addr_list = AdnlAddressListConfig()

        return cls(
            id=id_val,
            addr_list=addr_list,
            version=data.get("version", 0),
            signature=data.get("signature", ""),
        )


@dataclass
class DhtNodesConfig(ConfigModel):
    """Container for a list of DHT nodes.

    :param nodes: List of DHT node entries.
    """

    nodes: list[DhtNodeConfig] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: dict[str, t.Any]) -> DhtNodesConfig:
        """Create from a dictionary.

        :param data: Dictionary with ``nodes`` key.
        :return: Parsed :class:`DhtNodesConfig`.
        """
        raw_nodes = data.get("nodes", [])
        nodes = [
            DhtNodeConfig.from_dict(n) if isinstance(n, dict) else n
            for n in raw_nodes
        ]
        return cls(nodes=nodes)


@dataclass
class DhtConfig(ConfigModel):
    """DHT configuration from global config.

    :param k: Kademlia replication parameter.
    :param a: Kademlia concurrency parameter.
    :param static_nodes: Static DHT node list.
    """

    k: int
    a: int
    static_nodes: DhtNodesConfig = field(default_factory=DhtNodesConfig)

    @property
    def nodes(self) -> list[DhtNodeConfig]:
        """Static DHT nodes."""
        return self.static_nodes.nodes

    @classmethod
    def from_dict(cls, data: dict[str, t.Any]) -> DhtConfig:
        """Create from a dictionary.

        :param data: Dictionary with ``k``, ``a``, ``static_nodes`` keys.
        :return: Parsed :class:`DhtConfig`.
        """
        static_raw = data.get("static_nodes", {})
        if isinstance(static_raw, dict):
            static_nodes = DhtNodesConfig.from_dict(static_raw)
        elif isinstance(static_raw, DhtNodesConfig):
            static_nodes = static_raw
        else:
            static_nodes = DhtNodesConfig()

        return cls(
            k=data["k"],
            a=data["a"],
            static_nodes=static_nodes,
        )


@dataclass
class ValidatorConfig(ConfigModel):
    """Validator configuration from global config.

    :param zero_state: Genesis block identifier.
    :param init_block: Initial block identifier.
    :param hardforks: Optional list of hardfork blocks.
    """

    zero_state: BlockRef
    init_block: BlockRef
    hardforks: list[BlockRef] | None = None

    @classmethod
    def from_dict(cls, data: dict[str, t.Any]) -> ValidatorConfig:
        """Create from a dictionary.

        :param data: Dictionary with ``zero_state``, ``init_block``, ``hardforks`` keys.
        :return: Parsed :class:`ValidatorConfig`.
        """
        zero_raw = data["zero_state"]
        zero = BlockRef.from_dict(zero_raw) if isinstance(zero_raw, dict) else zero_raw

        init_raw = data["init_block"]
        init = BlockRef.from_dict(init_raw) if isinstance(init_raw, dict) else init_raw

        hardforks_raw = data.get("hardforks")
        hardforks: list[BlockRef] | None = None
        if isinstance(hardforks_raw, list):
            hardforks = [
                BlockRef.from_dict(h) if isinstance(h, dict) else h
                for h in hardforks_raw
            ]

        return cls(
            zero_state=zero,
            init_block=init,
            hardforks=hardforks,
        )


@dataclass
class GlobalConfig(ConfigModel):
    """TON global network configuration.

    :param liteservers: Available liteserver endpoints.
    :param dht: DHT configuration, or ``None``.
    :param validator: Validator configuration, or ``None``.
    """

    liteservers: list[LiteServerConfig] = field(default_factory=list)
    dht: DhtConfig | None = None
    validator: ValidatorConfig | None = None

    @classmethod
    def from_dict(cls, data: dict[str, t.Any]) -> GlobalConfig:
        """Create from a dictionary, resolving nested structures.

        :param data: Raw JSON-parsed dictionary.
        :return: Parsed :class:`GlobalConfig`.
        """
        raw_ls = data.get("liteservers", [])
        servers: list[LiteServerConfig] = []
        if isinstance(raw_ls, list):
            servers = [
                LiteServerConfig.from_dict(item) if isinstance(item, dict) else item
                for item in raw_ls
            ]

        dht: DhtConfig | None = None
        dht_raw = data.get("dht")
        if isinstance(dht_raw, dict):
            dht = DhtConfig.from_dict(dht_raw)
        elif isinstance(dht_raw, DhtConfig):
            dht = dht_raw

        validator: ValidatorConfig | None = None
        val_raw = data.get("validator")
        if isinstance(val_raw, dict):
            validator = ValidatorConfig.from_dict(val_raw)
        elif isinstance(val_raw, ValidatorConfig):
            validator = val_raw

        return cls(
            liteservers=servers,
            dht=dht,
            validator=validator,
        )


def load_global_config(source: str) -> GlobalConfig:
    """Load and validate a TON global configuration from URL or file path.

    :param source: URL or local file path to the JSON config.
    :return: Parsed :class:`GlobalConfig` instance.
    :raises RuntimeError: If validation fails.
    """
    try:
        data = load_json(source)
        return GlobalConfig.from_dict(data)
    except (TypeError, KeyError, ValueError) as e:
        raise RuntimeError(f"Config validation failed: {e} ({source})") from e


def get_mainnet_global_config() -> GlobalConfig:
    """Fetch mainnet global configuration from ton.org.

    :return: Parsed :class:`GlobalConfig` instance.
    """
    return load_global_config(MAINNET_GLOBAL_CONFIG_URL)


def get_testnet_global_config() -> GlobalConfig:
    """Fetch testnet global configuration from ton.org.

    :return: Parsed :class:`GlobalConfig` instance.
    """
    return load_global_config(TESTNET_GLOBAL_CONFIG_URL)

