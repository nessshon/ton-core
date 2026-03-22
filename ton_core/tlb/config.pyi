from ton_core.boc.slice import Slice
from ton_core.tlb.block import ExtraCurrencyCollection, GlobalVersion
from ton_core.tlb.tlb import TlbError, TlbScheme

class ConfigError(TlbError): ...

class ParamLimits(TlbScheme):
    underload: int
    soft_limit: int
    hard_limit: int
    def __init__(self, underload: int, soft_limit: int, hard_limit: int) -> None: ...
    @classmethod
    def deserialize(cls, cell_slice: Slice) -> ParamLimits: ...

class BlockCreateFees(TlbScheme):
    masterchain_block_fee: int
    basechain_block_fee: int
    def __init__(self, masterchain_block_fee: int, basechain_block_fee: int) -> None: ...
    @classmethod
    def deserialize(cls, cell_slice: Slice) -> BlockCreateFees: ...

class BlockLimits(TlbScheme):
    bytes: ParamLimits
    gas: ParamLimits
    lt_delta: ParamLimits
    def __init__(self, bytes: ParamLimits, gas: ParamLimits, lt_delta: ParamLimits) -> None: ...
    @classmethod
    def deserialize(cls, cell_slice: Slice) -> BlockLimits: ...

class CatchainConfig(TlbScheme):
    type_: str
    mc_catchain_lifetime: int
    shard_catchain_lifetime: int
    shard_validators_lifetime: int
    shard_validators_num: int
    shuffle_mc_validators: bool | None
    def __init__(self, type_: str, mc_catchain_lifetime: int, shard_catchain_lifetime: int, shard_validators_lifetime: int, shard_validators_num: int, shuffle_mc_validators: bool | None = ...) -> None: ...
    @classmethod
    def deserialize(cls, cell_slice: Slice) -> CatchainConfig: ...

class ComplaintPricing(TlbScheme):
    deposit: int
    bit_price: int
    cell_price: int
    def __init__(self, deposit: int, bit_price: int, cell_price: int) -> None: ...
    @classmethod
    def deserialize(cls, cell_slice: Slice) -> ComplaintPricing: ...

class ConfigProposalSetup(TlbScheme):
    min_tot_rounds: int
    max_tot_rounds: int
    min_wins: int
    max_losses: int
    min_store_sec: int
    max_store_sec: int
    bit_price: int
    cell_price: int
    def __init__(self, min_tot_rounds: int, max_tot_rounds: int, min_wins: int, max_losses: int, min_store_sec: int, max_store_sec: int, bit_price: int, cell_price: int) -> None: ...
    @classmethod
    def deserialize(cls, cell_slice: Slice) -> ConfigProposalSetup: ...

class ConfigVotingSetup(TlbScheme):
    normal_params: ConfigProposalSetup
    critical_params: ConfigProposalSetup
    def __init__(self, normal_params: ConfigProposalSetup, critical_params: ConfigProposalSetup) -> None: ...
    @classmethod
    def deserialize(cls, cell_slice: Slice) -> ConfigVotingSetup: ...

class ConsensusConfig(TlbScheme):
    type_: str
    round_candidates: int | None
    next_candidate_delay_ms: int | None
    consensus_timeout_ms: int | None
    fast_attempts: int | None
    attempt_duration: int | None
    catchain_max_deps: int | None
    max_block_bytes: int | None
    max_collated_bytes: int | None
    flags: int | None
    new_catchain_ids: int | None
    proto_version: int | None
    catchain_max_blocks_coeff: int | None
    def __init__(self, type_: str, round_candidates: int | None = ..., next_candidate_delay_ms: int | None = ..., consensus_timeout_ms: int | None = ..., fast_attempts: int | None = ..., attempt_duration: int | None = ..., catchain_max_deps: int | None = ..., max_block_bytes: int | None = ..., max_collated_bytes: int | None = ..., flags: int | None = ..., new_catchain_ids: int | None = ..., proto_version: int | None = ..., catchain_max_blocks_coeff: int | None = ...) -> None: ...
    @classmethod
    def deserialize(cls, cell_slice: Slice) -> ConsensusConfig: ...

