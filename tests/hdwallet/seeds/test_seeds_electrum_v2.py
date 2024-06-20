#!/usr/bin/env python3

# Copyright © 2020-2024, Meheret Tesfaye Batu <meherett.batu@gmail.com>
#             2024, Eyoel Tadesse <eyoel_tadesse@proton.me>
# Distributed under the MIT software license, see the accompanying
# file COPYING or https://opensource.org/license/mit

import json
import os
import pytest

from hdwallet.seeds.electrum.v2 import ElectrumV2Seed

# Test Values
base_path: str = os.path.dirname(__file__)
file_path: str = os.path.abspath(os.path.join(base_path, "../../data/seeds.json"))
values = open(file_path, "r", encoding="utf-8")
_: dict = json.loads(values.read())
values.close()


def test_electrum_v2_seeds():
    
    for words in _["Electrum-V2"].keys():
        for mnemonic_type in _["Electrum-V2"][words].keys():

            for lang in _["Electrum-V2"][words][mnemonic_type].keys():
                assert ElectrumV2Seed.from_mnemonic(
                    mnemonic= _["Electrum-V2"][words][mnemonic_type][lang]["mnemonic"], mnemonic_type=mnemonic_type
                ) ==  _["Electrum-V2"][words][mnemonic_type][lang]["non-passphrase-seed"]

                for passphrase in _["Electrum-V2"][words][mnemonic_type][lang]["passphrases"].keys():
                    assert ElectrumV2Seed.from_mnemonic(
                        mnemonic= _["Electrum-V2"][words][mnemonic_type][lang]["mnemonic"], 
                        passphrase=passphrase,
                        mnemonic_type=mnemonic_type
                    ) == _["Electrum-V2"][words][mnemonic_type][lang]["passphrases"][passphrase]

                    assert ElectrumV2Seed.from_mnemonic(
                        mnemonic= _["Electrum-V2"][words][mnemonic_type][lang]["mnemonic"], 
                        passphrase=passphrase,
                        mnemonic_type=mnemonic_type
                    ) == _["Electrum-V2"][words][mnemonic_type][lang]["passphrases"][passphrase]

