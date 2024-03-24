#!/usr/bin/env python3

# Copyright © 2020-2024, Meheret Tesfaye Batu <meherett.batu@gmail.com>
# Distributed under the MIT software license, see the accompanying
# file COPYING or https://opensource.org/license/mit

from ..exceptions import MnemonicError
from ..mnemonics.algorand import AlgorandMnemonic
from .iseed import ISeed


class AlgorandSeed(ISeed):

    @classmethod
    def name(cls) -> str:
        return "Algorand"

    @classmethod
    def generate(cls, mnemonic: str, **kwargs) -> str:

        if not AlgorandMnemonic.is_valid(mnemonic=mnemonic):
            raise MnemonicError(f"Invalid {cls.name()} mnemonic words")

        return AlgorandMnemonic.decode(mnemonic=mnemonic)
