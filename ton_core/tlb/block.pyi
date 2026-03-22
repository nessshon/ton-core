import builtins
from typing import Any

from ton_core.boc.cell import Cell
from ton_core.boc.slice import Slice
from ton_core.tlb.tlb import TlbError, TlbScheme
from ton_core.tlb.utils import MerkleUpdate

class BinTree(TlbScheme):
    list: builtins.list[Any]
    def __init__(self, list_: builtins.list[Any]) -> None: ...
    @classmethod
    def serialize(cls, *args: object) -> None: ...
    @classmethod
    def deserialize(cls, cell_slice: Slice) -> BinTree: ...

class BlkMasterInfo(TlbScheme):
    master: ExtBlkRef
    def __init__(self, master: ExtBlkRef) -> None: ...
    @classmethod
    def serialize(cls, *args: object) -> None: ...
    @classmethod
    def deserialize(cls, cell_slice: Slice) -> BlkMasterInfo: ...

class BlkPrevInfo(TlbScheme):
    type_: str
    prev: ExtBlkRef
    prev1: ExtBlkRef
    prev2: ExtBlkRef
    def __init__(self, type_: str, **kwargs: object) -> None: ...
    def serialize(self, *args: object) -> None: ...
    @classmethod
    def deserialize(cls, cell_slice: Slice, after_merge: int) -> BlkPrevInfo: ...

class Block(TlbScheme):
    global_id: int
    info: BlockInfo
    value_flow: ValueFlow
    state_update: MerkleUpdate
    extra: BlockExtra
    def __init__(self, global_id: int, info: BlockInfo, value_flow: ValueFlow, state_update: MerkleUpdate, extra: BlockExtra) -> None: ...
    @classmethod
    def serialize(cls, *args: object) -> None: ...
    @classmethod
    def deserialize(cls, cell_slice: Slice) -> Block: ...

class BlockCreateStats(TlbScheme):
    type_: str
    counters: builtins.dict[Any, Any]
    def __init__(self, type_: str, counters: builtins.dict[Any, Any]) -> None: ...
    @classmethod
    def serialize(cls, *args: object) -> None: ...
    @classmethod
    def deserialize(cls, cell_slice: Slice) -> BlockCreateStats: ...

class BlockError(TlbError): ...

class BlockExtra(TlbScheme):
    in_msg_descr: tuple[builtins.dict[Any, Any], builtins.list[Any]]
    out_msg_descr: tuple[builtins.dict[Any, Any], builtins.list[Any]]
    account_blocks: tuple[builtins.dict[Any, Any], builtins.list[Any]]
    rand_seed: bytes
    created_by: bytes
    custom: McBlockExtra | None
    def __init__(self, in_msg_descr: tuple[builtins.dict[Any, Any], builtins.list[Any]], out_msg_descr: tuple[builtins.dict[Any, Any], builtins.list[Any]], account_blocks: tuple[builtins.dict[Any, Any], builtins.list[Any]], rand_seed: bytes, created_by: bytes, custom: McBlockExtra | None) -> None: ...
    @classmethod
    def serialize(cls, *args: object) -> None: ...
    @classmethod
    def deserialize(cls, cell_slice: Slice) -> BlockExtra | None: ...

class BlockInfo(TlbScheme):
    version: int
    not_master: int
    after_merge: int
    before_split: int
    after_split: int
    want_split: bool
    want_merge: bool
    key_block: bool
    vert_seqno_incr: int
    flags: int
    seqno: int
    vert_seqno: int
    shard: ShardIdent
    gen_utime: int
    start_lt: int
    end_lt: int
    gen_validator_list_hash_short: int
    gen_catchain_seqno: int
    min_ref_mc_seqno: int
    prev_key_block_seqno: int
    gen_software: GlobalVersion | None
    master_ref: BlkMasterInfo | None
    prev_ref: BlkPrevInfo
    prev_vert_ref: BlkPrevInfo | None
    def __init__(self, cell_slice: Slice) -> None: ...
    def serialize(self, *args: object) -> None: ...
    @classmethod
    def deserialize(cls, cell_slice: Slice) -> BlockInfo | None: ...

class ConfigParams(TlbScheme):
    config_addr: str
    config: builtins.dict[Any, Any]
    def __init__(self, config_addr: str, config: builtins.dict[Any, Any]) -> None: ...
    @classmethod
    def serialize(cls, *args: object) -> None: ...
    @classmethod
    def deserialize(cls, cell_slice: Slice) -> ConfigParams: ...

class Counters(TlbScheme):
    last_updated: int
    total: int
    cnt2048: int
    cnt65536: int
    def __init__(self, last_updated: int, total: int, cnt2048: int, cnt65536: int) -> None: ...
    @classmethod
    def serialize(cls, *args: object) -> None: ...
    @classmethod
    def deserialize(cls, cell_slice: Slice) -> Counters: ...

