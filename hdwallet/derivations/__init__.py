#!/usr/bin/env python3

# Copyright © 2020-2024, Meheret Tesfaye Batu <meherett.batu@gmail.com>
# Distributed under the MIT software license, see the accompanying
# file COPYING or https://opensource.org/license/mit

from typing import (
    List, Dict, Type
)

from .iderivation import IDerivation
from .bip44 import (
    BIP44Derivation, CHANGES
)
from .bip49 import BIP49Derivation
from .bip84 import BIP84Derivation
from .bip86 import BIP86Derivation
from .cip1852 import (
    CIP1852Derivation, ROLES
)
from .custom import CustomDerivation
from .electrum import ElectrumDerivation

DERIVATIONS: Dict[str, Type[IDerivation]] = {
    BIP44Derivation.name(): BIP44Derivation,
    BIP49Derivation.name(): BIP49Derivation,
    BIP84Derivation.name(): BIP84Derivation,
    BIP86Derivation.name(): BIP86Derivation,
    CIP1852Derivation.name(): CIP1852Derivation,
    CustomDerivation.name(): CustomDerivation,
    ElectrumDerivation.name(): ElectrumDerivation
}

__all__: List[str] = ["IDerivation", "CHANGES", "ROLES", "DERIVATIONS"] + [
    derivation.__name__ for derivation in DERIVATIONS.values()
]