class GasLimitsPrices(TlbScheme):
    type_: str
    gas_price: int | None
    gas_limit: int | None
    gas_credit: int | None
    block_gas_limit: int | None
    freeze_due_limit: int | None
    delete_due_limit: int | None
    special_gas_limit: int | None
    flat_gas_limit: int | None
    flat_gas_price: int | None
    other: GasLimitsPrices | None
    def __init__(self, type_: str, gas_price: int | None = ..., gas_limit: int | None = ..., gas_credit: int | None = ..., block_gas_limit: int | None = ..., freeze_due_limit: int | None = ..., delete_due_limit: int | None = ..., special_gas_limit: int | None = ..., flat_gas_limit: int | None = ..., flat_gas_price: int | None = ..., other: GasLimitsPrices | None = ...) -> None: ...
    @classmethod
    def deserialize(cls, cell_slice: Slice) -> GasLimitsPrices: ...

class JettonBridgePrices(TlbScheme):
    bridge_burn_fee: int
    bridge_mint_fee: int
    wallet_min_tons_for_storage: int
    wallet_gas_consumption: int
    minter_min_tons_for_storage: int
    discover_gas_consumption: int
    def __init__(self, bridge_burn_fee: int, bridge_mint_fee: int, wallet_min_tons_for_storage: int, wallet_gas_consumption: int, minter_min_tons_for_storage: int, discover_gas_consumption: int) -> None: ...
    @classmethod
    def deserialize(cls, cell_slice: Slice) -> JettonBridgePrices: ...

class JettonBridgeParams(TlbScheme):
    type_: str
    bridge_address: bytes
    bridge_address_hex: str
    oracles_address: bytes
    oracles_address_hex: str
    oracles: dict[int, int]
    state_flags: int
    burn_bridge_fee: int | None
    prices: JettonBridgePrices | None
    external_chain_address: bytes | None
    def __init__(self, type_: str, bridge_address: bytes, oracles_address: bytes, oracles: dict[int, int], state_flags: int, burn_bridge_fee: int | None = ..., prices: JettonBridgePrices | None = ..., external_chain_address: bytes | None = ...) -> None: ...
    @classmethod
    def deserialize(cls, cell_slice: Slice) -> JettonBridgeParams: ...

class MsgForwardPrices(TlbScheme):
    lump_price: int
    bit_price: int
    cell_price: int
    ihr_price_factor: int
    first_frac: int
    next_frac: int
    def __init__(self, lump_price: int, bit_price: int, cell_price: int, ihr_price_factor: int, first_frac: int, next_frac: int) -> None: ...
    @classmethod
    def deserialize(cls, cell_slice: Slice) -> MsgForwardPrices: ...

class OracleBridgeParams(TlbScheme):
    bridge_address: bytes
    bridge_address_hex: str
    oracle_mutlisig_address: bytes
    oracle_mutlisig_address_hex: str
    oracles: dict[int, int]
    external_chain_address_hex: str
    def __init__(self, bridge_address: bytes, oracle_mutlisig_address: bytes, oracles: dict[int, int], external_chain_address: bytes) -> None: ...
    @classmethod
    def deserialize(cls, cell_slice: Slice) -> OracleBridgeParams: ...

class SigPubKey(TlbScheme):
    pubkey: bytes
    def __init__(self, pubkey: bytes) -> None: ...
    @classmethod
    def deserialize(cls, cell_slice: Slice) -> SigPubKey: ...

class StoragePrices(TlbScheme):
    utime_since: int
    bit_price_ps: int
    cell_price_ps: int
    mc_bit_price_ps: int
    mc_cell_price_ps: int
    def __init__(self, utime_since: int, bit_price_ps: int, cell_price_ps: int, mc_bit_price_ps: int, mc_cell_price_ps: int) -> None: ...
    @classmethod
    def deserialize(cls, cell_slice: Slice) -> StoragePrices: ...

class SuspendedAddressList(TlbScheme):
    addresses: dict[int, None]
    suspended_until: int
    def __init__(self, addresses: dict[int, None], suspended_until: int) -> None: ...
    @classmethod
    def deserialize(cls, cell_slice: Slice) -> SuspendedAddressList: ...

class ValidatorDescr(TlbScheme):
    type_: str
    public_key: SigPubKey
    weight: int
    adnl_addr: bytes | None
    def __init__(self, type_: str, public_key: SigPubKey, weight: int, adnl_addr: bytes | None = ...) -> None: ...
    @classmethod
    def deserialize(cls, cell_slice: Slice) -> ValidatorDescr: ...

