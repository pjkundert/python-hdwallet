#!/usr/bin/env python3

# Copyright © 2020-2024, Meheret Tesfaye Batu <meherett.batu@gmail.com>
# Distributed under the MIT software license, see the accompanying
# file COPYING or https://opensource.org/license/mit

from typing import (
    List, Dict, Type
)

from ..exceptions import HDError
from .bip32 import BIP32HD
from .bip44 import BIP44HD
from .bip49 import BIP49HD
from .bip84 import BIP84HD
from .bip86 import BIP86HD
from .bip141 import BIP141HD
from .cardano import CardanoHD
from .electrum import (
    ElectrumV1HD, ElectrumV2HD
)
from .monero import MoneroHD
from .ihd import IHD


class HDS:

    dictionary: Dict[str, Type[IHD]] = {
        BIP32HD.name(): BIP32HD,
        BIP44HD.name(): BIP44HD,
        BIP49HD.name(): BIP49HD,
        BIP84HD.name(): BIP84HD,
        BIP86HD.name(): BIP86HD,
        BIP141HD.name(): BIP141HD,
        CardanoHD.name(): CardanoHD,
        ElectrumV1HD.name(): ElectrumV1HD,
        ElectrumV2HD.name(): ElectrumV2HD,
        MoneroHD.name(): MoneroHD
    }

    @classmethod
    def names(cls) -> List[str]:
        return list(cls.dictionary.keys())

    @classmethod
    def classes(cls) -> List[Type[IHD]]:
        return list(cls.dictionary.values())

    @classmethod
    def hd(cls, name: str) -> Type[IHD]:

        if not cls.is_hd(name=name):
            raise HDError(
                "Invalid HD name", expected=cls.names(), got=name
            )

        return cls.dictionary[name]

    @classmethod
    def is_hd(cls, name: str) -> bool:
        return name in cls.names()


__all__: List[str] = [
    "IHD", "HDS"
] + [
    cls.__name__ for cls in HDS.classes()
]
