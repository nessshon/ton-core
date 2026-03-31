from __future__ import annotations

import abc
from typing import Any, ClassVar, cast

from ton_core.boc import Address, Cell, HashMap, Slice, begin_cell
from ton_core.contrib.contracts._utils import _load_std_address
from ton_core.contrib.contracts.nft.tlb import OffchainContent, OnchainContent
from ton_core.contrib.contracts.opcodes import OpCode
from ton_core.contrib.types import ADNL, AddressLike, BagID, Binary, BinaryLike, DNSCategory, DNSPrefix
from ton_core.contrib.utils import string_hash
from ton_core.tlb import TlbScheme

__all__ = [
    "BaseDNSRecord",
    "BaseDNSRecordAddress",
    "BaseDNSRecordBinary",
    "ChangeDNSRecordBody",
    "DNSBalanceReleaseBody",
    "DNSRecordDNSNextResolver",
    "DNSRecordSite",
    "DNSRecordStorage",
    "DNSRecordText",
    "DNSRecordWallet",
    "DNSRecords",
    "RenewDNSBody",
    "TONDNSAuction",
    "TONDNSCollectionData",
    "TONDNSItemData",
]


class BaseDNSRecord(TlbScheme, abc.ABC):
    """Abstract base for DNS record types."""

    PREFIX: ClassVar[DNSPrefix]

    def __init__(self, value: Any) -> None:
        """Initialize BaseDNSRecord.

        :param value: Record value (type depends on subclass).
        """
        self.value = value

    @abc.abstractmethod
    def _build_cell(self) -> Cell:
        """Build Cell from record value."""

    @classmethod
    @abc.abstractmethod
    def _parse_cell(cls, cs: Slice) -> Any:
        """Parse record value from Slice."""

    def serialize(self) -> Cell:
        """Serialize to Cell."""
        return self._build_cell()

    @classmethod
    def deserialize(cls, cs: Slice) -> Any:
        """Deserialize from Slice."""
        return cls._parse_cell(cs)


class BaseDNSRecordAddress(BaseDNSRecord):
    """Base for DNS records containing TON addresses."""

    def __init__(self, value: Address | str) -> None:
        """Initialize BaseDNSRecordAddress.

        :param value: TON address.
        """
        if not isinstance(value, Address):
            value = Address(value)
        super().__init__(value)

    def _build_cell(self) -> Cell:
        cell = begin_cell()
        cell.store_uint(self.PREFIX, 16)
        cell.store_address(self.value)
        cell.store_uint(0, 8)
        return cell.end_cell()

    @classmethod
    def _parse_cell(cls, cs: Slice) -> BaseDNSRecordAddress:
        cs.skip_bits(16)
        addr = cs.load_address()
        if not isinstance(addr, Address):
            raise ValueError(f"Expected Address, got {type(addr).__name__}")
        return cls(addr)


class BaseDNSRecordBinary(BaseDNSRecord):
    """Base for DNS records containing binary data."""

    BINARY_CLS: ClassVar[type[Binary]]

    def __init__(self, value: Binary | BinaryLike) -> None:
        """Initialize BaseDNSRecordBinary.

        :param value: Binary data.
        """
        if not isinstance(value, Binary):
            value = self.__class__.BINARY_CLS(value)
        super().__init__(value)

    def _build_cell(self) -> Cell:
        cell = begin_cell()
        cell.store_uint(self.PREFIX, 16)
        cell.store_bytes(self.value.as_bytes)
        cell.store_uint(0, 8)
        return cell.end_cell()

    @classmethod
    def _parse_cell(cls, cs: Slice) -> BaseDNSRecordBinary:
        cs.skip_bits(16)
        return cls(cs.load_bytes(32))


class DNSRecordDNSNextResolver(BaseDNSRecordAddress):
    """DNS record pointing to next resolver contract."""

    PREFIX: ClassVar[DNSPrefix] = DNSPrefix.DNS_NEXT_RESOLVER

    def _build_cell(self) -> Cell:
        cell = begin_cell()
        cell.store_uint(self.PREFIX, 16)
        cell.store_address(self.value)
        return cell.end_cell()

    @classmethod
    def _parse_cell(cls, cs: Slice) -> DNSRecordDNSNextResolver:
        cs.skip_bits(16)
        addr = cs.load_address()
        if not isinstance(addr, Address):
            raise ValueError(f"Expected Address, got {type(addr).__name__}")
        return cls(addr)

    @classmethod
    def deserialize(cls, cs: Slice) -> DNSRecordDNSNextResolver:
        """Deserialize from Slice."""
        return cast("DNSRecordDNSNextResolver", super().deserialize(cs))


