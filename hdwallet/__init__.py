#!/usr/bin/env python3

# Copyright © 2020-2024, Meheret Tesfaye Batu <meherett.batu@gmail.com>
# Distributed under the MIT software license, see the accompanying
# file COPYING or https://opensource.org/license/mit

from .hdwallet import HDWallet

__version__: str = "v3.0.0"
__license__: str = "MIT"
__author__: str = "Meheret Tesfaye Batu"
__email__: str = "meherett.batu@gmail.com"
__documentation__: str = "https://hdwallet.readthedocs.com"
__description__: str = "Python-based library for the implementation of a hierarchical deterministic wallet " \
                       "generator for more than 150+ multiple cryptocurrencies."
__website__: str = "https://hdwallet.online"


__all__: list = [
    "__version__",
    "__license__",
    "__author__",
    "__email__",
    "__documentation__",
    "__description__",
    "__website__",
    "HDWallet"
]