class ValidatorSet(TlbScheme):
    type_: str
    utime_since: int
    utime_until: int
    total: int
    main: int
    total_weight: int | None
    list: dict[int, ValidatorDescr]
    def __init__(self, type_: str, utime_since: int, utime_until: int, total: int, main: int, total_weight: int | None, list: dict[int, ValidatorDescr]) -> None: ...
    @classmethod
    def deserialize(cls, cell_slice: Slice) -> ValidatorSet: ...

class WcSplitMergeTimings(TlbScheme):
    split_merge_delay: int
    split_merge_interval: int
    min_split_merge_interval: int
    max_split_merge_delay: int
    def __init__(self, split_merge_delay: int, split_merge_interval: int, min_split_merge_interval: int, max_split_merge_delay: int) -> None: ...
    @classmethod
    def deserialize(cls, cell_slice: Slice) -> WcSplitMergeTimings: ...

class WorkchainFormat(TlbScheme):
    type_: str
    vm_version: int | None
    vm_mode: int | None
    min_addr_len: int | None
    max_addr_len: int | None
    addr_len_step: int | None
    workchain_type_id: int | None
    def __init__(self, type_: str, vm_version: int | None = ..., vm_mode: int | None = ..., min_addr_len: int | None = ..., max_addr_len: int | None = ..., addr_len_step: int | None = ..., workchain_type_id: int | None = ...) -> None: ...
    @classmethod
    def deserialize(cls, cell_slice: Slice, v: int = ...) -> WorkchainFormat: ...

class WorkchainDescr(TlbScheme):
    type_: str
    enabled_since: int
    actual_min_split: int
    min_split: int
    max_split: int
    basic: int
    active: bool
    accept_msgs: bool
    flags: int
    zerostate_root_hash: bytes
    zerostate_file_hash: bytes
    version: int
    format: WorkchainFormat
    split_merge_timings: WcSplitMergeTimings | None
    persistent_state_split_depth: int | None
    def __init__(self, type_: str, enabled_since: int, actual_min_split: int, min_split: int, max_split: int, basic: int, active: bool, accept_msgs: bool, flags: int, zerostate_root_hash: bytes, zerostate_file_hash: bytes, version: int, format: WorkchainFormat, split_merge_timings: WcSplitMergeTimings | None = ..., persistent_state_split_depth: int | None = ...) -> None: ...
    @classmethod
    def deserialize(cls, cell_slice: Slice) -> WorkchainDescr: ...

class ConfigParam(TlbScheme):
    params: dict[int, type[TlbScheme]]
    @classmethod
    def deserialize(cls, *args: object) -> None: ...

class ConfigParam0(TlbScheme):
    config_addr: bytes
    config_addr_hex: str
    def __init__(self, config_addr: bytes) -> None: ...
    @classmethod
    def deserialize(cls, cell_slice: Slice) -> ConfigParam0: ...

class ConfigParam1(TlbScheme):
    elector_addr: bytes
    elector_addr_hex: str
    def __init__(self, elector_addr: bytes) -> None: ...
    @classmethod
    def deserialize(cls, cell_slice: Slice) -> ConfigParam1: ...

class ConfigParam2(TlbScheme):
    minter_addr: bytes
    minter_addr_hex: str
    def __init__(self, minter_addr: bytes) -> None: ...
    @classmethod
    def deserialize(cls, cell_slice: Slice) -> ConfigParam2: ...

class ConfigParam3(TlbScheme):
    fee_collector_addr: bytes
    fee_collector_addr_hex: str
    def __init__(self, fee_collector_addr: bytes) -> None: ...
    @classmethod
    def deserialize(cls, cell_slice: Slice) -> ConfigParam3: ...

class ConfigParam4(TlbScheme):
    dns_root_addr: bytes
    dns_root_addr_hex: str
    def __init__(self, dns_root_addr: bytes) -> None: ...
    @classmethod
    def deserialize(cls, cell_slice: Slice) -> ConfigParam4: ...

