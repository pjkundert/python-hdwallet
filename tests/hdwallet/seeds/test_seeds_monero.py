#!/usr/bin/env python3

# Copyright © 2020-2024, Meheret Tesfaye Batu <meherett.batu@gmail.com>
#             2024, Eyoel Tadesse <eyoel_tadesse@proton.me>
# Distributed under the MIT software license, see the accompanying
# file COPYING or https://opensource.org/license/mit

import json
import os
import pytest

from hdwallet.seeds.monero import MoneroSeed

# Test Values
base_path: str = os.path.dirname(__file__)
file_path: str = os.path.abspath(os.path.join(base_path, "../../data/seeds.json"))
values = open(file_path, "r", encoding="utf-8")
_: dict = json.loads(values.read())
values.close()


def test_monero_seeds():
    
    for words in _["Monero"].keys():
        for lang in _["Monero"][words].keys():
            assert MoneroSeed.from_mnemonic(
                mnemonic= _["Monero"][words][lang]["mnemonic"]
            ) ==  _["Monero"][words][lang]["non-passphrase-seed"]

