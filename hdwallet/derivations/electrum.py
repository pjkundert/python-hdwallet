#!/usr/bin/env python3

# Copyright © 2020-2024, Meheret Tesfaye Batu <meherett.batu@gmail.com>
# Distributed under the MIT software license, see the accompanying
# file COPYING or https://opensource.org/license/mit

from typing import (
    Union, Tuple
)

from ..utils import (
    indexes_to_path, index_tuple_to_integer
)
from .iderivation import IDerivation


class ElectrumDerivation(IDerivation):

    _change: Tuple[int, bool]
    _address: Tuple[int, bool]

    def __init__(
        self, change: int = 0, address: int = 0
    ) -> None:
        super(ElectrumDerivation, self).__init__()

        self._change = (change, False)
        self._address = (address, False)
        self._indexes = [
            index_tuple_to_integer(index=self._change),
            index_tuple_to_integer(index=self._address)
        ]
        self._path = indexes_to_path(indexes=self._indexes)

    @classmethod
    def name(cls) -> str:
        return "Electrum"

    def from_change(self, change: int) -> "ElectrumDerivation":
        self._change = (change, False)
        self._indexes[0] = index_tuple_to_integer(index=self._change)
        self._path = indexes_to_path(indexes=self._indexes)
        return self

    def from_address(self, address: int) -> "ElectrumDerivation":
        self._address = (address, False)
        self._indexes[1] = index_tuple_to_integer(index=self._address)
        self._path = indexes_to_path(indexes=self._indexes)
        return self

    def change(self, only_index=False) -> Union[Tuple[int, bool], int]:
        return self._change[0] if not only_index else self._change

    def address(self, only_index=False) -> Union[Tuple[int, bool], int]:
        return self._address[0] if not only_index else self._address
