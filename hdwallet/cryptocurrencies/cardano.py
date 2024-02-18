#!/usr/bin/env python3

# Copyright © 2020-2024, Meheret Tesfaye Batu <meherett.batu@gmail.com>
# Distributed under the MIT software license, see the accompanying
# file COPYING or https://opensource.org/license/mit

from typing import List

from ..ecc import KholawEd25519
from .icryptocurrency import (
    ICryptocurrency, INetworks, INetwork, CoinType, XPrivateKeyVersions, XPublicKeyVersions, NestedNamespace
)


class Mainnet(INetwork):

    TYPE = 1
    PAYMENT_ADDRESS_HRP = "addr"
    REWARD_ADDRESS_HRP = "stake"
    XPRIVATE_KEY_VERSIONS = XPrivateKeyVersions({
        "P2PKH": 0x0f4331d4
    })
    XPUBLIC_KEY_VERSIONS = XPublicKeyVersions({
        "P2PKH": 0x0488b21e
    })


class Testnet(INetwork):

    TYPE = 0
    PAYMENT_ADDRESS_HRP = "addr_test"
    REWARD_ADDRESS_HRP = "stake_test"
    XPRIVATE_KEY_VERSIONS = XPrivateKeyVersions({
        "P2PKH": 0x0f4331d4
    })
    XPUBLIC_KEY_VERSIONS = XPublicKeyVersions({
        "P2PKH": 0x0488b21e
    })


class Networks(INetworks):

    MAINNET = Mainnet
    TESTNET = Testnet

    @classmethod
    def networks(cls) -> List[str]:
        return ["mainnet", "testnet"]


class Types(NestedNamespace):

    BYRON_ICARUS: str
    BYRON_LEDGER: str
    BYRON_LEGACY: str
    SHELLEY_ICARUS: str
    SHELLEY_LEDGER: str


class Cardano(ICryptocurrency):

    NAME = "Cardano"
    SYMBOL = "ADA"
    SOURCE_CODE = "https://github.com/cardano-foundation/cardano-wallet"
    ECC = KholawEd25519
    COIN_TYPE = CoinType({
        "INDEX": 1815,
        "HARDENED": True
    })
    NETWORKS = Networks
    ENTROPIES = [
        "BIP39"
    ]
    MNEMONICS = [
        "BIP39"
    ]
    SEEDS = [
        "Cardano", "BIP39"
    ]
    HDS = [
        "Cardano"
    ]

    PUBLIC_KEY_ADDRESS: int = 0
    REDEMPTION_ADDRESS: int = 2
    TYPES: Types = Types({
        "BYRON_ICARUS": "byron-icarus",
        "BYRON_LEDGER": "byron-ledger",
        "BYRON_LEGACY": "byron-legacy",
        "SHELLEY_ICARUS": "shelley-icarus",
        "SHELLEY_LEDGER":  "shelley-ledger"
    })
    PAYMENT_PREFIX: int = 0x00
    REWARD_PREFIX: int = 0x0e
