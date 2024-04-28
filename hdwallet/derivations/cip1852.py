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


class ROLES:

    EXTERNAL_CHAIN: str = "external-chain"
    INTERNAL_CHAIN: str = "internal-chain"
    STAKING_KEY: str = "staking-key"


class CIP1852Derivation(IDerivation):  # https://github.com/cardano-foundation/CIPs/blob/master/CIP-1852/README.md

    _purpose: Tuple[int, bool] = (1852, True)
    _coin_type: Tuple[int, bool]
    _account: Union[Tuple[int, bool], Tuple[int, int, bool]]
    _role: Tuple[int, bool]
    _address: Union[Tuple[int, bool], Tuple[int, int, bool]]
    roles: Dict[str, int] = {
        "external-chain": 0, "internal-chain": 1, "staking-key": 2
    }

    def __init__(
        self,
        coin_type: Union[str, int] = 1815,
        account: Union[str, int, Tuple[int, int]] = 0,
        role: Union[str, int] = "external-chain",
        address: Union[str, int, Tuple[int, int]] = 0
    ) -> None:
        super(CIP1852Derivation, self).__init__()

        if role not in [*self.roles.keys(), 0, "0", 1, "1", 2, "2"]:
            raise DerivationError(
                f"Bad {self.name()} role index", expected=[*self.roles.keys(), 0, "0", 1, "1", 2, "2"], got=role
            )

        self._coin_type = normalize_index(index=coin_type, hardened=True)
        self._account = normalize_index(index=account, hardened=True)
        self._role = normalize_index(
            index=(self.roles[role] if role in self.roles.keys() else role), hardened=False
        )
        self._address = normalize_index(index=address, hardened=False)
        self._path, self._indexes, self._derivations = normalize_derivation(path=(
            f"m/{index_tuple_to_string(index=self._purpose)}/"
            f"{index_tuple_to_string(index=self._coin_type)}/"
            f"{index_tuple_to_string(index=self._account)}/"
            f"{index_tuple_to_string(index=self._role)}/"
            f"{index_tuple_to_string(index=self._address)}"
        ))
        
    @classmethod
    def name(cls) -> str:
        return "CIP1852"

    def from_coin_type(self, coin_type: Union[str, int]) -> "CIP1852Derivation":
        self._coin_type = normalize_index(index=coin_type, hardened=True)
        self._path, self._indexes, self._derivations = normalize_derivation(path=(
            f"m/{index_tuple_to_string(index=self._purpose)}/"
            f"{index_tuple_to_string(index=self._coin_type)}/"
            f"{index_tuple_to_string(index=self._account)}/"
            f"{index_tuple_to_string(index=self._role)}/"
            f"{index_tuple_to_string(index=self._address)}"
        ))
        return self

    def from_account(self, account: Union[str, int, Tuple[int, int]]) -> "CIP1852Derivation":
        self._account = normalize_index(index=account, hardened=True)
        self._path, self._indexes, self._derivations = normalize_derivation(path=(
            f"m/{index_tuple_to_string(index=self._purpose)}/"
            f"{index_tuple_to_string(index=self._coin_type)}/"
            f"{index_tuple_to_string(index=self._account)}/"
            f"{index_tuple_to_string(index=self._role)}/"
            f"{index_tuple_to_string(index=self._address)}"
        ))
        return self

    def from_role(self, role: Union[str, int]) -> "CIP1852Derivation":
        if role not in [*self.roles.keys(), 0, "0", 1, "1", 2, "2"]:
            raise DerivationError(
                f"Bad {self.name()} role index", expected=[*self.roles.keys(), 0, "0", 1, "1", 2, "2"], got=role
            )
        self._role = normalize_index(
            index=(self.roles[role] if role in self.roles.keys() else role), hardened=False
        )
        self._path, self._indexes, self._derivations = normalize_derivation(path=(
            f"m/{index_tuple_to_string(index=self._purpose)}/"
            f"{index_tuple_to_string(index=self._coin_type)}/"
            f"{index_tuple_to_string(index=self._account)}/"
            f"{index_tuple_to_string(index=self._role)}/"
            f"{index_tuple_to_string(index=self._address)}"
        ))
        return self

    def from_address(self, address: Union[str, int, Tuple[int, int]]) -> "CIP1852Derivation":
        self._address = normalize_index(index=address, hardened=False)
        self._path, self._indexes, self._derivations = normalize_derivation(path=(
            f"m/{index_tuple_to_string(index=self._purpose)}/"
            f"{index_tuple_to_string(index=self._coin_type)}/"
            f"{index_tuple_to_string(index=self._account)}/"
            f"{index_tuple_to_string(index=self._role)}/"
            f"{index_tuple_to_string(index=self._address)}"
        ))
        return self

    def clean(self) -> "CIP1852Derivation":
        self._account = normalize_index(index=0, hardened=True)
        self._role = normalize_index(index=self.roles["external-chain"], hardened=False)
        self._address = normalize_index(index=0, hardened=False)
        self._path, self._indexes, self._derivations = normalize_derivation(path=(
            f"m/{index_tuple_to_string(index=self._purpose)}/"
            f"{index_tuple_to_string(index=self._coin_type)}/"
            f"{index_tuple_to_string(index=self._account)}/"
            f"{index_tuple_to_string(index=self._role)}/"
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

    def role(self) -> str:
        _role: Optional[str] = None
        for key, value in self.roles.items():
            if value == self._role[0]:
                _role = key
                break
        return _role

    def address(self) -> int:
        return (
            self._address[1] if len(self._address) == 3 else self._address[0]
        )
