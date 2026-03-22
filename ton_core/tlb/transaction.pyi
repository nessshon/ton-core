from ton_core.boc.address import Address
from ton_core.boc.cell import Cell
from ton_core.boc.slice import Slice
from ton_core.tlb.account import AccountStatus, StateInit, StorageUsedShort
from ton_core.tlb.block import CurrencyCollection
from ton_core.tlb.tlb import TlbError, TlbScheme
from ton_core.tlb.utils import HashUpdate

class AccStatusChange(TlbScheme):
    type_: str
    def __init__(self, type_: str) -> None: ...
    @classmethod
    def deserialize(cls, cell_slice: Slice) -> AccStatusChange: ...

class CommonMsgInfo(TlbScheme):
    def __init__(self) -> None: ...
    @classmethod
    def deserialize(cls, cell_slice: Slice) -> InternalMsgInfo | ExternalMsgInfo | ExternalOutMsgInfo: ...

class ComputeSkipReason(TlbScheme):
    type_: str
    def __init__(self, type_: str) -> None: ...
    @classmethod
    def deserialize(cls, cell_slice: Slice) -> ComputeSkipReason: ...

class ExternalMsgInfo(CommonMsgInfo):
    src: Address | None
    dest: Address | None
    import_fee: int
    def __init__(self, src: Address | None, dest: Address | None, import_fee: int) -> None: ...
    def serialize(self) -> Cell: ...
    @classmethod
    def deserialize(cls, cell_slice: Slice) -> ExternalMsgInfo: ...

class ExternalOutMsgInfo(CommonMsgInfo):
    src: Address
    dest: Address
    created_lt: int
    created_at: int
    def __init__(self, src: Address, dest: Address, created_lt: int, created_at: int) -> None: ...
    def serialize(self) -> Cell: ...
    @classmethod
    def deserialize(cls, cell_slice: Slice) -> ExternalOutMsgInfo: ...

class ImportFees(TlbScheme):
    fees_collected: int
    value_imported: CurrencyCollection
    def __init__(self, fees_collected: int, value_imported: CurrencyCollection) -> None: ...
    @classmethod
    def deserialize(cls, cell_slice: Slice) -> ImportFees: ...

class InMsg(TlbScheme):
    type_: str
    msg: MessageAny | None
    in_msg: MsgEnvelope | None
    transaction: Transaction | None
    def __init__(self, type_: str, msg: MessageAny | None = ..., in_msg: MsgEnvelope | None = ..., transaction: Transaction | None = ..., **kwargs: object) -> None: ...
    @classmethod
    def deserialize(cls, cell_slice: Slice) -> InMsg: ...

class IntermediateAddress(TlbScheme):
    type_: str
    use_dest_bits: int | None
    workchain_id: int | None
    addr_pfx: int | None
    def __init__(self, type_: str, use_dest_bits: int | None = ..., workchain_id: int | None = ..., addr_pfx: int | None = ...) -> None: ...
    @classmethod
    def deserialize(cls, cell_slice: Slice) -> IntermediateAddress: ...

class InternalMsgInfo(CommonMsgInfo):
    ihr_disabled: bool
    bounce: bool
    bounced: bool
    src: Address
    dest: Address
    value: CurrencyCollection
    value_coins: int
    ihr_fee: int
    fwd_fee: int
    created_lt: int
    created_at: int
    def __init__(self, ihr_disabled: bool | None, bounce: bool | None, bounced: bool | None, src: Address | None, dest: Address | None, value: CurrencyCollection, ihr_fee: int, fwd_fee: int, created_lt: int, created_at: int) -> None: ...
    def serialize(self) -> Cell: ...
    @classmethod
    def deserialize(cls, cell_slice: Slice) -> InternalMsgInfo: ...

class LibRef(TlbScheme):
    type_: str
    lib_hash: bytes | None
    library: Cell | None
    def __init__(self, type_: str, lib_hash: bytes | None = ..., library: Cell | None = ...) -> None: ...
    def serialize(self, *args: object) -> object: ...
    @classmethod
    def deserialize(cls, cell_slice: Slice) -> LibRef: ...

