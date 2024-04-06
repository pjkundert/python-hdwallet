#!/usr/bin/env python3

# Copyright © 2020-2024, Meheret Tesfaye Batu <meherett.batu@gmail.com>
# Distributed under the MIT software license, see the accompanying
# file COPYING or https://opensource.org/license/mit

from typing import (
    Tuple, Union, Optional
)

from ..utils import (
    normalize_derivation, index_tuple_to_string
)
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
    roles: dict = {
        "external-chain": 0, "internal-chain": 1, "staking-key": 2
    }

    def __init__(
        self,
        coin_type: Union[int, Tuple[int, bool]] = 1815,
        account: Union[int, Tuple[int, int]] = 0,
        role: Union[str, Tuple[int, bool]] = "external-chain",
        address: Union[int, Tuple[int, int]] = 0
    ) -> None:
        super(CIP1852Derivation, self).__init__()

        self._coin_type = (coin_type, True) if isinstance(coin_type, int) else coin_type
        self._account = (*account, True) if isinstance(account, tuple) else (account, True)
        self._role = (self.roles[role], False) if isinstance(role, str) else role
        self._address = (*address, False) if isinstance(address, tuple) else (address, False)
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

    def from_coin_type(self, coin_type: int) -> "CIP1852Derivation":
        self._coin_type = (coin_type, True)
        self._path, self._indexes, self._derivations = normalize_derivation(path=(
            f"m/{index_tuple_to_string(index=self._purpose)}/"
            f"{index_tuple_to_string(index=self._coin_type)}/"
            f"{index_tuple_to_string(index=self._account)}/"
            f"{index_tuple_to_string(index=self._role)}/"
            f"{index_tuple_to_string(index=self._address)}"
        ))
        return self

    def from_account(self, account: Union[int, Tuple[int, int]]) -> "CIP1852Derivation":
        self._account = (*account, True) if isinstance(account, tuple) else (account, True)
        self._path, self._indexes, self._derivations = normalize_derivation(path=(
            f"m/{index_tuple_to_string(index=self._purpose)}/"
            f"{index_tuple_to_string(index=self._coin_type)}/"
            f"{index_tuple_to_string(index=self._account)}/"
            f"{index_tuple_to_string(index=self._role)}/"
            f"{index_tuple_to_string(index=self._address)}"
        ))
        return self

    def from_role(self, role: str) -> "CIP1852Derivation":
        self._role = (self.roles[role], False)
        self._path, self._indexes, self._derivations = normalize_derivation(path=(
            f"m/{index_tuple_to_string(index=self._purpose)}/"
            f"{index_tuple_to_string(index=self._coin_type)}/"
            f"{index_tuple_to_string(index=self._account)}/"
            f"{index_tuple_to_string(index=self._role)}/"
            f"{index_tuple_to_string(index=self._address)}"
        ))
        return self

    def from_address(self, address: Union[int, Tuple[int, int]]) -> "CIP1852Derivation":
        self._address = (*address, False) if isinstance(address, tuple) else (address, False)
        self._path, self._indexes, self._derivations = normalize_derivation(path=(
            f"m/{index_tuple_to_string(index=self._purpose)}/"
            f"{index_tuple_to_string(index=self._coin_type)}/"
            f"{index_tuple_to_string(index=self._account)}/"
            f"{index_tuple_to_string(index=self._role)}/"
            f"{index_tuple_to_string(index=self._address)}"
        ))
        return self

    def clean(self) -> "CIP1852Derivation":
        self._account = (0, True)
        self._role = (self.roles["external-chain"], False)
        self._address = (0, False)
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

    def role(self) -> Optional[None]:
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
