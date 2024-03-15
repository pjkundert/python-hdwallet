#!/usr/bin/env python3

# Copyright © 2020-2023, Meheret Tesfaye Batu <meherett.batu@gmail.com>
# Distributed under the MIT software license, see the accompanying
# file COPYING or https://opensource.org/license/mit

from typing import (
    List, Dict, Type
)

from .imnemonic import IMnemonic
from .algorand import (
    AlgorandMnemonic, ALGORAND_MNEMONIC_WORDS, ALGORAND_MNEMONIC_LANGUAGES
)
from .bip39 import (
    BIP39Mnemonic, BIP39_MNEMONIC_WORDS, BIP39_MNEMONIC_LANGUAGES
)
from .electrum.v1 import (
    ElectrumV1Mnemonic, ELECTRUM_V1_MNEMONIC_WORDS, ELECTRUM_V1_MNEMONIC_LANGUAGES
)
from .electrum.v2 import (
    ElectrumV2Mnemonic, ELECTRUM_V2_MNEMONIC_WORDS, ELECTRUM_V2_MNEMONIC_LANGUAGES, ELECTRUM_V2_MNEMONIC_TYPES
)
from .monero import (
    MoneroMnemonic, MONERO_MNEMONIC_WORDS, MONERO_MNEMONIC_LANGUAGES
)

MNEMONICS: Dict[str, Type[IMnemonic]] = {
    AlgorandMnemonic.name(): AlgorandMnemonic,
    BIP39Mnemonic.name(): BIP39Mnemonic,
    ElectrumV1Mnemonic.name(): ElectrumV1Mnemonic,
    ElectrumV2Mnemonic.name(): ElectrumV2Mnemonic,
    MoneroMnemonic.name(): MoneroMnemonic
}

__all__: List[str] = [
    "IMnemonic",
    "ALGORAND_MNEMONIC_WORDS", "ALGORAND_MNEMONIC_LANGUAGES",
    "BIP39_MNEMONIC_WORDS", "BIP39_MNEMONIC_LANGUAGES",
    "ELECTRUM_V1_MNEMONIC_WORDS", "ELECTRUM_V1_MNEMONIC_LANGUAGES",
    "ELECTRUM_V2_MNEMONIC_WORDS", "ELECTRUM_V2_MNEMONIC_LANGUAGES", "ELECTRUM_V2_MNEMONIC_TYPES",
    "MONERO_MNEMONIC_WORDS", "MONERO_MNEMONIC_LANGUAGES",
    "MNEMONICS"
] + [
    mnemonic.__name__ for mnemonic in MNEMONICS.values()
]
