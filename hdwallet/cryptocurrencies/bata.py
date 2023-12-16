#!/usr/bin/env python3

# Copyright © 2020-2024, Meheret Tesfaye Batu <meherett.batu@gmail.com>
# Distributed under the MIT software license, see the accompanying
# file COPYING or https://opensource.org/license/mit

from typing import List

from ..ecc import SLIP10Secp256k1
from .icryptocurrency import (
    ICryptocurrency, INetworks, INetwork, CoinType, ExtendedPrivateKey, ExtendedPublicKey
)


class Mainnet(INetwork):

    PUBLIC_KEY_ADDRESS_PREFIX = 0x19
    SCRIPT_ADDRESS_PREFIX = 0x5
    SEGWIT_ADDRESS_PREFIX = None   
    EXTENDED_PRIVATE_KEY = ExtendedPrivateKey({
        "P2PKH": 0xa40b91bd,
        "P2SH": 0xa40b91bd,
        "P2WPKH": None,
        "P2WPKH_IN_P2SH": None,
        "P2WSH": None,
        "P2WSH_IN_P2SH": None
    })
    EXTENDED_PUBLIC_KEY = ExtendedPublicKey({
        "P2PKH": 0xa40c86fa,
        "P2SH": 0xa40c86fa,
        "P2WPKH": None,
        "P2WPKH_IN_P2SH": None,
        "P2WSH": None,
        "P2WSH_IN_P2SH": None
    })
    MESSAGE_PREFIX = "\x18Bata Signed Message:\n"
    WIF_PREFIX = 0xa4


class Networks(INetworks):

    MAINNET = Mainnet

    @classmethod
    def networks(cls) -> List[str]:
        return ["mainnet"]


class Bata(ICryptocurrency):

    NAME = "Bata"
    SYMBOL = "BTA"
    SOURCE_CODE = None
    ECC = SLIP10Secp256k1
    COIN_TYPE = CoinType({
        "INDEX": 89,
        "HARDENED": True
    })
    NETWORKS = Networks