class MessageAny(TlbScheme):
    info: InternalMsgInfo | ExternalMsgInfo | ExternalOutMsgInfo
    init: StateInit | None
    body: Cell
    def __init__(self, info: InternalMsgInfo | ExternalMsgInfo | ExternalOutMsgInfo, init: StateInit | None, body: Cell) -> None: ...
    @property
    def is_external(self) -> bool: ...
    @property
    def is_internal(self) -> bool: ...
    @property
    def is_external_out(self) -> bool: ...
    def serialize(self) -> Cell: ...
    @classmethod
    def deserialize(cls, cell_slice: Slice) -> MessageAny: ...

class MsgEnvelope(TlbScheme):
    type_: str
    cur_addr: IntermediateAddress
    next_addr: IntermediateAddress
    fwd_fee_remaining: int
    msg: MessageAny
    emitted_lt: int | None
    metadata: MsgMetadata | None
    def __init__(self, type_: str, cur_addr: IntermediateAddress, next_addr: IntermediateAddress, fwd_fee_remaining: int, msg: MessageAny, emitted_lt: int | None = ..., metadata: MsgMetadata | None = ...) -> None: ...
    @classmethod
    def deserialize(cls, cell_slice: Slice) -> MsgEnvelope: ...

class MsgMetadata(TlbScheme):
    depth: int
    initiator_addr: Address
    initiator_lt: int
    def __init__(self, depth: int, initiator_addr: Address, initiator_lt: int) -> None: ...
    @classmethod
    def deserialize(cls, cell_slice: Slice) -> MsgMetadata: ...

class OutAction(TlbScheme):
    type_: str
    mode: int | None
    out_msg: MessageAny | None
    new_code: Cell | None
    currency: CurrencyCollection | None
    libref: LibRef | None
    def __init__(self, type_: str, mode: int | None = ..., out_msg: MessageAny | None = ..., new_code: Cell | None = ..., currency: CurrencyCollection | None = ..., libref: LibRef | None = ...) -> None: ...
    def serialize(self, *args: object) -> object: ...
    @classmethod
    def deserialize(cls, cell_slice: Slice) -> OutAction: ...

class OutList(TlbScheme):
    type_: str
    actions: list[OutAction]
    def __init__(self, type_: str, actions: list[OutAction] | None = ...) -> None: ...
    def serialize(self, *args: object) -> object: ...
    @classmethod
    def deserialize(cls, cell_slice: Slice) -> list[OutAction]: ...

class OutMsg(TlbScheme):
    type_: str
    msg: MessageAny | None
    out_msg: MsgEnvelope | None
    transaction: Transaction | None
    def __init__(self, type_: str, msg: MessageAny | None = ..., out_msg: MsgEnvelope | None = ..., transaction: Transaction | None = ..., **kwargs: object) -> None: ...
    @classmethod
    def deserialize(cls, cell_slice: Slice) -> OutMsg: ...

class SplitMergeInfo(TlbScheme):
    cur_shard_pfx_len: int
    acc_split_depth: int
    this_addr: str
    sibling_addr: str
    def __init__(self, cur_shard_pfx_len: int, acc_split_depth: int, this_addr: bytes, sibling_addr: bytes) -> None: ...
    @classmethod
    def deserialize(cls, cell_slice: Slice) -> SplitMergeInfo: ...

class TrActionPhase(TlbScheme):
    success: bool
    valid: bool
    no_funds: bool
    status_change: AccStatusChange
    total_fwd_fees: int | None
    total_action_fees: int | None
    result_code: int
    result_arg: int | None
    tot_actions: int
    spec_actions: int
    skipped_actions: int
    msgs_created: int
    action_list_hash: bytes
    tot_msg_size: StorageUsedShort
    def __init__(self, success: bool, valid: bool, no_funds: bool, status_change: AccStatusChange, total_fwd_fees: int | None, total_action_fees: int | None, result_code: int, result_arg: int | None, tot_actions: int, spec_actions: int, skipped_actions: int, msgs_created: int, action_list_hash: bytes, tot_msg_size: StorageUsedShort) -> None: ...
    @classmethod
    def deserialize(cls, cell_slice: Slice) -> TrActionPhase: ...

