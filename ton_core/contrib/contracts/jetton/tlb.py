from __future__ import annotations

from ton_core.boc import begin_cell
from ton_core.boc.cell import Cell
from ton_core.boc.slice import Slice
from ton_core.contrib.contracts._utils import _load_std_address
from ton_core.contrib.contracts.nft.tlb import OffchainContent, OnchainContent
from ton_core.contrib.contracts.opcodes import OpCode
from ton_core.contrib.types import AddressLike
from ton_core.tlb.tlb import TlbScheme

__all__ = [
    "JettonBurnBody",
    "JettonChangeAdminBody",
    "JettonChangeContentBody",
    "JettonClaimAdminBody",
    "JettonDiscoveryBody",
    "JettonDropAdminBody",
    "JettonInternalTransferBody",
    "JettonMasterStablecoinData",
    "JettonMasterStandardData",
    "JettonMintBody",
    "JettonStandardChangeAdminBody",
    "JettonStandardChangeContentBody",
    "JettonStandardMintBody",
    "JettonTopUpBody",
    "JettonTransferBody",
    "JettonUpgradeBody",
    "JettonWalletStablecoinData",
    "JettonWalletStablecoinV2Data",
    "JettonWalletStandardData",
]


class JettonMasterStandardData(TlbScheme):
    """On-chain data for standard Jetton minter contracts (TEP-74)."""

    def __init__(
        self,
        admin_address: AddressLike | None,
        content: OnchainContent | OffchainContent,
        jetton_wallet_code: Cell,
        total_supply: int = 0,
    ) -> None:
        """Initialize JettonMasterStandardData.

        :param admin_address: Admin address with minting rights.
        :param content: Jetton metadata (on-chain or off-chain).
        :param jetton_wallet_code: Code cell for Jetton wallet contracts.
        :param total_supply: Total minted supply in base units.
        """
        self.total_supply = total_supply
        self.admin_address = admin_address
        self.content = content
        self.jetton_wallet_code = jetton_wallet_code

    def serialize(self) -> Cell:
        """Serialize to Cell."""
        cell = begin_cell()
        cell.store_coins(self.total_supply)
        cell.store_address(self.admin_address)
        cell.store_ref(self.content.serialize(True))
        cell.store_ref(self.jetton_wallet_code)
        return cell.end_cell()

    @classmethod
    def deserialize(cls, cs: Slice) -> JettonMasterStandardData:
        """Deserialize from Slice."""
        from ton_core.contrib.types import MetadataPrefix

        total_supply = cs.load_coins() or 0
        admin_address = _load_std_address(cs)
        content = cs.load_ref().begin_parse()
        return cls(
            total_supply=total_supply,
            admin_address=admin_address,
            content=(
                OnchainContent.deserialize(content, False)
                if MetadataPrefix(content.load_uint(8)) == MetadataPrefix.ONCHAIN
                else OffchainContent.deserialize(content, False)
            ),
            jetton_wallet_code=cs.load_ref(),
        )


class JettonMasterStablecoinData(TlbScheme):
    """On-chain data for stablecoin Jetton minter contracts."""

    def __init__(
        self,
        admin_address: AddressLike | None,
        jetton_wallet_code: Cell,
        content: OffchainContent,
        next_admin_address: AddressLike | None = None,
        total_supply: int = 0,
    ) -> None:
        """Initialize JettonMasterStablecoinData.

        :param admin_address: Current admin address.
        :param jetton_wallet_code: Code cell for Jetton wallet contracts.
        :param content: Off-chain Jetton metadata.
        :param next_admin_address: Pending admin address, or None.
        :param total_supply: Total minted supply in base units.
        """
        self.total_supply = total_supply
        self.admin_address = admin_address
        self.next_admin_address = next_admin_address
        self.jetton_wallet_code = jetton_wallet_code
        self.content = content

    def serialize(self) -> Cell:
        """Serialize to Cell."""
        cell = begin_cell()
        cell.store_coins(self.total_supply)
        cell.store_address(self.admin_address)
        cell.store_address(self.next_admin_address)
        cell.store_ref(self.jetton_wallet_code)
        cell.store_ref(self.content.serialize(False))
        return cell.end_cell()

    @classmethod
    def deserialize(cls, cs: Slice) -> JettonMasterStablecoinData:
        """Deserialize from Slice."""
        return cls(
            total_supply=cs.load_coins() or 0,
            admin_address=_load_std_address(cs),
            next_admin_address=_load_std_address(cs),
            jetton_wallet_code=cs.load_ref(),
            content=OffchainContent.deserialize(cs.load_ref().begin_parse(), False),
        )


