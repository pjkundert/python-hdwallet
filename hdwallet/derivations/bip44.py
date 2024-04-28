#!/usr/bin/env python3

# Copyright © 2020-2024, Meheret Tesfaye Batu <meherett.batu@gmail.com>
# Distributed under the MIT software license, see the accompanying
# file COPYING or https://opensource.org/license/mit

from typing import (
    Tuple, Union, Optional, Dict
)

from ..utils import (
    normalize_index, normalize_derivation, index_tuple_to_string
)
from ..exceptions import DerivationError
from .iderivation import IDerivation


class CHANGES:

    EXTERNAL_CHAIN: str = "external-chain"
    INTERNAL_CHAIN: str = "internal-chain"


class BIP44Derivation(IDerivation):  # https://github.com/bitcoin/bips/blob/master/bip-0044.mediawiki

    _purpose: Tuple[int, bool] = (44, True)
    _coin_type: Tuple[int, bool]
    _account: Union[Tuple[int, bool], Tuple[int, int, bool]]
    _change: Tuple[int, bool]
    _address: Union[Tuple[int, bool], Tuple[int, int, bool]]
    changes: Dict[str, int] = {
        "external-chain": 0, "internal-chain": 1
    }

    def __init__(
        self,
        coin_type: Union[str, int] = 0,
        account: Union[str, int, Tuple[int, int]] = 0,
        change: Union[str, int] = "external-chain",
        address: Union[str, int, Tuple[int, int]] = 0
    ) -> None:
        super(BIP44Derivation, self).__init__()

        if change not in [*self.changes.keys(), 0, "0", 1, "1"]:
            raise DerivationError(
                f"Bad {self.name()} change index", expected=[*self.changes.keys(), 0, "0", 1, "1"], got=change
            )

        self._coin_type = normalize_index(index=coin_type, hardened=True)
        self._account = normalize_index(index=account, hardened=True)
        self._change = normalize_index(
            index=(self.changes[change] if change in self.changes.keys() else change), hardened=False
        )
        self._address = normalize_index(index=address, hardened=False)
        self._path, self._indexes, self._derivations = normalize_derivation(path=(
            f"m/{index_tuple_to_string(index=self._purpose)}/"
            f"{index_tuple_to_string(index=self._coin_type)}/"
            f"{index_tuple_to_string(index=self._account)}/"
            f"{index_tuple_to_string(index=self._change)}/"
            f"{index_tuple_to_string(index=self._address)}"
        ))

    @classmethod
    def name(cls) -> str:
        return "BIP44"

    def from_coin_type(self, coin_type: Union[str, int]) -> "BIP44Derivation":
        self._coin_type = normalize_index(index=coin_type, hardened=True)
        self._path, self._indexes, self._derivations = normalize_derivation(path=(
            f"m/{index_tuple_to_string(index=self._purpose)}/"
            f"{index_tuple_to_string(index=self._coin_type)}/"
            f"{index_tuple_to_string(index=self._account)}/"
            f"{index_tuple_to_string(index=self._change)}/"
            f"{index_tuple_to_string(index=self._address)}"
        ))
        return self

    def from_account(self, account: Union[str, int, Tuple[int, int]]) -> "BIP44Derivation":
        self._account = normalize_index(index=account, hardened=True)
        self._path, self._indexes, self._derivations = normalize_derivation(path=(
            f"m/{index_tuple_to_string(index=self._purpose)}/"
            f"{index_tuple_to_string(index=self._coin_type)}/"
            f"{index_tuple_to_string(index=self._account)}/"
            f"{index_tuple_to_string(index=self._change)}/"
            f"{index_tuple_to_string(index=self._address)}"
        ))
        return self

    def from_change(self, change: Union[str, int]) -> "BIP44Derivation":
        if change not in [*self.changes.keys(), 0, "0", 1, "1"]:
            raise DerivationError(
                f"Bad {self.name()} change index", expected=[*self.changes.keys(), 0, "0", 1, "1"], got=change
            )
        self._change = normalize_index(
            index=(self.changes[change] if change in self.changes.keys() else change), hardened=False
        )
        self._path, self._indexes, self._derivations = normalize_derivation(path=(
            f"m/{index_tuple_to_string(index=self._purpose)}/"
            f"{index_tuple_to_string(index=self._coin_type)}/"
            f"{index_tuple_to_string(index=self._account)}/"
            f"{index_tuple_to_string(index=self._change)}/"
            f"{index_tuple_to_string(index=self._address)}"
        ))
        return self

    def from_address(self, address: Union[str, int, Tuple[int, int]]) -> "BIP44Derivation":
        self._address = normalize_index(index=address, hardened=False)
        self._path, self._indexes, self._derivations = normalize_derivation(path=(
            f"m/{index_tuple_to_string(index=self._purpose)}/"
            f"{index_tuple_to_string(index=self._coin_type)}/"
            f"{index_tuple_to_string(index=self._account)}/"
            f"{index_tuple_to_string(index=self._change)}/"
            f"{index_tuple_to_string(index=self._address)}"
        ))
        return self

    def clean(self) -> "BIP44Derivation":
        self._account = normalize_index(index=0, hardened=True)
        self._change = normalize_index(index=self.changes["external-chain"], hardened=False)
        self._address = normalize_index(index=0, hardened=False)
        self._path, self._indexes, self._derivations = normalize_derivation(path=(
            f"m/{index_tuple_to_string(index=self._purpose)}/"
            f"{index_tuple_to_string(index=self._coin_type)}/"
            f"{index_tuple_to_string(index=self._account)}/"
            f"{index_tuple_to_string(index=self._change)}/"
            f"{index_tuple_to_string(index=self._address)}"
        ))
        return self

    def purpose(self) -> int:
        return self._purpose[0]

    def coin_type(self) -> int:
        return self._coin_type[0]

    def account(self) -> int:
        return (
            self._account[1] if len(self._account) == 3 else self._account[0]
        )

    def change(self) -> str:
        _change: Optional[str] = None
        for key, value in self.changes.items():
            if value == self._change[0]:
                _change = key
                break
        return _change

    def address(self) -> int:
        return (
            self._address[1] if len(self._address) == 3 else self._address[0]
        )
