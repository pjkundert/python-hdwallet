#!/usr/bin/env python3

# Copyright © 2020-2024, Meheret Tesfaye Batu <meherett.batu@gmail.com>
#             2024, Eyoel Tadesse <eyoel_tadesse@proton.me>
# Distributed under the MIT software license, see the accompanying
# file COPYING or https://opensource.org/license/mit

import json
import os
import pytest

from hdwallet.entropies.algorand import (
    AlgorandEntropy, ALGORAND_ENTROPY_STRENGTHS
)
from hdwallet.utils import get_bytes
from hdwallet.exceptions import EntropyError

# Test Values
base_path: str = os.path.dirname(__file__)
file_path: str = os.path.abspath(os.path.join(base_path, "../../data/entropies.json"))
values = open(file_path, "r", encoding="utf-8")
_: dict = json.loads(values.read())
values.close()


def test_algorand_entropy():

    assert ALGORAND_ENTROPY_STRENGTHS.TWO_HUNDRED_FIFTY_SIX == 256
    assert AlgorandEntropy.is_valid_strength(strength=ALGORAND_ENTROPY_STRENGTHS.TWO_HUNDRED_FIFTY_SIX)
    assert AlgorandEntropy.is_valid_bytes_strength(bytes_strength=len(get_bytes(_["Algorand"]["256"]["entropy"])))
    assert AlgorandEntropy(entropy=AlgorandEntropy.generate(strength=ALGORAND_ENTROPY_STRENGTHS.TWO_HUNDRED_FIFTY_SIX)).strength() == 256

    algorand_256 = AlgorandEntropy(entropy=_["Algorand"]["256"]["entropy"])

    assert algorand_256.name() == _["Algorand"]["256"]["name"]
    assert algorand_256.strength() == _["Algorand"]["256"]["strength"]
    assert algorand_256.entropy() == _["Algorand"]["256"]["entropy"]

    with pytest.raises(EntropyError, match="Invalid entropy data"):
        AlgorandEntropy(entropy="INVALID_ENTROPY")

    with pytest.raises(EntropyError, match="Unsupported entropy strength"):
        AlgorandEntropy(entropy="cdf694ac868efd01673fc51e897c57a0bd428503080ad4c94c7d6f6d13f095fbc8")
