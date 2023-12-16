#!/usr/bin/env python3

# Copyright © 2020-2024, Meheret Tesfaye Batu <meherett.batu@gmail.com>
# Distributed under the MIT software license, see the accompanying
# file COPYING or https://opensource.org/license/mit

from typing import List

from ..ecc import SLIP10Secp256k1
from .icryptocurrency import (
    ICryptocurrency, INetworks, INetwork, CoinType, ExtendedPrivateKey, ExtendedPublicKey, SegwitAddress
)


class Mainnet(INetwork):

    PUBLIC_KEY_ADDRESS_PREFIX = 0x3
    SCRIPT_ADDRESS_PREFIX = 0x7d
    SEGWIT_ADDRESS = SegwitAddress({
        "HRP": "bitcore",
        "VERSION": 0x00
    })
    EXTENDED_PRIVATE_KEY = ExtendedPrivateKey({
        "P2PKH": 0x488ade4,
        "P2SH": 0x488ade4,
        "P2WPKH": 0x488ade4,
        "P2WPKH_IN_P2SH": 0x488ade4,
        "P2WSH": None,
        "P2WSH_IN_P2SH": None
    })
    EXTENDED_PUBLIC_KEY = ExtendedPublicKey({
        "P2PKH": 0x488b21e,
        "P2SH": 0x488b21e,
        "P2WPKH": 0x488b21e,
        "P2WPKH_IN_P2SH": 0x488b21e,
        "P2WSH": None,
        "P2WSH_IN_P2SH": None
    })
    MESSAGE_PREFIX = "\x18BitCore Signed Message:\n"
    WIF_PREFIX = 0x80


class Networks(INetworks):

    MAINNET = Mainnet

    @classmethod
    def networks(cls) -> List[str]:
        return ["mainnet"]


class Bitcore(ICryptocurrency):

    NAME = "Bitcore"
    SYMBOL = "BTX"
    SOURCE_CODE = None
    ECC = SLIP10Secp256k1
    COIN_TYPE = CoinType({
        "INDEX": 160,
        "HARDENED": True
    })
    NETWORKS = Networks
