#!/usr/bin/env python3

# Copyright © 2020-2024, Meheret Tesfaye Batu <meherett.batu@gmail.com>
# Distributed under the MIT software license, see the accompanying
# file COPYING or https://opensource.org/license/mit

from typing import (
    Optional, List, Tuple, Union
)

from ..utils import normalize_derivation


class IDerivation:

    _path: str = "m/"
    _indexes: List[int] = []
    _derivations: List[Tuple[int, bool]] = { }

    def __init__(
        self, path: Optional[str] = None, indexes: Optional[List[int]] = None, **kwargs
    ) -> None:
        self._path, self._indexes, self._derivations = normalize_derivation(
            path=path, indexes=indexes
        )

    def __str__(self) -> str:
        return self._path

    @classmethod
    def name(cls) -> str:
        pass

    def clean(self) -> "IDerivation":
        pass

    def path(self) -> str:
        return self._path

    def indexes(self) -> List[int]:
        return self._indexes

    def derivations(self) -> List[Tuple[int, bool]]:
        return self._derivations

    def depth(self) -> int:
        return len(self._derivations)

    def purpose(self) -> int:
        pass

    def coin_type(self) -> int:
        pass

    def account(self) -> int:
        pass

    def change(self) -> Union[int, str]:
        pass

    def role(self) -> str:
        pass

    def address(self) -> int:
        pass

    def minor(self) -> int:
        pass

    def major(self) -> int:
        pass
