#!/usr/bin/env python3

# Copyright © 2020-2024, Meheret Tesfaye Batu <meherett.batu@gmail.com>
#             2024, Eyoel Tadesse <eyoel_tadesse@proton.me>
# Distributed under the MIT software license, see the accompanying
# file COPYING or https://opensource.org/license/mit

import json
import os
import pytest

from hdwallet.seeds.cardano import CardanoSeed

# Test Values
base_path: str = os.path.dirname(__file__)
file_path: str = os.path.abspath(os.path.join(base_path, "../../data/seeds.json"))
values = open(file_path, "r", encoding="utf-8")
_: dict = json.loads(values.read())
values.close()


def test_cardano_seeds():
    
    for words in _["Cardano"].keys():
        for cardano_type in _["Cardano"][words].keys():

            for lang in _["Cardano"][words][cardano_type].keys():
                assert CardanoSeed.from_mnemonic(
                    mnemonic= _["Cardano"][words][cardano_type][lang]["mnemonic"], cardano_type=cardano_type
                ) ==  _["Cardano"][words][cardano_type][lang]["non-passphrase-seed"]

                if _["Cardano"][words][cardano_type][lang]["passphrases"] == None:
                    continue

                for passphrase in _["Cardano"][words][cardano_type][lang]["passphrases"].keys():
                    assert CardanoSeed.from_mnemonic(
                        mnemonic= _["Cardano"][words][cardano_type][lang]["mnemonic"], 
                        passphrase=passphrase,
                        cardano_type=cardano_type
                    ) == _["Cardano"][words][cardano_type][lang]["passphrases"][passphrase]

                    assert CardanoSeed.from_mnemonic(
                        mnemonic= _["Cardano"][words][cardano_type][lang]["mnemonic"], 
                        passphrase=passphrase,
                        cardano_type=cardano_type
                    ) == _["Cardano"][words][cardano_type][lang]["passphrases"][passphrase]