class ConfigParam5(TlbScheme):
    blackhole_addr: bytes | None
    blackhole_addr_hex: str | None
    fee_burn_nom: int
    fee_burn_denom: int
    def __init__(self, blackhole_addr: bytes | None, fee_burn_nom: int, fee_burn_denom: int) -> None: ...
    @classmethod
    def deserialize(cls, cell_slice: Slice) -> ConfigParam5: ...

class ConfigParam6(TlbScheme):
    mint_new_price: int
    mint_add_price: int
    def __init__(self, mint_new_price: int, mint_add_price: int) -> None: ...
    @classmethod
    def deserialize(cls, cell_slice: Slice) -> ConfigParam6: ...

class ConfigParam7(TlbScheme):
    to_mint: ExtraCurrencyCollection
    def __init__(self, to_mint: ExtraCurrencyCollection) -> None: ...
    @classmethod
    def deserialize(cls, cell_slice: Slice) -> ConfigParam7: ...

class ConfigParam8(GlobalVersion):
    def __init__(self, **kwargs: object) -> None: ...
    @classmethod
    def deserialize(cls, cell_slice: Slice) -> ConfigParam8: ...

class ConfigParam9(TlbScheme):
    mandatory_params: dict[int, bool]
    def __init__(self, mandatory_params: dict[int, bool]) -> None: ...
    @classmethod
    def deserialize(cls, cell_slice: Slice) -> ConfigParam9: ...

class ConfigParam10(TlbScheme):
    critical_params: dict[int, bool]
    def __init__(self, critical_params: dict[int, bool]) -> None: ...
    @classmethod
    def deserialize(cls, cell_slice: Slice) -> ConfigParam10: ...

class ConfigParam11(ConfigVotingSetup):
    def __init__(self, **kwargs: object) -> None: ...
    @classmethod
    def deserialize(cls, cell_slice: Slice) -> ConfigParam11: ...

class ConfigParam12(TlbScheme):
    workchains: dict[int, WorkchainDescr]
    def __init__(self, workchains: dict[int, WorkchainDescr]) -> None: ...
    @classmethod
    def deserialize(cls, cell_slice: Slice) -> ConfigParam12: ...

class ConfigParam13(ComplaintPricing):
    def __init__(self, **kwargs: object) -> None: ...
    @classmethod
    def deserialize(cls, cell_slice: Slice) -> ConfigParam13: ...

class ConfigParam14(BlockCreateFees):
    def __init__(self, **kwargs: object) -> None: ...
    @classmethod
    def deserialize(cls, cell_slice: Slice) -> ConfigParam14: ...

class ConfigParam15(TlbScheme):
    validators_elected_for: int
    elections_start_before: int
    elections_end_before: int
    stake_held_for: int
    def __init__(self, validators_elected_for: int, elections_start_before: int, elections_end_before: int, stake_held_for: int) -> None: ...
    @classmethod
    def deserialize(cls, cell_slice: Slice) -> ConfigParam15: ...

class ConfigParam16(TlbScheme):
    max_validators: int
    max_main_validators: int
    min_validators: int
    def __init__(self, max_validators: int, max_main_validators: int, min_validators: int) -> None: ...
    @classmethod
    def deserialize(cls, cell_slice: Slice) -> ConfigParam16: ...

class ConfigParam17(TlbScheme):
    min_stake: int
    max_stake: int
    min_total_stake: int
    max_stake_factor: int
    def __init__(self, min_stake: int, max_stake: int, min_total_stake: int, max_stake_factor: int) -> None: ...
    @classmethod
    def deserialize(cls, cell_slice: Slice) -> ConfigParam17: ...

class ConfigParam18(TlbScheme):
    @classmethod
    def deserialize(cls, cell_slice: Slice) -> dict[int, StoragePrices]: ...

class ConfigParam20(GasLimitsPrices):
    def __init__(self, **kwargs: object) -> None: ...
    @classmethod
    def deserialize(cls, cell_slice: Slice) -> ConfigParam20: ...

class ConfigParam21(GasLimitsPrices):
    def __init__(self, **kwargs: object) -> None: ...
    @classmethod
    def deserialize(cls, cell_slice: Slice) -> ConfigParam21: ...

class ConfigParam22(BlockLimits):
    def __init__(self, **kwargs: object) -> None: ...
    @classmethod
    def deserialize(cls, cell_slice: Slice) -> ConfigParam22: ...

