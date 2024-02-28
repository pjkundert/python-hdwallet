#!/usr/bin/env python3

# Copyright © 2020-2024, Meheret Tesfaye Batu <meherett.batu@gmail.com>
# Distributed under the MIT software license, see the accompanying
# file COPYING or https://opensource.org/license/mit

from ..ecc import KholawEd25519ECC
from ..const import (
    CARDANO_TYPES, CoinType, Entropies, Mnemonics, Seeds, HDs, Addresses, Networks, Params, XPrivateKeyVersions, XPublicKeyVersions
)
from .icryptocurrency import (
    ICryptocurrency, INetwork
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


class Cardano(ICryptocurrency):

    NAME = "Cardano"
    SYMBOL = "ADA"
    SOURCE_CODE = "https://github.com/cardano-foundation/cardano-wallet"
    ECC = KholawEd25519ECC
    COIN_TYPE = CoinType({
        "INDEX": 1815,
        "HARDENED": True
    })
    TYPES = CARDANO_TYPES
    NETWORKS = Networks({
        "MAINNET": Mainnet, "TESTNET": Testnet
    })
    DEFAULT_NETWORK = NETWORKS.MAINNET
    ENTROPIES = Entropies({
        "BIP39"
    })
    MNEMONICS = Mnemonics({
        "BIP39"
    })
    SEEDS = Seeds((
        {"CARDANO": "Cardano"}, "BIP39"
    ))
    HDS = HDs({
        "CARDANO": "Cardano"
    })
    DEFAULT_HD = HDS.CARDANO
    ADDRESSES = Addresses({
        "CARDANO": "Cardano"
    })
    DEFAULT_ADDRESS = ADDRESSES.CARDANO
    PARAMS = Params({
        "PUBLIC_KEY_ADDRESS": 0,
        "REDEMPTION_ADDRESS": 2,
        "PAYMENT_PREFIX": 0x00,
        "REWARD_PREFIX": 0x0e,
    })
