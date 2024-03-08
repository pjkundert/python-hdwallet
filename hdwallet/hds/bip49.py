#!/usr/bin/env python3

# Copyright © 2020-2024, Meheret Tesfaye Batu <meherett.batu@gmail.com>
# Distributed under the MIT software license, see the accompanying
# file COPYING or https://opensource.org/license/mit

from ..derivations import (
    IDerivation, BIP49Derivation
)
from .bip32 import BIP32HD


class BIP49HD(BIP32HD):

    @classmethod
    def name(cls) -> str:
        return "BIP49"

    def from_derivation(self, derivation: IDerivation) -> "BIP49HD":

        if not isinstance(derivation, BIP49Derivation):
            raise ValueError(f"Invalid derivation class, (expected: {BIP49Derivation}, got: {type(derivation)})")

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

    def update_derivation(self, derivation: IDerivation) -> "BIP49HD":

        if not isinstance(derivation, BIP49Derivation):
            raise ValueError(f"Invalid derivation class, (expected: {BIP49Derivation}, got: {type(derivation)})")

        self.clean_derivation()
        self.from_derivation(
            derivation=derivation
        )
        return self

    def address(self, **kwargs) -> str:
        pass
