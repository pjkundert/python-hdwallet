#!/usr/bin/env python3

# Copyright © 2020-2023, Meheret Tesfaye Batu <meherett.batu@gmail.com>
# Distributed under the MIT software license, see the accompanying
# file COPYING or https://opensource.org/license/mit

from ..mnemonics.monero import MoneroMnemonic
from . import ISeed


class MoneroSeed(ISeed):

    @classmethod
    def generate(cls, mnemonic: str, **kwargs) -> str:

        if not MoneroMnemonic.is_valid(mnemonic=mnemonic):
            ValueError("Invalid Monero mnemonic words")

        return MoneroMnemonic.decode(mnemonic=mnemonic)
