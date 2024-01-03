#!/usr/bin/env python3

# Copyright © 2020-2024, Meheret Tesfaye Batu <meherett.batu@gmail.com>
# Distributed under the MIT software license, see the accompanying
# file COPYING or https://opensource.org/license/mit

from ...mnemonics.bip39 import BIP39Mnemonic
from ..iseed import ISeed


class CardanoIcarusSeed(ISeed):

    _name = "Cardano-Icarus"

    @classmethod
    def generate(cls, mnemonic: str) -> str:

        if not BIP39Mnemonic.is_valid(mnemonic=mnemonic):
            ValueError("Invalid BIP39 mnemonic words")

        return BIP39Mnemonic.decode(mnemonic=mnemonic)
