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
    SCRIPT_ADDRESS_PREFIX = 0x3f
    SEGWIT_ADDRESS_PREFIX = None
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
    MESSAGE_PREFIX = "\x18Blocknode Signed Message:\n"
    WIF_PREFIX = 0x4b


class Testnet(INetwork):

    PUBLIC_KEY_ADDRESS_PREFIX = 0x55
    SCRIPT_ADDRESS_PREFIX = 0x7d
    SEGWIT_ADDRESS_PREFIX = None
    EXTENDED_PRIVATE_KEY = ExtendedPrivateKey({
        "P2PKH": 0x4358394,
        "P2SH": 0x4358394,
        "P2WPKH": None,
        "P2WPKH_IN_P2SH": None,
        "P2WSH": None,
        "P2WSH_IN_P2SH": None
    })
    EXTENDED_PUBLIC_KEY = ExtendedPublicKey({
        "P2PKH": 0x43587cf,
        "P2SH": 0x43587cf,
        "P2WPKH": None,
        "P2WPKH_IN_P2SH": None,
        "P2WSH": None,
        "P2WSH_IN_P2SH": None
    })
    MESSAGE_PREFIX = "\x18Blocknode Testnet Signed Message:\n"
    WIF_PREFIX = 0x89


class Networks(INetworks):

    MAINNET = Mainnet
    TESTNET = Testnet

    @classmethod
    def networks(cls) -> List[str]:
        return ["mainnet", "testnet"]


class Blocknode(ICryptocurrency):

    NAME = "Blocknode"
    SYMBOL = "BND"
    SOURCE_CODE = None
    ECC = SLIP10Secp256k1
    COIN_TYPE = CoinType({
        "INDEX": 2941,
        "HARDENED": True
    })
    NETWORKS = Networks
