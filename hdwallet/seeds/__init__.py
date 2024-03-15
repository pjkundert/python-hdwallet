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
    AlgorandSeed.name(): AlgorandSeed,
    BIP39Seed.name(): BIP39Seed,
    CardanoSeed.name(): CardanoSeed,
    ElectrumV1Seed.name(): ElectrumV1Seed,
    ElectrumV2Seed.name(): ElectrumV2Seed,
    MoneroSeed.name(): MoneroSeed
}

__all__: List[str] = ["ISeed", "SEEDS"] + [
    seed.__name__ for seed in SEEDS.values()
]
