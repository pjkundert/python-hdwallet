#!/usr/bin/env python3

# Copyright © 2020-2024, Meheret Tesfaye Batu <meherett.batu@gmail.com>
#             2024, Eyoel Tadesse <eyoel_tadesse@proton.me>
# Distributed under the MIT software license, see the accompanying
# file COPYING or https://opensource.org/license/mit

import json
import os
import pytest

from hdwallet.derivations.electrum import ElectrumDerivation
from hdwallet.exceptions import DerivationError

# Test Values
base_path: str = os.path.dirname(__file__)
file_path: str = os.path.abspath(os.path.join(base_path, "../../data/derivations.json"))
values = open(file_path, "r", encoding="utf-8")
_: dict = json.loads(values.read())
values.close()

def test_electrum_derivation():

    derivation = ElectrumDerivation()
    assert derivation.name() == _["Electrum"]["default"]["name"]
    assert derivation.change() == _["Electrum"]["default"]["change"]
    assert derivation.address() == _["Electrum"]["default"]["address"]

    derivation = ElectrumDerivation(
        change=_["Electrum"]["from"]["change"],
        address=_["Electrum"]["from"]["address"]

    )
    assert derivation.change() == _["Electrum"]["from"]["change"]
    assert derivation.address() == _["Electrum"]["from"]["address"]

    derivation.clean()
    assert derivation.change() == _["Electrum"]["default"]["change"]
    assert derivation.address() == _["Electrum"]["default"]["address"]

    derivation = ElectrumDerivation()
    derivation.from_change(_["Electrum"]["from"]["change"])
    derivation.from_address(_["Electrum"]["from"]["address"])
    assert derivation.change() == _["Electrum"]["from"]["change"]
    assert derivation.address() == _["Electrum"]["from"]["address"]