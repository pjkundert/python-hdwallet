#!/usr/bin/env python3

# Copyright © 2020-2024, Meheret Tesfaye Batu <meherett.batu@gmail.com>
# Distributed under the MIT software license, see the accompanying
# file COPYING or https://opensource.org/license/mit

from ..ecc import SLIP10Secp256k1ECC
from ..const import (
    Info, Entropies, Mnemonics, Seeds, HDs, Addresses, Networks, XPrivateKeyVersions, XPublicKeyVersions
)
from .icryptocurrency import (
    ICryptocurrency, INetwork
)


class Mainnet(INetwork):

    PUBLIC_KEY_ADDRESS_PREFIX = 0x19
    SCRIPT_ADDRESS_PREFIX = 0x3f
    XPRIVATE_KEY_VERSIONS = XPrivateKeyVersions({
        "P2PKH": 0x488ade4,
        "P2SH": 0x488ade4
    })
    XPUBLIC_KEY_VERSIONS = XPublicKeyVersions({
        "P2PKH": 0x488b21e,
        "P2SH": 0x488b21e
    })
    MESSAGE_PREFIX = "\x18Blocknode Signed Message:\n"
    WIF_PREFIX = 0x4b


class Testnet(INetwork):

    PUBLIC_KEY_ADDRESS_PREFIX = 0x55
    SCRIPT_ADDRESS_PREFIX = 0x7d
    XPRIVATE_KEY_VERSIONS = XPrivateKeyVersions({
        "P2PKH": 0x4358394,
        "P2SH": 0x4358394
    })
    XPUBLIC_KEY_VERSIONS = XPublicKeyVersions({
        "P2PKH": 0x43587cf,
        "P2SH": 0x43587cf
    })
    MESSAGE_PREFIX = "\x18Blocknode Testnet Signed Message:\n"
    WIF_PREFIX = 0x89


class Blocknode(ICryptocurrency):

    NAME = "Blocknode"
    SYMBOL = "BND"
    INFO = Info({
        "SOURCE_CODE": "https://github.com/blocknodetech/blocknode",
        "WEBSITES": [
            "https://blocknode.tech"
        ]
    })
    ECC = SLIP10Secp256k1ECC
    COIN_TYPE = 2941
    NETWORKS = Networks({
        "MAINNET": Mainnet, "TESTNET": Testnet
    })
    DEFAULT_NETWORK = NETWORKS.MAINNET
    ENTROPIES = Entropies({
        "BIP39"
    })
    MNEMONICS = Mnemonics({
        "BIP39"
    })
    SEEDS = Seeds({
        "BIP39"
    })
    HDS = HDs({
        "BIP32", "BIP44"
    })
    DEFAULT_HD = HDS.BIP44
    ADDRESSES = Addresses({
        "P2PKH", "P2SH"
    })
    DEFAULT_ADDRESS = ADDRESSES.P2PKH