class CreatorStats(TlbScheme):
    mc_blocks: Counters
    shard_blocks: Counters
    def __init__(self, mc_blocks: Counters, shard_blocks: Counters) -> None: ...
    @classmethod
    def serialize(cls, *args: object) -> None: ...
    @classmethod
    def deserialize(cls, cell_slice: Slice) -> CreatorStats: ...

class CurrencyCollection(TlbScheme):
    grams: int
    other: ExtraCurrencyCollection
    def __init__(self, grams: int, other: ExtraCurrencyCollection | None = ...) -> None: ...
    def serialize(self) -> Cell: ...
    @classmethod
    def deserialize(cls, cell_slice: Slice) -> CurrencyCollection: ...

class DepthBalanceInfo(TlbScheme):
    split_depth: int
    balance: CurrencyCollection
    def __init__(self, split_depth: int, balance: CurrencyCollection) -> None: ...
    @classmethod
    def serialize(cls, *args: object) -> None: ...
    @classmethod
    def deserialize(cls, cell_slice: Slice) -> DepthBalanceInfo: ...

class ExtBlkRef(TlbScheme):
    end_lt: int
    seqno: int
    root_hash: bytes
    file_hash: bytes
    def __init__(self, cell_slice: Slice) -> None: ...
    @classmethod
    def serialize(cls, *args: object) -> None: ...
    @classmethod
    def deserialize(cls, cell_slice: Slice) -> ExtBlkRef: ...

class ExtraCurrencyCollection(TlbScheme):
    dict: builtins.dict[Any, Any] | None
    def __init__(self, dict_: builtins.dict[Any, Any]) -> None: ...
    def serialize(self) -> Cell: ...
    @classmethod
    def deserialize(cls, cell_slice: Slice) -> ExtraCurrencyCollection: ...

class FutureSplitMerge(TlbScheme):
    type_: str
    def __init__(self, type_: str, **kwargs: object) -> None: ...
    @classmethod
    def serialize(cls, *args: object) -> None: ...
    @classmethod
    def deserialize(cls, cell_slice: Slice) -> FutureSplitMerge | None: ...

class GlobalVersion(TlbScheme):
    version: int
    capabilities: int
    def __init__(self, version: int, capabilities: int) -> None: ...
    @classmethod
    def serialize(cls, *args: object) -> None: ...
    @classmethod
    def deserialize(cls, cell_slice: Slice) -> GlobalVersion: ...

class KeyExtBlkRef(TlbScheme):
    key: bool
    blk_ref: ExtBlkRef
    def __init__(self, key: bool, blk_ref: ExtBlkRef) -> None: ...
    @classmethod
    def serialize(cls, *args: object) -> None: ...
    @classmethod
    def deserialize(cls, cell_slice: Slice) -> KeyExtBlkRef: ...

class KeyMaxLt(TlbScheme):
    key: bool
    max_end_lt: int
    def __init__(self, key: bool, max_end_lt: int) -> None: ...
    @classmethod
    def serialize(cls, *args: object) -> None: ...
    @classmethod
    def deserialize(cls, cell_slice: Slice) -> KeyMaxLt: ...

class McBlockExtra(TlbScheme):
    key_block: int
    shard_hashes: builtins.dict[Any, Any]
    shard_fees: Cell | None
    prev_blk_signatures: builtins.dict[Any, Any]
    recover_create_msg: Cell | None
    mint_msg: Cell | None
    config: ConfigParams | None
    def __init__(self, key_block: int, shard_hashes: builtins.dict[Any, Any], shard_fees: Cell | None, prev_blk_signatures: builtins.dict[Any, Any], recover_create_msg: Cell | None, mint_msg: Cell | None, config: ConfigParams | None) -> None: ...
    @classmethod
    def serialize(cls, *args: object) -> None: ...
    @classmethod
    def deserialize(cls, cell_slice: Slice) -> McBlockExtra | None: ...

class McStateExtra(TlbScheme):
    shard_hashes: builtins.dict[Any, Any]
    config: ConfigParams
    flags: int
    validator_info: ValidatorInfo
    prev_blocks: OldMcBlocksInfo
    after_key_block: bool
    last_key_block: ExtBlkRef | None
    block_create_stats: BlockCreateStats | None
    global_balance: CurrencyCollection
    def __init__(self, shard_hashes: builtins.dict[Any, Any], config: ConfigParams, flags: int, validator_info: ValidatorInfo, prev_blocks: OldMcBlocksInfo, after_key_block: bool, last_key_block: ExtBlkRef | None, block_create_stats: BlockCreateStats | None, global_balance: CurrencyCollection) -> None: ...
    @classmethod
    def serialize(cls, *args: object) -> None: ...
    @classmethod
    def deserialize(cls, cell_slice: Slice) -> McStateExtra | None: ...

class OldMcBlocksInfo(TlbScheme):
    @classmethod
    def serialize(cls, *args: object) -> None: ...
    @classmethod
    def deserialize(cls, cell_slice: Slice) -> object: ...

class OutMsgQueue(TlbScheme):
    @classmethod
    def serialize(cls, *args: object) -> None: ...
    @classmethod
    def deserialize(cls, *args: object) -> None: ...

