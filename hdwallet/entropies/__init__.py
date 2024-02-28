#!/usr/bin/env python3

# Copyright © 2020-2024, Meheret Tesfaye Batu <meherett.batu@gmail.com>
# Distributed under the MIT software license, see the accompanying
# file COPYING or https://opensource.org/license/mit

from typing import (
    List, Dict, Type
)

from .ientropy import IEntropy
from .algorand import (
    AlgorandEntropy, ALGORAND_ENTROPY_STRENGTHS
)
from .bip39 import (
    BIP39Entropy, BIP39_ENTROPY_STRENGTHS
)
from .electrum.v1 import (
    ElectrumV1Entropy, ELECTRUM_V1_ENTROPY_STRENGTHS
)
from .electrum.v2 import (
    ElectrumV2Entropy, ELECTRUM_V2_ENTROPY_STRENGTHS
)
from .monero import (
    MoneroEntropy, MONERO_ENTROPY_STRENGTHS
)


ENTROPIES: Dict[str, Type[IEntropy]] = {
    "Algorand": AlgorandEntropy,
    "BIP39": BIP39Entropy,
    "Electrum-V1": ElectrumV1Entropy,
    "Electrum-V2": ElectrumV2Entropy,
    "Monero": MoneroEntropy
}

__all__: List[str] = [
    "IEntropy",
    "AlgorandEntropy", "ALGORAND_ENTROPY_STRENGTHS",
    "BIP39Entropy", "BIP39_ENTROPY_STRENGTHS",
    "ElectrumV1Entropy", "ELECTRUM_V1_ENTROPY_STRENGTHS",
    "ElectrumV2Entropy", "ELECTRUM_V2_ENTROPY_STRENGTHS",
    "MoneroEntropy", "MONERO_ENTROPY_STRENGTHS",
    "ENTROPIES"
]