class JettonWalletStandardData(TlbScheme):
    """On-chain data for standard Jetton wallet contracts (TEP-74)."""

    def __init__(
        self,
        owner_address: AddressLike | None,
        jetton_master_address: AddressLike | None,
        jetton_wallet_code: Cell,
        balance: int = 0,
    ) -> None:
        """Initialize JettonWalletStandardData.

        :param owner_address: Wallet owner address.
        :param jetton_master_address: Jetton minter address.
        :param jetton_wallet_code: Code cell for Jetton wallet contracts.
        :param balance: Current Jetton balance in base units.
        """
        self.balance = balance
        self.owner_address = owner_address
        self.jetton_master_address = jetton_master_address
        self.jetton_wallet_code = jetton_wallet_code

    def serialize(self) -> Cell:
        """Serialize to Cell."""
        cell = begin_cell()
        cell.store_coins(self.balance)
        cell.store_address(self.owner_address)
        cell.store_address(self.jetton_master_address)
        cell.store_ref(self.jetton_wallet_code)
        return cell.end_cell()

    @classmethod
    def deserialize(cls, cs: Slice) -> JettonWalletStandardData:
        """Deserialize from Slice."""
        return cls(
            balance=cs.load_coins() or 0,
            owner_address=_load_std_address(cs),
            jetton_master_address=_load_std_address(cs),
            jetton_wallet_code=cs.load_ref(),
        )


class JettonWalletStablecoinData(TlbScheme):
    """On-chain data for stablecoin Jetton wallet contracts."""

    def __init__(
        self,
        owner_address: AddressLike | None,
        jetton_master_address: AddressLike | None,
        status: int,
        balance: int = 0,
    ) -> None:
        """Initialize JettonWalletStablecoinData.

        :param owner_address: Wallet owner address.
        :param jetton_master_address: Jetton minter address.
        :param status: Wallet status flags (4 bits).
        :param balance: Current Jetton balance in base units.
        """
        self.status = status
        self.balance = balance
        self.owner_address = owner_address
        self.jetton_master_address = jetton_master_address

    def serialize(self) -> Cell:
        """Serialize to Cell."""
        cell = begin_cell()
        cell.store_uint(self.status, 4)
        cell.store_coins(self.balance)
        cell.store_address(self.owner_address)
        cell.store_address(self.jetton_master_address)
        return cell.end_cell()

    @classmethod
    def deserialize(cls, cs: Slice) -> JettonWalletStablecoinData:
        """Deserialize from Slice."""
        return cls(
            status=cs.load_uint(4),
            balance=cs.load_coins() or 0,
            owner_address=_load_std_address(cs),
            jetton_master_address=_load_std_address(cs),
        )


class JettonWalletStablecoinV2Data(TlbScheme):
    """On-chain data for stablecoin v2 Jetton wallet contracts."""

    def __init__(
        self,
        owner_address: AddressLike | None,
        jetton_master_address: AddressLike | None,
        balance: int = 0,
    ) -> None:
        """Initialize JettonWalletStablecoinV2Data.

        :param owner_address: Wallet owner address.
        :param jetton_master_address: Jetton minter address.
        :param balance: Current Jetton balance in base units.
        """
        self.balance = balance
        self.owner_address = owner_address
        self.jetton_master_address = jetton_master_address

    def serialize(self) -> Cell:
        """Serialize to Cell."""
        cell = begin_cell()
        cell.store_coins(self.balance)
        cell.store_address(self.owner_address)
        cell.store_address(self.jetton_master_address)
        return cell.end_cell()

    @classmethod
    def deserialize(cls, cs: Slice) -> JettonWalletStablecoinV2Data:
        """Deserialize from Slice."""
        return cls(
            balance=cs.load_coins() or 0,
            owner_address=_load_std_address(cs),
            jetton_master_address=_load_std_address(cs),
        )


