#!/usr/bin/env python3

# Copyright © 2020-2023, Meheret Tesfaye Batu <meherett.batu@gmail.com>
# Distributed under the MIT software license, see the accompanying
# file COPYING or https://opensource.org/license/mit

from typing import (
    Tuple, Any
)

from ..utils import (
    indexes_to_path, index_tuple_to_integer
)
from .iderivation import IDerivation


class BIP44Derivation(IDerivation):  # https://github.com/bitcoin/bips/blob/master/bip-0044.mediawiki

    _purpose: Tuple[int, bool] = (44, True)
    change_types: dict = {
        "external-chain": 0, "internal-chain": 1
    }

    def __init__(
        self, coin_type: Any = 0, account: int = 0, change: str = "external-chain", address: int = 0
    ) -> None:

        super(BIP44Derivation, self).__init__()

        self._coin_type: Tuple[int, bool] = (int(coin_type), True)
        self._account: Tuple[int, bool] = (account, True)
        self._change: Tuple[int, bool] = (self.change_types[change], False)
        self._address: Tuple[int, bool] = (address, False)
        self._indexes = [
            index_tuple_to_integer(index=self._purpose),
            index_tuple_to_integer(index=self._coin_type),
            index_tuple_to_integer(index=self._account),
            index_tuple_to_integer(index=self._change),
            index_tuple_to_integer(index=self._address)
        ]
        self._path = indexes_to_path(indexes=self._indexes)

    def from_coin_type(self, coin_type: int) -> "BIP44Derivation":
        self._coin_type = (coin_type, True)
        self._indexes[1] = index_tuple_to_integer(index=self._coin_type)
        self._path = indexes_to_path(indexes=self._indexes)
        return self

    def from_account(self, account: int) -> "BIP44Derivation":
        self._account = (account, True)
        self._indexes[2] = index_tuple_to_integer(index=self._account)
        self._path = indexes_to_path(indexes=self._indexes)
        return self

    def from_change(self, change: str) -> "BIP44Derivation":
        self._change = (self.change_types[change], False)
        self._indexes[3] = index_tuple_to_integer(index=self._change)
        self._path = indexes_to_path(indexes=self._indexes)
        return self

    def from_address(self, address: int) -> "BIP44Derivation":
        self._address = (address, False)
        self._indexes[4] = index_tuple_to_integer(index=self._address)
        self._path = indexes_to_path(indexes=self._indexes)
        return self

    def purpose(self) -> Tuple[int, bool]:
        return self._purpose

    def coin_type(self) -> Tuple[int, bool]:
        return self._coin_type

    def account(self) -> Tuple[int, bool]:
        return self._account

    def change(self) -> Tuple[int, bool]:
        return self._change

    def address(self) -> Tuple[int, bool]:
        return self._address
