from ton_core.boc.address import Address
from ton_core.boc.cell import Cell
from ton_core.tl.block import BlockIdExt
from ton_core.tlb.account import ShardAccount
from ton_core.tlb.block import ShardDescr
from ton_core.tlb.config import CatchainConfig, ValidatorDescr, ValidatorSet

class ProofError(Exception): ...

def calculate_node_id_short(pub_key: bytes) -> bytes: ...
def check_proof(cell: Cell, hash_: bytes) -> None: ...
def check_block_header_proof(
    root_cell: Cell,
    block_hash: bytes,
    store_state_hash: bool = ...,
) -> bytes | None: ...
def check_shard_proof(
    shard_proof: bytes,
    blk: BlockIdExt,
    shrd_blk: BlockIdExt,
) -> ShardDescr | None: ...
def check_account_proof(
    proof: bytes,
    shrd_blk: BlockIdExt,
    address: Address,
    account_state_root: Cell,
    return_account_descr: bool = ...,
) -> ShardAccount | None: ...
def check_block_signatures(
    nodes: list[ValidatorDescr],
    signatures: list[dict[str, object]],
    blk: BlockIdExt,
) -> None: ...
def compute_validator_set(
    ccv_conf: CatchainConfig,
    blk: BlockIdExt,
    vset: ValidatorSet,
    cc_seqno: int | None = ...,
) -> list[ValidatorDescr]: ...
