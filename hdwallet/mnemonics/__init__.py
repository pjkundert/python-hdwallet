#!/usr/bin/env python3

# Copyright © 2020-2023, Meheret Tesfaye Batu <meherett.batu@gmail.com>
# Distributed under the MIT software license, see the accompanying
# file COPYING or https://opensource.org/license/mit

from typing import (
    List, Dict, Type
)

from ..exceptions import MnemonicError
from .algorand import (
    AlgorandMnemonic, ALGORAND_MNEMONIC_WORDS, ALGORAND_MNEMONIC_LANGUAGES
)
from .bip39 import (
    BIP39Mnemonic, BIP39_MNEMONIC_WORDS, BIP39_MNEMONIC_LANGUAGES
)
from .electrum import (
    ElectrumV1Mnemonic, ELECTRUM_V1_MNEMONIC_WORDS, ELECTRUM_V1_MNEMONIC_LANGUAGES,
    ElectrumV2Mnemonic, ELECTRUM_V2_MNEMONIC_WORDS, ELECTRUM_V2_MNEMONIC_LANGUAGES, ELECTRUM_V2_MNEMONIC_TYPES
)
from .monero import (
    MoneroMnemonic, MONERO_MNEMONIC_WORDS, MONERO_MNEMONIC_LANGUAGES
)
from .imnemonic import IMnemonic


class MNEMONICS:

    dictionary: Dict[str, Type[IMnemonic]] = {
        AlgorandMnemonic.name(): AlgorandMnemonic,
        BIP39Mnemonic.name(): BIP39Mnemonic,
        ElectrumV1Mnemonic.name(): ElectrumV1Mnemonic,
        ElectrumV2Mnemonic.name(): ElectrumV2Mnemonic,
        MoneroMnemonic.name(): MoneroMnemonic
    }

    @classmethod
    def names(cls) -> List[str]:
        return list(cls.dictionary.keys())

    @classmethod
    def classes(cls) -> List[Type[IMnemonic]]:
        return list(cls.dictionary.values())

    @classmethod
    def mnemonic(cls, name: str) -> Type[IMnemonic]:

        if not cls.is_mnemonic(name=name):
            raise MnemonicError(
                "Invalid mnemonic name", expected=cls.names(), got=name
            )

        return cls.dictionary[name]

    @classmethod
    def is_mnemonic(cls, name) -> bool:
        return name in cls.names()


__all__: List[str] = [
    "IMnemonic",
    "ALGORAND_MNEMONIC_WORDS", "ALGORAND_MNEMONIC_LANGUAGES",
    "BIP39_MNEMONIC_WORDS", "BIP39_MNEMONIC_LANGUAGES",
    "ELECTRUM_V1_MNEMONIC_WORDS", "ELECTRUM_V1_MNEMONIC_LANGUAGES",
    "ELECTRUM_V2_MNEMONIC_WORDS", "ELECTRUM_V2_MNEMONIC_LANGUAGES", "ELECTRUM_V2_MNEMONIC_TYPES",
    "MONERO_MNEMONIC_WORDS", "MONERO_MNEMONIC_LANGUAGES",
    "MNEMONICS"
] + [
    cls.__name__ for cls in MNEMONICS.classes()
]
