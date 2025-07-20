#!/usr/bin/env python3

# Copyright © 2020-2024, Meheret Tesfaye Batu <meherett.batu@gmail.com>
#             2024, Eyoel Tadesse <eyoel_tadesse@proton.me>
# Distributed under the MIT software license, see the accompanying
# file COPYING or https://opensource.org/license/mit

import json
import logging
import os
import pytest

from hdwallet.seeds.slip39 import SLIP39Seed
from hdwallet.mnemonics.bip39 import BIP39Mnemonic


def test_slip39_seeds(data):
    
    for words in data["seeds"]["SLIP39"].keys():
        for lang in data["seeds"]["SLIP39"][words].keys():
            mnemonic = data["seeds"]["SLIP39"][words][lang]["mnemonic"]
            try:
                mnemonic = BIP39Mnemonic(mnemonic=mnemonic)
            except Exception:
                logging.exception("Failed to interpret %s as BIP-39 Mnemonic", mnemonic)
                pass
            assert SLIP39Seed.from_mnemonic(
                mnemonic = mnemonic
            ) == data["seeds"]["SLIP39"][words][lang]["seed"]