class JettonTopUpBody(TlbScheme):
    """Message body for topping up Jetton wallet balance."""

    def __init__(self, query_id: int = 0) -> None:
        """Initialize JettonTopUpBody.

        :param query_id: Query identifier.
        """
        self.query_id = query_id

    def serialize(self) -> Cell:
        """Serialize to Cell."""
        cell = begin_cell()
        cell.store_uint(OpCode.TOP_UP, 32)
        cell.store_uint(self.query_id, 64)
        return cell.end_cell()

    @classmethod
    def deserialize(cls, cs: Slice) -> JettonTopUpBody:
        """Deserialize from Slice."""
        cs.skip_bits(32)
        return cls(query_id=cs.load_uint(64))


class JettonInternalTransferBody(TlbScheme):
    """Message body for internal Jetton transfers between wallets."""

    def __init__(
        self,
        jetton_amount: int,
        forward_amount: int,
        from_address: AddressLike | None = None,
        response_address: AddressLike | None = None,
        forward_payload: Cell | None = None,
        query_id: int = 0,
    ) -> None:
        """Initialize JettonInternalTransferBody.

        :param jetton_amount: Amount to transfer in base units.
        :param forward_amount: Amount to forward in nanotons.
        :param from_address: Original sender address, or None.
        :param response_address: Address for excess funds, or None.
        :param forward_payload: Payload to forward, or None.
        :param query_id: Query identifier.
        """
        self.query_id = query_id
        self.jetton_amount = jetton_amount
        self.from_address = from_address
        self.response_address = response_address
        self.forward_amount = forward_amount
        self.forward_payload = forward_payload

    def serialize(self) -> Cell:
        """Serialize to Cell."""
        cell = begin_cell()
        cell.store_uint(OpCode.JETTON_INTERNAL_TRANSFER, 32)
        cell.store_uint(self.query_id, 64)
        cell.store_coins(self.jetton_amount)
        cell.store_address(self.from_address)
        cell.store_address(self.response_address)
        cell.store_coins(self.forward_amount)
        cell.store_maybe_ref(self.forward_payload)
        return cell.end_cell()

    @classmethod
    def deserialize(cls, cs: Slice) -> JettonInternalTransferBody:
        """Deserialize from Slice."""
        cs.skip_bits(32)
        return cls(
            query_id=cs.load_uint(64),
            jetton_amount=cs.load_coins() or 0,
            from_address=_load_std_address(cs),
            response_address=_load_std_address(cs),
            forward_amount=cs.load_coins() or 0,
            forward_payload=cs.load_maybe_ref(),
        )


class JettonTransferBody(TlbScheme):
    """Message body for Jetton transfers (TEP-74)."""

    def __init__(
        self,
        destination: AddressLike | None,
        jetton_amount: int,
        response_address: AddressLike | None = None,
        custom_payload: Cell | None = None,
        forward_payload: Cell | None = None,
        forward_amount: int = 1,
        query_id: int = 0,
    ) -> None:
        """Initialize JettonTransferBody.

        :param destination: Recipient address.
        :param jetton_amount: Amount to transfer in base units.
        :param response_address: Address for excess funds, or None.
        :param custom_payload: Custom payload cell, or None.
        :param forward_payload: Payload to forward, or None.
        :param forward_amount: Amount to forward in nanotons.
        :param query_id: Query identifier.
        """
        self.query_id = query_id
        self.jetton_amount = jetton_amount
        self.destination = destination
        self.response_address = response_address
        self.custom_payload = custom_payload
        self.forward_amount = forward_amount
        self.forward_payload = forward_payload

    def serialize(self) -> Cell:
        """Serialize to Cell."""
        cell = begin_cell()
        cell.store_uint(OpCode.JETTON_TRANSFER, 32)
        cell.store_uint(self.query_id, 64)
        cell.store_coins(self.jetton_amount)
        cell.store_address(self.destination)
        cell.store_address(self.response_address)
        cell.store_maybe_ref(self.custom_payload)
        cell.store_coins(self.forward_amount)
        cell.store_maybe_ref(self.forward_payload)
        return cell.end_cell()

    @classmethod
    def deserialize(cls, cs: Slice) -> JettonTransferBody:
        """Deserialize from Slice."""
        cs.skip_bits(32)
        return cls(
            query_id=cs.load_uint(64),
            jetton_amount=cs.load_coins() or 0,
            destination=_load_std_address(cs),
            response_address=_load_std_address(cs),
            custom_payload=cs.load_maybe_ref(),
            forward_amount=cs.load_coins() or 0,
            forward_payload=cs.load_maybe_ref(),
        )


