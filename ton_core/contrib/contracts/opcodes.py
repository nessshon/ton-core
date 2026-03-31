from __future__ import annotations

from enum import Enum

__all__ = [
    "OpCode",
]


class OpCode(int, Enum):
    """Standard operation codes for TON smart contract messages."""

    TEXT_COMMENT = 0x00000000
    """Plain text comment."""
    ENCRYPTED_TEXT_COMMENT = 0x2167DA4B
    """Encrypted text comment."""
    AUTH_SIGNED_EXTERNAL = 0x7369676E
    """Signed authentication for external messages."""
    AUTH_SIGNED_INTERNAL = 0x73696E74
    """Signed authentication for internal messages."""
    OUT_ACTION_SEND_MSG = 0x0EC3C86D
    """Out action to send a message."""
    INTERNAL_TRANSFER = 0xAE42E5A4
    """Internal transfer operation."""
    TOP_UP = 0xD372158C
    """Top-up balance operation."""
    EXCESSES = 0xD53276DB
    """Return excess TON after operation."""

    NFT_TRANSFER = 0x5FCC3D14
    """Transfer ownership of an NFT."""
    NFT_OWNERSHIP_ASSIGNED = 0x05138D91
    """Notify new owner after NFT transfer."""
    NFT_GET_STATIC_DATA = 0x2FCB26A2
    """Request static data of an NFT item."""
    NFT_REPORT_STATIC_DATA = 0x8B771735
    """Response to get_static_data request."""
    NFT_EDIT_CONTENT = 0x1A0B9D51
    """Edit content of an NFT item or collection."""
    NFT_TRANSFER_EDITORSHIP = 0x1C04412A
    """Transfer editorship rights of an NFT."""
    NFT_EDITORSHIP_ASSIGNED = 0x511A4463
    """Notify new editor after editorship transfer."""
    NFT_GET_ROYALTY_PARAMS = 0x693D3950
    """Request royalty parameters of an NFT."""
    NFT_REPORT_ROYALTY_PARAMS = 0xA8CB00AD
    """Response to get_royalty_params request."""

    SBT_DESTROY = 0x1F04537A
    """Destroy a soulbound token."""
    SBT_REVOKE = 0x6F89F5E3
    """Revoke a soulbound token."""
    SBT_PROVE_OWNERSHIP = 0x04DED148
    """Prove ownership of a soulbound token."""
    SBT_REQUEST_OWNER = 0xD0C3BFEA
    """Request owner info of a soulbound token."""
    SBT_OWNERSHIP_PROOF = 0x0524C7AE
    """Response to prove_ownership request."""
    SBT_OWNER_INFO = 0x0DD607E3
    """Response to request_owner request."""

    JETTON_TRANSFER = 0xF8A7EA5
    """Transfer jettons to another address."""
    JETTON_INTERNAL_TRANSFER = 0x178D4519
    """Internal jetton transfer between wallets."""
    JETTON_TRANSFER_NOTIFICATION = 0x7362D09C
    """Notify recipient about incoming jetton transfer."""
    JETTON_BURN = 0x595F07BC
    """Burn jettons, removing them from supply."""
    JETTON_BURN_NOTIFICATION = 0x7BDD97DE
    """Notify jetton master about burn."""
    JETTON_PROVIDE_WALLET_ADDRESS = 0x2C76B973
    """Request the jetton wallet address for an owner."""
    JETTON_TAKE_WALLET_ADDRESS = 0xD1735400
    """Response to provide_wallet_address request."""
    JETTON_MINT = 0x642B7D07
    """Mint new jettons."""
    JETTON_CHANGE_ADMIN = 0x6501F354
    """Change the admin of a jetton master contract."""
    JETTON_CLAIM_ADMIN = 0xFB88E119
    """Claim admin rights for a jetton master contract."""
    JETTON_DROP_ADMIN = 0x7431F221
    """Drop admin rights from a jetton master contract."""
    JETTON_UPGRADE = 0x2508D66A
    """Upgrade the jetton contract code."""
    JETTON_CHANGE_METADATA = 0xCB862902
    """Change metadata of a jetton master contract."""

    CHANGE_DNS_RECORD = 0x4EB1F0F9
    """Change a DNS record in a TON DNS item."""
    DNS_BALANCE_RELEASE = 0x4ED14B65
    """Release balance from a TON DNS item."""

    TELEITEM_START_AUCTION = 0x487A8E81
    """Start an auction for a Telegram username NFT item."""
    TELEITEM_CANCEL_AUCTION = 0x371638AE
    """Cancel an active auction for a Telegram username NFT item."""

