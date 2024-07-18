#!/usr/bin/env python3

# Copyright © 2020-2024, Meheret Tesfaye Batu <meherett.batu@gmail.com>
# Distributed under the MIT software license, see the accompanying
# file COPYING or https://opensource.org/license/mit

from typing import List

__name__: str = "hdwallet"
__versions__: dict = {
    __name__: "v3.0.0a9",
    "desktop": "v0.1.0b1"
}
__license__: str = "MIT"
__author__: str = "Meheret Tesfaye Batu"
__email__: str = "meherett.batu@gmail.com"
__documentation__: str = "https://hdwallet.readthedocs.com"
__description__: str = "Python-based library for the implementation of a hierarchical deterministic wallet " \
                       "generator for more than 205+ multiple cryptocurrencies."
__url__: str = "https://github.com/meherett/python-hdwallet"
__tracker__: str = f"{__url__}/issues"
__keywords__: List[str] = [
    "ecc", "kholaw", "slip10", "ed25519", "nist256p1", "secp256k1"  # ECC keywords
    "hd", "bip32", "bip44", "bip49", "bip84", "bip86", "bip141", "monero", "cardano",  # HD keywords
    "entropy", "mnemonic", "seed", "bip39", "algorand", "electrum"  # Entropy, Mnemonic and Seed keywords
    "cryptocurrencies", "bitcoin", "ethereum", "cryptography", "cli", "cip1852"  # Other keywords
]
__websites__: List[str] = [
    "https://hdwallet.io",
    "https://hdwallet.online",
    "https://hd.wallet"  # On Web3 browsers like Brave
]
