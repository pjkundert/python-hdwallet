#!/usr/bin/env python3

# Copyright © 2020-2024, Meheret Tesfaye Batu <meherett.batu@gmail.com>
#             2024, Eyoel Tadesse <eyoel_tadesse@proton.me>
# Distributed under the MIT software license, see the accompanying
# file COPYING or https://opensource.org/license/mit

import json
import os
import pytest

from hdwallet.entropies.bip39 import (
    BIP39Entropy, BIP39_ENTROPY_STRENGTHS
)
from hdwallet.utils import get_bytes
from hdwallet.exceptions import EntropyError

# Test Values
base_path: str = os.path.dirname(__file__)
file_path: str = os.path.abspath(os.path.join(base_path, "../../data/entropies.json"))
values = open(file_path, "r", encoding="utf-8")
_: dict = json.loads(values.read())
values.close()


def test_bip39_entropy():

    assert BIP39_ENTROPY_STRENGTHS.ONE_HUNDRED_TWENTY_EIGHT == 128
    assert BIP39_ENTROPY_STRENGTHS.ONE_HUNDRED_SIXTY == 160
    assert BIP39_ENTROPY_STRENGTHS.ONE_HUNDRED_NINETY_TWO == 192
    assert BIP39_ENTROPY_STRENGTHS.TWO_HUNDRED_TWENTY_FOUR == 224
    assert BIP39_ENTROPY_STRENGTHS.TWO_HUNDRED_FIFTY_SIX == 256

    assert BIP39Entropy.is_valid_strength(strength=BIP39_ENTROPY_STRENGTHS.ONE_HUNDRED_TWENTY_EIGHT)
    assert BIP39Entropy.is_valid_strength(strength=BIP39_ENTROPY_STRENGTHS.ONE_HUNDRED_SIXTY)
    assert BIP39Entropy.is_valid_strength(strength=BIP39_ENTROPY_STRENGTHS.ONE_HUNDRED_NINETY_TWO)
    assert BIP39Entropy.is_valid_strength(strength=BIP39_ENTROPY_STRENGTHS.TWO_HUNDRED_TWENTY_FOUR)
    assert BIP39Entropy.is_valid_strength(strength=BIP39_ENTROPY_STRENGTHS.TWO_HUNDRED_FIFTY_SIX)

    assert BIP39Entropy.is_valid_bytes_strength(bytes_strength=len(get_bytes(_["BIP39"]["128"]["entropy"])))
    assert BIP39Entropy.is_valid_bytes_strength(bytes_strength=len(get_bytes(_["BIP39"]["160"]["entropy"])))
    assert BIP39Entropy.is_valid_bytes_strength(bytes_strength=len(get_bytes(_["BIP39"]["192"]["entropy"])))
    assert BIP39Entropy.is_valid_bytes_strength(bytes_strength=len(get_bytes(_["BIP39"]["224"]["entropy"])))
    assert BIP39Entropy.is_valid_bytes_strength(bytes_strength=len(get_bytes(_["BIP39"]["256"]["entropy"])))

    assert BIP39Entropy(entropy=BIP39Entropy.generate(strength=BIP39_ENTROPY_STRENGTHS.ONE_HUNDRED_TWENTY_EIGHT)).strength() == 128
    assert BIP39Entropy(entropy=BIP39Entropy.generate(strength=BIP39_ENTROPY_STRENGTHS.ONE_HUNDRED_SIXTY)).strength() == 160
    assert BIP39Entropy(entropy=BIP39Entropy.generate(strength=BIP39_ENTROPY_STRENGTHS.ONE_HUNDRED_NINETY_TWO)).strength() == 192
    assert BIP39Entropy(entropy=BIP39Entropy.generate(strength=BIP39_ENTROPY_STRENGTHS.TWO_HUNDRED_TWENTY_FOUR)).strength() == 224
    assert BIP39Entropy(entropy=BIP39Entropy.generate(strength=BIP39_ENTROPY_STRENGTHS.TWO_HUNDRED_FIFTY_SIX)).strength() == 256

    bip39_128 = BIP39Entropy(entropy=_["BIP39"]["128"]["entropy"])
    bip39_160 = BIP39Entropy(entropy=_["BIP39"]["160"]["entropy"])
    bip39_192 = BIP39Entropy(entropy=_["BIP39"]["192"]["entropy"])
    bip39_224 = BIP39Entropy(entropy=_["BIP39"]["224"]["entropy"])
    bip39_256 = BIP39Entropy(entropy=_["BIP39"]["256"]["entropy"])

    assert bip39_128.name() == _["BIP39"]["128"]["name"]
    assert bip39_160.name() == _["BIP39"]["160"]["name"]
    assert bip39_192.name() == _["BIP39"]["192"]["name"]
    assert bip39_224.name() == _["BIP39"]["224"]["name"]
    assert bip39_256.name() == _["BIP39"]["256"]["name"]

    assert bip39_128.strength() == _["BIP39"]["128"]["strength"]
    assert bip39_160.strength() == _["BIP39"]["160"]["strength"]
    assert bip39_192.strength() == _["BIP39"]["192"]["strength"]
    assert bip39_224.strength() == _["BIP39"]["224"]["strength"]
    assert bip39_256.strength() == _["BIP39"]["256"]["strength"]

    assert bip39_128.entropy() == _["BIP39"]["128"]["entropy"]
    assert bip39_160.entropy() == _["BIP39"]["160"]["entropy"]
    assert bip39_192.entropy() == _["BIP39"]["192"]["entropy"]
    assert bip39_224.entropy() == _["BIP39"]["224"]["entropy"]
    assert bip39_256.entropy() == _["BIP39"]["256"]["entropy"]

    with pytest.raises(EntropyError, match="Invalid entropy data"):
        BIP39Entropy(entropy="INVALID_ENTROPY")

    with pytest.raises(EntropyError, match="Unsupported entropy strength"):
        BIP39Entropy(entropy="cdf694ac868efd01673fc51e897c57a0bd428503080ad4c94c7d6f6d13f095fbc8")