class OutMsgQueueInfo(TlbScheme):
    @classmethod
    def serialize(cls, *args: object) -> None: ...
    @classmethod
    def deserialize(cls, *args: object) -> None: ...

class ShardAccounts(TlbScheme):
    def serialize(self, *args: object) -> None: ...
    @classmethod
    def deserialize(cls, cell_slice: Slice) -> tuple[builtins.dict[Any, Any], builtins.list[Any]]: ...

class ShardDescr(TlbScheme):
    seq_no: int
    reg_mc_seqno: int
    start_lt: int
    end_lt: int
    root_hash: bytes
    file_hash: bytes
    before_split: bool
    before_merge: bool
    want_split: bool
    want_merge: bool
    nx_cc_updated: bool
    flags: int
    next_catchain_seqno: int
    next_validator_shard: int
    next_validator_shard_signed: int
    min_ref_mc_seqno: int
    gen_utime: int
    split_merge_at: FutureSplitMerge | None
    fees_collected: CurrencyCollection
    funds_created: CurrencyCollection
    def __init__(self, seq_no: int, reg_mc_seqno: int, start_lt: int, end_lt: int, root_hash: bytes, file_hash: bytes, before_split: bool, before_merge: bool, want_split: bool, want_merge: bool, nx_cc_updated: bool, flags: int, next_catchain_seqno: int, next_validator_shard: int, min_ref_mc_seqno: int, gen_utime: int, split_merge_at: FutureSplitMerge | None, fees_collected: CurrencyCollection, funds_created: CurrencyCollection) -> None: ...
    @classmethod
    def serialize(cls, *args: object) -> None: ...
    @classmethod
    def deserialize(cls, cell_slice: Slice) -> ShardDescr: ...

class ShardIdent(TlbScheme):
    shard_pfx_bits: int
    workchain_id: int
    shard_prefix: int
    def __init__(self, shard_pfx_bits: int, workchain_id: int, shard_prefix: int) -> None: ...
    def serialize(self, *args: object) -> None: ...
    @classmethod
    def deserialize(cls, cell_slice: Slice) -> ShardIdent: ...
    def calculate_shard(self) -> int: ...
    def calculate_shard_signed(self) -> int: ...

class ShardState(TlbScheme):
    type_: str
    def __init__(self, type_: str, **kwargs: object) -> None: ...
    @classmethod
    def serialize(cls, *args: object) -> None: ...
    @classmethod
    def deserialize(cls, cell_slice: Slice) -> ShardState: ...

class ShardStateUnsplit(TlbScheme):
    global_id: int
    shard_id: ShardIdent
    seq_no: int
    vert_seq_no: int
    gen_utime: int
    gen_lt: int
    min_ref_mc_seqno: int
    out_msg_queue_info: Cell
    before_split: int
    accounts: ShardAccounts
    overload_history: int | None
    underload_history: int | None
    total_balance: CurrencyCollection | None
    total_validator_fees: CurrencyCollection | None
    libraries: builtins.dict[Any, Any] | None
    master_ref: BlkMasterInfo | None
    custom: McStateExtra | None
    def __init__(self, global_id: int, shard_id: ShardIdent, seq_no: int, vert_seq_no: int, gen_utime: int, gen_lt: int, min_ref_mc_seqno: int, out_msg_queue_info: Cell, before_split: int, accounts: ShardAccounts, overload_history: int | None, underload_history: int | None, total_balance: CurrencyCollection | None, total_validator_fees: CurrencyCollection | None, libraries: builtins.dict[Any, Any] | None, master_ref: BlkMasterInfo | None, custom: McStateExtra | None) -> None: ...
    @classmethod
    def serialize(cls, *args: object) -> None: ...
    @classmethod
    def deserialize(cls, cell_slice: Slice) -> ShardStateUnsplit | None: ...

class ValidatorInfo(TlbScheme):
    validator_list_hash_short: int
    catchain_seqno: int
    nx_cc_updated: bool
    def __init__(self, validator_list_hash_short: int, catchain_seqno: int, nx_cc_updated: bool) -> None: ...
    @classmethod
    def serialize(cls, *args: object) -> None: ...
    @classmethod
    def deserialize(cls, cell_slice: Slice) -> ValidatorInfo: ...

class ValueFlow(TlbScheme):
    type_: str
    from_prev_blk: CurrencyCollection
    to_next_blk: CurrencyCollection
    imported: CurrencyCollection
    exported: CurrencyCollection
    fees_collected: CurrencyCollection
    fees_imported: CurrencyCollection
    recovered: CurrencyCollection
    created: CurrencyCollection
    minted: CurrencyCollection
    burned: CurrencyCollection
    def __init__(self, type_: str, **kwargs: object) -> None: ...
    @classmethod
    def serialize(cls, *args: object) -> None: ...
    @classmethod
    def deserialize(cls, cell_slice: Slice) -> ValueFlow | None: ...
