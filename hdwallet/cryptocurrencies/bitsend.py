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

    PUBLIC_KEY_ADDRESS_PREFIX = 0x66
    SCRIPT_ADDRESS_PREFIX = 0x5
    XPRIVATE_KEY_VERSIONS = XPrivateKeyVersions({
        "P2PKH": 0x488ade4,
        "P2SH": 0x488ade4
    })
    XPUBLIC_KEY_VERSIONS = XPublicKeyVersions({
        "P2PKH": 0x488b21e,
        "P2SH": 0x488b21e
    })
    MESSAGE_PREFIX = "\x18Bitsend Signed Message:\n"
    WIF_PREFIX = 0xcc


class BitSend(ICryptocurrency):

    NAME = "Bit Send"
    SYMBOL = "BSD"
    INFO = Info({
        "SOURCE_CODE": "https://github.com/LIMXTEC/BitSend",
        "WHITEPAPER": "https://github.com/LIMXTEC/BitSend/releases/download/v0.14.0.5/Z.bitsend_whitePaper.Dec_17.pdf",
        "WEBSITES": [
            "https://bitsend.cc",
            "http://www.mybitsend.com"
        ]
    })
    ECC = SLIP10Secp256k1ECC
    COIN_TYPE = 91
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