class JettonMintBody(TlbScheme):
    """Message body for minting Jettons (stablecoin version)."""

    def __init__(
        self,
        destination: AddressLike | None,
        internal_transfer: JettonInternalTransferBody,
        forward_amount: int,
        query_id: int = 0,
    ) -> None:
        """Initialize JettonMintBody.

        :param destination: Recipient wallet address.
        :param internal_transfer: Internal transfer body with mint details.
        :param forward_amount: Amount to forward in nanotons.
        :param query_id: Query identifier.
        """
        self.query_id = query_id
        self.destination = destination
        self.forward_amount = forward_amount
        self.internal_transfer = internal_transfer

    def serialize(self) -> Cell:
        """Serialize to Cell."""
        cell = begin_cell()
        cell.store_uint(OpCode.JETTON_MINT, 32)
        cell.store_uint(self.query_id, 64)
        cell.store_address(self.destination)
        cell.store_coins(self.forward_amount)
        cell.store_ref(self.internal_transfer.serialize())
        return cell.end_cell()

    @classmethod
    def deserialize(cls, cs: Slice) -> JettonMintBody:
        """Deserialize from Slice."""
        cs.skip_bits(32)
        return cls(
            query_id=cs.load_uint(64),
            destination=_load_std_address(cs),
            forward_amount=cs.load_coins() or 0,
            internal_transfer=JettonInternalTransferBody.deserialize(cs.load_ref().begin_parse()),
        )


class JettonStandardMintBody(TlbScheme):
    """Message body for minting Jettons (standard version)."""

    def __init__(
        self,
        destination: AddressLike | None,
        internal_transfer: JettonInternalTransferBody,
        forward_amount: int,
        query_id: int = 0,
    ) -> None:
        """Initialize JettonStandardMintBody.

        :param destination: Recipient wallet address.
        :param internal_transfer: Internal transfer body with mint details.
        :param forward_amount: Amount to forward in nanotons.
        :param query_id: Query identifier.
        """
        self.query_id = query_id
        self.destination = destination
        self.forward_amount = forward_amount
        self.internal_transfer = internal_transfer

    def serialize(self) -> Cell:
        """Serialize to Cell."""
        cell = begin_cell()
        cell.store_uint(21, 32)
        cell.store_uint(self.query_id, 64)
        cell.store_address(self.destination)
        cell.store_coins(self.forward_amount)
        cell.store_ref(self.internal_transfer.serialize())
        return cell.end_cell()

    @classmethod
    def deserialize(cls, cs: Slice) -> JettonStandardMintBody:
        """Deserialize from Slice."""
        cs.skip_bits(32)
        return cls(
            query_id=cs.load_uint(64),
            destination=_load_std_address(cs),
            forward_amount=cs.load_coins() or 0,
            internal_transfer=JettonInternalTransferBody.deserialize(cs.load_ref().begin_parse()),
        )


class JettonChangeAdminBody(TlbScheme):
    """Message body for changing Jetton minter admin (stablecoin version)."""

    def __init__(
        self,
        admin_address: AddressLike | None,
        query_id: int = 0,
    ) -> None:
        """Initialize JettonChangeAdminBody.

        :param admin_address: New admin address.
        :param query_id: Query identifier.
        """
        self.query_id = query_id
        self.admin_address = admin_address

    def serialize(self) -> Cell:
        """Serialize to Cell."""
        cell = begin_cell()
        cell.store_uint(OpCode.JETTON_CHANGE_ADMIN, 32)
        cell.store_uint(self.query_id, 64)
        cell.store_address(self.admin_address)
        return cell.end_cell()

    @classmethod
    def deserialize(cls, cs: Slice) -> JettonChangeAdminBody:
        """Deserialize from Slice."""
        cs.skip_bits(32)
        return cls(
            query_id=cs.load_uint(64),
            admin_address=_load_std_address(cs),
        )