class TrBouncePhase(TlbScheme):
    type_: str
    msg_size: StorageUsedShort | None
    req_fwd_fees: int | None
    msg_fees: int | None
    fwd_fees: int | None
    def __init__(self, type_: str, msg_size: StorageUsedShort | None = ..., req_fwd_fees: int | None = ..., msg_fees: int | None = ..., fwd_fees: int | None = ...) -> None: ...
    @classmethod
    def deserialize(cls, cell_slice: Slice) -> TrBouncePhase: ...

class TrComputePhase(TlbScheme):
    type_: str
    reason: ComputeSkipReason | None
    success: bool | None
    msg_state_used: bool | None
    account_activated: bool | None
    gas_fees: int | None
    gas_used: int | None
    gas_limit: int | None
    gas_credit: int | None
    mode: int | None
    exit_code: int | None
    exit_arg: int | None
    vm_steps: int | None
    vm_init_state_hash: bytes | None
    vm_final_state_hash: bytes | None
    def __init__(self, type_: str, reason: ComputeSkipReason | None = ..., success: bool | None = ..., msg_state_used: bool | None = ..., account_activated: bool | None = ..., gas_fees: int | None = ..., gas_used: int | None = ..., gas_limit: int | None = ..., gas_credit: int | None = ..., mode: int | None = ..., exit_code: int | None = ..., exit_arg: int | None = ..., vm_steps: int | None = ..., vm_init_state_hash: bytes | None = ..., vm_final_state_hash: bytes | None = ...) -> None: ...
    @classmethod
    def deserialize(cls, cell_slice: Slice) -> TrComputePhase: ...

class TrCreditPhase(TlbScheme):
    due_fees_collected: int | None
    credit: CurrencyCollection
    def __init__(self, due_fees_collected: int | None, credit: CurrencyCollection) -> None: ...
    @classmethod
    def deserialize(cls, cell_slice: Slice) -> TrCreditPhase: ...

class TrStoragePhase(TlbScheme):
    storage_fees_collected: int
    storage_fees_due: int | None
    status_change: AccStatusChange
    def __init__(self, storage_fees_collected: int, storage_fees_due: int | None, status_change: AccStatusChange) -> None: ...
    @classmethod
    def deserialize(cls, cell_slice: Slice) -> TrStoragePhase: ...

class Transaction(TlbScheme):
    account_addr: bytes
    account_addr_hex: str
    lt: int
    prev_trans_hash: bytes
    prev_trans_lt: int
    now: int
    outmsg_cnt: int
    orig_status: AccountStatus
    end_status: AccountStatus
    in_msg: MessageAny | None
    out_msgs: list[MessageAny]
    total_fees: CurrencyCollection
    state_update: HashUpdate
    description: TransactionOrdinary | TransactionStorage | TransactionTickTock | TransactionSplitPrepare | TransactionSplitInstall | TransactionMergePrepare | TransactionMergeInstall
    cell: Cell
    def __init__(self, account_addr: bytes, lt: int, prev_trans_hash: bytes, prev_trans_lt: int, now: int, outmsg_cnt: int, orig_status: AccountStatus, end_status: AccountStatus, in_msg: MessageAny | None, out_msgs: list[MessageAny], total_fees: CurrencyCollection, state_update: HashUpdate, description: TransactionDescr, cell: Cell | None = ...) -> None: ...
    def serialize(self) -> Cell: ...
    @classmethod
    def deserialize(cls, cell_slice: Slice) -> Transaction | Cell: ...

