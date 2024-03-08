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

    PUBLIC_KEY_ADDRESS_PREFIX = 0x49
    SCRIPT_ADDRESS_PREFIX = 0x57
    XPRIVATE_KEY_VERSIONS = XPrivateKeyVersions({
        "P2PKH": 0x48894ed,
        "P2SH": 0x48894ed
    })
    XPUBLIC_KEY_VERSIONS = XPublicKeyVersions({
        "P2PKH": 0x4887f1e,
        "P2SH": 0x4887f1e
    })
    MESSAGE_PREFIX = "\x18Whitecoin Signed Message:\n"
    WIF_PREFIX = 0xc9


class Whitecoin(ICryptocurrency):

    NAME = "Whitecoin"
    SYMBOL = "XWC"
    INFO = Info({
        "SOURCE_CODE": "https://github.com/Whitecoin-XWC/Whitecoin-core",
        "WHITEPAPER": "https://www.whitecoin.info/pdf/Whitecoin%20Technical%20White%20Paper_en.pdf",
        "WEBSITES": [
            "http://whitecoin.info",
            "http://xwc.com"
        ]
    })
    ECC = SLIP10Secp256k1ECC
    COIN_TYPE = 559
    NETWORKS = Networks({
        "MAINNET": Mainnet
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
