#!/usr/bin/env python3

# Copyright © 2020-2024, Meheret Tesfaye Batu <meherett.batu@gmail.com>
# Distributed under the MIT software license, see the accompanying
# file COPYING or https://opensource.org/license/mit

from ..mnemonics.algorand import AlgorandMnemonic
from .iseed import ISeed


class AlgorandSeed(ISeed):

    @classmethod
    def generate(cls, mnemonic: str, **kwargs) -> str:

        if not AlgorandMnemonic.is_valid(mnemonic=mnemonic):
            ValueError("Invalid Algorand mnemonic words")

        return AlgorandMnemonic.decode(mnemonic=mnemonic)
