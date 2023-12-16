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

    PUBLIC_KEY_ADDRESS_PREFIX = 0x1c
    SCRIPT_ADDRESS_PREFIX = 0x28
    SEGWIT_ADDRESS = SegwitAddress({
        "HRP": "bc",
        "VERSION": 0x00
    })
    EXTENDED_PRIVATE_KEY = ExtendedPrivateKey({
        "P2PKH": 0x0488ade4,
        "P2SH": 0x0488ade4,
        "P2WPKH": 0x04b2430c,
        "P2WPKH_IN_P2SH": 0x049d7878,
        "P2WSH": 0x02aa7a99,
        "P2WSH_IN_P2SH": 0x0295b005
    })
    EXTENDED_PUBLIC_KEY = ExtendedPublicKey({
        "P2PKH": 0x0488b21e,
        "P2SH": 0x0488b21e,
        "P2WPKH": 0x04b24746,
        "P2WPKH_IN_P2SH": 0x049d7cb2,
        "P2WSH": 0x02aa7ed3,
        "P2WSH_IN_P2SH": 0x0295b43f
    })
    MESSAGE_PREFIX = None
    WIF_PREFIX = 0x80


class Networks(INetworks):

    MAINNET = Mainnet

    @classmethod
    def networks(cls) -> List[str]:
        return ["mainnet"]


class BitcoinCash(ICryptocurrency):

    NAME = "Bitcoin Cash"
    SYMBOL = "BCH"
    SOURCE_CODE = "https://github.com/bitcoincashorg/bitcoincash.org"
    ECC = SLIP10Secp256k1
    COIN_TYPE = CoinType({
        "INDEX": 145,
        "HARDENED": True
    })
    NETWORKS = Networks