class JettonStandardChangeAdminBody(TlbScheme):
    """Message body for changing Jetton minter admin (standard version)."""

    def __init__(
        self,
        admin_address: AddressLike | None,
        query_id: int = 0,
    ) -> None:
        """Initialize JettonStandardChangeAdminBody.

        :param admin_address: New admin address.
        :param query_id: Query identifier.
        """
        self.query_id = query_id
        self.admin_address = admin_address

    def serialize(self) -> Cell:
        """Serialize to Cell."""
        cell = begin_cell()
        cell.store_uint(3, 32)
        cell.store_uint(self.query_id, 64)
        cell.store_address(self.admin_address)
        return cell.end_cell()

    @classmethod
    def deserialize(cls, cs: Slice) -> JettonStandardChangeAdminBody:
        """Deserialize from Slice."""
        cs.skip_bits(32)
        return cls(
            query_id=cs.load_uint(64),
            admin_address=_load_std_address(cs),
        )


class JettonDiscoveryBody(TlbScheme):
    """Message body for discovering Jetton wallet address."""

    def __init__(
        self,
        owner_address: AddressLike | None,
        include_address: bool = True,
        query_id: int = 0,
    ) -> None:
        """Initialize JettonDiscoveryBody.

        :param owner_address: Owner address to query wallet for.
        :param include_address: Include address in response.
        :param query_id: Query identifier.
        """
        self.query_id = query_id
        self.owner_address = owner_address
        self.include_address = include_address

    def serialize(self) -> Cell:
        """Serialize to Cell."""
        cell = begin_cell()
        cell.store_uint(OpCode.JETTON_PROVIDE_WALLET_ADDRESS, 32)
        cell.store_uint(self.query_id, 64)
        cell.store_address(self.owner_address)
        cell.store_bool(self.include_address)
        return cell.end_cell()

    @classmethod
    def deserialize(cls, cs: Slice) -> JettonDiscoveryBody:
        """Deserialize from Slice."""
        cs.skip_bits(32)
        return cls(
            query_id=cs.load_uint(64),
            owner_address=_load_std_address(cs),
            include_address=cs.load_bool(),
        )


class JettonClaimAdminBody(TlbScheme):
    """Message body for claiming Jetton minter admin rights."""

    def __init__(self, query_id: int = 0) -> None:
        """Initialize JettonClaimAdminBody.

        :param query_id: Query identifier.
        """
        self.query_id = query_id

    def serialize(self) -> Cell:
        """Serialize to Cell."""
        cell = begin_cell()
        cell.store_uint(OpCode.JETTON_CLAIM_ADMIN, 32)
        cell.store_uint(self.query_id, 64)
        return cell.end_cell()

    @classmethod
    def deserialize(cls, cs: Slice) -> JettonClaimAdminBody:
        """Deserialize from Slice."""
        cs.skip_bits(32)
        return cls(query_id=cs.load_uint(64))


class JettonDropAdminBody(TlbScheme):
    """Message body for dropping Jetton minter admin rights."""

    def __init__(self, query_id: int = 0) -> None:
        """Initialize JettonDropAdminBody.

        :param query_id: Query identifier.
        """
        self.query_id = query_id

    def serialize(self) -> Cell:
        """Serialize to Cell."""
        cell = begin_cell()
        cell.store_uint(OpCode.JETTON_DROP_ADMIN, 32)
        cell.store_uint(self.query_id, 64)
        return cell.end_cell()

    @classmethod
    def deserialize(cls, cs: Slice) -> JettonDropAdminBody:
        """Deserialize from Slice."""
        cs.skip_bits(32)
        return cls(query_id=cs.load_uint(64))


class JettonChangeContentBody(TlbScheme):
    """Message body for changing Jetton metadata (stablecoin version)."""

    def __init__(
        self,
        content: OffchainContent,
        query_id: int = 0,
    ) -> None:
        """Initialize JettonChangeContentBody.

        :param content: New off-chain content.
        :param query_id: Query identifier.
        """
        self.query_id = query_id
        self.content = content

    def serialize(self) -> Cell:
        """Serialize to Cell."""
        cell = begin_cell()
        cell.store_uint(OpCode.JETTON_CHANGE_METADATA, 32)
        cell.store_uint(self.query_id, 64)
        cell.store_snake_string(self.content.uri)
        return cell.end_cell()

    @classmethod
    def deserialize(cls, cs: Slice) -> JettonChangeContentBody:
        """Deserialize from Slice."""
        cs.skip_bits(32)
        return cls(
            query_id=cs.load_uint(64),
            content=OffchainContent(uri=cs.load_snake_string()),
        )


