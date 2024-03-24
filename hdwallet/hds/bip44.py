#!/usr/bin/env python3

# Copyright © 2020-2024, Meheret Tesfaye Batu <meherett.batu@gmail.com>
# Distributed under the MIT software license, see the accompanying
# file COPYING or https://opensource.org/license/mit

from typing import (
    Union, Tuple, Type
)

from ..cryptocurrencies import Bitcoin
from ..ecc import IEllipticCurveCryptography
from ..const import PUBLIC_KEY_TYPES
from ..addresses import P2PKHAddress
from ..exceptions import DerivationError
from ..derivations import (
    IDerivation, BIP44Derivation
)
from .bip32 import BIP32HD


class BIP44HD(BIP32HD):

    _derivation: BIP44Derivation

    def __init__(
        self, ecc: Type[IEllipticCurveCryptography], public_key_type: str = PUBLIC_KEY_TYPES.COMPRESSED, **kwargs
    ) -> None:
        super(BIP44HD, self).__init__(ecc=ecc, public_key_type=public_key_type, **kwargs)

        self._derivation = BIP44Derivation(
            coin_type=kwargs.get("coin_type", 0),
            account=kwargs.get("account", 0),
            change=kwargs.get("change", "external-chain"),
            address=kwargs.get("address", 0)
        )

    @classmethod
    def name(cls) -> str:
        return "BIP44"

    def __update__(self) -> "BIP44HD":
        self.from_derivation(derivation=self._derivation)
        return self

    def from_coin_type(self, coin_type: int) -> "BIP44HD":
        self._derivation.from_coin_type(coin_type=coin_type)
        self.__update__()
        return self

    def from_account(self, account: Union[int, Tuple[int, int]]) -> "BIP44HD":
        self._derivation.from_account(account=account)
        self.__update__()
        return self

    def from_change(self, change: str) -> "BIP44HD":
        self._derivation.from_change(change=change)
        self.__update__()
        return self

    def from_address(self, address: Union[int, Tuple[int, int]]) -> "BIP44HD":
        self._derivation.from_address(address=address)
        self.__update__()
        return self

    def from_derivation(self, derivation: IDerivation) -> "BIP44HD":

        if not isinstance(derivation, BIP44Derivation):
            raise DerivationError(
                "Invalid derivation instance", expected=BIP44Derivation, got=type(derivation)
            )

        self.clean_derivation()
        for index in derivation.indexes():
            self._path += ((
               f"{index - 0x80000000}'"
               if self._path == "m/" else
               f"/{index - 0x80000000}'"
            ) if index & 0x80000000 else (
                f"{index}"
                if self._path == "m/" else
                f"/{index}"
            ))
            self._indexes.append(index)
            self.drive(index)
        return self

    def address(
        self, public_key_address_prefix: int = Bitcoin.NETWORKS.MAINNET.PUBLIC_KEY_ADDRESS_PREFIX, **kwargs
    ) -> str:
        return P2PKHAddress.encode(
            public_key=self._public_key,
            public_key_address_prefix=public_key_address_prefix,
            public_key_type=self._public_key_type
        )