class ConfigParam23(BlockLimits):
    def __init__(self, **kwargs: object) -> None: ...
    @classmethod
    def deserialize(cls, cell_slice: Slice) -> ConfigParam23: ...

class ConfigParam24(MsgForwardPrices):
    def __init__(self, **kwargs: object) -> None: ...
    @classmethod
    def deserialize(cls, cell_slice: Slice) -> ConfigParam24: ...

class ConfigParam25(MsgForwardPrices):
    def __init__(self, **kwargs: object) -> None: ...
    @classmethod
    def deserialize(cls, cell_slice: Slice) -> ConfigParam25: ...

class ConfigParam28(CatchainConfig):
    def __init__(self, **kwargs: object) -> None: ...
    @classmethod
    def deserialize(cls, cell_slice: Slice) -> ConfigParam28: ...

class ConfigParam29(ConsensusConfig):
    def __init__(self, **kwargs: object) -> None: ...
    @classmethod
    def deserialize(cls, cell_slice: Slice) -> ConfigParam29: ...

class ConfigParam31(TlbScheme):
    fundamental_smc_addr: dict[int, bool]
    def __init__(self, fundamental_smc_addr: dict[int, bool]) -> None: ...
    @classmethod
    def deserialize(cls, cell_slice: Slice) -> ConfigParam31: ...

class ConfigParam32(TlbScheme):
    prev_validators: ValidatorSet
    def __init__(self, prev_validators: ValidatorSet) -> None: ...
    @classmethod
    def deserialize(cls, cell_slice: Slice) -> ConfigParam32: ...

class ConfigParam33(TlbScheme):
    prev_temp_validators: ValidatorSet
    def __init__(self, prev_temp_validators: ValidatorSet) -> None: ...
    @classmethod
    def deserialize(cls, cell_slice: Slice) -> ConfigParam33: ...

class ConfigParam34(TlbScheme):
    cur_validators: ValidatorSet
    def __init__(self, cur_validators: ValidatorSet) -> None: ...
    @classmethod
    def deserialize(cls, cell_slice: Slice) -> ConfigParam34: ...

class ConfigParam35(TlbScheme):
    cur_temp_validators: ValidatorSet
    def __init__(self, cur_temp_validators: ValidatorSet) -> None: ...
    @classmethod
    def deserialize(cls, cell_slice: Slice) -> ConfigParam35: ...

class ConfigParam36(TlbScheme):
    next_validators: ValidatorSet
    def __init__(self, next_validators: ValidatorSet) -> None: ...
    @classmethod
    def deserialize(cls, cell_slice: Slice) -> ConfigParam36: ...

class ConfigParam37(TlbScheme):
    next_temp_validators: ValidatorSet
    def __init__(self, next_temp_validators: ValidatorSet) -> None: ...
    @classmethod
    def deserialize(cls, cell_slice: Slice) -> ConfigParam37: ...

class ConfigParam44(SuspendedAddressList):
    def __init__(self, **kwargs: object) -> None: ...
    @classmethod
    def deserialize(cls, cell_slice: Slice) -> ConfigParam44: ...

class ConfigParam71(OracleBridgeParams):
    def __init__(self, **kwargs: object) -> None: ...
    @classmethod
    def deserialize(cls, cell_slice: Slice) -> ConfigParam71: ...

class ConfigParam72(OracleBridgeParams):
    def __init__(self, **kwargs: object) -> None: ...
    @classmethod
    def deserialize(cls, cell_slice: Slice) -> ConfigParam72: ...

class ConfigParam73(OracleBridgeParams):
    def __init__(self, **kwargs: object) -> None: ...
    @classmethod
    def deserialize(cls, cell_slice: Slice) -> ConfigParam73: ...

class ConfigParam79(JettonBridgeParams):
    def __init__(self, **kwargs: object) -> None: ...
    @classmethod
    def deserialize(cls, cell_slice: Slice) -> ConfigParam79: ...

class ConfigParam81(JettonBridgeParams):
    def __init__(self, **kwargs: object) -> None: ...
    @classmethod
    def deserialize(cls, cell_slice: Slice) -> ConfigParam81: ...

class ConfigParam82(JettonBridgeParams):
    def __init__(self, **kwargs: object) -> None: ...
    @classmethod
    def deserialize(cls, cell_slice: Slice) -> ConfigParam82: ...
