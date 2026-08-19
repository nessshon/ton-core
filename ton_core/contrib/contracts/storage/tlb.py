from __future__ import annotations

from typing import Any

from ton_core.boc import Cell, HashMap, Slice, begin_cell
from ton_core.boc.builder import Builder
from ton_core.contrib.contracts._utils import _load_std_address
from ton_core.contrib.contracts.opcodes import OpCode
from ton_core.contrib.types import AddressLike, BagID, Binary, BinaryLike, PublicKey, Signature
from ton_core.tlb.tlb import TlbScheme

__all__ = [
    "StorageData",
    "StorageModifyProvidersBody",
    "StorageProofBody",
    "StorageProvider",
    "StorageProviderInfo",
    "StorageWithdrawOwnerBody",
]


def _load_public_key(key: str) -> PublicKey:
    """Deserialize a hashmap key bitstring into a public key.

    :param key: Key bitstring of 256 bits.
    :return: Public key held by the key.
    """
    return PublicKey(int(key, 2).to_bytes(32, "big"))


def _store_scheme(value: Any, builder: Builder) -> Builder:
    """Store a serialized TL-B scheme as hashmap value.

    :param value: Scheme to serialize.
    :param builder: Destination builder.
    :return: Destination builder.
    """
    return builder.store_slice(value.serialize().begin_parse())


def _build_providers(providers: dict[PublicKey | BinaryLike, Any]) -> HashMap:
    """Build a hashmap of providers keyed by public key.

    :param providers: Providers to store, keyed by public key.
    :return: Hashmap holding the providers.
    """
    hashmap = HashMap(key_size=256, value_serializer=_store_scheme)
    for key, value in providers.items():
        public_key = key if isinstance(key, PublicKey) else PublicKey(key)
        hashmap.set_int_key(public_key.as_int, value)
    return hashmap


class StorageProviderInfo(TlbScheme):
    """Terms a provider is hired on inside a storage contract."""

    def __init__(self, payment_max_span: int, rate_per_mb_day: int) -> None:
        """Initialize StorageProviderInfo.

        :param payment_max_span: Longest paid gap between proofs, in seconds.
        :param rate_per_mb_day: Price per megabyte per day, in nanotons.
        """
        self.payment_max_span = payment_max_span
        self.rate_per_mb_day = rate_per_mb_day

    def serialize(self) -> Cell:
        """Serialize to Cell."""
        cell = begin_cell()
        cell.store_uint(self.payment_max_span, 32)
        cell.store_coins(self.rate_per_mb_day)
        return cell.end_cell()

    @classmethod
    def deserialize(cls, cs: Slice) -> StorageProviderInfo:
        """Deserialize from Slice."""
        return cls(
            payment_max_span=cs.load_uint(32),
            rate_per_mb_day=cs.load_coins(),
        )


class StorageProvider(TlbScheme):
    """Active provider slot of a storage contract."""

    def __init__(
        self,
        info: StorageProviderInfo,
        next_proof_byte: int = 0,
        last_proof_time: int = 0,
        nonce: int = 0,
    ) -> None:
        """Initialize StorageProvider.

        :param info: Terms this provider serves the bag on.
        :param next_proof_byte: Byte offset the next proof must cover.
        :param last_proof_time: Unix time of the last accepted proof, 0 if none yet.
        :param nonce: Nonce the next proof must carry.
        """
        self.info = info
        self.next_proof_byte = next_proof_byte
        self.last_proof_time = last_proof_time
        self.nonce = nonce

    def serialize(self) -> Cell:
        """Serialize to Cell."""
        cell = begin_cell()
        cell.store_uint(self.next_proof_byte, 64)
        cell.store_uint(self.last_proof_time, 32)
        cell.store_uint(self.nonce, 64)
        cell.store_ref(self.info.serialize())
        return cell.end_cell()

    @classmethod
    def deserialize(cls, cs: Slice) -> StorageProvider:
        """Deserialize from Slice."""
        return cls(
            next_proof_byte=cs.load_uint(64),
            last_proof_time=cs.load_uint(32),
            nonce=cs.load_uint(64),
            info=StorageProviderInfo.deserialize(cs.load_ref().begin_parse()),
        )


