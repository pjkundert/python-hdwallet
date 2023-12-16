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

    PUBLIC_KEY_ADDRESS_PREFIX = 0x55
    SCRIPT_ADDRESS_PREFIX = 0x5
    SEGWIT_ADDRESS = None
    EXTENDED_PRIVATE_KEY = ExtendedPrivateKey({
        "P2PKH": 0x488ade4,
        "P2SH": 0x488ade4,
        "P2WPKH": None,
        "P2WPKH_IN_P2SH": None,
        "P2WSH": None,
        "P2WSH_IN_P2SH": None
    })
    EXTENDED_PUBLIC_KEY = ExtendedPublicKey({
        "P2PKH": 0x488b21e,
        "P2SH": 0x488b21e,
        "P2WPKH": None,
        "P2WPKH_IN_P2SH": None,
        "P2WSH": None,
        "P2WSH_IN_P2SH": None
    })
    MESSAGE_PREFIX = "Bolivarcoin Signed Message:\n"
    WIF_PREFIX = 0xd5


class Networks(INetworks):

    MAINNET = Mainnet

    @classmethod
    def networks(cls) -> List[str]:
        return ["mainnet"]


class Bolivarcoin(ICryptocurrency):

    NAME = "Bolivarcoin"
    SYMBOL = "BOLI"
    SOURCE_CODE = None
    ECC = SLIP10Secp256k1
    COIN_TYPE = CoinType({
        "INDEX": 278,
        "HARDENED": True
    })
    NETWORKS = Networks