class TransactionDescr(TlbScheme):
    def __init__(self) -> None: ...
    @classmethod
    def deserialize(cls, cell_slice: Slice) -> TransactionOrdinary | TransactionStorage | TransactionTickTock | TransactionSplitPrepare | TransactionSplitInstall | TransactionMergePrepare | TransactionMergeInstall: ...

class TransactionError(TlbError): ...

class TransactionMergeInstall(TlbScheme):
    type_: str
    split_info: SplitMergeInfo
    prepare_transaction: Transaction
    storage_ph: TrStoragePhase | None
    credit_ph: TrCreditPhase | None
    compute_ph: TrComputePhase
    action: TrActionPhase | None
    aborted: bool
    destroyed: bool
    def __init__(self, split_info: SplitMergeInfo, prepare_transaction: Transaction, storage_ph: TrStoragePhase | None, credit_ph: TrCreditPhase | None, compute_ph: TrComputePhase, action: TrActionPhase | None, aborted: bool, destroyed: bool) -> None: ...
    @classmethod
    def deserialize(cls, cell_slice: Slice) -> TransactionMergeInstall: ...

class TransactionMergePrepare(TlbScheme):
    type_: str
    split_info: SplitMergeInfo
    storage_ph: TrStoragePhase
    aborted: bool
    def __init__(self, split_info: SplitMergeInfo, storage_ph: TrStoragePhase, aborted: bool) -> None: ...
    @classmethod
    def deserialize(cls, cell_slice: Slice) -> TransactionMergePrepare: ...

class TransactionOrdinary(TlbScheme):
    type_: str
    credit_first: bool
    storage_ph: TrStoragePhase | None
    credit_ph: TrCreditPhase | None
    compute_ph: TrComputePhase
    action: TrActionPhase | None
    aborted: bool
    bounce: TrBouncePhase | None
    destroyed: bool
    def __init__(self, credit_first: bool, storage_ph: TrStoragePhase | None, credit_ph: TrCreditPhase | None, compute_ph: TrComputePhase | None, action: TrActionPhase | None, aborted: bool, bounce: TrBouncePhase | None, destroyed: bool) -> None: ...
    def serialize(self, *args: object) -> object: ...
    @classmethod
    def deserialize(cls, cell_slice: Slice) -> TransactionOrdinary: ...

class TransactionSplitInstall(TlbScheme):
    type_: str
    split_info: SplitMergeInfo
    prepare_transaction: Transaction
    installed: bool
    def __init__(self, split_info: SplitMergeInfo, prepare_transaction: Transaction, installed: bool) -> None: ...
    @classmethod
    def deserialize(cls, cell_slice: Slice) -> TransactionSplitInstall: ...

class TransactionSplitPrepare(TlbScheme):
    type_: str
    split_info: SplitMergeInfo
    storage_ph: TrStoragePhase | None
    compute_ph: TrComputePhase
    action: TrActionPhase | None
    aborted: bool
    destroyed: bool
    def __init__(self, split_info: SplitMergeInfo, storage_ph: TrStoragePhase | None, compute_ph: TrComputePhase, action: TrActionPhase | None, aborted: bool, destroyed: bool) -> None: ...
    @classmethod
    def deserialize(cls, cell_slice: Slice) -> TransactionSplitPrepare: ...

class TransactionStorage(TlbScheme):
    type_: str
    storage_ph: TrStoragePhase
    def __init__(self, storage_ph: TrStoragePhase) -> None: ...
    @classmethod
    def deserialize(cls, cell_slice: Slice) -> TransactionStorage: ...

class TransactionTickTock(TlbScheme):
    type_: str
    is_tock: bool
    storage_ph: TrStoragePhase
    compute_ph: TrComputePhase
    action: TrActionPhase | None
    aborted: bool
    destroyed: bool
    def __init__(self, is_tock: bool, storage_ph: TrStoragePhase, compute_ph: TrComputePhase, action: TrActionPhase | None, aborted: bool, destroyed: bool) -> None: ...
    @classmethod
    def deserialize(cls, cell_slice: Slice) -> TransactionTickTock: ...
