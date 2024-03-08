#!/usr/bin/env python3

# Copyright © 2020-2024, Meheret Tesfaye Batu <meherett.batu@gmail.com>
# Distributed under the MIT software license, see the accompanying
# file COPYING or https://opensource.org/license/mit

from typing import (
    List, Dict, Type
)

from .iderivation import IDerivation
from .bip44 import BIP44Derivation
from .bip49 import BIP49Derivation
from .bip84 import BIP84Derivation
from .bip86 import BIP86Derivation
from .cip1852 import CIP1852Derivation
from .custom import CustomDerivation
from .electrum import ElectrumDerivation

DERIVATIONS: Dict[str, Type[IDerivation]] = {
    "BIP44": BIP44Derivation,
    "BIP49": BIP49Derivation,
    "BIP84": BIP84Derivation,
    "BIP86": BIP86Derivation,
    "CIP1852": CIP1852Derivation,
    "Custom": CustomDerivation,
    "Electrum": ElectrumDerivation
}

__all__: List[Type[IDerivation]] = DERIVATIONS.values()
