#!/usr/bin/env python3

# Copyright © 2020-2024, Meheret Tesfaye Batu <meherett.batu@gmail.com>
# Distributed under the MIT software license, see the accompanying
# file COPYING or https://opensource.org/license/mit

from typing import (
    List, Dict, Type
)

from .iseed import ISeed
from .algorand import AlgorandSeed
from .bip39 import BIP39Seed
from .cardano import CardanoSeed
from .electrum import (
    ElectrumV1Seed, ElectrumV2Seed
)
from .monero import MoneroSeed


SEEDS: Dict[str, Type[ISeed]] = {
    "Algorand": AlgorandSeed,
    "BIP39": BIP39Seed,
    "Cardano": CardanoSeed,
    "Electrum-V1": ElectrumV1Seed,
    "Electrum-V2": ElectrumV2Seed,
    "Monero": MoneroSeed
}

__all__: List[str] = [
    "ISeed",
    "AlgorandSeed",
    "BIP39Seed",
    "CardanoSeed",
    "ElectrumV1Seed",
    "ElectrumV2Seed",
    "MoneroSeed",
    "SEEDS"
]
