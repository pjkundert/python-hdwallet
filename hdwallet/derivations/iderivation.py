#!/usr/bin/env python3

# Copyright © 2020-2024, Meheret Tesfaye Batu <meherett.batu@gmail.com>
# Distributed under the MIT software license, see the accompanying
# file COPYING or https://opensource.org/license/mit

from typing import (
    Optional, List
)

from ..utils import (
    path_to_indexes, indexes_to_path
)


class IDerivation:

    _path: str
    _indexes: List[int]

    def __init__(
        self, path: Optional[str] = None, indexes: Optional[List[int]] = None
    ) -> None:

        if (path and not indexes) or path:
            self._indexes = path_to_indexes(path=path)
            self._path = path
        elif (not path and indexes) or indexes:
            self._path = indexes_to_path(indexes=indexes)
            self._indexes = indexes
        else:
            self._path: str = "m/"
            self._indexes: List[int] = []

    def __str__(self) -> str:
        return self._path

    @classmethod
    def name(cls) -> str:
        pass

    def path(self) -> str:
        return self._path

    def indexes(self) -> List[int]:
        return self._indexes
