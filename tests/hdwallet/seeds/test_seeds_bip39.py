#!/usr/bin/env python3

# Copyright © 2020-2024, Meheret Tesfaye Batu <meherett.batu@gmail.com>
#             2024, Eyoel Tadesse <eyoel_tadesse@proton.me>
# Distributed under the MIT software license, see the accompanying
# file COPYING or https://opensource.org/license/mit

import json
import os
import pytest

from hdwallet.seeds.bip39 import BIP39Seed

# Test Values
base_path: str = os.path.dirname(__file__)
file_path: str = os.path.abspath(os.path.join(base_path, "../../data/seeds.json"))
values = open(file_path, "r", encoding="utf-8")
_: dict = json.loads(values.read())
values.close()


def test_bip39_seeds():
    
    for words in _["BIP39"].keys():
        for lang in _["BIP39"][words].keys():
            assert BIP39Seed.from_mnemonic(
                mnemonic= _["BIP39"][words][lang]["mnemonic"]
            ) ==  _["BIP39"][words][lang]["non-passphrase-seed"]

            for passphrase in _["BIP39"][words][lang]["passphrases"].keys():
                assert BIP39Seed.from_mnemonic(
                    mnemonic= _["BIP39"][words][lang]["mnemonic"], passphrase=passphrase
                ) == _["BIP39"][words][lang]["passphrases"][passphrase]

                assert BIP39Seed.from_mnemonic(
                    mnemonic= _["BIP39"][words][lang]["mnemonic"], passphrase=passphrase
                ) == _["BIP39"][words][lang]["passphrases"][passphrase]

