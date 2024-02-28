#!/usr/bin/env python3

# Copyright © 2020-2024, Meheret Tesfaye Batu <meherett.batu@gmail.com>
# Distributed under the MIT software license, see the accompanying
# file COPYING or https://opensource.org/license/mit

from ..ecc import SLIP10Ed25519ECC
from ..const import (
    CoinType, Entropies, Mnemonics, Seeds, HDs, Addresses, Networks, XPrivateKeyVersions, XPublicKeyVersions
)
from .icryptocurrency import (
    ICryptocurrency, INetwork
)


class Mainnet(INetwork):

    XPRIVATE_KEY_VERSIONS = XPrivateKeyVersions({
        "P2PKH": 0x0488ade4
    })
    XPUBLIC_KEY_VERSIONS = XPublicKeyVersions({
        "P2PKH": 0x0488b21e
    })


class Algorand(ICryptocurrency):

    NAME = "Algorand"
    SYMBOL = "ALGO"
    SOURCE_CODE = "https://github.com/algorand/go-algorand"
    ECC = SLIP10Ed25519ECC
    COIN_TYPE = CoinType({
        "INDEX": 283,
        "HARDENED": True
    })
    NETWORKS = Networks({
        "MAINNET": Mainnet
    })
    DEFAULT_NETWORK = NETWORKS.MAINNET
    ENTROPIES = Entropies((
        {"ALGORAND": "Algorand"}, "BIP39"
    ))
    MNEMONICS = Mnemonics((
        {"ALGORAND": "Algorand"}, "BIP39"
    ))
    SEEDS = Seeds((
        {"ALGORAND": "Algorand"}, "BIP39"
    ))
    HDS = HDs({
        "BIP32", "BIP32"
    })
    DEFAULT_HD = HDS.BIP32
    ADDRESSES = Addresses({
        "ALGORAND": "Algorand"
    })
    DEFAULT_ADDRESS = ADDRESSES.ALGORAND
