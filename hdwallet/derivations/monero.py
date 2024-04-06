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


class MoneroDerivation(IDerivation):

    _minor: Union[Tuple[int, bool], Tuple[int, int, bool]]
    _major: Union[Tuple[int, bool], Tuple[int, int, bool]]

    def __init__(
        self, minor: Union[int, Tuple[int, int]] = 1, major: Union[int, Tuple[int, int]] = 0
    ) -> None:
        super(MoneroDerivation, self).__init__()

        self._minor = (*minor, False) if isinstance(minor, tuple) else (minor, False)
        self._major = (*major, False) if isinstance(major, tuple) else (major, False)
        self._path, self._indexes, self._derivations = normalize_derivation(path=(
            f"m/{index_tuple_to_string(index=self._minor)}/"
            f"{index_tuple_to_string(index=self._major)}"
        ))

    @classmethod
    def name(cls) -> str:
        return "Monero"

    def from_minor(self, minor: Union[int, Tuple[int, int]]) -> "MoneroDerivation":
        self._minor = (*minor, False) if isinstance(minor, tuple) else (minor, False)
        self._path, self._indexes, self._derivations = normalize_derivation(path=(
            f"m/{index_tuple_to_string(index=self._minor)}/"
            f"{index_tuple_to_string(index=self._major)}"
        ))
        return self

    def from_major(self, major: Union[int, Tuple[int, int]]) -> "MoneroDerivation":
        self._major = (*major, False) if isinstance(major, tuple) else (major, False)
        self._path, self._indexes, self._derivations = normalize_derivation(path=(
            f"m/{index_tuple_to_string(index=self._minor)}/"
            f"{index_tuple_to_string(index=self._major)}"
        ))
        return self

    def clean(self) -> "MoneroDerivation":
        self._minor = (1, False)
        self._major = (0, False)
        self._path, self._indexes, self._derivations = normalize_derivation(path=(
            f"m/{index_tuple_to_string(index=self._minor)}/"
            f"{index_tuple_to_string(index=self._major)}"
        ))
        return self

    def minor(self) -> int:
        return (
            self._minor[1] if len(self._minor) == 3 else self._minor[0]
        )

    def major(self) -> int:
        return (
            self._major[1] if len(self._major) == 3 else self._major[0]
        )
