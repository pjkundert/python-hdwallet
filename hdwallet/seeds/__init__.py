#!/usr/bin/env python3

# Copyright © 2020-2024, Meheret Tesfaye Batu <meherett.batu@gmail.com>
# Distributed under the MIT software license, see the accompanying
# file COPYING or https://opensource.org/license/mit

from typing import (
    List, Dict, Type
)

from .iseed import ISeed
from ..exceptions import SeedError
from .algorand import AlgorandSeed
from .bip39 import BIP39Seed
from .cardano import CardanoSeed
from .electrum import (
    ElectrumV1Seed, ElectrumV2Seed
)
from .monero import MoneroSeed


class SEEDS:

    dictionary: Dict[str, Type[ISeed]] = {
        AlgorandSeed.name(): AlgorandSeed,
        BIP39Seed.name(): BIP39Seed,
        CardanoSeed.name(): CardanoSeed,
        ElectrumV1Seed.name(): ElectrumV1Seed,
        ElectrumV2Seed.name(): ElectrumV2Seed,
        MoneroSeed.name(): MoneroSeed
    }

    @classmethod
    def names(cls) -> List[str]:
        return list(cls.dictionary.keys())

    @classmethod
    def classes(cls) -> List[Type[ISeed]]:
        return list(cls.dictionary.values())

    @classmethod
    def seed(cls, name: str) -> Type[ISeed]:

        if not cls.is_seed(name=name):
            raise SeedError(
                "Invalid seed name", expected=cls.names(), got=name
            )

        return cls.dictionary[name]

    @classmethod
    def is_seed(cls, name) -> bool:
        return name in cls.names()


__all__: List[str] = [
    "ISeed", "SEEDS"
] + [
    cls.__name__ for cls in SEEDS.classes()
]