class DNSRecordWallet(BaseDNSRecordAddress):
    """DNS record pointing to wallet address."""

    PREFIX: ClassVar[DNSPrefix] = DNSPrefix.WALLET

    @classmethod
    def deserialize(cls, cs: Slice) -> DNSRecordWallet:
        """Deserialize from Slice."""
        return cast("DNSRecordWallet", super().deserialize(cs))


class DNSRecordStorage(BaseDNSRecordBinary):
    """DNS record pointing to TON Storage bag."""

    PREFIX: ClassVar[DNSPrefix] = DNSPrefix.STORAGE
    BINARY_CLS: ClassVar[type[BagID]] = BagID

    def _build_cell(self) -> Cell:
        cell = begin_cell()
        cell.store_uint(self.PREFIX, 16)
        cell.store_bytes(self.value.as_bytes)
        return cell.end_cell()

    @classmethod
    def _parse_cell(cls, cs: Slice) -> DNSRecordStorage:
        cs.skip_bits(16)
        return cls(cs.load_bytes(32))

    @classmethod
    def deserialize(cls, cs: Slice) -> DNSRecordStorage:
        """Deserialize from Slice."""
        return cast("DNSRecordStorage", super().deserialize(cs))


class DNSRecordSite(BaseDNSRecordBinary):
    """DNS record pointing to TON Site (ADNL address)."""

    PREFIX: ClassVar[DNSPrefix] = DNSPrefix.SITE
    BINARY_CLS: ClassVar[type[ADNL]] = ADNL

    @classmethod
    def deserialize(cls, cs: Slice) -> DNSRecordSite:
        """Deserialize from Slice."""
        return cast("DNSRecordSite", super().deserialize(cs))


class DNSRecordText(BaseDNSRecord):
    """DNS text record."""

    PREFIX: ClassVar[DNSPrefix] = DNSPrefix.TEXT

    def __init__(self, value: str) -> None:
        """Initialize DNSRecordText.

        :param value: Text content.
        """
        super().__init__(value)

    def _build_cell(self) -> Cell:
        cell = begin_cell()
        cell.store_uint(self.PREFIX, 16)
        cell.store_snake_string(self.value)
        return cell.end_cell()

    @classmethod
    def _parse_cell(cls, cs: Slice) -> DNSRecordText:
        cs.skip_bits(16)
        return cls(cs.load_snake_string())

    @classmethod
    def deserialize(cls, cs: Slice) -> DNSRecordText:
        """Deserialize from Slice."""
        return cast("DNSRecordText", super().deserialize(cs))


class DNSRecords(OnchainContent):
    """Collection of DNS records for a domain."""

    _DNS_RECORDS_CLASSES: ClassVar[dict[str, type[BaseDNSRecord]]] = {
        "dns_next_resolver": DNSRecordDNSNextResolver,
        "storage": DNSRecordStorage,
        "wallet": DNSRecordWallet,
        "site": DNSRecordSite,
        "text": DNSRecordText,
    }

    _DNS_CATEGORIES: ClassVar[dict[int, str]] = {
        DNSCategory.DNS_NEXT_RESOLVER: "dns_next_resolver",
        DNSCategory.STORAGE: "storage",
        DNSCategory.WALLET: "wallet",
        DNSCategory.SITE: "site",
        DNSCategory.TEXT: "text",
    }

    _DNS_KEYS: ClassVar[set[str]] = set(_DNS_RECORDS_CLASSES.keys())

    def __init__(self, data: dict[str | int, Any]) -> None:
        """Initialize DNSRecords.

        :param data: Record keys to values.
        """
        self.records: dict[str | int, BaseDNSRecord] = {}

        other: dict[str | int, Any] = {}

        for raw_key, val in data.items():
            if isinstance(raw_key, int) and raw_key in self._DNS_CATEGORIES:
                key: str = self._DNS_CATEGORIES[raw_key]
            elif isinstance(raw_key, str):
                key = raw_key
            else:
                other[raw_key] = val
                continue
            if key not in self._DNS_KEYS:
                other[raw_key] = val
                continue
            if not isinstance(val, BaseDNSRecord):
                record_cls = self._DNS_RECORDS_CLASSES[key]
                val = self._to_record(record_cls, val)
            self.records[key] = val

        super().__init__(other)

    @classmethod
    def _to_record(
        cls, record_cls: type[BaseDNSRecord], val: Any
    ) -> BaseDNSRecord:
        if isinstance(val, Cell):
            cs = val.begin_parse().load_ref().begin_parse()
            return cast("BaseDNSRecord", record_cls.deserialize(cs))
        return record_cls(val)

    def _build_hashmap(self) -> HashMap:
        hashmap = super()._build_hashmap()
        for key, val in self.records.items():
            if isinstance(key, str):
                key = string_hash(key)
            hashmap.set_int_key(key, val.serialize())
        return hashmap

    @classmethod
    def _parse_hashmap(
        cls,
        hashmap: dict[str | int, Cell],
    ) -> dict[str | int, Any]:
        hashmap = super()._parse_hashmap(hashmap)
        for key in cls._DNS_KEYS:
            int_key = string_hash(key)
            if int_key in hashmap:
                val = hashmap.pop(int_key)
                cs = val.begin_parse().load_ref().begin_parse()
                hashmap[key] = cls._DNS_RECORDS_CLASSES[key].deserialize(cs)
        return hashmap


