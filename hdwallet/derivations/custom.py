#!/usr/bin/env python3

# Copyright © 2020-2024, Meheret Tesfaye Batu <meherett.batu@gmail.com>
# Distributed under the MIT software license, see the accompanying
# file COPYING or https://opensource.org/license/mit

from typing import (
    Optional, List
)

from ..utils import normalize_derivation
from .iderivation import IDerivation


class CustomDerivation(IDerivation):

    def __init__(self, path: Optional[str] = None, indexes: Optional[List[int]] = None) -> None:
        super(CustomDerivation, self).__init__(path, indexes)

    @classmethod
    def name(cls) -> str:
        return "Custom"

    def from_path(self, path: str) -> "CustomDerivation":

        if path[0:2] != "m/":
            raise ValueError(
                f"Bad path, please insert like this type of path \"m/0'/0\"!, not: ({path})"
            )

        self._path, self._indexes, self._derivations = normalize_derivation(path=path)
        return self

    def from_indexes(self, indexes: List[int]) -> "CustomDerivation":

        if not isinstance(indexes, list):
            raise ValueError("Bad indexes, please import only list of integer numbers")

        self._path, self._indexes, self._derivations = normalize_derivation(indexes=indexes)
        return self

    def from_index(self, index: int, hardened: bool = False) -> "CustomDerivation":

        if not isinstance(index, int):
            raise ValueError("Bad index, please import only integer number")

        self._indexes.append(index + 0x80000000) if hardened else self._indexes.append(index)
        self._path += (
            (f"{index}'" if hardened else f"{index}")
            if self._path == "m/" else
            (f"/{index}'" if hardened else f"/{index}")
        )
        return self
