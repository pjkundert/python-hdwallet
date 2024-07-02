#!/usr/bin/env python3

# Copyright © 2020-2024, Meheret Tesfaye Batu <meherett.batu@gmail.com>
# Distributed under the MIT software license, see the accompanying
# file COPYING or https://opensource.org/license/mit

from typing import (
    Union, Tuple
)

from ..utils import (
    normalize_index, normalize_derivation, index_tuple_to_string
)
from .iderivation import IDerivation


class ElectrumDerivation(IDerivation):

    _change: Union[Tuple[int, bool], Tuple[int, int, bool]]
    _address: Union[Tuple[int, bool], Tuple[int, int, bool]]

    def __init__(
        self, change: Union[str, int, Tuple[int, int]] = 0, address: Union[str, int, Tuple[int, int]] = 0
    ) -> None:
        super(ElectrumDerivation, self).__init__()

        self._change = normalize_index(index=change, hardened=False)
        self._address = normalize_index(index=address, hardened=False)
        self._path, self._indexes, self._derivations = normalize_derivation(path=(
            f"m/{index_tuple_to_string(index=self._change)}/"
            f"{index_tuple_to_string(index=self._address)}"
        ))

    @classmethod
    def name(cls) -> str:
        """
        Get the name of the derivation class.

        :return: The name of the derivation class.
        :rtype: str

        >>> from hdwallet.derivations.custom import CustomDerivation
        >>> derivation: CustomDerivation = CustomDerivation(electrum="...")
        >>> derivation.name()
        "Electrum"
        """

        return "Electrum"

    def from_change(self, change: Union[str, int, Tuple[int, int]]) -> "ElectrumDerivation":
        self._change = normalize_index(index=change, hardened=False)
        self._path, self._indexes, self._derivations = normalize_derivation(path=(
            f"m/{index_tuple_to_string(index=self._change)}/"
            f"{index_tuple_to_string(index=self._address)}"
        ))
        return self

    def from_address(self, address: Union[str, int, Tuple[int, int]]) -> "ElectrumDerivation":
        self._address = normalize_index(index=address, hardened=False)
        self._path, self._indexes, self._derivations = normalize_derivation(path=(
            f"m/{index_tuple_to_string(index=self._change)}/"
            f"{index_tuple_to_string(index=self._address)}"
        ))
        return self

    def clean(self) -> "ElectrumDerivation":
        self._change = normalize_index(index=0, hardened=False)
        self._address = normalize_index(index=0, hardened=False)
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
