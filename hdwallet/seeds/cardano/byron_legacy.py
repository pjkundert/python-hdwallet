#!/usr/bin/env python3

# Copyright © 2020-2024, Meheret Tesfaye Batu <meherett.batu@gmail.com>
# Distributed under the MIT software license, see the accompanying
# file COPYING or https://opensource.org/license/mit

import cbor2

from ...utils import get_bytes, bytes_to_string
from ...crypto import blake2b_256
from ...mnemonics.bip39 import BIP39Mnemonic
from ..iseed import ISeed


class CardanoByronLegacySeed(ISeed):

    _name = "Cardano-Byron-Legacy"

    @classmethod
    def generate(cls, mnemonic: str) -> str:

        if not BIP39Mnemonic.is_valid(mnemonic=mnemonic):
            ValueError("Invalid BIP39 mnemonic words")

        return bytes_to_string(blake2b_256(
            cbor2.dumps(get_bytes(BIP39Mnemonic.decode(mnemonic=mnemonic)))
        ))