class TONDNSAuction(TlbScheme):
    """Auction state for a TON DNS domain."""

    def __init__(
        self,
        max_bid_address: AddressLike | None,
        max_bid_amount: int,
        auction_end_time: int,
    ) -> None:
        """Initialize TONDNSAuction.

        :param max_bid_address: Highest bidder address.
        :param max_bid_amount: Highest bid in nanotons.
        :param auction_end_time: Auction end unix timestamp.
        """
        self.max_bid_address = max_bid_address
        self.max_bid_amount = max_bid_amount
        self.auction_end_time = auction_end_time

    def serialize(self) -> Cell:
        """Serialize to Cell."""
        cell = begin_cell()
        cell.store_address(self.max_bid_address)
        cell.store_coins(self.max_bid_amount)
        cell.store_uint(self.auction_end_time, 64)
        return cell.end_cell()

    @classmethod
    def deserialize(cls, cs: Slice) -> TONDNSAuction:
        """Deserialize from Slice."""
        return cls(
            max_bid_address=_load_std_address(cs),
            max_bid_amount=cs.load_coins() or 0,
            auction_end_time=cs.load_uint(64),
        )


class TONDNSCollectionData(TlbScheme):
    """On-chain data for TON DNS collection contract."""

    def __init__(
        self,
        content: OffchainContent,
        nft_item_code: Cell,
    ) -> None:
        """Initialize TONDNSCollectionData.

        :param content: Off-chain collection metadata.
        :param nft_item_code: Code cell for DNS item contracts.
        """
        self.content = content
        self.nft_item_code = nft_item_code

    def serialize(self) -> Cell:
        """Serialize to Cell."""
        cell = begin_cell()
        cell.store_ref(self.content.serialize(True))
        cell.store_ref(self.nft_item_code)
        return cell.end_cell()

    @classmethod
    def deserialize(cls, cs: Slice) -> TONDNSCollectionData:
        """Deserialize from Slice."""
        return cls(
            content=OffchainContent.deserialize(cs.load_ref().begin_parse(), True),
            nft_item_code=cs.load_ref(),
        )


class TONDNSItemData(TlbScheme):
    """On-chain data for TON DNS item (domain) contract."""

    def __init__(
        self,
        index: int,
        collection_address: AddressLike | None,
        owner_address: AddressLike | None,
        content: OnchainContent,
        domain: str,
        last_fill_up_time: int,
        auction: TONDNSAuction | None = None,
    ) -> None:
        """Initialize TONDNSItemData.

        :param index: Item index within collection.
        :param collection_address: Parent collection address.
        :param owner_address: Current domain owner address.
        :param content: On-chain DNS records and metadata.
        :param domain: Domain name string.
        :param last_fill_up_time: Last renewal unix timestamp.
        :param auction: Active auction state, or None.
        """
        self.index = index
        self.collection_address = collection_address
        self.owner_address = owner_address
        self.content = content
        self.domain = domain
        self.auction = auction
        self.last_fill_up_time = last_fill_up_time

    def serialize(self) -> Cell:
        """Serialize to Cell."""
        cell = begin_cell()
        cell.store_uint(self.index, 256)
        cell.store_address(self.collection_address)
        cell.store_address(self.owner_address)
        cell.store_ref(self.content.serialize(True))
        cell.store_ref(begin_cell().store_snake_string(self.domain).end_cell())
        cell.store_dict(self.auction.serialize() if self.auction else None)
        cell.store_uint(self.last_fill_up_time, 64)
        return cell.end_cell()

    @classmethod
    def deserialize(cls, cs: Slice) -> TONDNSItemData:
        """Deserialize from Slice."""
        return cls(
            index=cs.load_uint(256),
            collection_address=_load_std_address(cs),
            owner_address=_load_std_address(cs),
            content=OnchainContent.deserialize(cs.load_ref().begin_parse(), True),
            domain=cs.load_ref().begin_parse().load_snake_string(),
            auction=(
                TONDNSAuction.deserialize(auction_cell.begin_parse())
                if (auction_cell := cs.load_maybe_ref()) is not None
                else None
            ),
            last_fill_up_time=cs.load_uint(64),
        )


