#!/usr/bin/env python3

# Copyright © 2020-2024, Meheret Tesfaye Batu <meherett.batu@gmail.com>
#             2024, Eyoel Tadesse <eyoel_tadesse@proton.me>
# Distributed under the MIT software license, see the accompanying
# file COPYING or https://opensource.org/license/mit

import json
import os
import pytest

from hdwallet.derivations.bip49 import BIP49Derivation
from hdwallet.exceptions import DerivationError

# Test Values
base_path: str = os.path.dirname(__file__)
file_path: str = os.path.abspath(os.path.join(base_path, "../../data/derivations.json"))
values = open(file_path, "r", encoding="utf-8")
_: dict = json.loads(values.read())
values.close()

def test_bip49_derivation():

    derivation = BIP49Derivation()
    assert derivation.name() == _["BIP49"]["default"]["name"]
    assert derivation.purpose() == _["BIP49"]["default"]["purpose"]
    assert derivation.coin_type() == _["BIP49"]["default"]["coin_type"]
    assert derivation.account() == _["BIP49"]["default"]["account"]
    assert derivation.change() == _["BIP49"]["default"]["change"]
    assert derivation.address() == _["BIP49"]["default"]["address"]
    assert derivation.path() == _["BIP49"]["default"]["path"]

    derivation = BIP49Derivation(
        coin_type=_["BIP49"]["from"]["coin_type"],
        account=_["BIP49"]["from"]["account"],
        change=_["BIP49"]["from"]["change"],
        address=_["BIP49"]["from"]["address"]
    )
    assert derivation.coin_type() == _["BIP49"]["from"]["coin_type"]
    assert derivation.account() == _["BIP49"]["from"]["account"]
    assert derivation.change() == _["BIP49"]["from"]["change"]
    assert derivation.address() == _["BIP49"]["from"]["address"]
    assert derivation.path() == _["BIP49"]["from"]["path"]

    derivation.clean()
    assert derivation.name() == _["BIP49"]["default"]["name"]
    assert derivation.purpose() == _["BIP49"]["default"]["purpose"]
    assert derivation.coin_type() == _["BIP49"]["from"]["coin_type"]
    assert derivation.account() == _["BIP49"]["default"]["account"]
    assert derivation.change() == _["BIP49"]["default"]["change"]
    assert derivation.address() == _["BIP49"]["default"]["address"]

    derivation = BIP49Derivation()
    derivation.from_coin_type(_["BIP49"]["from"]["coin_type"])
    derivation.from_account(_["BIP49"]["from"]["account"])
    derivation.from_change(_["BIP49"]["from"]["change"])
    derivation.from_address(_["BIP49"]["from"]["address"])
    assert derivation.coin_type() == _["BIP49"]["from"]["coin_type"]
    assert derivation.account() == _["BIP49"]["from"]["account"]
    assert derivation.change() == _["BIP49"]["from"]["change"]
    assert derivation.address() == _["BIP49"]["from"]["address"]
    assert derivation.path() == _["BIP49"]["from"]["path"]

    with pytest.raises(DerivationError):
        BIP49Derivation(change="invalid-change")

    with pytest.raises(DerivationError):
        derivation = BIP49Derivation()
        derivation.from_change("invalid-change")