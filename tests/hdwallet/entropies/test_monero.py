#!/usr/bin/env python3

# Copyright © 2020-2024, Meheret Tesfaye Batu <meherett.batu@gmail.com>
#             2024, Eyoel Tadesse <eyoel_tadesse@proton.me>
# Distributed under the MIT software license, see the accompanying
# file COPYING or https://opensource.org/license/mit

import json
import os
import pytest

from hdwallet.entropies.monero import (
    MoneroEntropy, MONERO_ENTROPY_STRENGTHS
)
from hdwallet.utils import get_bytes
from hdwallet.exceptions import EntropyError

# Test Values
base_path: str = os.path.dirname(__file__)
file_path: str = os.path.abspath(os.path.join(base_path, "../../data/entropies.json"))
values = open(file_path, "r", encoding="utf-8")
_: dict = json.loads(values.read())
values.close()


def test_monero_entropy():

    assert MONERO_ENTROPY_STRENGTHS.ONE_HUNDRED_TWENTY_EIGHT == 128
    assert MONERO_ENTROPY_STRENGTHS.TWO_HUNDRED_FIFTY_SIX == 256

    assert MoneroEntropy.is_valid_strength(strength=MONERO_ENTROPY_STRENGTHS.ONE_HUNDRED_TWENTY_EIGHT)
    assert MoneroEntropy.is_valid_strength(strength=MONERO_ENTROPY_STRENGTHS.TWO_HUNDRED_FIFTY_SIX)

    assert MoneroEntropy.is_valid_bytes_strength(bytes_strength=len(get_bytes(_["Monero"]["128"]["entropy"])))
    assert MoneroEntropy.is_valid_bytes_strength(bytes_strength=len(get_bytes(_["Monero"]["256"]["entropy"])))

    assert MoneroEntropy(entropy=MoneroEntropy.generate(strength=MONERO_ENTROPY_STRENGTHS.ONE_HUNDRED_TWENTY_EIGHT)).strength() == 128
    assert MoneroEntropy(entropy=MoneroEntropy.generate(strength=MONERO_ENTROPY_STRENGTHS.TWO_HUNDRED_FIFTY_SIX)).strength() == 256

    monero_128 = MoneroEntropy(entropy=_["Monero"]["128"]["entropy"])
    monero_256 = MoneroEntropy(entropy=_["Monero"]["256"]["entropy"])

    assert monero_128.name() == _["Monero"]["128"]["name"]
    assert monero_256.name() == _["Monero"]["256"]["name"]

    assert monero_128.strength() == _["Monero"]["128"]["strength"]
    assert monero_256.strength() == _["Monero"]["256"]["strength"]

    assert monero_128.entropy() == _["Monero"]["128"]["entropy"]
    assert monero_256.entropy() == _["Monero"]["256"]["entropy"]

    with pytest.raises(EntropyError, match="Invalid entropy data"):
        MoneroEntropy(entropy="INVALID_ENTROPY")

    with pytest.raises(EntropyError, match="Unsupported entropy strength"):
        MoneroEntropy(entropy="cdf694ac868efd01673fc51e897c57a0bd428503080ad4c94c7d6f6d13f095fbc8")
