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
    SCRIPT_ADDRESS_PREFIX = 0x5   
    XPRIVATE_KEY_VERSIONS = XPrivateKeyVersions({
        "P2PKH": 0xa40b91bd,
        "P2SH": 0xa40b91bd
    })
    XPUBLIC_KEY_VERSIONS = XPublicKeyVersions({
        "P2PKH": 0xa40c86fa,
        "P2SH": 0xa40c86fa
    })
    MESSAGE_PREFIX = "\x18Bata Signed Message:\n"
    WIF_PREFIX = 0xa4


class Bata(ICryptocurrency):

    NAME = "Bata"
    SYMBOL = "BTA"
    INFO = Info({
        "SOURCE_CODE": "https://github.com/BTA-BATA/Bataoshi",
        "WHITEPAPER": "https://bata.io/wp-content/uploads/2021/09/Bata-Cryptocurrency-Whitepaper.pdf",
        "WEBSITES": [
            "https://bata.io",
            "https://bata.digital"
        ]
    })
    ECC = SLIP10Secp256k1ECC
    COIN_TYPE = 89
    SUPPORT_BIP38 = True
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