class JettonStandardChangeContentBody(TlbScheme):
    """Message body for changing Jetton metadata (standard version)."""

    def __init__(
        self,
        content: OnchainContent | OffchainContent,
        query_id: int = 0,
    ) -> None:
        """Initialize JettonStandardChangeContentBody.

        :param content: New content (on-chain or off-chain).
        :param query_id: Query identifier.
        """
        self.query_id = query_id
        self.content = content

    def serialize(self) -> Cell:
        """Serialize to Cell."""
        cell = begin_cell()
        cell.store_uint(4, 32)
        cell.store_uint(self.query_id, 64)
        cell.store_ref(self.content.serialize(True))
        return cell.end_cell()

    @classmethod
    def deserialize(cls, cs: Slice) -> JettonStandardChangeContentBody:
        """Deserialize from Slice."""
        from ton_core.contrib.types import MetadataPrefix

        cs.skip_bits(32)
        query_id = cs.load_uint(64)
        content_cs = cs.load_ref().begin_parse()
        prefix = MetadataPrefix(content_cs.load_uint(8))
        content: OnchainContent | OffchainContent
        if prefix == MetadataPrefix.ONCHAIN:
            content = OnchainContent.deserialize(content_cs, False)
        else:
            content = OffchainContent.deserialize(content_cs, False)
        return cls(query_id=query_id, content=content)


class JettonBurnBody(TlbScheme):
    """Message body for burning Jettons (TEP-74)."""

    def __init__(
        self,
        jetton_amount: int,
        response_address: AddressLike | None,
        custom_payload: Cell | None = None,
        query_id: int = 0,
    ) -> None:
        """Initialize JettonBurnBody.

        :param jetton_amount: Amount to burn in base units.
        :param response_address: Address for excess funds.
        :param custom_payload: Custom payload cell, or None.
        :param query_id: Query identifier.
        """
        self.query_id = query_id
        self.jetton_amount = jetton_amount
        self.response_address = response_address
        self.custom_payload = custom_payload

    def serialize(self) -> Cell:
        """Serialize to Cell."""
        cell = begin_cell()
        cell.store_uint(OpCode.JETTON_BURN, 32)
        cell.store_uint(self.query_id, 64)
        cell.store_coins(self.jetton_amount)
        cell.store_address(self.response_address)
        cell.store_maybe_ref(self.custom_payload)
        return cell.end_cell()

    @classmethod
    def deserialize(cls, cs: Slice) -> JettonBurnBody:
        """Deserialize from Slice."""
        cs.skip_bits(32)
        return cls(
            query_id=cs.load_uint(64),
            jetton_amount=cs.load_coins() or 0,
            response_address=_load_std_address(cs),
            custom_payload=cs.load_maybe_ref(),
        )


class JettonUpgradeBody(TlbScheme):
    """Message body for upgrading Jetton contract code."""

    def __init__(
        self,
        code: Cell,
        data: Cell,
        query_id: int = 0,
    ) -> None:
        """Initialize JettonUpgradeBody.

        :param code: New contract code cell.
        :param data: New contract data cell.
        :param query_id: Query identifier.
        """
        self.query_id = query_id
        self.data = data
        self.code = code

    def serialize(self) -> Cell:
        """Serialize to Cell."""
        cell = begin_cell()
        cell.store_uint(OpCode.JETTON_UPGRADE, 32)
        cell.store_uint(self.query_id, 64)
        cell.store_ref(self.data)
        cell.store_ref(self.code)
        return cell.end_cell()

    @classmethod
    def deserialize(cls, cs: Slice) -> JettonUpgradeBody:
        """Deserialize from Slice."""
        cs.skip_bits(32)
        return cls(
            query_id=cs.load_uint(64),
            data=cs.load_ref(),
            code=cs.load_ref(),
        )