class StorageData(TlbScheme):
    """On-chain data of a TON Storage contract holding a single bag."""

    def __init__(
        self,
        torrent_hash: BagID | BinaryLike,
        owner_address: AddressLike | None,
        file_size: int,
        chunk_size: int,
        merkle_hash: Binary | BinaryLike,
        providers: dict[PublicKey | BinaryLike, StorageProvider] | None = None,
        key_len: int = 0,
    ) -> None:
        """Initialize StorageData.

        :param torrent_hash: Bag identifier stored by this contract.
        :param owner_address: Address that pays for the storage.
        :param file_size: Bag size in bytes.
        :param chunk_size: Piece size in bytes.
        :param merkle_hash: Root hash of the bag merkle tree.
        :param providers: Active providers, keyed by public key.
        :param key_len: Merkle proof depth, 0 until the first provider is hired.
        """
        self.torrent_hash = torrent_hash if isinstance(torrent_hash, BagID) else BagID(torrent_hash)
        self.owner_address = owner_address
        self.file_size = file_size
        self.chunk_size = chunk_size
        self.merkle_hash = merkle_hash if isinstance(merkle_hash, Binary) else Binary(merkle_hash)
        self.providers = providers or {}
        self.key_len = key_len

    def serialize(self) -> Cell:
        """Serialize to Cell."""
        cell = begin_cell()
        cell.store_bytes(self.torrent_hash.as_bytes)
        cell.store_dict(_build_providers(self.providers).serialize())
        cell.store_address(self.owner_address)
        cell.store_uint(self.file_size, 64)
        cell.store_uint(self.chunk_size, 32)
        cell.store_bytes(self.merkle_hash.as_bytes)
        cell.store_uint(self.key_len, 8)
        return cell.end_cell()

    @classmethod
    def deserialize(cls, cs: Slice) -> StorageData:
        """Deserialize from Slice."""
        return cls(
            torrent_hash=cs.load_bytes(32),
            providers=cs.load_dict(
                key_length=256,
                key_deserializer=_load_public_key,
                value_deserializer=StorageProvider.deserialize,
            )
            or {},
            owner_address=_load_std_address(cs),
            file_size=cs.load_uint(64),
            chunk_size=cs.load_uint(32),
            merkle_hash=cs.load_bytes(32),
            key_len=cs.load_uint(8),
        )


class StorageModifyProvidersBody(TlbScheme):
    """Message body replacing the provider set of a storage contract (opcode 0x3DC680AE)."""

    def __init__(
        self,
        providers: dict[PublicKey | BinaryLike, StorageProviderInfo] | None = None,
        query_id: int = 0,
    ) -> None:
        """Initialize StorageModifyProvidersBody.

        :param providers: Wanted providers, keyed by public key.
        :param query_id: Query identifier.
        """
        self.providers = providers or {}
        self.query_id = query_id

    def serialize(self) -> Cell:
        """Serialize to Cell."""
        cell = begin_cell()
        cell.store_uint(OpCode.STORAGE_MODIFY_PROVIDERS, 32)
        cell.store_uint(self.query_id, 64)
        cell.store_dict(_build_providers(self.providers).serialize())
        return cell.end_cell()

    @classmethod
    def deserialize(cls, cs: Slice) -> StorageModifyProvidersBody:
        """Deserialize from Slice."""
        cs.skip_bits(32)
        return cls(
            query_id=cs.load_uint(64),
            providers=cs.load_dict(
                key_length=256,
                key_deserializer=_load_public_key,
                value_deserializer=StorageProviderInfo.deserialize,
            )
            or {},
        )


class StorageWithdrawOwnerBody(TlbScheme):
    """Message body terminating a storage contract and returning its balance (opcode 0x61FFF683)."""

    def __init__(self, query_id: int = 0) -> None:
        """Initialize StorageWithdrawOwnerBody.

        :param query_id: Query identifier.
        """
        self.query_id = query_id

    def serialize(self) -> Cell:
        """Serialize to Cell."""
        cell = begin_cell()
        cell.store_uint(OpCode.STORAGE_WITHDRAW_OWNER, 32)
        cell.store_uint(self.query_id, 64)
        return cell.end_cell()

    @classmethod
    def deserialize(cls, cs: Slice) -> StorageWithdrawOwnerBody:
        """Deserialize from Slice."""
        cs.skip_bits(32)
        return cls(query_id=cs.load_uint(64))


class StorageProofBody(TlbScheme):
    """Message body carrying a storage proof from a provider (opcode 0x48F548CE)."""

    def __init__(
        self,
        key: PublicKey | BinaryLike,
        signature: Signature | BinaryLike,
        nonce: int,
        proof: Cell,
        query_id: int = 0,
    ) -> None:
        """Initialize StorageProofBody.

        :param key: Public key of the proving provider.
        :param signature: Ed25519 signature over the rest of the body, 64 bytes.
        :param nonce: Nonce the contract expects from this provider.
        :param proof: Merkle proof cell for the requested byte.
        :param query_id: Query identifier.
        """
        self.key = key if isinstance(key, PublicKey) else PublicKey(key)
        self.signature = signature if isinstance(signature, Signature) else Signature(signature)
        self.nonce = nonce
        self.proof = proof
        self.query_id = query_id

    def serialize(self) -> Cell:
        """Serialize to Cell."""
        cell = begin_cell()
        cell.store_uint(OpCode.STORAGE_PROOF, 32)
        cell.store_uint(self.query_id, 64)
        cell.store_bytes(self.key.as_bytes)
        cell.store_bytes(self.signature.as_bytes)
        cell.store_uint(self.nonce, 64)
        cell.store_ref(self.proof)
        return cell.end_cell()

    @classmethod
    def deserialize(cls, cs: Slice) -> StorageProofBody:
        """Deserialize from Slice."""
        cs.skip_bits(32)
        return cls(
            query_id=cs.load_uint(64),
            key=cs.load_bytes(32),
            signature=cs.load_bytes(64),
            nonce=cs.load_uint(64),
            proof=cs.load_ref(),
        )
