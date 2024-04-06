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
        super(ElectrumDerivation, self).__init__()

        self._change = (*change, False) if isinstance(change, tuple) else (change, False)
        self._address = (*address, False) if isinstance(address, tuple) else (address, False)
        self._path, self._indexes, self._derivations = normalize_derivation(path=(
            f"m/{index_tuple_to_string(index=self._change)}/"
            f"{index_tuple_to_string(index=self._address)}"
        ))

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

    def clean(self) -> "ElectrumDerivation":
        self._change = (0, False)
        self._address = (0, False)
        self._path, self._indexes, self._derivations = normalize_derivation(path=(
            f"m/{index_tuple_to_string(index=self._change)}/"
            f"{index_tuple_to_string(index=self._address)}"
        ))
        return self

    def change(self) -> int:
        return (
            self._change[1] if len(self._change) == 3 else self._change[0]
        )

    def address(self) -> int:
        return (
            self._address[1] if len(self._address) == 3 else self._address[0]
        )