class ChangeDNSRecordBody(TlbScheme):
    """Message body for changing a DNS record."""

    def __init__(
        self,
        category: DNSCategory,
        record: DNSRecordDNSNextResolver | DNSRecordSite | DNSRecordStorage | DNSRecordWallet | None = None,
        query_id: int = 0,
    ) -> None:
        """Initialize ChangeDNSRecordBody.

        :param category: DNS record category to change.
        :param record: New record value, or None to delete.
        :param query_id: Query identifier.
        """
        self.query_id = query_id
        self.category = category
        self.record = record

    def serialize(self) -> Cell:
        """Serialize to Cell."""
        cell = begin_cell()
        cell.store_uint(OpCode.CHANGE_DNS_RECORD, 32)
        cell.store_uint(self.query_id, 64)
        cell.store_uint(self.category.value, 256)
        if self.record is not None:
            cell.store_ref(self.record.serialize())
        return cell.end_cell()

    @classmethod
    def deserialize(cls, cs: Slice) -> ChangeDNSRecordBody:
        """Deserialize from Slice."""
        cs.skip_bits(32)
        query_id = cs.load_uint(64)
        category_value = cs.load_uint(256)
        record = None
        if cs.remaining_refs > 0:
            record_cs = cs.load_ref().begin_parse()
            prefix = record_cs.preload_uint(16)
            record_map: dict[int, type[BaseDNSRecord]] = {
                DNSPrefix.DNS_NEXT_RESOLVER: DNSRecordDNSNextResolver,
                DNSPrefix.WALLET: DNSRecordWallet,
                DNSPrefix.STORAGE: DNSRecordStorage,
                DNSPrefix.SITE: DNSRecordSite,
                DNSPrefix.TEXT: DNSRecordText,
            }
            record_cls = record_map.get(prefix)
            if record_cls is not None:
                record = record_cls.deserialize(record_cs)
        return cls(
            query_id=query_id,
            category=DNSCategory(category_value),
            record=record,
        )


class RenewDNSBody(TlbScheme):
    """Message body for renewing a DNS domain (change_dns_record with category=0 and no value)."""

    def __init__(self, query_id: int = 0) -> None:
        """Initialize RenewDNSBody.

        :param query_id: Query identifier.
        """
        self.query_id = query_id

    def serialize(self) -> Cell:
        """Serialize to Cell."""
        cell = begin_cell()
        cell.store_uint(OpCode.CHANGE_DNS_RECORD, 32)
        cell.store_uint(self.query_id, 64)
        cell.store_uint(0, 256)
        return cell.end_cell()

    @classmethod
    def deserialize(cls, cs: Slice) -> RenewDNSBody:
        """Deserialize from Slice."""
        cs.skip_bits(32)
        query_id = cs.load_uint(64)
        cs.skip_bits(256)
        return cls(query_id=query_id)


class DNSBalanceReleaseBody(TlbScheme):
    """Message body for releasing DNS domain balance."""

    def __init__(self, query_id: int = 0) -> None:
        """Initialize DNSBalanceReleaseBody.

        :param query_id: Query identifier.
        """
        self.query_id = query_id

    def serialize(self) -> Cell:
        """Serialize to Cell."""
        cell = begin_cell()
        cell.store_uint(OpCode.DNS_BALANCE_RELEASE, 32)
        cell.store_uint(self.query_id, 64)
        return cell.end_cell()

    @classmethod
    def deserialize(cls, cs: Slice) -> DNSBalanceReleaseBody:
        """Deserialize from Slice."""
        cs.skip_bits(32)
        return cls(query_id=cs.load_uint(64))

