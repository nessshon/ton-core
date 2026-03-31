from __future__ import annotations

from enum import Enum

__all__ = [
    "ContractVersion",
]


class ContractVersion(str, Enum):
    """Standard TON smart contract version identifier."""

    WalletV1R1 = "wallet_v1r1"
    """Wallet contract version 1, revision 1."""
    WalletV1R2 = "wallet_v1r2"
    """Wallet contract version 1, revision 2."""
    WalletV1R3 = "wallet_v1r3"
    """Wallet contract version 1, revision 3."""
    WalletV2R1 = "wallet_v2r1"
    """Wallet contract version 2, revision 1."""
    WalletV2R2 = "wallet_v2r2"
    """Wallet contract version 2, revision 2."""
    WalletV3R1 = "wallet_v3r1"
    """Wallet contract version 3, revision 1."""
    WalletV3R2 = "wallet_v3r2"
    """Wallet contract version 3, revision 2."""
    WalletV4R1 = "wallet_v4r1"
    """Wallet contract version 4, revision 1."""
    WalletV4R2 = "wallet_v4r2"
    """Wallet contract version 4, revision 2."""
    WalletV5Beta = "wallet_v5_beta"
    """Wallet contract version 5, beta release."""
    WalletV5R1 = "wallet_v5r1"
    """Wallet contract version 5, revision 1."""

    WalletHighloadV2 = "wallet_highload_v2"
    """Highload wallet contract version 2."""
    WalletHighloadV3R1 = "wallet_highload_v3r1"
    """Highload wallet contract version 3, revision 1."""

    WalletPreprocessedV2 = "wallet_preprocessed_v2"
    """Preprocessed wallet contract version 2."""

    NFTCollectionStandard = "nft_collection_standard"
    """Standard NFT collection contract."""
    NFTCollectionEditable = "nft_collection_editable"
    """Editable NFT collection contract."""
    NFTItemStandard = "nft_item_standard"
    """Standard NFT item contract."""
    NFTItemEditable = "nft_item_editable"
    """Editable NFT item contract."""
    NFTItemSoulbound = "nft_item_soulbound"
    """Soulbound NFT item contract."""

    JettonMasterStandard = "jetton_master_standard"
    """Standard jetton master contract."""
    JettonMasterStablecoin = "jetton_master_stablecoin"
    """Stablecoin jetton master contract."""
    JettonMasterStablecoinV2 = "jetton_master_stablecoin_v2"
    """Stablecoin jetton master contract, version 2."""
    JettonWalletStandard = "jetton_wallet_standard"
    """Standard jetton wallet contract."""
    JettonWalletStablecoin = "jetton_wallet_stablecoin"
    """Stablecoin jetton wallet contract."""
    JettonWalletStablecoinV2 = "jetton_wallet_stablecoin_v2"
    """Stablecoin jetton wallet contract, version 2."""

    TelegramUsernamesCollection = "telegram_usernames_collection"
    """Telegram usernames NFT collection contract."""
    TelegramGiftsCollection = "telegram_gifts_collection"
    """Telegram gifts NFT collection contract."""
    TelegramUsernameItem = "telegram_username_item"
    """Telegram username NFT item contract."""
    TelegramGiftItem = "telegram_gift_item"
    """Telegram gift NFT item contract."""

    TONDNSCollection = "ton_dns_collection"
    """TON DNS collection contract."""
    TONDNSItem = "ton_dns_item"
    """TON DNS item contract."""

