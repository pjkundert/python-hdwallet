#!/usr/bin/env python3

# Copyright © 2020-2024, Meheret Tesfaye Batu <meherett.batu@gmail.com>
#             2024, Eyoel Tadesse <eyoel_tadesse@proton.me>
# Distributed under the MIT software license, see the accompanying
# file COPYING or https://opensource.org/license/mit

import json
import os
import pytest

from hdwallet.derivations.custom import CustomDerivation
from hdwallet.exceptions import DerivationError

# Test Values
base_path: str = os.path.dirname(__file__)
file_path: str = os.path.abspath(os.path.join(base_path, "../../data/derivations.json"))
values = open(file_path, "r", encoding="utf-8")
_: dict = json.loads(values.read())
values.close()


def test_custom_derivation():

    assert CustomDerivation().name() == _["Custom"]["name"]
    assert CustomDerivation().path() == _["Custom"]["default-path"]
    
    derivation = CustomDerivation().from_path(
        path=_["Custom"]["from-path"]["path"]
    )
    assert derivation.path() == _["Custom"]["from-path"]["path"]
    derivation.clean()
    assert derivation.path() == _["Custom"]["default-path"]

    assert CustomDerivation().from_indexes(
        indexes=_["Custom"]["from-path"]["indexes"]
    ).path() == _["Custom"]["from-path"]["path"]

    assert CustomDerivation().from_index(
        index=_["Custom"]["from-index"]["index"],
        hardened=_["Custom"]["from-index"]["hardened"]
    ).path() == _["Custom"]["from-index"]["path"]

    with pytest.raises(DerivationError, match="Bad path instance"):
        CustomDerivation().from_path(path={'FAKE_DICT'})

    with pytest.raises(DerivationError, match="Bad path format"):
        CustomDerivation().from_path(path='n/15/0/0/0/0')

    with pytest.raises(DerivationError, match="Bad indexes instance"):
        CustomDerivation().from_indexes(indexes={'FAKE_DICT'})

    with pytest.raises(DerivationError, match="Bad index instance"):
        CustomDerivation().from_index(index={'FAKE_DICT'})
