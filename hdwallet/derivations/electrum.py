#!/usr/bin/env python3

# Copyright © 2020-2024, Meheret Tesfaye Batu <meherett.batu@gmail.com>
# Distributed under the MIT software license, see the accompanying
# file COPYING or https://opensource.org/license/mit

from typing import (
    Union, Tuple
)

from ..utils import (
    normalize_derivation, index_tuple_to_string
)
from .iderivation import IDerivation


class ElectrumDerivation(IDerivation):

    _change: Union[Tuple[int, bool], Tuple[int, int, bool]]
    _address: Union[Tuple[int, bool], Tuple[int, int, bool]]

    def __init__(
        self, change: Union[int, Tuple[int, int]] = 0, address: Union[int, Tuple[int, int]] = 0
    ) -> None:

        self._change = (*change, False) if isinstance(change, tuple) else (change, False)
        self._address = (*address, False) if isinstance(address, tuple) else (address, False)
        self._path, self._indexes, self._derivations = normalize_derivation(path=(
            f"m/{index_tuple_to_string(index=self._change)}/"
            f"{index_tuple_to_string(index=self._address)}"
        ))
        super(ElectrumDerivation, self).__init__(path=self._path)

    @classmethod
    def name(cls) -> str:
        return "Electrum"

    def from_change(self, change: Union[int, Tuple[int, int]]) -> "ElectrumDerivation":
        self._change = (*change, False) if isinstance(change, tuple) else (change, False)
        self._path, self._indexes, self._derivations = normalize_derivation(path=(
            f"m/{index_tuple_to_string(index=self._change)}/"
            f"{index_tuple_to_string(index=self._address)}"
        ))
        return self

    def from_address(self, address: Union[int, Tuple[int, int]]) -> "ElectrumDerivation":
        self._address = (*address, False) if isinstance(address, tuple) else (address, False)
        self._path, self._indexes, self._derivations = normalize_derivation(path=(
            f"m/{index_tuple_to_string(index=self._change)}/"
            f"{index_tuple_to_string(index=self._address)}"
        ))
        return self

    def change(self) -> Union[Tuple[int, bool], Tuple[int, int, bool]]:
        return self._change

    def address(self) -> Union[Tuple[int, bool], Tuple[int, int, bool]]:
        return self._address
