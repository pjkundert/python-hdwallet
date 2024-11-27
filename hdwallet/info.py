#!/usr/bin/env python3

# Copyright © 2020-2024, Meheret Tesfaye Batu <meherett.batu@gmail.com>
# Distributed under the MIT software license, see the accompanying
# file COPYING or https://opensource.org/license/mit

from typing import List

__name__: str = "hdwallet"
__version__: str = "v3.0.1"
__license__: str = "MIT"
__author__: str = "Meheret Tesfaye Batu"
__email__: str = "meherett.batu@gmail.com"
__documentation__: str = "https://hdwallet.readthedocs.com"
__description__: str = "Python-based library for the implementation of a Hierarchical Deterministic (HD) Wallet generator supporting more than 200 cryptocurrencies."
__source__: str = "https://github.com/talonlab/python-hdwallet"
__url__: str = "https://hdwallet.io"
__tracker__: str = f"{__source__}/issues"
__keywords__: List[str] = [
    "ecc", "kholaw", "slip10", "ed25519", "nist256p1", "secp256k1",  # ECC keywords
    "hd", "bip32", "bip44", "bip49", "bip84", "bip86", "bip141", "monero", "cardano",  # HD keywords
    "entropy", "mnemonic", "seed", "bip39", "algorand", "electrum",  # Entropy, Mnemonic and Seed keywords
    "cryptocurrencies", "bitcoin", "ethereum", "cryptography", "cli", "cip1852"  # Other keywords
]
__websites__: List[str] = [
    __url__,
    "https://hdwallet.online",
    "https://hd.wallet"  # On Web3 browsers like Brave
]
