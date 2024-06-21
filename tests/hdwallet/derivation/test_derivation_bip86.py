#!/usr/bin/env python3

# Copyright © 2020-2024, Meheret Tesfaye Batu <meherett.batu@gmail.com>
#             2024, Eyoel Tadesse <eyoel_tadesse@proton.me>
# Distributed under the MIT software license, see the accompanying
# file COPYING or https://opensource.org/license/mit

import json
import os
import pytest

from hdwallet.derivations.bip86 import BIP86Derivation
from hdwallet.exceptions import DerivationError

# Test Values
base_path: str = os.path.dirname(__file__)
file_path: str = os.path.abspath(os.path.join(base_path, "../../data/derivations.json"))
values = open(file_path, "r", encoding="utf-8")
_: dict = json.loads(values.read())
values.close()

def test_bip86_derivation():

    derivation = BIP86Derivation()
    assert derivation.name() == _["BIP86"]["default"]["name"]
    assert derivation.purpose() == _["BIP86"]["default"]["purpose"]
    assert derivation.coin_type() == _["BIP86"]["default"]["coin_type"]
    assert derivation.account() == _["BIP86"]["default"]["account"]
    assert derivation.change() == _["BIP86"]["default"]["change"]
    assert derivation.address() == _["BIP86"]["default"]["address"]
    assert derivation.path() == _["BIP86"]["default"]["path"]

    derivation = BIP86Derivation(
        coin_type=_["BIP86"]["from"]["coin_type"],
        account=_["BIP86"]["from"]["account"],
        change=_["BIP86"]["from"]["change"],
        address=_["BIP86"]["from"]["address"]
    )
    assert derivation.coin_type() == _["BIP86"]["from"]["coin_type"]
    assert derivation.account() == _["BIP86"]["from"]["account"]
    assert derivation.change() == _["BIP86"]["from"]["change"]
    assert derivation.address() == _["BIP86"]["from"]["address"]
    assert derivation.path() == _["BIP86"]["from"]["path"]

    derivation.clean()
    assert derivation.name() == _["BIP86"]["default"]["name"]
    assert derivation.purpose() == _["BIP86"]["default"]["purpose"]
    assert derivation.coin_type() == _["BIP86"]["from"]["coin_type"]
    assert derivation.account() == _["BIP86"]["default"]["account"]
    assert derivation.change() == _["BIP86"]["default"]["change"]
    assert derivation.address() == _["BIP86"]["default"]["address"]

    derivation = BIP86Derivation()
    derivation.from_coin_type(_["BIP86"]["from"]["coin_type"])
    derivation.from_account(_["BIP86"]["from"]["account"])
    derivation.from_change(_["BIP86"]["from"]["change"])
    derivation.from_address(_["BIP86"]["from"]["address"])
    assert derivation.coin_type() == _["BIP86"]["from"]["coin_type"]
    assert derivation.account() == _["BIP86"]["from"]["account"]
    assert derivation.change() == _["BIP86"]["from"]["change"]
    assert derivation.address() == _["BIP86"]["from"]["address"]
    assert derivation.path() == _["BIP86"]["from"]["path"]

    with pytest.raises(DerivationError):
        BIP86Derivation(change="invalid-change")

    with pytest.raises(DerivationError):
        derivation = BIP86Derivation()
        derivation.from_change("invalid-change")