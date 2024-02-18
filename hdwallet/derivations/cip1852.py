#!/usr/bin/env python3

# Copyright © 2020-2024, Meheret Tesfaye Batu <meherett.batu@gmail.com>
# Distributed under the MIT software license, see the accompanying
# file COPYING or https://opensource.org/license/mit

from typing import Tuple

from ..utils import (
    indexes_to_path, index_tuple_to_integer
)
from .iderivation import IDerivation


class CIP1852Derivation(IDerivation):  # https://github.com/cardano-foundation/CIPs/blob/master/CIP-1852/README.md

    _purpose: Tuple[int, bool] = (1852, True)
    role_types: dict = {
        "external-chain": 0, "internal-chain": 1, "staking-key": 2
    }

    def __init__(
        self,
        coin_type: int = 1815,
        account: int = 0,
        role: str = "external-chain",
        address: int = 0
    ) -> None:

        super(CIP1852Derivation, self).__init__()

        self._coin_type: Tuple[int, bool] = (coin_type, True)
        self._account: Tuple[int, bool] = (account, True)
        self._role: Tuple[int, bool] = (self.role_types[role], False)
        self._address: Tuple[int, bool] = (address, False)

        self._indexes = [
            index_tuple_to_integer(index=self._purpose),
            index_tuple_to_integer(index=self._coin_type),
            index_tuple_to_integer(index=self._account),
            index_tuple_to_integer(index=self._role),
            index_tuple_to_integer(index=self._address)
        ]
        self._path = indexes_to_path(indexes=self._indexes)
        
    @classmethod
    def name(cls) -> str:
        return "CIP1852"

    def from_coin_type(self, coin_type: int) -> "CIP1852Derivation":
        self._coin_type = (coin_type, True)
        self._indexes[1] = index_tuple_to_integer(index=self._coin_type)
        self._path = indexes_to_path(indexes=self._indexes)
        return self

    def from_account(self, account: int) -> "CIP1852Derivation":
        self._account = (account, False)
        self._indexes[2] = index_tuple_to_integer(index=self._account)
        self._path = indexes_to_path(indexes=self._indexes)
        return self

    def from_role(self, role: str) -> "CIP1852Derivation":
        self._role = (self.role_types[role], False)
        self._indexes[3] = index_tuple_to_integer(index=self._role)
        self._path = indexes_to_path(indexes=self._indexes)
        return self

    def from_address(self, address: int) -> "CIP1852Derivation":
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

    def role(self) -> Tuple[int, bool]:
        return self._role

    def address(self) -> Tuple[int, bool]:
        return self._address
