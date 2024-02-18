#!/usr/bin/env python3

# Copyright © 2020-2024, Meheret Tesfaye Batu <meherett.batu@gmail.com>
# Distributed under the MIT software license, see the accompanying
# file COPYING or https://opensource.org/license/mit

from typing import Tuple

from ..utils import (
    indexes_to_path, index_tuple_to_integer
)
from .iderivation import IDerivation


class ElectrumDerivation(IDerivation):

    _change_index: Tuple[int, bool]
    _address_index: Tuple[int, bool]

    def __init__(
        self, change_index: int = 0, address_index: int = 0
    ) -> None:
        super(ElectrumDerivation, self).__init__()

        self._change_index = (change_index, False)
        self._address_index = (address_index, False)
        self._indexes = [
            index_tuple_to_integer(index=self._change_index),
            index_tuple_to_integer(index=self._address_index)
        ]
        self._path = indexes_to_path(indexes=self._indexes)

    @classmethod
    def name(cls) -> str:
        return "Electrum"

    def from_change_index(self, change_index: int) -> "ElectrumDerivation":
        self._change_index = (change_index, False)
        self._indexes[0] = index_tuple_to_integer(index=self._change_index)
        self._path = indexes_to_path(indexes=self._indexes)
        return self

    def from_address_index(self, address_index: int) -> "ElectrumDerivation":
        self._address_index = (address_index, False)
        self._indexes[1] = index_tuple_to_integer(index=self._address_index)
        self._path = indexes_to_path(indexes=self._indexes)
        return self

    def change_index(self) -> Tuple[int, bool]:
        return self._change_index

    def address_index(self) -> Tuple[int, bool]:
        return self._address_index
