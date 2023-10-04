#!/usr/bin/env python3

# Copyright © 2023, Meheret Tesfaye Batu <meherett.batu@gmail.com>
# Distributed under the MIT software license, see the accompanying
# file COPYING or https://opensource.org/license/mit

from typing import (
    Optional, List
)

from ..utils import (
    path_to_indexes, indexes_to_path
)
from . import IDerivation


class Derivation(IDerivation):

    def __init__(self, path: Optional[str] = None, indexes: Optional[List[int]] = None) -> None:
        super(Derivation, self).__init__(path, indexes)

    @classmethod
    def from_path(cls, path: str) -> "Derivation":
        return Derivation(
            indexes=path_to_indexes(path=path)
        )

    @classmethod
    def from_indexes(cls, indexes: List[int]) -> "Derivation":
        return Derivation(
            path=indexes_to_path(indexes=indexes)
        )

    def from_index(self, index: int, hardened: bool = False) -> "Derivation":

        if not isinstance(index, int):
            raise ValueError("Bad index, please import only integer number!")

        self._indexes.append(index + 0x80000000) if hardened else self._indexes.append(index)
        self._path += (
            (f"{index}'" if hardened else f"{index}")
            if self._path == "m/" else
            (f"/{index}'" if hardened else f"/{index}")
        )
        return self
