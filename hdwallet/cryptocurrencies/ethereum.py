#!/usr/bin/env python3

# Copyright © 2020-2024, Meheret Tesfaye Batu <meherett.batu@gmail.com>
# Distributed under the MIT software license, see the accompanying
# file COPYING or https://opensource.org/license/mit

from ..ecc import SLIP10Secp256k1ECC
from ..const import (
    Info, Entropies, Mnemonics, Seeds, HDs, Addresses, Networks, Params, XPrivateKeyVersions, XPublicKeyVersions
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
    WIF_PREFIX = 0x80


class Ethereum(ICryptocurrency):

    NAME = "Ethereum"
    SYMBOL = "ETH"
    INFO = Info({
        "SOURCE_CODE": "https://github.com/ethereum/go-ethereum",
        "WHITEPAPER": "https://github.com/ethereum/wiki/wiki/White-Paper",
        "WEBSITES": [
            "https://www.ethereum.org",
            "https://en.wikipedia.org/wiki/Ethereum"
        ]
    })
    ECC = SLIP10Secp256k1ECC
    COIN_TYPE = 60
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
        "ETHEREUM": "Ethereum"
    })
    DEFAULT_ADDRESS = ADDRESSES.ETHEREUM
    PARAMS = Params({
        "ADDRESS_PREFIX": "0x"
    })
