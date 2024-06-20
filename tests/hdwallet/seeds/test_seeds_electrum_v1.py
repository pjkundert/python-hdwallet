#!/usr/bin/env python3

# Copyright © 2020-2024, Meheret Tesfaye Batu <meherett.batu@gmail.com>
#             2024, Eyoel Tadesse <eyoel_tadesse@proton.me>
# Distributed under the MIT software license, see the accompanying
# file COPYING or https://opensource.org/license/mit

import json
import os
import pytest

from hdwallet.seeds.electrum.v1 import ElectrumV1Seed

# Test Values
base_path: str = os.path.dirname(__file__)
file_path: str = os.path.abspath(os.path.join(base_path, "../../data/seeds.json"))
values = open(file_path, "r", encoding="utf-8")
_: dict = json.loads(values.read())
values.close()


def test_electrum_v1_seeds():
    assert ElectrumV1Seed.from_mnemonic(mnemonic=_["Electrum-V1"]["12"]["english"]["mnemonic"]) == _["Electrum-V1"]["12"]["english"]["non-passphrase-seed"]

